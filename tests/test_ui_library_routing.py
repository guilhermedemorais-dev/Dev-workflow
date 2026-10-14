"""Packaging provenance and reference boundaries; runtime behavior is separately verified."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/ui-ux-standard'
SKILLS = PLUGIN / 'skills'


class UiLibraryRouting(unittest.TestCase):
    def test_frappe_pinned_source_integrity_and_original_contract_body(self):
        skill = SKILLS / 'frappe-ui'
        origin = json.loads((skill / 'ORIGIN.json').read_text(encoding='utf-8'))
        self.assertEqual(origin['repository'], 'https://github.com/frappe/frappe-ui')
        self.assertRegex(origin['revision'], r'^[0-9a-f]{40}$')
        self.assertEqual(origin['license'], 'MIT')
        self.assertTrue(origin['source_package_version'])
        for name, record in origin['files'].items():
            self.assertEqual(hashlib.sha256((skill / name).read_bytes()).hexdigest(), record['packaged_sha256'])
            if name in ('CORE.md', 'DATA.md', 'SETUP.md'):
                self.assertEqual(record['upstream_sha256'], record['packaged_sha256'])
        body = (skill / 'SKILL.md').read_text(encoding='utf-8').split('<!-- BEGIN UPSTREAM BODY -->\n', 1)[1]
        self.assertEqual(hashlib.sha256(body.encode('utf-8')).hexdigest(), origin['upstream_body_sha256'])

    def test_instruction_subset_omits_upstream_operational_eval_tools(self):
        skill = SKILLS / 'frappe-ui'
        origin = json.loads((skill / 'ORIGIN.json').read_text(encoding='utf-8'))
        for omitted in origin['omitted']:
            self.assertFalse((skill / omitted['path']).exists())
            self.assertRegex(omitted['sha256'], r'^[0-9a-f]{64}$')
        self.assertFalse(any(p.suffix in ('.py', '.js', '.sh', '.ps1') for p in skill.rglob('*') if p.is_file()))

    def test_skill_references_resolve_inside_the_plugin(self):
        for name in ('ui-ux-standard', 'frappe-ui', 'react-bits'):
            skill = SKILLS / name
            entry = (skill / 'SKILL.md').read_text(encoding='utf-8')
            self.assertRegex(entry, rf'(?m)^name: {name}$')
            self.assertTrue((skill / 'agents/openai.yaml').is_file())
            for document in skill.rglob('*.md'):
                for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
                    target = target.split('#', 1)[0]
                    if not target or '://' in target or target.startswith('mailto:'):
                        continue
                    path = (document.parent / target).resolve()
                    self.assertTrue(path.is_relative_to(PLUGIN.resolve()), (document, target))
                    self.assertTrue(path.exists(), (document, target))

    def test_react_adapter_preserves_exact_restricted_license_without_components(self):
        skill = SKILLS / 'react-bits'
        license_bytes = (skill / 'LICENSE.upstream.md').read_bytes()
        self.assertEqual(hashlib.sha256(license_bytes).hexdigest(), 'f4c33af6739191537738662d223b68d77bc226f4b57ea883e16481d8cc5c73c9')
        self.assertIn('MIT + Commons Clause', license_bytes.decode('utf-8'))
        self.assertFalse(any(p.suffix in ('.jsx', '.tsx', '.js', '.ts', '.css', '.vue') for p in skill.rglob('*') if p.is_file()))
        origin = (skill / 'ORIGIN.md').read_text(encoding='utf-8')
        self.assertIn('496968c4117e21278f13917201b7d615bc5e7450', origin)
        self.assertIn('not claim upstream skill authorship', origin)

    def test_markdown_skills_not_executable_platform_catalog_entries(self):
        for catalog in (ROOT / 'plugins/dev-environment-standard').glob('Tools */catalog.json'):
            records = json.loads(catalog.read_text(encoding='utf-8'))['tools']
            for record in records:
                self.assertNotIn('/skills/frappe-ui/', record['path'])
                self.assertNotIn('/skills/react-bits/', record['path'])
        for name, framework in [('frappe-ui', 'Vue 3'), ('react-bits', 'React')]:
            entry = (SKILLS / name / 'SKILL.md').read_text(encoding='utf-8')
            description = re.search(r'(?m)^description: (.+)$', entry).group(1)
            self.assertIn(framework, description)
            self.assertNotRegex(description, r'Windows|Linux|macOS|sys\.platform')
            self.assertIn('ui-ux-standard', entry)
        for manifest in (PLUGIN / 'plugin.json', PLUGIN / '.codex-plugin/plugin.json', PLUGIN / '.claude-plugin/plugin.json'):
            data = json.loads(manifest.read_text(encoding='utf-8'))
            if 'skills' in data:
                self.assertEqual((PLUGIN / data['skills']).resolve(), SKILLS.resolve())
            self.assertEqual(data['name'], 'ui-ux-standard')


if __name__ == '__main__':
    unittest.main()
