"""Verify conditional design integration, source preservation and decision gates."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'plugins/ui-ux-standard/skills/ui-ux-standard'
SDD = ROOT / 'plugins/sdd-spec-factory/skills/sdd-spec-factory'
HARNESS = ROOT / 'plugins/dev-workflow-standard/skills/dev-workflow-standard'


class EvidenceDesignRouting(unittest.TestCase):
    def test_hig_package_has_exact_pinned_markdown_and_license(self):
        folder = UI / 'references/apple-hig-designer'
        provenance = json.loads((folder / 'provenance.json').read_text())
        self.assertEqual(provenance['commit'], 'ff17b91ff2903ecd52940afabf97de5a73c9cd1b')
        self.assertEqual(provenance['license'], 'MIT')
        self.assertEqual(len(provenance['files']), 5)
        for row in provenance['files']:
            path = folder / row['destination']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), row['sha256'])
        self.assertEqual({p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()},
                         {x['destination'] for x in provenance['files']} | {'LICENSE', 'provenance.json'})
        self.assertIn('Copyright (c) 2024 Apple HIG Designer Contributors', (folder / 'LICENSE').read_text())
        self.assertFalse((folder / 'SKILL.md').exists())
        self.assertEqual(provenance['repository'], 'https://github.com/axiaoge2/Apple-Hig-Designer')
        self.assertFalse((folder.parent / 'apple-hig').exists())

    def test_ui_does_not_load_hig_by_default_or_override_product_requirements(self):
        skill = (UI / 'SKILL.md').read_text()
        self.assertLessEqual(len(skill.splitlines()), 220)
        self.assertIn('This is conditional', skill)
        self.assertNotIn('44×44', skill)
        route = (UI / 'references/apple-hig-routing.md').read_text()
        for term in ('Do not read all references', 'approved PRD', 'CSS pixels',
                     'community-authored', 'MIT', 'official'):
            self.assertIn(term.lower(), route.lower())

    def test_ui_extracted_sections_are_preserved_except_declared_policy_and_links(self):
        mapping = json.loads((ROOT / 'docs/ui-ux-section-migration.json').read_text())
        for row in mapping:
            result = subprocess.run(['git', 'show', row['source_commit'] + ':' +
                                     str((UI / 'SKILL.md').relative_to(ROOT))],
                                    cwd=ROOT, capture_output=True, text=True)
            if result.returncode:
                self.skipTest('source commit unavailable in this checkout')
            blocks = {x.splitlines()[0][3:]: x for x in re.split(r'(?m)(?=^## )', result.stdout)[1:]}
            original = blocks[row['heading']]
            self.assertEqual(hashlib.sha256(original.encode()).hexdigest(), row['source_sha256'])
            expected = original.replace('Preserve the Harness whole-inventory rule.',
                'Follow the Harness targeted-inventory policy; expand discovery only for a gap.').replace('](references/', '](')
            self.assertEqual((UI / row['destination']).read_text(), expected.rstrip() + '\n')

    def test_material_decisions_route_from_executor_and_router(self):
        executor = (ROOT / 'plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md').read_text()
        self.assertIn('references/technical-decision-procedure.md', executor)
        self.assertIn('technical-decision-procedure.md', (SDD / 'references/technical-knowledge-router.md').read_text())
        procedure = (SDD / 'references/technical-decision-procedure.md').read_text()
        for term in ('approved PRD/spec/ADR', 'version-matched', 'API/protocol',
                     'Do not ask the owner', 'positive/negative validation',
                     'requirement → microtask → acceptance → execution-evidence',
                     'NOT VERIFIED', 'rollback', 'bounded check'):
            self.assertIn(term, procedure)

    def test_redis_and_training_are_conditional_and_do_not_claim_runtime(self):
        text = (HARNESS / 'references/ai-context-options.md').read_text()
        for term in ('not configured', 'No fine-tuning', 'not train a model',
                     'contract revision', 'source/code hash', 'holdout/eval',
                     'does not install', '2027-01-06', 'No account'):
            self.assertIn(term, text)
        self.assertIn('ai-context-options.md', (HARNESS / 'SKILL.md').read_text())


if __name__ == '__main__':
    unittest.main()
