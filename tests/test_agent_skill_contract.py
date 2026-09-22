"""Regression tests for provider-neutral agents and mandatory skill execution."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
EXECUTOR = ROOT / "plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md"
PIPELINE = ROOT / "docs/workflow-pipeline.md"
AGENTS = ROOT / "AGENTS.md"


class TestAgentSkillContract(unittest.TestCase):

    def test_skill_receipt_is_mandatory(self):
        contract = (ORCHESTRATOR / "references/skill-execution-contract.md").read_text()
        self.assertIn("naming a skill does not apply its methodology", contract)
        self.assertIn("SKILL_RECEIPT", contract)
        self.assertIn("Read each selected `SKILL.md` completely", contract)

    def test_minimal_code_gate_blocks_duplicate_work(self):
        gate = (ORCHESTRATOR / "references/minimal-code-gate.md").read_text()
        self.assertIn("REUSE_INVENTORY", gate)
        self.assertIn("Similar behavior with different names is still", gate)
        self.assertIn("MINIMAL_CODE_GATE", gate)

    def test_llm_handoff_continues_without_restart(self):
        handoff = (ORCHESTRATOR / "references/llm-handoff.md").read_text()
        self.assertIn("LLM_TOKEN_EXHAUSTED", handoff)
        self.assertIn("EXECUTION_HANDOFF", handoff)
        self.assertIn("execution_contract_path", handoff)
        self.assertIn("do not restart the task", handoff)

    def test_harness_requires_execution_receipt(self):
        harness = (ORCHESTRATOR / "references/harness-execution.md").read_text()
        skill = (ORCHESTRATOR / "SKILL.md").read_text()
        self.assertIn("EXECUTION_RECEIPT", harness)
        self.assertIn("ASSIGNED", harness)
        self.assertIn("A task without `invocation_evidence` is `NOT EXECUTED`", harness)
        self.assertIn("assigning a task is not execution", skill)

    def test_harness_bootstrap_is_lean_and_receipt_is_output(self):
        harness = (ORCHESTRATOR / "references/harness-execution.md").read_text()
        self.assertIn("`task_id`", harness)
        self.assertIn("`execution_contract_path`", harness)
        self.assertIn("Do not paste those bodies into", harness)
        self.assertIn("never treated as an implementation input", harness)

    def test_capability_registry_has_fallback_contract(self):
        registry = (ORCHESTRATOR / "references/capability-registry.md").read_text()
        self.assertIn("Preferred capability", registry)
        self.assertIn("Fallback", registry)
        self.assertIn("A fallback must satisfy the same task contract", registry)

    def test_executor_requires_all_three_receipts(self):
        executor = EXECUTOR.read_text()
        self.assertIn("SKILL_RECEIPT", executor)
        self.assertIn("REUSE_INVENTORY", executor)
        self.assertIn("MINIMAL_CODE_GATE", executor)

    def test_execution_receipt_follows_result_and_precedes_validation(self):
        for path in (ORCHESTRATOR / "SKILL.md", PIPELINE):
            content = path.read_text(encoding="utf-8")
            result_pos = content.find("execution result")
            if result_pos < 0:
                result_pos = content.find("resultado inspecionavel")
            receipt_pos = content.find("EXECUTION_RECEIPT", result_pos)
            validating_pos = content.find("VALIDATING", receipt_pos)
            self.assertGreaterEqual(result_pos, 0, path)
            self.assertGreater(receipt_pos, result_pos, path)
            self.assertGreater(validating_pos, receipt_pos, path)

    def test_practice_provenance_labels_local_extensions(self):
        skill = (ORCHESTRATOR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Practice Provenance", skill)
        self.assertIn("Local architectural decisions", skill)
        self.assertIn("Local extensions", skill)
        self.assertIn("not present", skill.lower())

    def test_change_complexity_preserves_validation(self):
        skill = (ORCHESTRATOR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Change Complexity Gate", skill)
        for tier in ("`TRIVIAL`", "`NORMAL`", "`COMPLEX`"):
            self.assertIn(tier, skill)
        self.assertIn("Complexity changes documentation", skill)

    def test_agents_file_is_a_short_map_to_canonical_sources(self):
        content = AGENTS.read_text(encoding="utf-8")
        self.assertLessEqual(len(content.splitlines()), 100)
        for target in (
            "README.md",
            "docs/workflow-pipeline.md",
            "plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md",
            "docs/engineering-harness-audit.md",
        ):
            self.assertIn(target, content)
            self.assertTrue((ROOT / target).exists(), target)


if __name__ == "__main__":
    unittest.main()
