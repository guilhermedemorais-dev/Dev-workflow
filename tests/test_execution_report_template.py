"""
Tests for plugins/dev-implementation-standard/templates/execution-report-template.md
changes introduced in this PR.

Validates new and updated content:
- New "Status e rastreabilidade" section with 9 traceability fields
- Referências expanded: Docs obrigatórios seguidos, Arquivos/módulos permitidos
- New "Prompt utilizado" section
- New "Checklist executado" section with 6 items
- "Escopo respeitado": removed "sem justificativa" phrasing
- New "Evidências" section
- "Resultado detalhado por camada" (replacing "Mudanças por camada") with subsections
- "Alterações fora do escopo" must be N/A
- "Bloqueios" includes status visual applied and escalation info
- "PR" renamed to "PR / Review"
"""

import os
import re
import unittest

TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'plugins', 'dev-implementation-standard',
    'templates', 'execution-report-template.md'
)


def read_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()


class TestExecutionReportStatusSection(unittest.TestCase):
    """Tests for the NEW 'Status e rastreabilidade' section."""

    def setUp(self):
        self.content = read_template()

    def test_status_e_rastreabilidade_section_exists(self):
        """NEW section: Status e rastreabilidade must exist."""
        self.assertIn('## Status e rastreabilidade', self.content)

    def test_status_visual_atual_field(self):
        """Status visual atual field must be present with valid options."""
        self.assertIn('Status visual atual:', self.content)
        self.assertIn('🟡 Em andamento', self.content)
        self.assertIn('🔴 Bloqueada', self.content)
        self.assertIn('🟢 Concluída', self.content)

    def test_status_kanban_atual_field(self):
        """Status Kanban atual field must include all 6 columns."""
        self.assertIn('Status Kanban atual:', self.content)
        kanban_columns = ['Backlog', 'Discovery / SDD', 'Ready for Dev', 'In Progress', 'In Review', 'Done']
        for column in kanban_columns:
            with self.subTest(column=column):
                self.assertIn(column, self.content)

    def test_data_hora_inicio_field(self):
        """Data/hora de início field must be present."""
        self.assertIn('Data/hora de início:', self.content)

    def test_data_hora_conclusao_field(self):
        """Data/hora de conclusão field must be present."""
        self.assertIn('Data/hora de conclusão:', self.content)

    def test_executor_field(self):
        """Executor field must be present."""
        self.assertIn('Executor:', self.content)

    def test_task_field(self):
        """Task field must be present."""
        self.assertIn('- Task:', self.content)

    def test_issue_criada_vinculada_field(self):
        """Issue criada / vinculada field must be present."""
        self.assertIn('Issue criada / vinculada:', self.content)

    def test_branch_field(self):
        """Branch field must be present."""
        self.assertIn('- Branch:', self.content)

    def test_responsavel_field(self):
        """Responsável field must be present."""
        self.assertIn('Responsável:', self.content)

    def test_pronto_para_github_projects_field(self):
        """Pronto para GitHub Projects: sim/não field must be present."""
        self.assertIn('Pronto para GitHub Projects: sim/não', self.content)


