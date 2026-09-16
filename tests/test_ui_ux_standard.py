"""Regression tests for UI/UX component intelligence and visual quality gates."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md"
REFS = SKILL.parent / "references"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestUiUxComponentIntelligence(unittest.TestCase):

    def test_skill_requires_component_source_inventory(self):
        content = read(SKILL)
        self.assertIn("COMPONENT_SOURCE_INVENTORY", content)
        self.assertIn("project-native candidates", content)
        self.assertIn("external candidates searched", content)
        self.assertIn("custom-build justification", content)

    def test_skill_loads_component_intelligence_references(self):
        content = read(SKILL)
        for reference in (
            "references/component-sources.md",
            "references/component-selection.md",
            "references/anti-ai-design.md",
        ):
            self.assertIn(reference, content)

    def test_external_components_are_not_default_source_of_truth(self):
        content = read(SKILL)
        self.assertIn("Reuse project components and design tokens", content)
        self.assertIn("External components are references or implementation candidates", content)
        self.assertIn("Do not combine several component libraries", content)

    def test_registry_policy_is_mcp_aware_and_safe(self):
        content = read(SKILL)
        self.assertIn("If shadcn MCP is already available", content)
        self.assertIn("Do not silently modify global MCP configuration", content)
        self.assertIn("community registries as third-party code", content)

    def test_curated_sources_are_documented(self):
        content = read(REFS / "component-sources.md")
        for marker in (
            "21st.dev",
            "Magic UI",
            "Origin UI",
            "Animate UI",
            "Kokonut UI",
            "Cult UI",
            "Aceternity UI",
        ):
            self.assertIn(marker, content)

    def test_anti_generic_quality_gate_has_product_rules(self):
        content = read(REFS / "anti-ai-design.md")
        self.assertIn("generic-AI failure modes", content)
        self.assertIn("Product UI", content)
        self.assertIn("Marketing UI", content)
        self.assertIn("E-commerce", content)
        self.assertIn("Differentiation check", content)


if __name__ == "__main__":
    unittest.main()
