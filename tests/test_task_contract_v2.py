"""Contract tests for the human-card / LLM-JSON task model."""

import json
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SDD = ROOT / "plugins/sdd-spec-factory"
HARNESS = ROOT / "plugins/dev-workflow-standard/skills/dev-workflow-standard"
TASK_TEMPLATE = SDD / "templates/task-template.md"
CONTRACT_TEMPLATE = SDD / "templates/execution-contract-template.json"
COMMENT_TEMPLATE = ROOT / "plugins/dev-implementation-standard/templates/execution-report-comment-template.md"
PIPELINE = ROOT / "docs/workflow-pipeline.md"

STANDARD_SECTORS = {
    "database", "backend", "frontend", "ui_ux", "qa", "security",
    "devops", "observability", "documentation", "harness",
}


class TestTaskContractV2(unittest.TestCase):

    def setUp(self):
        self.task = TASK_TEMPLATE.read_text(encoding="utf-8")
        self.contract = json.loads(CONTRACT_TEMPLATE.read_text(encoding="utf-8"))

    def test_json_is_equivalent_task_contract_v2(self):
        self.assertEqual(self.contract["schema_version"], 2)
        for field in (
            "contract_revision", "human_task", "summary", "discovery", "goal",
            "current_state", "expected_result", "scope", "out_of_scope",
            "allowed_paths", "protected_paths", "requirements",
            "business_rules", "references", "design", "microtasks", "sectors",
            "specs", "docs", "pipeline", "gates", "required_tests",
            "acceptance_criteria", "stop_conditions",
            "execution_prompt", "reporting",
        ):
            self.assertIn(field, self.contract)
        self.assertEqual(self.contract["human_task"]["representation"], "github_issue")
        self.assertIn("normative_equivalence", self.contract["human_task"])

    def test_reference_library_and_design_are_first_class(self):
        self.assertIn("docs/biblioteca-referencias/", self.task)
        self.assertIn("Design Guide", self.task)
        self.assertIn("Arquivo e seção", self.task)
        self.assertIn("purpose", self.contract["references"][0])
        self.assertIn("project_path", self.contract["references"][0])
        for field in ("guide", "tokens", "visual_references", "component_library", "mockup"):
            self.assertIn(field, self.contract["design"])

    def test_card_has_glanceable_summary_and_collaborative_discovery(self):
        self.assertIn("> **Resumo:**", self.task)
        self.assertIn("## Discovery / SDD colaborativo", self.task)
        for term in (
            "Perguntas e respostas", "Pesquisa realizada", "Decisões consolidadas",
            "DISCOVERY_SDD_COMPLETED", "aprovação humana",
        ):
            self.assertIn(term, self.task)
        for heading in (
            "## Estado atual encontrado", "## Resultado esperado",
            "## Requisitos", "## Paths permitidos e protegidos",
            "## Condições de parada",
        ):
            self.assertIn(heading, self.task)

    def test_microtasks_route_skills_plugins_capabilities_and_tools(self):
        for term in (
            "## Microtarefas", "Skill executora", "Plugin", "Capability",
            "Tool preferencial", "Referências obrigatórias", "Depende de",
            "Condição para concluir",
        ):
            self.assertIn(term, self.task)
        sample = self.contract["microtasks"][0]
        for field in (
            "id", "title", "summary", "owner_skill", "owner_plugin",
            "capability", "preferred_tool", "depends_on", "references",
            "allowed_paths", "checklist", "deliverables", "completion_condition",
        ):
            self.assertIn(field, sample)

    def test_full_delivery_and_independent_validation_are_present(self):
        for heading in (
            "Implementação", "Testes do executor", "QA funcional independente",
            "QA de segurança", "QA UI / UX", "DevOps e observabilidade",
            "Rework e reteste", "Gate do PR", "Gate Final do Harness",
            "Aceite e merge humanos",
        ):
            self.assertIn(heading, self.task)
        self.assertEqual(set(self.contract["sectors"]), STANDARD_SECTORS)

    def test_template_sector_dependencies_are_executable(self):
        sectors = self.contract["sectors"]
        required = {
            name for name, sector in sectors.items()
            if sector["applicability"] == "REQUIRED"
        }
        for name, sector in sectors.items():
            for dependency in sector["depends_on"]:
                self.assertIn(dependency, required, f"{name} depends on non-REQUIRED {dependency}")
        self.assertEqual(set(sectors["harness"]["depends_on"]), required - {"harness"})
        self.assertIn(self.contract["design"]["applicability"], ("REQUIRED", "N/A"))

    def test_json_reports_policy_not_runtime_evidence(self):
        self.assertNotIn("status", self.contract)
        reporting = self.contract["reporting"]
        self.assertNotIn("publication_evidence", reporting)
        self.assertNotIn("token_usage", reporting)
        self.assertNotIn("changed_surface", reporting)
        self.assertIn("publication_evidence_requirement", reporting)
        self.assertIn("token_usage_fields", reporting)
        self.assertIn("changed_surface_fields", reporting)

    def test_delivery_card_covers_every_normative_json_value(self):
        contract = json.loads((ROOT / "docs/execution/TASK-011.json").read_text())
        card = (ROOT / contract["human_task"]["local_mirror"]).read_text()
        def leaves(value):
            if isinstance(value, dict):
                for child in value.values():
                    yield from leaves(child)
            elif isinstance(value, list):
                for child in value:
                    yield from leaves(child)
            else:
                yield str(value).lower()
        for field, value in contract.items():
            if field in {"schema_version", "task_id", "human_task", "contract_revision"}:
                continue
            match = re.search(
                rf"<!-- contract-field: {field} -->(.*?)<!-- /contract-field: {field} -->",
                card, re.S,
            )
            self.assertIsNotNone(match, field)
            section = " ".join(match.group(1).lower().split())
            for leaf in leaves(value):
                self.assertIn(" ".join(leaf.split()), section, f"{field}: {leaf}")
        self.assertIn("contract_revision: " + contract["contract_revision"], card)
        self.assertIn(contract["human_task"]["issue_url"], card)

    def test_delivery_references_and_microtasks_resolve(self):
        contract = json.loads((ROOT / "docs/execution/TASK-011.json").read_text())
        refs = {ref["id"] for ref in contract["references"]}
        tasks = {task["id"] for task in contract["microtasks"]}
        for ref in contract["references"]:
            self.assertTrue((ROOT / ref["project_path"]).is_file())
            self.assertTrue(ref["purpose"])
        for task in contract["microtasks"]:
            self.assertTrue(set(task["references"]) <= refs)
            self.assertTrue(set(task["depends_on"]) <= tasks - {task["id"]})
        for sector in contract["sectors"].values():
            self.assertTrue(set(sector["required_sources"]) <= refs)
            self.assertTrue(set(sector["microtasks"]) <= tasks)

    def test_reporting_requires_tokens_and_changed_surface(self):
        reference = (HARNESS / "references/execution-report-comments.md").read_text(encoding="utf-8")
        comment = COMMENT_TEMPLATE.read_text(encoding="utf-8")
        for content in (reference, comment):
            self.assertIn("DISCOVERY_SDD_COMPLETED", content)
            self.assertIn("input_tokens", content)
            self.assertIn("output_tokens", content)
            self.assertIn("total_tokens", content)
            self.assertIn("NOT_AVAILABLE", content)
            self.assertIn("changed_files", content)
            self.assertIn("remote_mutations", content)
        self.assertIn("returned comment URL or identifier", reference)
        next_step = comment.index("### Próximo passo")
        changed = comment.index("### Superfície alterada")
        tokens = comment.index("### Uso de tokens")
        self.assertLess(next_step, changed)
        self.assertLess(changed, tokens)

    def test_pipeline_requires_published_planning_report_before_ready(self):
        pipeline = PIPELINE.read_text(encoding="utf-8")
        planning = pipeline.index("DISCOVERY_SDD_COMPLETED")
        approval = pipeline.index("HUMAN APPROVAL", planning)
        implementation = pipeline.index("dev-implementation-standard", approval)
        self.assertLess(planning, approval)
        self.assertLess(approval, implementation)

    def test_skills_share_the_same_contract_model(self):
        expected = {
            "dev-workflow-standard": "normative equivalence",
            "sdd-spec-factory": "normative equivalence",
            "dev-implementation-standard": "normative equivalence",
            "qa-testing-standard": "normative equivalence",
            "security-standard": "normative equivalence",
            "ui-ux-standard": "normative equivalence",
            "devops-standard": "normative equivalence",
        }
        for plugin, phrase in expected.items():
            path = ROOT / f"plugins/{plugin}/skills/{plugin}/SKILL.md"
            with self.subTest(plugin=plugin):
                self.assertIn(phrase, path.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
