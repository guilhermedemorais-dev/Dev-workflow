"""
Tests for README.md changes introduced in this PR.

Validates the new and updated content in README.md related to:
- Orchestrator role clarification (never writes code, delegates to dev-implementation-standard)
- Lean delegation model (task, specs, module, constraints, acceptance criteria)
- Claude Code transport checks (CLAUDE_STATUS, VISIBLE_TERMINAL, SANDBOX_NETWORK_BLOCKED)
- Updated Agents & CLIs model (three-role model)
- Constraint that orchestrator and executor don't edit same files simultaneously
"""

import re
import os
import unittest

README_PATH = os.path.join(os.path.dirname(__file__), '..', 'README.md')


def read_readme():
    with open(README_PATH, 'r', encoding='utf-8') as f:
        return f.read()


class TestReadmeOrchestratorRole(unittest.TestCase):

    def setUp(self):
        self.content = read_readme()

    def test_orchestrator_never_writes_product_code(self):
        """Orchestrator must explicitly state it never writes product code."""
        self.assertIn('orquestrador nunca escreve codigo de produto', self.content)

    def test_orchestrator_delegates_to_dev_implementation_standard(self):
        """Orchestrator delegates implementation to dev-implementation-standard after specs and task approved."""
        # The diff added explicit statement about delegating to dev-implementation-standard
        self.assertIn('dev-implementation-standard', self.content)
        # Check delegation relationship
        self.assertIn('delega a implementacao para `dev-implementation-standard`', self.content)

    def test_dev_implementation_standard_can_run_via_claude_code(self):
        """dev-implementation-standard can be executed via Claude Code as execution medium."""
        self.assertIn('via Claude Code como meio de execucao', self.content)

    def test_lean_delegation_fields(self):
        """Each delegation receives only lean context: task, mandatory specs, module, constraints, acceptance criteria."""
        # New text explicitly describes what each delegation receives
        self.assertIn('cada delegacao recebe a task', self.content)
        self.assertIn('as specs obrigatorias', self.content)
        self.assertIn('o modulo\npermitido', self.content)
        self.assertIn('restricoes', self.content)
        self.assertIn('os criterios de aceite', self.content)

    def test_orchestrator_does_not_send_full_project(self):
        """Orchestrator does not send the whole project or full conversation to delegations."""
        self.assertIn('nao envia o projeto inteiro nem a conversa\ncompleta', self.content)

    def test_layer_separation_in_delegations(self):
        """Banco, API/Backend, Frontend/UI are separated when independently reviewable."""
        self.assertIn('Banco, API/Backend, Frontend/UI', self.content)
        self.assertIn('separados quando puderem ser revisados de forma\nindependente', self.content)


class TestReadmeClaudeCodeTransport(unittest.TestCase):

    def setUp(self):
        self.content = read_readme()

    def test_claude_version_check_before_first_delegation(self):
        """Codex checks claude --version before first delegation when running via Claude Code."""
        self.assertIn('claude --version', self.content)

    def test_claude_auth_status_check(self):
        """Codex checks claude auth status before first delegation."""
        self.assertIn('claude auth status', self.content)

    def test_claude_status_registration(self):
        """CLAUDE_STATUS is registered after the health check."""
        self.assertIn('CLAUDE_STATUS', self.content)

    def test_visible_terminal_mode(self):
        """VISIBLE_TERMINAL mode is referenced as the transport mechanism."""
        self.assertIn('VISIBLE_TERMINAL', self.content)

    def test_sandbox_network_blocked_status(self):
        """SANDBOX_NETWORK_BLOCKED is referenced for restricted network environments."""
        self.assertIn('SANDBOX_NETWORK_BLOCKED', self.content)

    def test_claude_p_as_fallback(self):
        """claude -p is referenced as a fallback transport."""
        self.assertIn('claude -p', self.content)

    def test_orchestrator_stops_if_claude_code_unavailable(self):
        """Orchestrator stops instead of implementing alone if Claude Code is unavailable."""
        self.assertIn('o orquestrador para em vez de implementar\nsozinho', self.content)

    def test_claude_delegation_md_reference(self):
        """README references claude-delegation.md for the transport protocol."""
        self.assertIn('claude-delegation.md', self.content)


