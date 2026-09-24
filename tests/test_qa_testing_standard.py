"""QA bundle structure/protocol checks, not simulated product QA or LLM execution."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "plugins/qa-testing-standard"
SKILL = BUNDLE / "skills/qa-testing-standard"


class QATestingStandardTests(unittest.TestCase):
    def text(self, name="SKILL.md"):
        self.assertTrue((SKILL / name).is_file(), "Required QA protocol missing: " + name)
        return (SKILL / name).read_text()

    def test_23_bundle_and_platforms(self):
        for name in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            with self.subTest(manifest=name):
                self.assertTrue((BUNDLE / name).is_file(), "Required platform manifest missing")
                manifest = json.loads((BUNDLE / name).read_text())
                self.assertEqual(manifest["name"], "qa-testing-standard")
                self.assertTrue((BUNDLE / manifest["skills"]).is_dir())
        for name in ("qa-standard", "testing-standard", "quality-standard"):
            self.assertFalse((ROOT / "plugins" / name).exists())

    def test_24_capability_registry(self):
        registry = (ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard/references/capability-registry.md").read_text()
        self.assertIn("qa-testing-standard", registry)
        self.assertIn("QA_STATUS", registry)

    def test_25_no_product_edits(self):
        self.assertIn("Do not write or fix product code", self.text())
        self.assertIn("dev-implementation-standard", self.text())

    def test_26_rework_returns_to_owner(self):
        self.assertIn("REWORK_REQUESTED", self.text())
        self.assertIn("Never mark another sector PASS", self.text())

    def test_27_security_boundary(self):
        for term in ("SECURITY_CANDIDATE", "security-standard", "CONFIRMED_SECURITY_FINDING"):
            self.assertIn(term, self.text())

    def test_28_ui_boundary(self):
        for term in ("ui-ux-standard", "visual hierarchy", "design fidelity"):
            self.assertIn(term, self.text())

    def test_29_devops_boundary(self):
        for term in ("devops-standard", "dev-environment-standard", "deployment"):
            self.assertIn(term, self.text())

    def test_30_failure_classification(self):
        for term in ("PRODUCT_BUG", "TEST_BUG", "ENVIRONMENT_FAILURE", "FLAKY_TEST", "TOOL_FAILURE"):
            self.assertIn(term, self.text("references/test-strategy.md"))

    def test_31_bug_reproduction(self):
        self.assertIn("bug-reproduction", self.text())
        self.assertIn("NOT_REPRODUCED", self.text("references/bug-report.md"))

    def test_32_fix_verification(self):
        self.assertIn("fix-verification", self.text())
        self.assertIn("fixed revision", self.text("references/bug-report.md"))

    def test_33_regression(self):
        self.assertIn("REGRESSION_TARGETS", self.text("references/test-strategy.md"))
        self.assertIn("fails before", self.text("references/bug-report.md"))

    def test_34_statuses_and_existing_receipts(self):
        for term in ("QA_STATUS", "PASS", "PARTIAL", "BLOCKED", "NOT_VALIDATED", "SKILL_RECEIPT", "EXECUTION_RECEIPT"):
            self.assertIn(term, self.text())
        for name in ("QA_RECEIPT", "TEST_RECEIPT", "SECTOR_RECEIPT"):
            self.assertNotIn(name, self.text())

    def test_35_pass_requires_execution(self):
        self.assertIn("No execution means no PASS", self.text())
        self.assertIn("mandatory cases passed", self.text())
        self.assertIn("Planning completion is not validation PASS", self.text())

    def test_36_confirmation_evidence_template(self):
        report = self.text("references/bug-report.md")
        for field in ("Expected behavior", "Actual behavior", "Reproduction steps", "Environment", "Affected revision", "Evidence", "Impact", "Reproducibility", "Confidence"):
            self.assertIn(field, report)

    def test_37_retest_required(self):
        report = self.text("references/bug-report.md")
        self.assertIn("FIXED requires QA retest", report)
        self.assertIn("ACCEPTED", report)
        self.assertIn("DEFERRED", report)
        self.assertIn("authorized decision", report)

    def test_38_planning_before_implementation(self):
        strategy = self.text("references/test-strategy.md")
        for term in ("QA_GUARDRAILS", "TEST_SCENARIOS", "REGRESSION_TARGETS", "VALIDATION_REQUIREMENTS"):
            self.assertIn(term, strategy)
        self.assertIn("before implementation", self.text())

    def test_marketplaces_append_discoverable_qa_once(self):
        for marketplace in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            data = json.loads((ROOT / marketplace).read_text())
            matches = [p for p in data["plugins"] if p["name"] == "qa-testing-standard"]
            self.assertEqual(len(matches), 1)
            source = matches[0]["source"]
            self.assertEqual(source["path"] if isinstance(source, dict) else source, "./plugins/qa-testing-standard")

    def test_tool_ownership_not_duplicated(self):
        self.assertFalse((SKILL / "references/tool-registry.json").exists())
        owners = {}
        for registry in (ROOT / "plugins").glob("*/skills/*/references/tool-registry.json"):
            data = json.loads(registry.read_text())
            for tool in data["tools"]:
                if tool["id"] in ("pytest", "hypothesis", "playwright"):
                    self.assertNotIn(tool["id"], owners)
                    owners[tool["id"]] = data["owner"]
        self.assertEqual(owners, {"pytest": "dev-implementation-standard", "hypothesis": "dev-implementation-standard", "playwright": "ui-ux-standard"})

    def test_conditional_references_exist_and_are_bounded(self):
        for name in ("test-strategy.md", "bug-report.md"):
            self.assertTrue((SKILL / "references" / name).is_file())
            self.assertIn("references/" + name, self.text())
        self.assertLess(len(self.text().splitlines()), 220)
        self.assertFalse((SKILL / "scripts").exists())
        self.assertFalse((SKILL / "references/bug-knowledge-registry.json").exists())

    def test_sector_context_is_purpose_based(self):
        for term in ("task_sections", "required_sources", "conditional_sources", "purpose", "CONTEXT_EXPANSION", "source_of_truth_conflict", "schema_version: 1"):
            self.assertIn(term, self.text())
        self.assertIn("OPTIONAL sources are not loaded automatically", self.text())

    def test_environment_agent_metadata(self):
        metadata = SKILL / "agents/openai.yaml"
        self.assertTrue(metadata.is_file(), "Environment health requires skill agent metadata")
        lines = metadata.read_text().splitlines()
        self.assertEqual(lines[0], "interface:")
        fields = {}
        for line in lines[1:]:
            key, value = line.strip().split(":", 1)
            self.assertTrue(value.strip().startswith('"') and value.strip().endswith('"'))
            fields[key] = value.strip()[1:-1]
        self.assertEqual(fields["display_name"], "QA Testing Standard")
        self.assertTrue(25 <= len(fields["short_description"]) <= 64)
        self.assertIn("$qa-testing-standard", fields["default_prompt"])


if __name__ == "__main__":
    unittest.main()
