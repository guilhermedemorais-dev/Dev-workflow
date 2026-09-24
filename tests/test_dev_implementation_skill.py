"""
Tests for plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md
changes introduced in this PR.

Validates new and updated content:
- Mission section: lean Execution Contract bootstrap and TDD
- New Preconditions: SDD already complete, GitHub-ready fields required
- Hard Limits: scope exit requires stopping (not justifying)
- New Task Status Rules section: 3 statuses, filename stability
- Expanded Workflow (9 steps, including status transitions)
- New GitHub Projects Readiness section with 9 fields
- New Recommended Task Template section with 21+ mandatory sections
- Escalation: new trigger for leaving approved scope, blocked label + visual status update
- Definition of done: TDD language, fully filled report, not self-approved
"""

import os
import re
import unittest

SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'plugins', 'dev-implementation-standard',
    'skills', 'dev-implementation-standard', 'SKILL.md'
)


def read_skill():
    with open(SKILL_PATH, 'r', encoding='utf-8') as f:
        return f.read()


class TestDevImplementationMission(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_validate_contract_before_loading_references(self):
        """Mission starts from and validates the lean contract."""
        self.assertIn('Start from the task ID and Execution Contract path', self.content)
        self.assertIn('Validate the contract, then load only the mandatory referenced', self.content)

    def test_prompt_base_is_not_the_operational_contract(self):
        self.assertNotIn("Execute the task's prompt-base as the operational contract", self.content)

    def test_tdd_in_mission(self):
        """Mission must include using TDD when applicable."""
        self.assertIn('Use TDD when applicable', self.content)

    def test_update_execution_result_and_final_report(self):
        """Mission must include updating the execution result AND final report."""
        self.assertIn("Update the task's execution result and final report", self.content)

    def test_return_work_for_review_with_links(self):
        """Mission must say return work for review with task, issue, branch and specs linked."""
        self.assertIn('Return the work for review with task, issue, branch and specs linked', self.content)


class TestDevImplementationPreconditions(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_approved_task_precondition(self):
        """Preconditions must require an approved task to exist."""
        self.assertIn('An approved task exists', self.content)
        self.assertIn('Never implement without an approved task', self.content)

    def test_sdd_spec_work_already_complete(self):
        """NEW: Precondition that SDD/spec work is already complete and executor doesn't do SDD."""
        self.assertIn('SDD/spec work is already complete', self.content)
        self.assertIn('The executor does not do SDD', self.content)

    def test_github_ready_fields_precondition(self):
        """NEW: Precondition requiring GitHub-ready fields in the task."""
        self.assertIn('GitHub-ready fields', self.content)
        self.assertIn('responsável', self.content)
        self.assertIn('bloqueios', self.content)
        self.assertIn('specs\n  obrigatórias', self.content)
        self.assertIn('branch sugerida', self.content)
        self.assertIn('evidências', self.content)
        self.assertIn('issue criada/vinculada', self.content)

    def test_stop_and_return_if_precondition_missing(self):
        """Must stop and return to orchestrator if any precondition is missing."""
        self.assertIn('If any precondition is missing, stop and return to `dev-workflow-standard`', self.content)


class TestDevImplementationHardLimits(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_never_change_out_of_scope(self):
        """Hard limit: Never change anything out of scope (no 'justification' escape)."""
        self.assertIn('Never change anything out of scope', self.content)

    def test_out_of_scope_requires_stopping(self):
        """When leaving scope is required, must stop and record in Bloqueios."""
        self.assertIn('If leaving scope is required, stop and\n  record it in `Bloqueios`', self.content)

    def test_no_architecture_change_without_approval(self):
        """Must not change architecture without approval."""
        self.assertIn('Do not change architecture without approval', self.content)

    def test_no_secrets_in_repo(self):
        """Hard limit: No secrets, tokens, cookies, client data or temporary URLs in repo."""
        self.assertIn('No secrets, tokens, cookies, client data or temporary URLs in the repo', self.content)

    def test_no_merge_or_deploy(self):
        """Hard limit: Do not merge or deploy."""
        self.assertIn('Do not merge or deploy', self.content)

    def test_no_mark_complete_without_evidence(self):
        """Hard limit: Do not mark work complete without validation evidence."""
        self.assertIn('Do not mark work complete without validation evidence', self.content)

    def test_out_of_scope_no_longer_justifiable(self):
        """Old language allowing justified out-of-scope changes was removed."""
        self.assertNotIn('Never change anything out of scope without recording a justification', self.content)


class TestDevImplementationTaskStatusRules(unittest.TestCase):
    """Tests for the NEW Task Status Rules section."""

    def setUp(self):
        self.content = read_skill()

    def test_task_status_rules_section_exists(self):
        """NEW section: Task Status Rules must exist."""
        self.assertIn('## Task Status Rules', self.content)

    def test_status_in_content_not_filename(self):
        """Status is updated in task content, never in physical filename."""
        self.assertIn('Visual status is updated in the task content, never in the physical filename', self.content)

    def test_em_andamento_status(self):
        """Em andamento status defined for when starting execution."""
        self.assertIn('🟡 Em andamento', self.content)
        self.assertIn('set this when starting execution', self.content)

    def test_bloqueada_status(self):
        """Bloqueada status defined for blocked tasks."""
        self.assertIn('🔴 Bloqueada', self.content)
        self.assertIn('set this when blocked, with the reason in `Bloqueios`', self.content)

    def test_concluida_status(self):
        """Concluída status defined for completed tasks."""
        self.assertIn('🟢 Concluída', self.content)
        self.assertIn('set this only after implementation and validation evidence are\n  recorded', self.content)

    def test_filename_remains_stable(self):
        """Task filename must remain stable."""
        self.assertIn('The task filename remains stable', self.content)

    def test_no_emoji_in_filename(self):
        """No emojis or status prefixes in the filename."""
        self.assertIn('Do not use emojis or status prefixes in the\nfilename', self.content)


class TestDevImplementationWorkflow(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_workflow_section_exists(self):
        """Workflow section must exist."""
        self.assertIn('## Workflow', self.content)

    def test_workflow_starts_from_contract(self):
        self.assertIn('**Bootstrap**: receive `task_id` and `execution_contract_path`', self.content)
        self.assertIn('**Contract validation**', self.content)
        self.assertIn('**Progressive disclosure**', self.content)
        self.assertNotIn('read the whole approved task and every mandatory', self.content)

    def test_workflow_step_2_set_status_em_andamento(self):
        """Step 2: Set status to Em andamento when starting."""
        self.assertIn('**Set status** to `🟡 Em andamento` in the Human Task when starting', self.content)

    def test_workflow_does_not_reexpand_prompt_base(self):
        self.assertNotIn('**Execute the prompt-base**', self.content)

    def test_workflow_step_4_implementation_by_layer(self):
        """Step 4: Implement only approved scope, by layer."""
        self.assertIn('**Implementação**', self.content)
        self.assertIn('implement only the approved scope, by layer', self.content)
        self.assertIn('Banco, API/Backend, Frontend/UI', self.content)

    def test_workflow_step_5_tdd(self):
        """Step 5: TDD when applicable, manual validation with evidence otherwise."""
        self.assertIn('**TDD/Testes**', self.content)
        self.assertIn('use TDD when applicable', self.content)
        self.assertIn('If full TDD is not viable, record why\n   and perform manual validation with objective evidence', self.content)

    def test_workflow_step_6_validation(self):
        """Step 6: Run required commands and capture evidence."""
        self.assertIn('**Validação**', self.content)
        self.assertIn('Capture\n   evidence', self.content)

    def test_workflow_step_7_update_report(self):
        """Step 7: Fill mandatory final report."""
        self.assertIn('**Atualização do relatório**', self.content)
        self.assertIn('templates/execution-report-template.md', self.content)

    def test_workflow_step_8_set_final_status(self):
        """Step 8: Set final status (Bloqueada or Concluída)."""
        self.assertIn('**Set final status**', self.content)
        self.assertIn('`🔴 Bloqueada` if blocked', self.content)
        self.assertIn('**Set final status** for your own sector', self.content)
        self.assertIn('only with implementation/developer-test evidence', self.content)
        self.assertIn('not\n   completion of the entire Task', self.content)
        self.assertIn('Harness reconciles all REQUIRED owners', self.content)

    def test_workflow_step_9_handoff_for_review(self):
        """Step 9: Handoff for review, do not self-approve, merge, or deploy."""
        self.assertIn('**Handoff para review**', self.content)
        self.assertIn('return to `dev-workflow-standard`', self.content)
        self.assertIn('Do not\n   self-approve, merge, or deploy', self.content)


class TestDevImplementationGitHubProjectsReadiness(unittest.TestCase):
    """Tests for the NEW GitHub Projects Readiness section."""

    def setUp(self):
        self.content = read_skill()

    def test_github_projects_readiness_section_exists(self):
        """NEW section: GitHub Projects Readiness must exist."""
        self.assertIn('## GitHub Projects Readiness', self.content)

    def test_do_not_assume_github_projects_available(self):
        """Must not assume GitHub Projects is available."""
        self.assertIn('Do not assume GitHub Projects is available', self.content)

    def test_required_fields_in_task_content(self):
        """GitHub Projects readiness fields must all be present."""
        required_fields = [
            'status visual',
            'status Kanban',
            'responsável',
            'bloqueios',
            'specs obrigatórias',
            'branch sugerida',
            'issue criada / vinculada',
            'evidências',
            'Pronto para GitHub Projects: sim/não',
        ]
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, self.content)

    def test_stop_if_fields_missing(self):
        """Must stop before implementation and ask orchestrator if fields are missing."""
        self.assertIn('If the fields are missing, stop before implementation', self.content)


class TestDevImplementationRecommendedTaskTemplate(unittest.TestCase):
    """Executor routes to SDD's single maintained task template."""

    def setUp(self):
        self.skill = read_skill()
        path = os.path.join(os.path.dirname(__file__), '..', 'plugins',
                            'sdd-spec-factory', 'templates', 'task-template.md')
        with open(path, encoding='utf-8') as source:
            self.content = source.read()

    def test_recommended_task_template_section_exists(self):
        """NEW section: Recommended Task Template must exist."""
        self.assertIn('## Recommended Task Template', self.skill)
        self.assertIn('plugins/sdd-spec-factory/templates/task-template.md', self.skill)
        self.assertNotIn('```markdown', self.skill)

    def test_template_contains_titulo(self):
        """Template must include a Título field."""
        self.assertIn('# TASK-XXX:', self.content)

    def test_template_contains_status_visual(self):
        """Template must include Status visual section."""
        self.assertIn('## Status visual', self.content)
        self.assertIn('Status visual: A definir', self.content)

    def test_template_contains_tipo(self):
        """Template must include Tipo section."""
        self.assertIn('## Tipo', self.content)
        self.assertIn('Feature | Bugfix | Refactor', self.content)

    def test_template_contains_prioridade(self):
        """Template must include Prioridade with P0-P3."""
        self.assertIn('## Prioridade', self.content)
        self.assertIn('Alta | Média | Baixa', self.content)

    def test_template_contains_prompt_para_executor(self):
        """Template must include Prompt para o executor section."""
        self.assertIn('## Prompt para o executor', self.content)

    def test_template_contains_checklist_de_execucao(self):
        """Template must include Checklist de execução with correct steps."""
        self.assertIn('## Checklist de execução', self.content)
        checklist_items = [
            'Leitura da fatia e fontes obrigatórias',
            'Execução do escopo',
            'Testes',
            'validação material',
            'Evidências e resultado do próprio setor',
            'Handoff para review',
        ]
        for item in checklist_items:
            with self.subTest(item=item):
                self.assertIn(item, self.content)

    def test_template_contains_resultado_da_execucao(self):
        """Template must include Resultado da execução section."""
        self.assertIn('## Resultado da execução', self.content)

    def test_template_kanban_status_options(self):
        """Template must include all Kanban status options."""
        self.assertIn('Backlog | Discovery / SDD | Ready for Dev | In Progress | Validation | In Review | Awaiting Final Approval | Done', self.content)

    def test_template_pronto_para_github_projects(self):
        """Template must include Pronto para GitHub Projects field."""
        self.assertIn('Pronto para GitHub Projects: sim/não', self.content)


class TestDevImplementationEscalation(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_escalation_section_exists(self):
        """Escalation section must exist."""
        self.assertIn('## Escalation', self.content)

    def test_escalation_trigger_leaving_scope(self):
        """NEW escalation trigger: leaving the approved scope requires escalation."""
        self.assertIn('leaving the approved scope is required', self.content)

    def test_escalation_missing_precondition(self):
        """Existing trigger: missing precondition (no approved task / specs)."""
        self.assertIn('a precondition is missing (no approved task / specs)', self.content)

    def test_escalation_architecture_change(self):
        """Existing trigger: task cannot be completed without architecture change."""
        self.assertIn('the task cannot be completed without an architecture change', self.content)

    def test_escalation_records_blocked_label(self):
        """NEW: Escalation must mention adding blocked label when a project board exists."""
        self.assertIn('add the `blocked` label when a project board exists', self.content)

    def test_escalation_updates_visual_status_to_bloqueada(self):
        """NEW: Escalation must mention updating visual status to Bloqueada."""
        self.assertIn('update\nvisual status to `🔴 Bloqueada`', self.content)

    def test_escalation_keeps_kanban_column(self):
        """NEW: Escalation must keep the card in its current Kanban column."""
        self.assertIn('keep the card in its current\nKanban column', self.content)


class TestDevImplementationDefinitionOfDone(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_definition_of_done_section_exists(self):
        """Definition of done section must exist."""
        self.assertIn('## Definition of done', self.content)

    def test_nothing_out_of_scope(self):
        """Done: nothing out of scope (no 'unjustified' qualifier)."""
        self.assertIn('nothing out of scope', self.content)
        self.assertNotIn('nothing out of scope unjustified', self.content)

    def test_tdd_when_applicable(self):
        """Done: TDD used when applicable; otherwise manual validation is evidenced."""
        self.assertIn('TDD used when applicable; otherwise manual validation is evidenced', self.content)

    def test_tests_pass_or_blockers_recorded(self):
        """Done: tests/validation pass OR blockers are recorded."""
        self.assertIn('tests/validation pass or blockers are recorded', self.content)

    def test_fully_filled_final_report(self):
        """Done: task execution result fully filled with the mandatory final report."""
        self.assertIn('Task execution result fully filled with the mandatory final report', self.content)

    def test_pr_review_package(self):
        """Done: PR/review package prepared (not just PR)."""
        self.assertIn('PR/review package prepared', self.content)

    def test_not_self_approved(self):
        """Done: not merged, deployed, or self-approved."""
        self.assertIn('not merged, deployed, or self-approved', self.content)


class TestDevImplementationSkillFileIntegrity(unittest.TestCase):

    def setUp(self):
        self.content = read_skill()

    def test_skill_file_exists(self):
        """SKILL.md must exist at the expected path."""
        self.assertTrue(os.path.isfile(SKILL_PATH))

    def test_skill_file_not_empty(self):
        """SKILL.md must not be empty."""
        self.assertGreater(len(self.content.strip()), 0)

    def test_frontmatter_name(self):
        """SKILL.md must have frontmatter with name: dev-implementation-standard."""
        self.assertIn('name: dev-implementation-standard', self.content)

    def test_main_heading(self):
        """SKILL.md must have the main heading."""
        self.assertIn('# Dev Implementation Standard (Executor Agent)', self.content)

    def test_skill_does_not_do_sdd(self):
        """SKILL.md must state that the executor does not do SDD."""
        self.assertIn('does not do SDD', self.content)

    def test_skill_does_not_plan_product_scope(self):
        """SKILL.md must state that the executor does not plan product scope."""
        self.assertIn('does not plan product scope', self.content)

    def test_skill_does_not_write_specs(self):
        """SKILL.md must state that the executor does not write specs."""
        self.assertIn('does not\nwrite specs', self.content)

    def test_interfaces_section_exists(self):
        """Interfaces with other skills section must exist."""
        self.assertIn('## Interfaces with other skills', self.content)

    def test_interfaces_with_dev_workflow(self):
        """Must receive task and approval from dev-workflow-standard."""
        self.assertIn('Receives the task and approval from `dev-workflow-standard`', self.content)


if __name__ == '__main__':
    unittest.main()
