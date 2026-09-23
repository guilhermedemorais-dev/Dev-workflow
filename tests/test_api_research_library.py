"""Structural contract for conditional API research during planning/spec work.

These checks validate routing and documentation, not the external APIs themselves.
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / 'plugins/sdd-spec-factory/skills/sdd-spec-factory'
HARNESS = ROOT / 'plugins/dev-workflow-standard/skills/dev-workflow-standard'
REFERENCE = SDD / 'references/api-research-library.md'


class ApiResearchLibraryContract(unittest.TestCase):
    def test_discovery_sources_have_exact_canonical_urls(self):
        text = REFERENCE.read_text(encoding='utf-8')
        for url in (
            'https://github.com/philipecomputacao/inventario-apis-gratuitas',
            'https://publicapis.io/category/development',
        ):
            with self.subTest(source=url):
                self.assertIn(url, text)

    def test_sdd_routes_conditional_planning_and_spec_research(self):
        text = (SDD / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references/api-research-library.md', text)
        reference = REFERENCE.read_text(encoding='utf-8').lower()
        self.assertRegex(reference, r'planning|plan\b')
        self.assertRegex(reference, r'\bspec(?:s|ification)?\b')
        self.assertRegex(reference, r'\b(?:when|if|conditional|only)\b')
        self.assertIn('validation', reference)

    def test_harness_routes_to_canonical_sdd_reference(self):
        text = (HARNESS / 'SKILL.md').read_text(encoding='utf-8')
        paths = re.findall(r'[^\s`()<>"]*api-research-library\.md', text)
        self.assertTrue(paths, 'Harness must route API discovery to the SDD reference')
        self.assertTrue(
            any((HARNESS / path).resolve() == REFERENCE.resolve()
                or (ROOT / path).resolve() == REFERENCE.resolve() for path in paths),
            'Harness route must resolve to the single canonical SDD reference',
        )

    def test_api_mcp_and_mock_are_distinguished_without_bulk_actions(self):
        text = REFERENCE.read_text(encoding='utf-8').lower()
        for concept in ('api', 'mcp', 'mock'):
            with self.subTest(concept=concept):
                self.assertRegex(text, rf'\b{concept}s?\b')
        self.assertRegex(text, r'(?s)(?:do not|never|no)\b.{0,120}\b(?:bulk|import|copy)\b')
        self.assertRegex(text, r'(?s)(?:do not|never|no)\b.{0,120}\binstall(?:ation|ing|s)?\b')

    def test_evidence_contract_requires_provider_verification_and_test_status(self):
        text = REFERENCE.read_text(encoding='utf-8').lower()
        for term in ('official', 'auth', 'limit', 'licen', 'data', 'decision', 'test'):
            with self.subTest(field=term):
                self.assertIn(term, text)
        self.assertRegex(text, r'cost|pric(?:e|es|ing)')
        self.assertIn('NOT VALIDATED', REFERENCE.read_text(encoding='utf-8'))
        self.assertRegex(text, r'(?s)(?:template|record|evidence).{0,160}(?:candidate|decision|provider)')


if __name__ == '__main__':
    unittest.main()
