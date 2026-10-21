"""Catalog packaging, provenance and existing artifact handoff."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'plugins/ui-ux-standard/skills/ui-ux-standard'


class UiLibraryRouting(unittest.TestCase):
    def test_catalog_preserves_official_source_pins_and_restricted_terms(self):
        catalog = (UI / 'references/component-sources.md').read_text(encoding='utf-8')
        self.assertIn('d39298ec2155a1c4cda57a4be656568217506982/skills/frappe-ui', catalog)
        self.assertIn('496968c4117e21278f13917201b7d615bc5e7450/LICENSE.md', catalog)
        self.assertIn('MIT + Commons Clause', catalog)
        self.assertIn('package 1.0.2', catalog)
        for repository in ('https://github.com/frappe/frappe-ui', 'https://github.com/DavidHDev/react-bits'):
            self.assertIn(repository, catalog)

    def test_no_standalone_library_skills_components_or_dependencies_shipped(self):
        plugin = UI.parents[1]
        skills = {p.parent.name for p in plugin.glob('skills/*/SKILL.md')}
        self.assertNotIn('frappe-ui', skills)
        self.assertNotIn('react-bits', skills)
        for name in ('frappe-ui', 'react-bits'):
            self.assertFalse(any(p.is_file() for p in (plugin / 'skills' / name).rglob('*')))
        self.assertFalse(any(p.name in ('package.json', 'node_modules') for p in plugin.rglob('*')))
        for path in (ROOT / 'plugins/dev-environment-standard').glob('Tools */catalog.json'):
            for record in json.loads(path.read_text(encoding='utf-8'))['tools']:
                self.assertNotIn('/skills/frappe-ui/', record['path'])
                self.assertNotIn('/skills/react-bits/', record['path'])

    def test_ui_local_reference_closure_after_removal(self):
        for document in UI.rglob('*.md'):
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
                target = target.split('#', 1)[0]
                if not target or '://' in target or target.startswith('mailto:'):
                    continue
                resolved = (document.parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(UI.parents[1].resolve()), (document, target))
                self.assertTrue(resolved.exists(), (document, target))

    def test_existing_prd_spec_task_sources_retain_identity_and_unknown_values(self):
        handoff = (UI / 'references/library-source-handoff.md').read_text(encoding='utf-8')
        for field in ('Library ID / source ID', 'Official repository / docs URL', 'Version / commit',
                      'Component path / variant', 'Purpose / module', 'License', 'Dependencies',
                      'Adaptations', 'Decision state'):
            self.assertIn(field, handoff)
        self.assertIn('references[].id', handoff)
        for path in ('plugins/studio-prd/skills/studio-prd/assets/prd-template.md',
                     'plugins/sdd-spec-factory/templates/page-spec-template.md',
                     'plugins/sdd-spec-factory/templates/component-spec-template.md',
                     'plugins/sdd-spec-factory/templates/task-template.md'):
            text = (ROOT / path).read_text(encoding='utf-8')
            self.assertIn('ID fonte', text, path)
            self.assertIn('UNKNOWN', text, path)
        for path in ('plugins/studio-prd/skills/studio-prd/SKILL.md',
                     'plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md'):
            text = (ROOT / path).read_text(encoding='utf-8')
            self.assertIn('stable library/source ID', text)
            self.assertIn('Context7', text)

    def test_nonselected_candidates_not_required_and_instructions_not_os_gated(self):
        handoff = (UI / 'references/library-source-handoff.md').read_text(encoding='utf-8')
        self.assertIn('Nonselected candidates are not REQUIRED sources', handoff)
        self.assertIn('not a new runtime/schema/gate', handoff)
        canonical = (UI / 'SKILL.md').read_text(encoding='utf-8')
        canonical += (UI / 'references/ui-component-procedure.md').read_text(encoding='utf-8')
        self.assertIn('only executable tools use OS catalogs', canonical)
        self.assertIn('not standalone installed skills', canonical)
        self.assertNotIn('../frappe-ui/SKILL.md', canonical)
        self.assertNotIn('../react-bits/SKILL.md', canonical)


if __name__ == '__main__':
    unittest.main()
