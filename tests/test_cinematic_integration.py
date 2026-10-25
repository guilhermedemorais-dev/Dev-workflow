"""Cinematic stays in UI/UX; deterministic helpers reject broken media contracts."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CINEMATIC = ROOT / 'plugins/ui-ux-standard/skills/cinematic-web-standard'


class CinematicIntegration(unittest.TestCase):
    def run_script(self, script, directory, *args):
        return subprocess.run([sys.executable, str(CINEMATIC / 'scripts' / script), str(directory), *args], capture_output=True, text=True)

    def test_nested_skill_resources_close_without_new_plugin(self):
        self.assertTrue((CINEMATIC / 'SKILL.md').is_file())
        self.assertFalse((ROOT / 'plugins/cinematic-web-standard').exists())
        manifest = json.loads((ROOT / 'plugins/ui-ux-standard/.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['skills'], './skills/')
        skill = (CINEMATIC / 'SKILL.md').read_text()
        for relative in re.findall(r'`((?:references|scripts)/[^`]+)`', skill):
            self.assertTrue((CINEMATIC / relative).is_file(), relative)
        for path in CINEMATIC.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((path.parent / target.split('#')[0]).exists(), (path, target))

    def test_manifest_orders_numeric_frames_and_preserves_sizes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'frame-00002.webp').write_bytes(b'abc')
            (root / 'frame-00001.webp').write_bytes(b'a')
            (root / 'notes.txt').write_text('not a frame')
            result = self.run_script('make_manifest.py', root, '--base-url', '/cinematic/scene')
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)
            self.assertEqual(manifest['frameCount'], 2)
            self.assertEqual(manifest['totalBytes'], 4)
            self.assertEqual([x['index'] for x in manifest['frames']], [1, 2])
            self.assertEqual(manifest['frames'][0]['src'], '/cinematic/scene/frame-00001.webp')

    def test_sequence_rejects_gaps_duplicates_and_strict_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'frame-00001.webp').write_bytes(b'a')
            (root / 'frame-00003.webp').write_bytes(b'abc')
            result = self.run_script('validate_sequence.py', root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing frame numbers', result.stdout)
            (root / 'frame-00002.webp').write_bytes(b'b')
            self.assertEqual(self.run_script('validate_sequence.py', root, '--strict').returncode, 0)
            result = self.run_script('validate_sequence.py', root, '--max-frames', '1', '--strict')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('exceeds budget', result.stdout)
            (root / 'other-00002.png').write_bytes(b'b')
            result = self.run_script('validate_sequence.py', root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('duplicate frame numbers', result.stdout)

    def test_v2_selection_is_opt_in_and_owned_by_existing_ux_sector(self):
        if not (ROOT / 'scripts/office.py').exists():
            self.skipTest('Legacy repository has no V2 router')
        spec = importlib.util.spec_from_file_location('office', ROOT / 'scripts/office.py')
        office = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(office)
        ordinary = office.select_skills(ROOT, 'ux-design', ['ux-components'])
        self.assertNotIn('ux-cinematic', [x['id'] for x in ordinary['skills']])
        cinematic = office.select_skills(ROOT, 'ux-design', ['ux-cinematic'])
        self.assertEqual([x['id'] for x in cinematic['skills']], ['global-core', 'ux-core', 'ux-cinematic'])
        self.assertEqual(cinematic['skills'][-1]['reference_base'], 'plugins/ui-ux-standard/skills/cinematic-web-standard')
        self.assertEqual(cinematic['decision'], 'PLANNED_NOT_EXECUTED')
        registry = office.read_json(ROOT / 'library/indexes/skill-routes.json')
        self.assertNotIn('cinematic', registry['sectors'])


if __name__ == '__main__':
    unittest.main()
