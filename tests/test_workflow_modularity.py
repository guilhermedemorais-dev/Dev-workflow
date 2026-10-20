"""Verify lossless section routing and bounded permanent context."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / 'plugins/dev-workflow-standard/skills/dev-workflow-standard'


def sections(text):
    return {block.splitlines()[0][3:]: block
            for block in re.split(r'(?m)(?=^## )', text)[1:]}


def digest(text):
    return hashlib.sha256((text.rstrip() + "\n").encode()).hexdigest()


class WorkflowModularity(unittest.TestCase):
    def setUp(self):
        self.mapping = json.loads((ROOT / 'docs/workflow-section-migration.json').read_text())
        self.skill = (OWNER / 'SKILL.md').read_text()

    def test_permanent_contract_is_bounded_and_routes_every_procedure(self):
        self.assertLessEqual(len(self.skill.splitlines()), 200)
        destinations = {x['destination'] for x in self.mapping['sections']} - {'SKILL.md'}
        self.assertEqual(len(destinations), 5)
        for path in destinations:
            self.assertIn(path, self.skill)
            self.assertTrue((OWNER / path).is_file())

    def test_each_source_section_has_one_traceable_destination(self):
        rows = self.mapping['sections']
        self.assertEqual(len(rows), len({x['heading'] for x in rows}))
        for row in rows:
            with self.subTest(heading=row['heading']):
                target = sections((OWNER / row['destination']).read_text())[row['heading']]
                self.assertEqual(digest(target), row['destination_sha256'])
                if row['status'] == 'preserved':
                    self.assertEqual(row['source_sha256'], row['destination_sha256'])
                else:
                    self.assertTrue(row['reason'])
        changed = {x['heading'] for x in rows if x['status'] == 'revised'}
        self.assertEqual(changed, {'Harness Contract', 'Delegation Rules', 'Mandatory Flow',
                                   'When to Trigger Each Specialist', 'Context Budget Rules',
                                   'Repository Readiness Bootstrap'})

    def test_mapping_matches_original_commit_not_an_invented_inventory(self):
        result = subprocess.run(['git', 'show', self.mapping['source_commit'] + ':' +
                                 self.mapping['source_path']], cwd=ROOT,
                                capture_output=True, text=True)
        if result.returncode:
            self.skipTest('original commit unavailable in this checkout')
        original = sections(result.stdout)
        self.assertEqual(set(original), {x['heading'] for x in self.mapping['sections']})
        for row in self.mapping['sections']:
            self.assertEqual(digest(original[row['heading']]), row['source_sha256'])
            if row['status'] == 'revised' and row['heading'] not in ('Harness Contract', 'Delegation Rules'):
                relocated = original[row['heading']].replace('](../../../../docs/',
                    '](../../../../../docs/').replace('](../../../sdd-spec-factory/',
                    '](../../../../sdd-spec-factory/').replace('](references/', '](')
                self.assertEqual(digest(relocated), row['destination_sha256'])

    def test_phase_selection_reuse_and_external_specs_are_explicit(self):
        for term in ('Classify before loading references', 'do not load this table',
                     'compatible cached routing evidence', 'Spec Kit',
                     'instead of generating', 'does not replace JSON v2',
                     'Only each owner attests its own PASS'):
            self.assertIn(term, self.skill)
        registry = (OWNER / 'references/capability-registry.md').read_text()
        self.assertNotIn('Before choosing a capability or a fallback for any phase, inspect the complete', registry)
        self.assertIn('not a mandatory read for every phase', registry)

    def test_relocated_markdown_links_resolve(self):
        for path in {x['destination'] for x in self.mapping['sections']}:
            source = OWNER / path
            for link in re.findall(r'\]\(([^)]+)\)', source.read_text()):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((source.parent / link.split('#')[0]).is_file(),
                                    f'{path}: {link}')


if __name__ == '__main__':
    unittest.main()
