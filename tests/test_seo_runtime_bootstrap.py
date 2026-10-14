"""Portable bootstrap boundaries using an isolated owned ZIP, no installs/network."""
import hashlib
import os
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class SeoBootstrap(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = self.root / 'runtime'
        self.runtime.mkdir()
        shutil.copyfile(ROOT / 'plugins/seo-standard/runtime/bootstrap.py', self.runtime / 'bootstrap.py')
        self.archive = self.root / 'fixture.zip'
        with zipfile.ZipFile(self.archive, 'w') as stream:
            stream.writestr('fixture/scripts/setup.py',
                "import json,sys\nfrom pathlib import Path\n"
                "runtime=Path(sys.argv[sys.argv.index('--venv')+1])\n"
                "runtime.mkdir(exist_ok=True)\n"
                "(runtime/'arguments.json').write_text(json.dumps(sys.argv[1:]))\n")
        self.lock = {'vendored_zip': '../fixture.zip', 'sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest(), 'version': 'fixture'}
        (self.runtime / 'runtime.lock.json').write_text(json.dumps(self.lock), encoding='utf-8')

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(self.runtime / 'bootstrap.py'), *args], capture_output=True, text=True)

    def test_http_only_is_forwarded_and_existing_runtime_is_preserved(self):
        target = self.runtime / '.runtime'
        target.mkdir()
        (target / 'user-marker').write_text('preserve', encoding="utf-8")
        result = self.invoke('--http-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--http-only', json.loads((target / 'arguments.json').read_text(encoding="utf-8")))
        self.assertEqual((target / 'user-marker').read_text(encoding="utf-8"), 'preserve')

    def test_checksum_failure_prevents_runtime_creation(self):
        self.archive.write_bytes(b'changed archive')
        result = self.invoke('--http-only')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.runtime / '.runtime').exists())

    def test_unknown_option_cannot_trigger_install(self):
        result = self.invoke('--unknown-option')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.runtime / '.runtime').exists())

    @unittest.skipUnless(os.name == 'nt', 'native Windows junction guard')
    def test_runtime_junction_rejected_before_install_or_external_write(self):
        outside = self.root / 'owned-outside'
        outside.mkdir()
        marker = outside / 'user-marker'
        marker.write_text('preserve', encoding="utf-8")
        target = self.runtime / '.runtime'
        linked = subprocess.run([os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/c', 'mklink', '/J', str(target), str(outside)], capture_output=True)
        self.assertEqual(linked.returncode, 0, linked.stderr)
        try:
            result = self.invoke('--http-only')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('runtime reparse point', result.stderr)
            self.assertFalse((outside / 'arguments.json').exists())
            self.assertEqual(marker.read_text(encoding="utf-8"), 'preserve')
            self.assertEqual(sorted(p.name for p in outside.iterdir()), ['user-marker'])
        finally:
            target.rmdir()
        missing = self.root / 'missing-destination'
        linked = subprocess.run([os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/c', 'mklink', '/J', str(target), str(missing)], capture_output=True)
        self.assertEqual(linked.returncode, 0, linked.stderr)
        try:
            result = self.invoke('--http-only')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('runtime reparse point', result.stderr)
            self.assertFalse(missing.exists())
        finally:
            target.rmdir()


if __name__ == '__main__':
    unittest.main()
