"""Document/fixture contract checks, not a production router or LLM runtime test."""

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
SDD = ROOT / "plugins/sdd-spec-factory"
EXAMPLE = ROOT / "docs/examples/sector-context-qa/execution-contract.json"
STANDARD = {"database", "backend", "frontend", "ui_ux", "qa", "security",
            "devops", "observability", "documentation", "harness"}
FIELDS = {"owner", "applicability", "depends_on", "task_sections",
          "required_sources", "conditional_sources", "required_validations"}


class TestSectorContextRouting(unittest.TestCase):
    """Assertions validate published shapes and deliberately malformed fixtures."""

    def setUp(self):
        self.contract = json.loads(EXAMPLE.read_text())
        self.rules = (HARNESS / "references/context-routing.md").read_text()
        self.template = (SDD / "templates/task-template.md").read_text()

    def assert_reference(self, reference, contract):
        path, _, anchor = reference.partition("#")
        if path == "task:":
            path = contract["task_path"]
        source = ROOT / path
        self.assertTrue(source.is_file(), f"mandatory_reference_missing: {reference}")
        if anchor:
            self.assertIn(f'<a id="{anchor}"></a>', source.read_text(), reference)

    def assert_routed_shape(self, contract):
        """Test-only fixture assertions. No CLI, invocation or state transitions."""
        self.assertEqual(contract["schema_version"], 1)
        sectors = contract["sectors"]
        self.assertTrue(STANDARD.issubset(sectors))
        self.assert_reference(contract["task_path"], contract)
        for reference in contract["global_acceptance_refs"]:
            self.assert_reference(reference, contract)
        for name, sector in sectors.items():
            self.assertTrue(FIELDS.issubset(sector), name)
            self.assertIn(sector["applicability"], ("REQUIRED", "N/A"))
            owner = sector["owner"]
            self.assertTrue((ROOT / f"plugins/{owner}/skills/{owner}/SKILL.md").is_file(), owner)
            if name not in STANDARD:
                self.assertIn(name, (ROOT / contract["task_path"]).read_text())
            if sector["applicability"] == "N/A":
                self.assertTrue(sector.get("reason", "").strip(), name)
                self.assertFalse(sector["depends_on"], name)
            else:
                self.assertTrue(sector["task_sections"], name)
                self.assertTrue(sector["required_validations"], name)
            self.assertFalse({"status", "result", "receipts", "evidence", "logs",
                              "checklist", "spec_body"} & sector.keys())
            for reference in sector["task_sections"]:
                self.assertTrue(reference.startswith("task:#"))
                self.assert_reference(reference, contract)
            for kind in ("required_sources", "conditional_sources", "optional_sources"):
                for source in sector.get(kind, []):
                    self.assertTrue(source["purpose"].strip())
                    self.assert_reference(source["path"], contract)
                    if kind == "conditional_sources":
                        self.assertTrue(source["condition"].strip())
            for phase in ("depends_on", "planning_depends_on"):
                dependencies = sector.get(phase, [])
                self.assertEqual(len(dependencies), len(set(dependencies)))
                for dependency in dependencies:
                    self.assertIn(dependency, sectors)
                    self.assertNotEqual(dependency, name)
                    self.assertEqual(sectors[dependency]["applicability"], "REQUIRED")
        # Independent phase DAG checks do not implement checkpoint execution.
        for phase in ("depends_on", "planning_depends_on"):
            def assert_acyclic(name, ancestors):
                self.assertNotIn(name, ancestors, f"cycle in {phase}")
                for dependency in sectors[name].get(phase, []):
                    assert_acyclic(dependency, ancestors | {name})
            for name in sectors:
                assert_acyclic(name, set())
        required = {name for name, sector in sectors.items()
                    if sector["applicability"] == "REQUIRED"} - {"harness"}
        self.assertEqual(set(sectors["harness"]["depends_on"]), required)

    def test_t01_t04_template_ten_rows_have_owners_applicability_dependencies(self):
        self.assertIn("Sector Validation Matrix", self.template)
        rows = [line for line in self.template.splitlines() if line.startswith("| ")]
        for name in STANDARD:
            row = next(row for row in rows if f"/ {name} |" in row)
            self.assertIn("REQUIRED", row)
            self.assertGreaterEqual(len(row.split("|")), 8)
        self.assertIn("N/A exige motivo", self.template)

    def test_t05_t07_example_and_actual_task_sources_resolve(self):
        self.assert_routed_shape(self.contract)
        self.assert_routed_shape(json.loads((ROOT / "docs/execution/TASK-009.json").read_text()))

    def test_t08_t09_router_contains_no_mutable_state_or_bodies(self):
        allowed = FIELDS | {"reason", "planning_depends_on", "optional_sources"}
        for sector in self.contract["sectors"].values():
            self.assertTrue(set(sector) <= allowed)
        self.assertLess(len(EXAMPLE.read_text()), 9000)
        self.assertNotIn("steps_to_reproduce", EXAMPLE.read_text())
        self.assertNotIn("commands_and_results", EXAMPLE.read_text())

    def test_t10_t13_harness_full_task_specialist_slice_and_sources(self):
        normalized = " ".join(self.rules.split())
        self.assertIn("Harness reads the complete Human Task", normalized)
        self.assertIn("specialist does not read the complete Human Task by default", normalized)
        for field in ("task_sections", "required_sources", "global_acceptance_refs",
                      "dependency_receipts", "allowed paths"):
            self.assertIn(field, self.rules)

    def test_t14_t15_conditional_and_optional_are_not_automatic(self):
        normalized = " ".join(self.rules.split())
        self.assertIn("do not load OPTIONAL automatically", normalized)
        self.assertIn("evaluate that condition before loading", normalized)
        source = self.contract["sectors"]["backend"]["conditional_sources"][0]
        self.assertEqual(set(source), {"path", "purpose", "condition"})
        self.assertTrue(self.contract["sectors"]["security"]["optional_sources"])

    def test_t16_owner_cannot_attest_another_owner(self):
        self.assertIn("Only the sector owner attests its result", self.rules)
        self.assertIn("cannot mark another sector PASS", self.rules)
        self.assertIn("REWORK_REQUESTED", self.rules)

    def test_t17_t18_final_gate_requires_all_required_but_not_na(self):
        normalized = " ".join(self.rules.split())
        self.assertIn("justified N/A does not block", normalized)
        self.assertIn("every other REQUIRED sector", normalized)
        self.assertIn("prevents Task COMPLETED", normalized)
        self.assert_routed_shape(self.contract)

    def test_t19_missing_required_source_rejected(self):
        self.contract["sectors"]["backend"]["required_sources"][0]["path"] = "missing-required.md"
        with self.assertRaisesRegex(AssertionError, "mandatory_reference_missing"):
            self.assert_routed_shape(self.contract)

    def test_t19_missing_anchor_rejected(self):
        self.contract["sectors"]["qa"]["task_sections"] = ["task:#missing-anchor"]
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_t20_source_conflict_and_context_expansion_stop_claim(self):
        for term in ("source_of_truth_conflict", "CONTEXT_EXPANSION", "reason",
                     "required_source", "blocking_claim", "do not silently pick one"):
            self.assertIn(term, self.rules)

    def test_t21_existing_receipts_and_freshness_required(self):
        for term in ("SKILL_RECEIPT", "EXECUTION_RECEIPT", "stale", "revision",
                     "Revalidate after material artifact changes"):
            self.assertIn(term, self.rules)
        self.assertNotRegex(self.rules, r"(?:QA|SECTOR|TEST)_RECEIPT")

    def test_t22_public_docs_explain_sector_routing(self):
        readme = (ROOT / "README.md").read_text()
        for term in ("qa-testing-standard", "Context Routing", "Sector Validation Matrix"):
            self.assertIn(term, readme)

    def test_negative_na_without_reason(self):
        self.contract["sectors"]["database"]["reason"] = " "
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_negative_source_without_purpose_and_condition(self):
        for field in ("purpose", "condition"):
            contract = deepcopy(self.contract)
            contract["sectors"]["backend"]["conditional_sources"][0][field] = ""
            with self.subTest(field=field), self.assertRaises(AssertionError):
                self.assert_routed_shape(contract)

    def test_negative_unknown_dependency(self):
        self.contract["sectors"]["qa"]["depends_on"] = ["unknown"]
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_negative_unknown_owner_and_sector(self):
        contract = deepcopy(self.contract)
        contract["sectors"]["qa"]["owner"] = "unregistered-qa"
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(contract)
        self.assertNotIn("unknown", self.contract["sectors"])
        self.assertIn("Unknown sectors, owners, dependencies", self.rules)

    def test_negative_cycles_in_either_phase(self):
        for phase in ("depends_on", "planning_depends_on"):
            contract = deepcopy(self.contract)
            contract["sectors"]["backend"][phase] = ["qa"]
            contract["sectors"]["qa"][phase] = ["backend"]
            with self.subTest(phase=phase), self.assertRaisesRegex(AssertionError, "cycle"):
                self.assert_routed_shape(contract)

    def test_negative_self_dependency(self):
        self.contract["sectors"]["qa"]["depends_on"] = ["qa"]
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_negative_harness_omits_required_sector(self):
        self.contract["sectors"]["harness"]["depends_on"].remove("qa")
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_negative_state_in_contract(self):
        self.contract["sectors"]["qa"]["status"] = "PASS"
        with self.assertRaises(AssertionError):
            self.assert_routed_shape(self.contract)

    def test_s01_docs_only_shape_does_not_require_other_specialists(self):
        for name, sector in self.contract["sectors"].items():
            if name not in {"documentation", "harness"}:
                sector.update(applicability="N/A", reason="Docs-only fixture, no behavior",
                              depends_on=[], task_sections=[], required_sources=[],
                              conditional_sources=[], required_validations=[])
        self.contract["sectors"]["documentation"]["depends_on"] = []
        self.contract["sectors"]["harness"]["depends_on"] = ["documentation"]
        self.assert_routed_shape(self.contract)

    def test_s05_s07_final_qa_dependencies_separate_from_planning(self):
        qa = self.contract["sectors"]["qa"]
        self.assertEqual(qa["depends_on"], ["backend", "frontend"])
        self.assertEqual(qa["planning_depends_on"], [])
        self.assertEqual(self.contract["sectors"]["security"]["depends_on"], ["backend"])
        self.assertIn("Planning completion never satisfies final validation", self.rules)
        self.assertIn("PENDING", self.rules)

    def test_s09_security_slice_has_no_unrelated_sections_or_sources(self):
        security = self.contract["sectors"]["security"]
        self.assertEqual(security["task_sections"], ["task:#security"])
        self.assertEqual({source["path"].split("#")[-1] for source in security["required_sources"]},
                         {"security", "api"})
        self.assertEqual(security["depends_on"], ["backend"])

    def test_s10_persistence_source_is_conditional_not_global(self):
        backend = self.contract["sectors"]["backend"]
        self.assertTrue(backend["conditional_sources"][0]["path"].endswith("#persistence"))
        self.assertFalse(any(source["path"].endswith("#persistence")
                             for source in backend["required_sources"]))
        self.assertIn("An active conditional source becomes mandatory", self.rules)

    def test_legacy_v1_remains_valid_without_sectors(self):
        legacy = json.loads((ROOT / "docs/execution/TASK-002.json").read_text())
        self.assertEqual(legacy["schema_version"], 1)
        self.assertNotIn("sectors", legacy)
        self.assertIn("Without `sectors`, v1 is valid legacy input", self.rules)

    def test_example_is_not_fabricated_execution(self):
        task = (ROOT / self.contract["task_path"]).read_text()
        self.assertIn("NÃO EXECUTADO", task)
        self.assertIn("nenhum SKILL_RECEIPT ou EXECUTION_RECEIPT fictício", task)
        self.assertNotRegex(task, r"Status:?\s*PASS")

    def test_installed_host_and_checkpoint_completion_boundaries(self):
        self.assertIn("not assumptions about sibling versioned plugin caches", self.rules)
        execution = (HARNESS / "references/harness-execution.md").read_text()
        self.assertIn("checkpoint gate applies to its own scope", execution)
        self.assertIn("For final Task completion", execution)


if __name__ == "__main__":
    unittest.main()