class TestExecutionReportReferenciasSection(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_referencias_section_exists(self):
        """Referências section must exist."""
        self.assertIn('## Referências', self.content)

    def test_specs_obrigatorias_seguidas(self):
        """Specs obrigatórias seguidas field must be present."""
        self.assertIn('Specs obrigatórias seguidas:', self.content)

    def test_docs_obrigatorios_seguidos_new(self):
        """NEW field: Docs obrigatórios seguidos must be present."""
        self.assertIn('Docs obrigatórios seguidos:', self.content)

    def test_arquivos_modulos_permitidos_new(self):
        """NEW field: Arquivos/módulos permitidos must be present."""
        self.assertIn('Arquivos/módulos permitidos:', self.content)


class TestExecutionReportPromptUtilizadoSection(unittest.TestCase):
    """Tests for the NEW 'Prompt utilizado' section."""

    def setUp(self):
        self.content = read_template()

    def test_prompt_utilizado_section_exists(self):
        """NEW section: Prompt utilizado must exist."""
        self.assertIn('## Prompt utilizado', self.content)

    def test_prompt_utilizado_instructions(self):
        """Prompt utilizado must reference the executor prompt in the task."""
        self.assertIn('Prompt para o executor', self.content)
        self.assertIn('Cole o prompt-base executado ou referencie o trecho', self.content)


class TestExecutionReportChecklistExecutado(unittest.TestCase):
    """Tests for the NEW 'Checklist executado' section."""

    def setUp(self):
        self.content = read_template()

    def test_checklist_executado_section_exists(self):
        """NEW section: Checklist executado must exist."""
        self.assertIn('## Checklist executado', self.content)

    def test_checklist_has_six_items(self):
        """Checklist must have exactly 6 checkboxes."""
        # Count checkboxes within the Checklist executado section
        checklist_section_match = re.search(
            r'## Checklist executado\n(.*?)(?=\n##|\Z)',
            self.content, re.DOTALL
        )
        self.assertIsNotNone(checklist_section_match)
        checklist_text = checklist_section_match.group(1)
        checkboxes = re.findall(r'- \[ \]', checklist_text)
        self.assertEqual(len(checkboxes), 6, f"Expected 6 checkboxes, found {len(checkboxes)}")

    def test_checklist_item_leitura(self):
        """Checklist must include Leitura da task e specs."""
        self.assertIn('- [ ] Leitura da task e specs', self.content)

    def test_checklist_item_implementacao(self):
        """Checklist must include Implementação."""
        self.assertIn('- [ ] Implementação', self.content)

    def test_checklist_item_testes(self):
        """Checklist must include Testes."""
        self.assertIn('- [ ] Testes', self.content)

    def test_checklist_item_validacao(self):
        """Checklist must include Validação."""
        self.assertIn('- [ ] Validação', self.content)

    def test_checklist_item_atualizacao_relatorio(self):
        """Checklist must include Atualização do relatório."""
        self.assertIn('- [ ] Atualização do relatório', self.content)

    def test_checklist_item_handoff(self):
        """Checklist must include Handoff para review."""
        self.assertIn('- [ ] Handoff para review', self.content)


class TestExecutionReportEscopoRespeitado(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_escopo_respeitado_section_exists(self):
        """Escopo respeitado section must exist."""
        self.assertIn('## Escopo respeitado', self.content)

    def test_apenas_escopo_task_implementado(self):
        """Must state only task scope was implemented."""
        self.assertIn('- [ ] Apenas o escopo da task foi implementado.', self.content)

    def test_nada_fora_do_escopo_sem_justificativa_removed(self):
        """OLD: 'sem justificativa' was removed from out-of-scope statement."""
        self.assertNotIn('sem justificativa', self.content)

    def test_nada_fora_do_escopo_updated(self):
        """Updated statement: nothing out of scope was changed (no justification escape)."""
        self.assertIn('- [ ] Nada fora do escopo foi alterado.', self.content)

    def test_nenhuma_mudanca_arquitetura(self):
        """Must state no architecture change without approval."""
        self.assertIn('- [ ] Nenhuma mudança de arquitetura sem aprovação.', self.content)


class TestExecutionReportEvidenciasSection(unittest.TestCase):
    """Tests for the NEW 'Evidências' section."""

    def setUp(self):
        self.content = read_template()

    def test_evidencias_section_exists(self):
        """NEW section: Evidências must exist."""
        self.assertIn('## Evidências', self.content)

    def test_evidencias_content_description(self):
        """Evidências section must describe what to include."""
        self.assertIn('Comandos, prints, logs, links de CI, screenshots ou saídas relevantes', self.content)


class TestExecutionReportResultadoDetalhadoPorCamada(unittest.TestCase):
    """Tests for the NEW 'Resultado detalhado por camada' section replacing 'Mudanças por camada'."""

    def setUp(self):
        self.content = read_template()

    def test_resultado_detalhado_por_camada_section_exists(self):
        """NEW section: Resultado detalhado por camada must exist."""
        self.assertIn('## Resultado detalhado por camada', self.content)

    def test_old_mudancas_por_camada_removed(self):
        """OLD section name 'Mudanças por camada' must not exist."""
        self.assertNotIn('## Mudanças por camada', self.content)

    def test_banco_subsection(self):
        """Banco subsection must exist with expanded description."""
        self.assertIn('### Banco', self.content)
        self.assertIn('Migrações, schema, seeds, queries, dados afetados ou `N/A`', self.content)

    def test_api_backend_subsection(self):
        """API/Backend subsection must exist with expanded description."""
        self.assertIn('### API/Backend', self.content)
        self.assertIn('Endpoints, serviços, validações, contratos, jobs, integrações ou `N/A`', self.content)

    def test_frontend_ui_subsection(self):
        """Frontend/UI subsection must exist with expanded description."""
        self.assertIn('### Frontend/UI', self.content)
        self.assertIn('Telas, componentes, estados visuais, responsividade, acessibilidade ou `N/A`', self.content)

    def test_validacao_subsection(self):
        """NEW subsection: Validação must exist with TDD and manual validation language."""
        self.assertIn('### Validação', self.content)
        self.assertIn('TDD quando aplicável', self.content)
        self.assertIn('validação manual com evidência quando TDD completo não for viável', self.content)

    def test_riscos_lacunas_subsection(self):
        """NEW subsection: Riscos/Lacunas must exist."""
        self.assertIn('### Riscos/Lacunas', self.content)
        self.assertIn('Riscos restantes, lacunas não resolvidas, limitações e follow-ups', self.content)


class TestExecutionReportComandosResultadoTestes(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_comandos_executados_section_exists(self):
        """Comandos executados section must exist."""
        self.assertIn('## Comandos executados', self.content)

    def test_comandos_executados_updated_description(self):
        """Updated: includes 'validações executadas'."""
        self.assertIn('Build, lint, testes, migrações e validações executadas', self.content)

    def test_resultado_dos_testes_section_exists(self):
        """Resultado dos testes section must exist."""
        self.assertIn('## Resultado dos testes', self.content)

    def test_resultado_testes_mentions_manual_validation(self):
        """Resultado dos testes must mention manual validation when no automated tests."""
        self.assertIn(
            'Se não houve teste automatizado, registrar validação manual e justificativa',
            self.content
        )


class TestExecutionReportAlteracoesForaDoEscopo(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_alteracoes_fora_do_escopo_section_exists(self):
        """Alterações fora do escopo section must exist."""
        self.assertIn('## Alterações fora do escopo', self.content)

    def test_must_be_na(self):
        """Alterações fora do escopo must state it should be N/A."""
        self.assertIn('Deve ser `N/A`', self.content)

    def test_not_na_means_execution_should_have_stopped(self):
        """If not N/A, execution should have stopped and recorded a blocker."""
        self.assertIn('a execução deveria ter parado e registrado bloqueio', self.content)


class TestExecutionReportBloqueios(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_bloqueios_section_exists(self):
        """Bloqueios section must exist."""
        self.assertIn('## Bloqueios', self.content)

    def test_bloqueios_mentions_status_visual(self):
        """NEW: Bloqueios must mention status visual applied."""
        self.assertIn('status visual aplicado', self.content)

    def test_bloqueios_mentions_escalation(self):
        """Bloqueios must mention to whom it was escalated."""
        self.assertIn('a quem foi escalado', self.content)


class TestExecutionReportPRSection(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_pr_review_section_exists(self):
        """NEW section name: PR / Review must exist."""
        self.assertIn('## PR / Review', self.content)

    def test_old_pr_section_renamed(self):
        """OLD section name '## PR' (standalone) must not appear as a heading."""
        # The old heading was '## PR' - it should now be '## PR / Review'
        lines = self.content.split('\n')
        for line in lines:
            if line.strip() == '## PR':
                self.fail("Old '## PR' section heading still present; should be '## PR / Review'")

    def test_pr_review_includes_link_description(self):
        """PR / Review section must mention task, issue, branch and specs linked."""
        self.assertIn('task, issue, branch e specs vinculados', self.content)

    def test_pr_review_includes_pacote_de_review(self):
        """PR / Review must mention 'pacote de review'."""
        self.assertIn('pacote de review', self.content)


class TestExecutionReportTemplateIntegrity(unittest.TestCase):

    def setUp(self):
        self.content = read_template()

    def test_template_file_exists(self):
        """execution-report-template.md must exist at the expected path."""
        self.assertTrue(os.path.isfile(TEMPLATE_PATH))

    def test_template_not_empty(self):
        """Template must not be empty."""
        self.assertGreater(len(self.content.strip()), 0)

    def test_template_main_heading(self):
        """Template must have the main heading."""
        self.assertIn('# Execution Report:', self.content)

    def test_template_mandatory_note(self):
        """Template must include the mandatory note about evidence."""
        self.assertIn('Evidência é obrigatória para concluir', self.content)

    def test_template_executor_note(self):
        """Template must note it's filled by dev-implementation-standard."""
        self.assertIn('dev-implementation-standard', self.content)

    def test_template_criterios_de_aceite_section(self):
        """Template must include Critérios de aceite section."""
        self.assertIn('## Critérios de aceite', self.content)

    def test_template_observacoes_section(self):
        """Template must include Observações section."""
        self.assertIn('## Observações', self.content)

    def test_template_resumo_section(self):
        """Template must include Resumo section."""
        self.assertIn('## Resumo', self.content)

    def test_template_arquivos_alterados_section(self):
        """Template must include Arquivos alterados section."""
        self.assertIn('## Arquivos alterados', self.content)

    def test_section_order_status_before_referencias(self):
        """Status e rastreabilidade must appear before Referências."""
        status_pos = self.content.find('## Status e rastreabilidade')
        referencias_pos = self.content.find('## Referências')
        self.assertLess(status_pos, referencias_pos)

    def test_section_order_prompt_before_checklist(self):
        """Prompt utilizado must appear before Checklist executado."""
        prompt_pos = self.content.find('## Prompt utilizado')
        checklist_pos = self.content.find('## Checklist executado')
        self.assertLess(prompt_pos, checklist_pos)


if __name__ == '__main__':
    unittest.main()