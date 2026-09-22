"""Structural contract tests for human execution reporting."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATOR = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
HARNESS = ORCHESTRATOR / "SKILL.md"
REFERENCE = ORCHESTRATOR / "references/execution-report-comments.md"
EXECUTOR = ROOT / "plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md"
COMMENT_TEMPLATE = ROOT / "plugins/dev-implementation-standard/templates/execution-report-comment-template.md"
TASK_TEMPLATE = ROOT / "plugins/sdd-spec-factory/templates/task-template.md"
PIPELINE = ROOT / "docs/workflow-pipeline.md"


class TestExecutionReportComments(unittest.TestCase):

    def test_harness_recognizes_separate_human_report(self):
        content = HARNESS.read_text(encoding="utf-8")
        self.assertIn("Execution Report Comment", content)
        self.assertIn("EXECUTION_REPORT_COMMENT", content)
        self.assertIn("never replaces", content)

    def test_material_checkpoints_and_spam_control_are_defined(self):
        content = REFERENCE.read_text(encoding="utf-8")
        for state in ("`RUNNING`", "`VALIDATING`", "`REWORK`", "`BLOCKED`", "`COMPLETED`"):
            self.assertIn(state, content)
        self.assertIn("do not publish the same normalized report body twice", content)
        self.assertIn("Consolidate", content)

    def test_publication_requires_remote_success_evidence(self):
        for path in (REFERENCE, EXECUTOR):
            content = path.read_text(encoding="utf-8")
            self.assertRegex(content, r"URL(?:/| or )identifier")
        self.assertIn("PUBLISHED", REFERENCE.read_text(encoding="utf-8"))
        self.assertIn("NOT PUBLISHED", EXECUTOR.read_text(encoding="utf-8"))

    def test_rework_and_blocked_reports_are_actionable(self):
        content = REFERENCE.read_text(encoding="utf-8")
        rework = content.split("- `REWORK`:", 1)[1].split("\n- `BLOCKED`:", 1)[0]
        blocked = content.split("- `BLOCKED`:", 1)[1].split("\n- `COMPLETED`:", 1)[0]
        for term in ("failed criterion", "evidence", "correction strategy"):
            self.assertIn(term, rework)
        for term in ("concrete blocker", "impact", "required", "next safe action"):
            self.assertIn(term, blocked)

    def test_completed_still_requires_validation_and_receipt(self):
        content = REFERENCE.read_text(encoding="utf-8")
        completed = content.split("- `COMPLETED`:", 1)[1]
        self.assertIn("completed receipt", completed)
        self.assertIn("validation evidence", completed)
        self.assertIn("no open blocker", completed)

    def test_report_uses_verifiable_rationale_without_chain_of_thought(self):
        reference = REFERENCE.read_text(encoding="utf-8")
        template = COMMENT_TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("concise and verifiable", reference)
        self.assertIn("Never publish private\nchain-of-thought", reference)
        self.assertIn("rationale verificável", template)
        self.assertIn("Não inclua chain-of-thought", template)

    def test_task_project_issue_and_pr_traceability_remains(self):
        content = TASK_TEMPLATE.read_text(encoding="utf-8")
        for heading in ("## Issue GitHub", "## PR", "## Execution Contract", "## Resultado da execução"):
            self.assertIn(heading, content)
        self.assertIn("## Relatórios humanos na Issue", content)

    def test_pipeline_orders_receipt_before_human_comment(self):
        content = PIPELINE.read_text(encoding="utf-8")
        receipt = content.index("completed EXECUTION_RECEIPT")
        task = content.index("Human Task updated", receipt)
        report = content.index("EXECUTION_REPORT_COMMENT", task)
        validating = content.index("VALIDATING", report)
        self.assertLess(receipt, task)
        self.assertLess(task, report)
        self.assertLess(report, validating)


if __name__ == "__main__":
    unittest.main()
