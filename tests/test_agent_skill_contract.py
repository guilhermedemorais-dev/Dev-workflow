"""Regression tests for provider-neutral agents and mandatory skill execution."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
EXECUTOR = ROOT / "plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md"


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
        self.assertIn("do not restart the task", handoff)

    def test_harness_requires_execution_receipt(self):
        harness = (ORCHESTRATOR / "references/harness-execution.md").read_text()
        skill = (ORCHESTRATOR / "SKILL.md").read_text()
        self.assertIn("EXECUTION_RECEIPT", harness)
        self.assertIn("ASSIGNED", harness)
        self.assertIn("A task without `invocation_evidence` is `NOT EXECUTED`", harness)
        self.assertIn("assigning a task is not execution", skill)

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


if __name__ == "__main__":
    unittest.main()
