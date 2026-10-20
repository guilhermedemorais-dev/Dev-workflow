"""Instruction-contract regression; these checks do not measure LLM behavior/cost."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
EXECUTOR = ROOT / "plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md"


def section(text, heading):
    tail = text.split(heading + "\n", 1)[1]
    return tail.split("\n## ", 1)[0]


class TrivialWorkflowContract(unittest.TestCase):
    def setUp(self):
        self.skill = (HARNESS / "SKILL.md").read_text()

    def test_path_is_selected_before_full_execution_contract(self):
        entry = section(self.skill, "## Select the execution path first")
        self.assertIn("takes precedence", entry)
        self.assertIn("existing approved full contract retains its gates", entry)
        self.assertLess(self.skill.index("## Select the execution path first"),
                        self.skill.index("## Harness Contract"))

    def test_inline_path_retains_scope_validation_and_evidence(self):
        inline = section(self.skill, "### TRIVIAL inline execution")
        for required in ("allowed paths", "acceptance criterion", "Validate the actual diff",
                         "check and result", "preserve the diff", "reclassify",
                         "no automatic", "merge/deploy", "Never claim another agent ran"):
            self.assertIn(required, inline)

    def test_complexity_gate_does_not_require_full_artifacts_for_trivial(self):
        gate = section(self.skill, "## Change Complexity Gate")
        trivial = gate.split("- `NORMAL`", 1)[0]
        self.assertIn("Do not require a ten-sector matrix, JSON v2, SDD", trivial)
        self.assertIn("separate receipt/report templates", trivial)
        for trigger in ("architecture", "infrastructure", "security", "data",
                        "dependencies", "public contracts", "UI/UX", "independent functional QA"):
            self.assertIn(trigger, gate)

    def test_executor_exception_precedes_full_contract_preconditions(self):
        text = EXECUTOR.read_text()
        entry = section(text, "## Entry path")
        self.assertIn("instead of the full-contract preconditions", entry)
        self.assertIn("Read it", entry)
        self.assertIn("return to Harness", entry)
        self.assertIn("approved inline intent", entry)
        self.assertLess(text.index("## Entry path"), text.index("## Preconditions"))

    def test_references_do_not_reintroduce_trivial_artifact_requirements(self):
        for name in ("context-routing.md", "capability-registry.md", "skill-execution-contract.md"):
            text = (HARNESS / "references" / name).read_text()
            self.assertIn("TRIVIAL", text, name)
            self.assertIn("inline path", text, name)

    def test_full_contract_and_independent_review_remain_available(self):
        for requirement in ("New NORMAL/COMPLEX executable tasks require a valid Execution Contract",
                            "Never silently substitute", "QA_STATUS", "contract_revision",
                            "Only each owner attests its own PASS"):
            self.assertIn(requirement, self.skill)


if __name__ == "__main__":
    unittest.main()