class TestReadmeAgentsCLIsSection(unittest.TestCase):

    def setUp(self):
        self.content = read_readme()

    def test_dev_workflow_standard_role_defined(self):
        """`dev-workflow-standard` is described as CTO/orchestrator with specific responsibilities."""
        self.assertIn('`dev-workflow-standard` (CTO/orquestrador)', self.content)
        # Must include specific responsibilities
        self.assertIn('diagnostico, escopo, delegacao', self.content)
        self.assertIn('gates e revisao', self.content)

    def test_sdd_spec_factory_role_defined(self):
        """`sdd-spec-factory` generates specs and executable task."""
        self.assertIn('`sdd-spec-factory`', self.content)
        self.assertIn('gera as specs e a task executavel', self.content)

    def test_dev_implementation_standard_role_defined(self):
        """`dev-implementation-standard` is described as executor."""
        self.assertIn('`dev-implementation-standard` (executor)', self.content)
        self.assertIn('implementa a task aprovada', self.content)

    def test_auxiliary_tools_do_not_replace_specs(self):
        """Auxiliary tools do not replace PRD, specs, docs, tests, or review."""
        self.assertIn('nao substituem PRD, specs, documentacao, testes nem\nrevisao', self.content)

    def test_orchestrator_and_executor_not_simultaneously_editing(self):
        """Orchestrator and executor must not edit the same files simultaneously."""
        self.assertIn('O orquestrador e o executor nao devem editar os mesmos arquivos\nsimultaneamente', self.content)

    def test_transport_is_execution_medium_not_division_of_labor(self):
        """Transport (Claude Code) is only the execution medium; division of labor stays with orchestrator."""
        self.assertIn(
            'Esse transporte e apenas o meio de execucao do `dev-implementation-standard`',
            self.content
        )
        self.assertIn('a\ndivisao do trabalho', self.content)
        self.assertIn('o controle de escopo', self.content)
        self.assertIn('a revisao de cada diff/PR continuam\ncom o orquestrador', self.content)


class TestReadmeRemovedContent(unittest.TestCase):
    """Tests that verify old content was replaced and does not appear in changed sections."""

    def setUp(self):
        self.content = read_readme()

    def test_old_visible_terminal_paragraph_replaced(self):
        """The old paragraph describing VISIBLE_TERMINAL default mode in detail was replaced."""
        # The old paragraph explicitly said gnome-terminal and described the interactive session
        self.assertNotIn('gnome-terminal', self.content)
        self.assertNotIn('interface interativa do Claude Code com o\ncheckpoint ja enviado', self.content)

    def test_old_single_cli_model_replaced(self):
        """Old 'Codex: planejamento / Claude Code: implementacao' model was replaced by three-role model."""
        self.assertNotIn('Codex: planejamento tecnico, arquitetura, coordenacao, revisao e validacao.', self.content)
        self.assertNotIn('Claude Code: implementacao pesada ou repetitiva, quando disponivel.', self.content)

    def test_old_scope_reference_updated(self):
        """The old phrasing about coordinating tasks updated from 'executar' to 'coordenar'."""
        # The final paragraph changed from "executar" to "coordenar"
        self.assertIn('tarefas que ja consegue coordenar com', self.content)
        self.assertNotIn('tarefas que ja consegue executar com', self.content)


class TestReadmeNegativeAndBoundary(unittest.TestCase):

    def setUp(self):
        self.content = read_readme()

    def test_readme_file_exists(self):
        """README.md file must exist."""
        self.assertTrue(os.path.isfile(README_PATH))

    def test_readme_is_not_empty(self):
        """README.md must not be empty."""
        self.assertGreater(len(self.content.strip()), 0)

    def test_readme_has_plugins_section(self):
        """README.md must retain the Plugins section."""
        self.assertIn('## Plugins', self.content)

    def test_readme_has_dev_workflow_standard_section(self):
        """README.md must retain the Dev Workflow Standard section."""
        self.assertIn('## Dev Workflow Standard', self.content)

    def test_readme_has_agentes_e_clis_section(self):
        """README.md must contain the Agentes e CLIs section."""
        self.assertIn('### Agentes e CLIs', self.content)

    def test_readme_has_skill_table(self):
        """README.md must retain the skill roles table."""
        self.assertIn('| Skill | Papel |', self.content)
        self.assertIn('dev-workflow-standard', self.content)
        self.assertIn('CTO / orquestrador / revisor final', self.content)

    def test_readme_has_invariant_rules(self):
        """README.md must retain the invariant rules section."""
        self.assertIn('Regras invariantes:', self.content)

    def test_dev_workflow_standard_codex_runtime(self):
        """`dev-workflow-standard` typically runs in Codex per the updated model."""
        self.assertIn('Roda tipicamente no Codex', self.content)


if __name__ == '__main__':
    unittest.main()