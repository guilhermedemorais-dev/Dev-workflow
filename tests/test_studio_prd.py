import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/studio-prd/skills/studio-prd"
SCRIPT = SKILL / "scripts/plan.py"
SPEC = importlib.util.spec_from_file_location("studio_plan", SCRIPT)
PLAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLAN)


class StudioPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((SKILL / "assets/plan-template.json").read_text())

    def two_modules(self):
        second = copy.deepcopy(self.plan["modules"][0])
        second.update(id="MOD-002", task_id="TASK-002", name="Emissão fiscal")
        second["dependencies"] = [{"module_id": "MOD-001", "capability": "Dados cadastrais validados", "reason": "Documento exige destinatário"}]
        self.plan["modules"].append(second)
        self.plan["module_count"] = 2
        self.plan["stages"][0]["module_ids"].append("MOD-002")
        for phase in self.plan["orders"]:
            self.plan["orders"][phase].append("MOD-002")

    def test_unknown_estimates_are_valid_and_not_converted_to_zero(self):
        PLAN.validate(self.plan)
        output = PLAN.render(self.plan)
        self.assertIn("Capacidade (horas/semana)", output)
        self.assertIn("Não informado", output)
        self.assertIsNone(self.plan["total_estimate"]["effort_hours"])

    def test_urgent_fiscal_cannot_precede_required_capability(self):
        self.two_modules()
        self.plan["modules"][1]["urgency"]["level"] = "URGENT"
        PLAN.validate(self.plan)
        self.plan["orders"]["execution"].reverse()
        with self.assertRaisesRegex(ValueError, "dependency order"):
            PLAN.validate(self.plan)

    def test_specification_can_start_with_urgent_module(self):
        self.two_modules()
        self.plan["orders"]["specification"].reverse()
        PLAN.validate(self.plan)

    def test_cycle_rejected(self):
        self.two_modules()
        self.plan["modules"][0]["dependencies"] = [{"module_id": "MOD-002", "capability": "Fiscal", "reason": "Conflict"}]
        with self.assertRaisesRegex(ValueError, "cycle"):
            PLAN.validate(self.plan)

    def test_unknown_dependency_rejected(self):
        self.two_modules()
        self.plan["modules"][1]["dependencies"][0]["module_id"] = "MISSING"
        with self.assertRaisesRegex(ValueError, "unknown/self"):
            PLAN.validate(self.plan)

    def test_module_count_and_task_uniqueness(self):
        self.plan["module_count"] = 2
        with self.assertRaisesRegex(ValueError, "module_count"):
            PLAN.validate(self.plan)
        self.plan["module_count"] = 1
        self.two_modules()
        self.plan["modules"][1]["task_id"] = "TASK-001"
        with self.assertRaisesRegex(ValueError, "distinct complete task"):
            PLAN.validate(self.plan)

    def test_no_execution_prompt_without_real_contract_link(self):
        prompt = self.plan["modules"][0]["prompt"]
        self.assertIn("implementação não está liberada", PLAN.render(self.plan))
        self.assertIn("ainda não criado", PLAN.render(self.plan))
        prompt["mode"] = "execution"
        with self.assertRaisesRegex(ValueError, "task/contract"):
            PLAN.validate(self.plan)
        prompt.update(task_url="https://github.com/example/project/issues/1", contract_path="docs/tasks/TASK-001.json")
        self.assertIn("autorizações antes de executar", PLAN.render(self.plan))

    def test_invalid_estimates_fail(self):
        for value in ({"min": 20, "max": 10}, {"min": -1, "max": 4}, {"min": True, "max": 4}, {"min": 1, "max": float("nan")}):
            with self.subTest(value=value):
                self.plan["total_estimate"]["effort_hours"] = value
                with self.assertRaisesRegex(ValueError, "range"):
                    PLAN.validate(self.plan)

    def test_stage_coverage_required(self):
        self.two_modules()
        self.plan["stages"][0]["module_ids"] = ["MOD-001"]
        with self.assertRaisesRegex(ValueError, "one stage"):
            PLAN.validate(self.plan)

    def test_stages_cannot_put_urgent_module_before_dependency(self):
        self.two_modules()
        early = copy.deepcopy(self.plan["stages"][0])
        early.update(id="EARLY", module_ids=["MOD-002"])
        self.plan["stages"][0]["module_ids"] = ["MOD-001"]
        self.plan["stages"].insert(0, early)
        with self.assertRaisesRegex(ValueError, "stage dependency order"):
            PLAN.validate(self.plan)

    def test_prompt_links_are_clickable_and_root_relative(self):
        output = PLAN.render(self.plan)
        self.assertIn("[briefing](<../briefing/briefing.md>)", output)
        self.assertIn("[PRD](<../prd/PRD.md>)", output)
        self.assertEqual(PLAN.link("task", "https://github.com/example/p/issues/1"), "[task](<https://github.com/example/p/issues/1>)")

    def test_unsafe_links_rejected(self):
        for link in ("javascript:alert(1)", "data:text/html,payload", "//evil.example", "https://name:secret@example.com"):
            with self.subTest(link=link):
                self.plan["sources"]["briefing"] = link
                with self.assertRaises(ValueError):
                    PLAN.validate(self.plan)

    def test_bundled_md_matches_json_template(self):
        self.assertEqual((SKILL / "assets/plan-template.md").read_text(), PLAN.render(self.plan))

    def test_dependent_parallelism_rejected(self):
        self.two_modules()
        self.plan["parallel_groups"] = [{"module_ids": ["MOD-001", "MOD-002"], "rationale": "More chats"}]
        with self.assertRaisesRegex(ValueError, "cannot run in parallel"):
            PLAN.validate(self.plan)

    def test_independent_parallelism_allowed_with_rationale(self):
        self.two_modules()
        self.plan["modules"][1]["dependencies"] = []
        self.plan["parallel_groups"] = [{"module_ids": ["MOD-001", "MOD-002"], "rationale": "Separate code and data; integration gate later"}]
        PLAN.validate(self.plan)

    def test_all_normative_extensions_and_context_render(self):
        self.plan["decisions"].append({"source": "briefing decision D01", "decision": "No automatic MVP"})
        self.plan["modules"][0]["prompt"]["notes"] = ["Não duplicar identidade aprovada", "Auditar mudança de estado"]
        output = PLAN.render(self.plan)
        self.assertIn("briefing decision D01", output)
        self.assertIn("Não duplicar identidade aprovada", output)
        self.assertIn("Auditar mudança de estado", output)

    def test_raw_html_is_not_executable_in_markdown(self):
        self.plan["project"] = "<script>alert(1)</script>"
        self.assertNotIn("<script>", PLAN.render(self.plan))

    def test_cli_check_detects_md_and_revision_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            source, target = Path(temp) / "plan.json", Path(temp) / "plan.md"
            source.write_text(json.dumps(self.plan))
            target.write_text(PLAN.render(self.plan))
            command = [sys.executable, str(SCRIPT), "check", str(source), str(target)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.plan["revision"] = 2
            source.write_text(json.dumps(self.plan))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("divergence", result.stderr)

    def test_cli_invalid_input_fails_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "bad.json"
            source.write_text('{"schema_version":')
            result = subprocess.run([sys.executable, str(SCRIPT), "validate", str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
