"""
Tests for plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md
changes introduced in this PR.

Validates new and updated content:
- Mission: "Enforce the mandatory task contract before delegation"
- Hard Limits: "Reject any executable task that does not follow the mandatory task structure"
- NEW Mandatory Task Governance section: 22 required fields list, filename stability
- NEW Official Kanban Method: 6 columns, no blocked column, labels, rework label
- NEW Definition of Entry / Exit table: 6 columns with entry/exit criteria
- NEW GitHub-Ready Task Structure section
- NEW Recommended Task Template section
- Review Rules update: rejected review moves card to In Progress with rework label
"""

import os
import re
import unittest

SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'plugins', 'dev-workflow-standard',
    'skills', 'dev-workflow-standard', 'SKILL.md'
)


def read_skill():
    with open(SKILL_PATH, 'r', encoding='utf-8') as f:
        return f.read()


class TestDevWorkflowMission(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_enforce_task_contract_in_mission(self):
        """NEW Mission item: Enforce the mandatory task contract before delegation."""
        self.assertIn('Enforce the mandatory task contract before delegation', self.content)

    def test_require_specs_before_tasks_in_mission(self):
        """Mission must require specs before tasks and tasks before implementation."""
        self.assertIn('Require specs before tasks, and tasks before implementation', self.content)

    def test_delegate_review_approve_in_mission(self):
        """Mission must include delegate, review and approve."""
        self.assertIn('Delegate, review and approve', self.content)


class TestDevWorkflowHardLimits(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_never_write_product_code(self):
        """Hard limit: Never write product code directly."""
        self.assertIn('Never write product code directly', self.content)

    def test_never_skip_specs(self):
        """Hard limit: Never skip specs."""
        self.assertIn('Never skip specs', self.content)

    def test_never_create_task_without_specs(self):
        """Hard limit: Never create a task without sufficient specs."""
        self.assertIn('Never create a task without sufficient specs', self.content)

    def test_reject_task_without_mandatory_structure(self):
        """NEW Hard limit: Reject any executable task that does not follow the mandatory task structure."""
        self.assertIn('Reject any executable task that does not follow the mandatory task structure', self.content)

    def test_no_deploy_without_approved_pr(self):
        """Hard limit: No deploy approved without an approved PR."""
        self.assertIn('No deploy is approved without an approved PR', self.content)

    def test_docs_conflict_stop_and_ask(self):
        """Hard limit: If docs conflict with code, stop and ask for a decision."""
        self.assertIn('If docs conflict with code, stop and ask for a decision', self.content)


class TestDevWorkflowMandatoryTaskGovernance(unittest.TestCase):
    """Tests for the NEW 'Mandatory Task Governance' section."""

    def setUp(self):
        self.content = read_skill()

    def test_mandatory_task_governance_section_exists(self):
        """NEW section: Mandatory Task Governance must exist."""
        self.assertIn('## Mandatory Task Governance', self.content)

    def test_spec_first_task_second_implementation_third(self):
        """Official order: spec first, executable task second, implementation third."""
        self.assertIn('spec first, executable task second,\nimplementation third', self.content)

    def test_rejects_task_without_specs(self):
        """Orchestrator rejects task that skips specs."""
        self.assertIn('rejects any task that skips specs', self.content)

    def test_rejects_task_lacking_mandatory_fields(self):
        """Orchestrator rejects task that lacks mandatory fields."""
        self.assertIn('lacks\nmandatory fields', self.content)

    def test_mandatory_field_titulo(self):
        """Mandatory field: Título."""
        self.assertIn('- Título', self.content)

    def test_mandatory_field_status_visual(self):
        """Mandatory field: Status visual."""
        self.assertIn('- Status visual', self.content)

    def test_mandatory_field_tipo(self):
        """Mandatory field: Tipo."""
        self.assertIn('- Tipo', self.content)

    def test_mandatory_field_prioridade(self):
        """Mandatory field: Prioridade."""
        self.assertIn('- Prioridade', self.content)

    def test_mandatory_field_objetivo(self):
        """Mandatory field: Objetivo."""
        self.assertIn('- Objetivo', self.content)

    def test_mandatory_field_specs_obrigatorias(self):
        """Mandatory field: Specs obrigatórias."""
        self.assertIn('- Specs obrigatórias', self.content)

    def test_mandatory_field_docs_obrigatorios(self):
        """Mandatory field: Docs obrigatórios."""
        self.assertIn('- Docs obrigatórios', self.content)

    def test_mandatory_field_arquivos_e_modulos_permitidos(self):
        """Mandatory field: Arquivos e módulos permitidos."""
        self.assertIn('- Arquivos e módulos permitidos', self.content)

    def test_mandatory_field_fora_do_escopo(self):
        """Mandatory field: Fora do escopo."""
        self.assertIn('- Fora do escopo', self.content)

    def test_mandatory_field_estado_atual_encontrado(self):
        """Mandatory field: Estado atual encontrado."""
        self.assertIn('- Estado atual encontrado', self.content)

    def test_mandatory_field_resultado_esperado(self):
        """Mandatory field: Resultado esperado."""
        self.assertIn('- Resultado esperado', self.content)

    def test_mandatory_field_regras_obrigatorias(self):
        """Mandatory field: Regras obrigatórias da implementação."""
        self.assertIn('- Regras obrigatórias da implementação', self.content)

    def test_mandatory_field_checklist_execucao(self):
        """Mandatory field: Checklist de execução."""
        self.assertIn('- Checklist de execução', self.content)

    def test_mandatory_field_prompt_para_executor(self):
        """Mandatory field: Prompt para o executor."""
        self.assertIn('- Prompt para o executor', self.content)

    def test_mandatory_field_condicoes_de_parada(self):
        """Mandatory field: Condições de parada."""
        self.assertIn('- Condições de parada', self.content)

    def test_mandatory_field_testes_obrigatorios(self):
        """Mandatory field: Testes obrigatórios."""
        self.assertIn('- Testes obrigatórios', self.content)

    def test_mandatory_field_evidencias_esperadas_no_pr(self):
        """Mandatory field: Evidências esperadas no PR."""
        self.assertIn('- Evidências esperadas no PR', self.content)

    def test_mandatory_field_criterios_de_aceite(self):
        """Mandatory field: Critérios de aceite."""
        self.assertIn('- Critérios de aceite', self.content)

    def test_mandatory_field_banco(self):
        """Mandatory field: Banco."""
        self.assertIn('- Banco', self.content)

    def test_mandatory_field_api_backend(self):
        """Mandatory field: API/Backend."""
        self.assertIn('- API/Backend', self.content)

    def test_mandatory_field_frontend_ui(self):
        """Mandatory field: Frontend/UI."""
        self.assertIn('- Frontend/UI', self.content)

    def test_mandatory_field_validacao(self):
        """Mandatory field: Validação."""
        self.assertIn('- Validação', self.content)

    def test_mandatory_field_riscos_lacunas(self):
        """Mandatory field: Riscos/Lacunas."""
        self.assertIn('- Riscos/Lacunas', self.content)

    def test_mandatory_field_resultado_da_execucao(self):
        """Mandatory field: Resultado da execução."""
        self.assertIn('- Resultado da execução', self.content)

    def test_task_filename_remains_stable(self):
        """Task filename must remain stable for traceability."""
        self.assertIn('The task filename remains stable for traceability', self.content)

    def test_no_status_in_filename(self):
        """No visual status, emojis, Kanban status, or transient state in physical filename."""
        self.assertIn('Do not put visual status', self.content)
        self.assertIn('emojis, Kanban status, or transient workflow state in the physical filename', self.content)

    def test_status_belongs_in_content_only(self):
        """Status belongs in the task content only."""
        self.assertIn('Status belongs in the task content only', self.content)


class TestDevWorkflowOfficialKanbanMethod(unittest.TestCase):
    """Tests for the NEW 'Official Kanban Method' section."""

    def setUp(self):
        self.content = read_skill()

    def test_official_kanban_method_section_exists(self):
        """NEW section: Official Kanban Method must exist."""
        self.assertIn('## Official Kanban Method', self.content)

    def test_six_kanban_columns(self):
        """Must define exactly 6 Kanban columns."""
        self.assertIn('1. Backlog', self.content)
        self.assertIn('2. Discovery / SDD', self.content)
        self.assertIn('3. Ready for Dev', self.content)
        self.assertIn('4. In Progress', self.content)
        self.assertIn('5. In Review', self.content)
        self.assertIn('6. Done', self.content)

    def test_no_blocked_column(self):
        """Must state: do not create a blocked column."""
        self.assertIn('Do not create\na blocked column', self.content)

    def test_blocked_card_stays_in_current_column(self):
        """A blocked card stays in its current column with the blocked label."""
        self.assertIn('A blocked card stays in its current column with the `blocked`\nlabel', self.content)

    def test_rework_label_on_review_failure(self):
        """If review fails, move card back to In Progress and add rework label."""
        self.assertIn('move the card back to\n`In Progress` and add the `rework` label', self.content)

    def test_recommended_blocked_label(self):
        """Recommended labels must include blocked."""
        self.assertIn('- `blocked`', self.content)

    def test_recommended_needs_info_label(self):
        """Recommended labels must include needs-info."""
        self.assertIn('- `needs-info`', self.content)

    def test_recommended_rework_label(self):
        """Recommended labels must include rework."""
        self.assertIn('- `rework`', self.content)

    def test_recommended_high_priority_label(self):
        """Recommended labels must include high-priority."""
        self.assertIn('- `high-priority`', self.content)

    def test_recommended_bug_label(self):
        """Recommended labels must include bug."""
        self.assertIn('- `bug`', self.content)

    def test_recommended_feature_label(self):
        """Recommended labels must include feature."""
        self.assertIn('- `feature`', self.content)

    def test_recommended_tech_debt_label(self):
        """Recommended labels must include tech-debt."""
        self.assertIn('- `tech-debt`', self.content)

    def test_column_means_process_step(self):
        """Column means process step; label means condition or classification."""
        self.assertIn('Column means process step', self.content)
        self.assertIn('Label means condition or classification', self.content)


class TestDevWorkflowDefinitionOfEntryExit(unittest.TestCase):
    """Tests for the NEW 'Definition of Entry / Exit' section."""

    def setUp(self):
        self.content = read_skill()

    def test_definition_of_entry_exit_section_exists(self):
        """NEW section: Definition of Entry / Exit must exist."""
        self.assertIn('## Definition of Entry / Exit', self.content)

    def test_entry_exit_table_exists(self):
        """Entry/Exit table must exist with Column, Definition of Entry, Definition of Exit headers."""
        self.assertIn('| Column | Definition of Entry | Definition of Exit |', self.content)

    def test_backlog_entry_exit(self):
        """Backlog column must have entry and exit criteria."""
        self.assertIn('| Backlog |', self.content)
        self.assertIn('Demand, bug, idea, or risk captured as an item', self.content)

    def test_discovery_sdd_entry_exit(self):
        """Discovery / SDD column must have entry and exit criteria."""
        self.assertIn('| Discovery / SDD |', self.content)
        self.assertIn('Required specs exist, scope is clear', self.content)

    def test_ready_for_dev_entry_exit(self):
        """Ready for Dev column must have entry and exit criteria."""
        self.assertIn('| Ready for Dev |', self.content)
        self.assertIn('Executable task exists, mandatory specs are linked', self.content)
        # Exit: Executor starts the task and sets status to Em andamento
        self.assertIn('updates task status to `🟡 Em andamento`', self.content)

    def test_in_progress_entry_exit(self):
        """In Progress column must have entry and exit criteria."""
        self.assertIn('| In Progress |', self.content)
        self.assertIn('Executor accepted the task, read task/specs', self.content)

    def test_in_review_entry_exit(self):
        """In Review column must have entry and exit criteria."""
        self.assertIn('| In Review |', self.content)
        self.assertIn('PR or review package exists with task, specs, evidence', self.content)

    def test_done_entry_exit(self):
        """Done column must have entry and exit criteria."""
        self.assertIn('| Done |', self.content)
        self.assertIn('Review passed, required validations are evidenced', self.content)

    def test_orchestrator_uses_definitions_as_gate_checks(self):
        """Orchestrator must use entry/exit definitions as gate checks."""
        self.assertIn('orchestrator must use these definitions as gate checks', self.content)


class TestDevWorkflowGitHubReadyTaskStructure(unittest.TestCase):
    """Tests for the NEW 'GitHub-Ready Task Structure' section."""

    def setUp(self):
        self.content = read_skill()

    def test_github_ready_task_structure_section_exists(self):
        """NEW section: GitHub-Ready Task Structure must exist."""
        self.assertIn('## GitHub-Ready Task Structure', self.content)

    def test_do_not_assume_github_available(self):
        """Must not assume GitHub Projects, Issues, or boards are available."""
        self.assertIn('Do not assume GitHub Projects, Issues, or boards are available', self.content)

    def test_one_issue_per_task(self):
        """One issue per task when the project uses GitHub Issues."""
        self.assertIn('one issue per task when the project uses GitHub Issues', self.content)

    def test_branch_sugerida_recorded(self):
        """Branch sugerida recorded in the task."""
        self.assertIn('branch sugerida recorded in the task', self.content)

    def test_status_consistent_with_kanban(self):
        """Status field consistent with official Kanban columns."""
        self.assertIn('status field consistent with the official Kanban columns', self.content)

    def test_explicit_fields_list(self):
        """Explicit required fields for GitHub readiness."""
        fields = [
            'responsável',
            'bloqueios',
            'specs obrigatórias',
            'branch\n  sugerida',
            'evidências',
            'issue criada/vinculada',
            'Pronto para GitHub Projects',
        ]
        for field in fields:
            with self.subTest(field=field):
                self.assertIn(field, self.content)


class TestDevWorkflowRecommendedTaskTemplate(unittest.TestCase):
    """Tests for the NEW 'Recommended Task Template' section in dev-workflow-standard."""

    def setUp(self):
        self.content = read_skill()

    def test_recommended_task_template_section_exists(self):
        """NEW section: Recommended Task Template must exist."""
        self.assertIn('## Recommended Task Template', self.content)

    def test_template_starts_with_titulo(self):
        """Template must start with # Título."""
        self.assertIn('# Título', self.content)

    def test_template_has_status_visual(self):
        """Template must include Status visual section."""
        self.assertIn('## Status visual', self.content)

    def test_template_kanban_all_columns(self):
        """Template status Kanban includes all 6 columns."""
        self.assertIn('Backlog | Discovery / SDD | Ready for Dev | In Progress | In Review | Done', self.content)

    def test_template_has_prompt_para_executor(self):
        """Template must include Prompt para o executor with operational contract text."""
        self.assertIn('## Prompt para o executor', self.content)
        self.assertIn('Use esta task como contrato operacional', self.content)

    def test_template_checklist_de_execucao(self):
        """Template must include Checklist de execução."""
        self.assertIn('## Checklist de execução', self.content)
        self.assertIn('1. Leitura da task e specs', self.content)
        self.assertIn('6. Handoff para review', self.content)

    def test_template_has_resultado_da_execucao(self):
        """Template must include Resultado da execução."""
        self.assertIn('## Resultado da execução', self.content)

    def test_template_has_all_layer_sections(self):
        """Template must have Banco, API/Backend, Frontend/UI, Validação sections."""
        for section in ['## Banco', '## API/Backend', '## Frontend/UI', '## Validação']:
            with self.subTest(section=section):
                self.assertIn(section, self.content)

    def test_template_has_riscos_lacunas(self):
        """Template must include Riscos/Lacunas."""
        self.assertIn('## Riscos/Lacunas', self.content)

    def test_template_pronto_para_github_projects(self):
        """Template must include Pronto para GitHub Projects: sim/não."""
        self.assertIn('Pronto para GitHub Projects: sim/não', self.content)


class TestDevWorkflowReviewRules(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_review_rules_section_exists(self):
        """Review Rules section must exist."""
        self.assertIn('## Review Rules', self.content)

    def test_rejected_review_moves_to_in_progress(self):
        """NEW: Rejected review moves the card back to In Progress."""
        self.assertIn("Rejected review moves the card back to `In Progress`", self.content)

    def test_rework_label_on_rejected_review(self):
        """NEW: Rejected review adds the rework label until corrected."""
        self.assertIn("the `rework` label until corrected", self.content)

    def test_approve_or_request_rework(self):
        """Review must result in approve or request rework."""
        self.assertIn('**approve**', self.content)
        self.assertIn('**request rework**', self.content)

    def test_review_checks_pr_links(self):
        """Review must check PR points to task, issue, branch and specs."""
        self.assertIn('PR points to task, issue, branch and the specs it followed', self.content)

    def test_review_checks_scope(self):
        """Review must check nothing was built outside the task scope."""
        self.assertIn('Nothing was built outside the task scope', self.content)

    def test_review_checks_tests_with_evidence(self):
        """Review must check tests pass with evidence."""
        self.assertIn('Tests required by the task exist and pass, with evidence', self.content)

    def test_unvalidated_areas_marked_nao_validado(self):
        """Unvalidated areas must be marked NAO VALIDADO."""
        self.assertIn('marked `NAO VALIDADO`', self.content)


class TestDevWorkflowSkillFileIntegrity(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_skill_file_exists(self):
        """SKILL.md must exist at the expected path."""
        self.assertTrue(os.path.isfile(SKILL_PATH))

    def test_skill_file_not_empty(self):
        """SKILL.md must not be empty."""
        self.assertGreater(len(self.content.strip()), 0)

    def test_frontmatter_name(self):
        """SKILL.md must have frontmatter with name: dev-workflow-standard."""
        self.assertIn('name: dev-workflow-standard', self.content)

    def test_main_heading(self):
        """SKILL.md must have the provider-neutral orchestrator heading."""
        self.assertIn('# Dev Workflow Standard (Orchestrator Agent)', self.content)

    def test_skill_roles_table(self):
        """Skill Roles table must exist."""
        self.assertIn('## Skill Roles (who does what)', self.content)
        self.assertIn('| Skill | Role | Owns |', self.content)

    def test_mandatory_flow_section(self):
        """Mandatory Flow section must exist."""
        self.assertIn('## Mandatory Flow', self.content)

    def test_delegation_rules_section(self):
        """Delegation Rules section must exist."""
        self.assertIn('## Delegation Rules', self.content)

    def test_context_budget_rules_section(self):
        """Context Budget Rules section must exist."""
        self.assertIn('## Context Budget Rules', self.content)

    def test_two_executors_not_same_files(self):
        """Must state two executors must not edit the same files simultaneously."""
        self.assertIn('Two executors must not edit the same files simultaneously', self.content)

    def test_section_order_governance_before_kanban(self):
        """Mandatory Task Governance section must appear before Official Kanban Method."""
        governance_pos = self.content.find('## Mandatory Task Governance')
        kanban_pos = self.content.find('## Official Kanban Method')
        self.assertLess(governance_pos, kanban_pos)

    def test_section_order_kanban_before_entry_exit(self):
        """Official Kanban Method must appear before Definition of Entry / Exit."""
        kanban_pos = self.content.find('## Official Kanban Method')
        entry_exit_pos = self.content.find('## Definition of Entry / Exit')
        self.assertLess(kanban_pos, entry_exit_pos)

    def test_section_order_entry_exit_before_github_ready(self):
        """Definition of Entry / Exit must appear before GitHub-Ready Task Structure."""
        entry_exit_pos = self.content.find('## Definition of Entry / Exit')
        github_pos = self.content.find('## GitHub-Ready Task Structure')
        self.assertLess(entry_exit_pos, github_pos)


class TestDevWorkflowNegativeCases(unittest.TestCase):
    """Edge cases and boundary tests."""

    def setUp(self):
        self.content = read_skill()

    def test_spec_factory_always_triggered_before_implementation(self):
        """sdd-spec-factory is always used before any implementation, no exceptions."""
        self.assertIn('always, before any implementation. No exceptions', self.content)

    def test_ui_ux_mandatory_when_ui_present(self):
        """ui-ux-standard is mandatory whenever there is UI."""
        self.assertIn('mandatory whenever there is UI', self.content)

    def test_security_standard_mandatory_when_triggered(self):
        """security-standard is mandatory when the change touches auth, authz, etc."""
        self.assertIn('mandatory whenever the change touches', self.content)

    def test_does_not_absorb_specialist_responsibilities(self):
        """Orchestrator does not absorb specialist skill responsibilities."""
        self.assertIn('It does not absorb their responsibilities', self.content)

    def test_final_acceptance_belongs_to_user(self):
        """Final acceptance belongs to the user."""
        self.assertIn('Final acceptance belongs to the user', self.content)


if __name__ == '__main__':
    unittest.main()
