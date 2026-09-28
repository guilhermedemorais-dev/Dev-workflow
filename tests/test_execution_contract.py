"""Structural tests for v2 task contracts and v1 compatibility."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "plugins/sdd-spec-factory/templates/execution-contract-template.json"
CONTRACT = ROOT / "docs/execution/TASK-002.json"
TASK_TEMPLATE = ROOT / "plugins/sdd-spec-factory/templates/task-template.md"
SDD_SKILL = ROOT / "plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md"
EXECUTOR = ROOT / "plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md"

LEGACY_REQUIRED_FIELDS = {
    "schema_version", "task_id", "task_path", "goal", "specs", "docs",
    "allowed_paths", "out_of_scope", "requirements", "acceptance_criteria",
    "required_tests", "required_skills", "stop_conditions",
}


class TestExecutionContract(unittest.TestCase):

    def test_template_v2_and_legacy_contract_are_valid(self):
        template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        legacy = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(template["schema_version"], 2)
        self.assertEqual(legacy["schema_version"], 1)
        self.assertTrue(template["task_id"].startswith("TASK-"))
        self.assertTrue(template["human_task"]["local_mirror"].endswith(".md"))
        self.assertTrue(LEGACY_REQUIRED_FIELDS.issubset(legacy))

    def test_current_contract_references_existing_mandatory_paths(self):
        payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for key in ("task_path",):
            self.assertTrue((ROOT / payload[key]).is_file(), payload[key])
        for key in ("specs", "docs", "required_skills"):
            for relative_path in payload[key]:
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_human_task_template_uses_copy_ready_ignition_prompt(self):
        content = TASK_TEMPLATE.read_text(encoding="utf-8")
        prompt = content.split("## Prompt para o executor", 1)[1].split("\n## ", 1)[0]
        self.assertIn("docs/execution/TASK-XXX.json", prompt)
        self.assertIn("contract_revision", prompt)
        self.assertIn("equivalência normativa", prompt)
        self.assertIn("microtarefa", prompt)
        self.assertIn("Não faça merge nem deploy", prompt)

    def test_sdd_produces_both_human_and_machine_artifacts(self):
        content = SDD_SKILL.read_text(encoding="utf-8")
        self.assertIn("Human Task", content)
        self.assertIn("machine-readable execution contract", content.lower())
        self.assertIn("legacy task", content.lower())

    def test_executor_uses_progressive_disclosure(self):
        content = EXECUTOR.read_text(encoding="utf-8")
        self.assertIn("execution_contract_path", content)
        self.assertIn("Progressive disclosure", content)
        self.assertNotIn("read the whole approved task and every mandatory", content)
        self.assertNotIn("prompt-base as the operational contract", content)

    def test_sector_router_supports_v2_and_legacy_v1(self):
        template = json.loads(TEMPLATE.read_text())
        legacy = json.loads(CONTRACT.read_text())
        self.assertEqual(template["schema_version"], 2)
        self.assertEqual(legacy["schema_version"], 1)
        self.assertIn("sectors", template)
        self.assertIn("microtasks", template)
        self.assertNotIn("sectors", legacy)
        self.assertTrue(LEGACY_REQUIRED_FIELDS.issubset(legacy))


if __name__ == "__main__":
    unittest.main()
