"""Native Windows file guards, using only test-owned temporary files."""
import ctypes
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('windows_governance_guards', ROOT / 'plugins/devops-standard/skills/devops-standard/scripts/github_governance.py')
governance = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(governance)


@unittest.skipUnless(os.name == 'nt', 'native Windows HANDLE adapter')
class WindowsFileGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'workspace'
        self.root.mkdir()

    def execute(self, path, before=None):
        governance.execute_action(None, self.root, {'repository': {'owner': 'fixture', 'name': 'app'}},
                                  {'kind': 'local_file', 'path': path, 'before_sha256': before, 'content': 'approved'}, {})

    def test_new_nested_file_creation_and_approved_existing_replacement(self):
        self.execute('docs/owned.txt')
        path = self.root / 'docs/owned.txt'
        self.assertEqual(path.read_text(encoding="utf-8"), 'approved')
        path.write_text('original', encoding="utf-8")
        self.execute('docs/owned.txt', hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(path.read_text(encoding="utf-8"), 'approved')

    def test_existing_file_is_not_overwritten_by_new_file_proposal(self):
        path = self.root / 'owned.txt'
        path.write_text('user content', encoding="utf-8")
        with self.assertRaises(OSError):
            self.execute('owned.txt')
        self.assertEqual(path.read_text(encoding="utf-8"), 'user content')

    def test_write_time_hash_preserves_concurrent_content(self):
        path = self.root / 'owned.txt'
        path.write_text('original', encoding="utf-8")
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        path.write_text('concurrent edit', encoding="utf-8")
        with self.assertRaises(governance.GovernanceError):
            self.execute('owned.txt', before)
        self.assertEqual(path.read_text(encoding="utf-8"), 'concurrent edit')

    def test_hardlink_is_rejected_without_changing_owned_external_file(self):
        outside = self.base / 'outside.txt'
        outside.write_text('sentinel', encoding="utf-8")
        os.link(outside, self.root / 'owned.txt')
        with self.assertRaises(governance.GovernanceError):
            self.execute('owned.txt', hashlib.sha256(outside.read_bytes()).hexdigest())
        self.assertEqual(outside.read_text(encoding="utf-8"), 'sentinel')

    def test_junction_parent_rejected_without_creating_external_file(self):
        outside = self.base / 'outside'
        outside.mkdir()
        junction = self.root / 'junction'
        result = subprocess.run([os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/c', 'mklink', '/J', str(junction), str(outside)], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        try:
            with self.assertRaises((governance.GovernanceError, OSError)):
                self.execute('junction/owned.txt')
            self.assertEqual(list(outside.iterdir()), [])
        finally:
            junction.rmdir()

    def test_exclusive_file_and_pinned_root_reject_concurrent_mutation(self):
        path = self.root / 'owned.txt'
        path.write_text('original', encoding="utf-8")
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        real_hash = hashlib.sha256
        def checked_hash(content):
            with self.assertRaises(OSError):
                path.write_text('concurrent write', encoding="utf-8")
            with self.assertRaises(OSError):
                self.root.rename(self.base / 'moved')
            return real_hash(content)
        with patch.object(governance.hashlib, 'sha256', side_effect=checked_hash):
            self.execute('owned.txt', before)
        self.assertEqual(path.read_text(encoding="utf-8"), 'approved')


if __name__ == '__main__':
    unittest.main()
