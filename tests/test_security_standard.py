"""Regression tests for security-standard validation and publication gates."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/security-standard/skills/security-standard/SKILL.md"
REFS = SKILL.parent / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestSecurityValidationGate(unittest.TestCase):

    def test_skill_loads_false_positive_and_multistack_references(self):
        content = read(SKILL)
        self.assertIn("references/false-positive-validation.md", content)
        self.assertIn("references/stack-profiles.md", content)

    def test_external_tracking_requires_confirmation(self):
        content = read(SKILL)
        self.assertIn("Do not create or update a GitHub issue", content)
        self.assertIn("status is `CONFIRMED`", content)
        self.assertIn("confidence is `HIGH` or `MEDIUM`", content)

    def test_false_positive_checklist_is_mandatory_and_complete(self):
        content = read(REFS / "false-positive-validation.md")
        self.assertIn("Answer every item", content)
        self.assertIn("imported validators, guards, policies, middleware", content)
        self.assertIn("If any answer is `UNKNOWN`", content)
        self.assertIn("Automatic creation or update of GitHub issues", content)

    def test_profiles_are_multistack_and_version_aware(self):
        content = read(REFS / "stack-profiles.md")
        for marker in (
            "Node.js", "PHP", "WordPress/WooCommerce", "Laravel", "Python",
            "Java", "Go modules", "Docker", "Nginx",
        ):
            self.assertIn(marker, content)
        self.assertIn("Resolve the installed version", content)

    def test_report_separates_unconfirmed_candidates(self):
        content = read(REFS / "report-template.md")
        self.assertIn("## Validation Backlog", content)
        self.assertIn("not confirmed vulnerabilities", content)
        self.assertIn("not eligible for automatic external issue creation", content)


if __name__ == "__main__":
    unittest.main()
