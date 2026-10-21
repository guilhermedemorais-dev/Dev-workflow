"""Structural routing regressions, not proof of application/domain correctness."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / 'plugins/sdd-spec-factory/skills/sdd-spec-factory'
HARNESS = ROOT / 'plugins/dev-workflow-standard/skills/dev-workflow-standard'
ROUTER = SDD / 'references/technical-knowledge-router.md'
TOPICS = {
    'technical-architecture.md', 'technical-data-concurrency.md',
    'technical-auth-sessions.md', 'technical-apis-jobs.md',
    'technical-quality-operations.md', 'technical-fiscal.md',
}


class TechnicalKnowledgeLibraryContract(unittest.TestCase):
    def test_harness_and_sdd_reach_one_canonical_router(self):
        for owner in (HARNESS, SDD):
            text = (owner / 'SKILL.md').read_text(encoding='utf-8')
            paths = re.findall(r'[^\s`()<>]*technical-knowledge-router\.md', text)
            self.assertTrue(paths)
            self.assertTrue(any(
                (owner / path).resolve() == ROUTER.resolve()
                or (ROOT / path).resolve() == ROUTER.resolve()
                for path in paths
            ), f'{owner.name} must resolve the canonical router')

    def test_domain_rows_resolve_to_packaged_topic_files(self):
        router = ROUTER.read_text(encoding='utf-8')
        links = re.findall(r'\]\((technical-[^)]+\.md)\)', router)
        self.assertEqual(set(links) - {'technical-decision-procedure.md'}, TOPICS)
        rows = [row for row in router.splitlines()
                if row.startswith('| ') and '](' in row]
        self.assertEqual(len(rows), 10)
        for path in links:
            self.assertTrue((ROUTER.parent / path).is_file(), path)

    def test_topics_are_directly_discoverable_from_sdd(self):
        skill = (SDD / 'SKILL.md').read_text(encoding='utf-8')
        for topic in TOPICS:
            self.assertIn(f'references/{topic}', skill)
        for source in [ROUTER, *(ROUTER.parent / name for name in TOPICS)]:
            for link in re.findall(r'\]\(([^)]+)\)', source.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((source.parent / link.split('#')[0]).is_file(),
                                    f'Broken local reference: {source.name}: {link}')

    def test_selection_preserves_existing_transport_and_ownership(self):
        text = ROUTER.read_text(encoding='utf-8')
        for field in ('project_path', 'section', 'purpose', 'applies_to',
                      'required_sources', 'conditional_sources',
                      'execution_lists', 'contract_revision'):
            self.assertIn(field, text)
        for boundary in ('v1 compatibility', 'normative', 'specialists read',
                         'receipts', 'Issue comments', 'human acceptance'):
            self.assertIn(boundary, text)
        self.assertRegex(text, r'Do not add a\s+knowledge schema')
        self.assertIn('Never load every domain', text)

    def test_every_topic_has_decision_and_verification_guidance(self):
        for topic in TOPICS:
            with self.subTest(topic=topic):
                text = (ROUTER.parent / topic).read_text(encoding='utf-8')
                self.assertIn('## When to consult', text)
                self.assertRegex(text.lower(), r'decid|decision')
                self.assertRegex(text.lower(), r'verif|test')
                self.assertIn('LOCAL', text)

    def test_security_and_operations_reuse_existing_owners(self):
        text = (ROUTER.parent / 'technical-quality-operations.md').read_text(encoding='utf-8')
        for skill in ('qa-testing-standard', 'security-standard', 'devops-standard'):
            self.assertIn(skill, text)
        for invariant in ('PARTIAL', 'BLOCKED', 'NOT_VALIDATED', 'REQUIRED'):
            self.assertIn(invariant, text)
        self.assertIn('not another Quality Gate implementation', text)

    def test_knowledge_gap_learning_reuses_research_and_durable_ownership(self):
        text = ROUTER.read_text(encoding='utf-8')
        for requirement in ('stale version', 'capability-registry',
                            'version-matched', 'docs/biblioteca-referencias/',
                            'revision/version', 'checked date',
                            'freshness/applicability', 'continuous-improvement.md',
                            'NOT VERIFIED', 'preserve the old provenance'):
            self.assertIn(requirement, text)
        self.assertIn('not search\n   snippets alone', text)
        self.assertIn('do not modify\n   installed caches', text)
        for owner in (SDD, HARNESS):
            self.assertRegex((owner / 'SKILL.md').read_text(encoding='utf-8'),
                             r'(?s)(?:Missing/stale|missing, stale).*?(?:update|updates)')

    def test_critical_examples_do_not_claim_executed_domain_tests(self):
        expected = {
            'technical-data-concurrency.md': ('last-unit checkout', 'two independent DB',
                                             'exactly one', 'not application execution evidence'),
            'technical-auth-sessions.md': ('refresh rotation', 'Replay', 'race independent',
                                          'until executed'),
            'technical-fiscal.md': ('fiscal document', 'duplicate', 'NOT VERIFIED',
                                    'BLOCKED', 'Never issue/cancel'),
        }
        for topic, terms in expected.items():
            text = (ROUTER.parent / topic).read_text(encoding='utf-8')
            for term in terms:
                with self.subTest(topic=topic, term=term):
                    self.assertIn(term, text)

    def test_skill_discovery_sources_preserve_authority_and_adoption_gates(self):
        text = (HARNESS / 'references/continuous-improvement.md').read_text(encoding='utf-8')
        for url in ('https://github.com/google/skills',
                    'https://github.com/google-labs-code/stitch-skills',
                    'https://antigravity.google/docs/skills',
                    'https://github.com/sickn33/agentic-awesome-skills'):
            self.assertIn(url, text)
        for boundary in ('Community discovery catalog', 'not an official Google',
                         'No individual candidate', 'pinned source revision',
                         'Do not bulk', 'Human\nApproval Gate'):
            self.assertIn(boundary, text)


if __name__ == '__main__':
    unittest.main()
