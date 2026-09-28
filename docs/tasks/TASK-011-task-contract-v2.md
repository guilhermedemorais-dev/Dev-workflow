# TASK-011: Adotar card humano completo e JSON equivalente para LLM

> **Resumo:** Adotar card humano completo e JSON equivalente para LLM.

## Identidade

- contract_revision: 1
- Issue GitHub: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/34
- Execution Contract: `docs/execution/TASK-011.json`
- Branch: `feat/task-contract-v2`
- Status: Implementação validada, aguardando revisão da entrega.
- PR: ainda não publicado.

<!-- contract-field: summary -->
## Resumo

Adotar card humano completo e JSON equivalente para LLM.

<!-- /contract-field: summary -->

<!-- contract-field: goal -->
## Objetivo

Aplicar Task Contract v2 aos templates, documentação e skills consumidoras sem quebrar v1.

<!-- /contract-field: goal -->

<!-- contract-field: current_state -->
## Estado atual encontrado

JSON v1 é índice reduzido e o card não explicita todo o pipeline aprovado.

<!-- /contract-field: current_state -->

<!-- contract-field: expected_result -->
## Resultado esperado

Issue completa e JSON v2 equivalente roteiam microtarefas, referências e gates.

<!-- /contract-field: expected_result -->

<!-- contract-field: scope -->
## Escopo

- templates
- sete skills consumidoras
- README
- pipeline
- referências
- testes

<!-- /contract-field: scope -->

<!-- contract-field: out_of_scope -->
## Fora do escopo

- produto externo
- deploy
- migração em massa de tasks v1

<!-- /contract-field: out_of_scope -->

<!-- contract-field: allowed_paths -->
## Paths permitidos

- README.md
- docs/**
- plugins/**
- tests/**

<!-- /contract-field: allowed_paths -->

<!-- contract-field: protected_paths -->
## Paths protegidos

- runtime-state/**
- credenciais
- contratos v1 históricos não retomados

<!-- /contract-field: protected_paths -->

<!-- contract-field: requirements -->
## Requisitos

-
  - ID: REQ-01
  - Descrição: Issue e JSON v2 têm equivalência normativa
  - Fonte: docs/specs/task-contract-v2/module-spec.md#regras-de-equivalência
  - Prioridade: MUST
-
  - ID: REQ-02
  - Descrição: Pipeline completo e validações independentes
  - Fonte: docs/specs/task-contract-v2/module-spec.md#pipeline-obrigatório
  - Prioridade: MUST

<!-- /contract-field: requirements -->

<!-- contract-field: business_rules -->
## Regras de negócio

-
  - ID: RN-01
  - Descrição: Divergência card/JSON bloqueia execução
  - Fonte: docs/specs/task-contract-v2/validation-rules.md#tc2-02-equivalência-normativa
-
  - ID: RN-02
  - Descrição: Tokens sem fonte usam NOT_AVAILABLE
  - Fonte: docs/specs/task-contract-v2/validation-rules.md#tc2-06-tokens

<!-- /contract-field: business_rules -->

<!-- contract-field: specs -->
## Specs obrigatórias

- docs/specs/task-contract-v2/module-spec.md
- docs/specs/task-contract-v2/validation-rules.md

<!-- /contract-field: specs -->

<!-- contract-field: docs -->
## Docs obrigatórios

- README.md
- docs/workflow-pipeline.md

<!-- /contract-field: docs -->

<!-- contract-field: references -->
## Referências

-
  - ID: REF-01
  - Título: Context Routing
  - Origem: repository
  - Arquivo: plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md
  - Seção: #v2-task-contract-and-v1-compatibility
  - Propósito: Equivalência e roteamento
  - Microtarefas:
    - MT-01
    - MT-02
-
  - ID: REF-02
  - Título: Execution Report Comments
  - Origem: repository
  - Arquivo: plugins/dev-workflow-standard/skills/dev-workflow-standard/references/execution-report-comments.md
  - Seção: #publication-protocol
  - Propósito: Publicação e evidência
  - Microtarefas:
    - MT-01
    - MT-02

<!-- /contract-field: references -->

<!-- contract-field: design -->
## Biblioteca de design e Design Guide

- Aplicabilidade: N/A
- Design Guide: N/A
- Design tokens: N/A
- Referências visuais:
  - Nenhum.
- Biblioteca de componentes: N/A
- Mockup: N/A
- Motivo N/A: Mudança documental sem interface de produto

<!-- /contract-field: design -->

<!-- contract-field: microtasks -->
## Microtarefas

-
  - ID: MT-01
  - Título: Criar teste do contrato
  - Resumo: Fixar comportamento v2 antes da implementação
  - Skill executora: dev-implementation-standard
  - Plugin: dev-implementation-standard
  - Capability: contract-testing
  - Tool preferencial: python-unittest
  - Depende de:
    - Nenhum.
  - Referências:
    - REF-01
    - REF-02
  - Paths permitidos:
    - tests/**
  - Checklist:
    - escrever teste
    - observar falha
    - preservar v1
  - Entregáveis:
    - tests/test_task_contract_v2.py
  - Condição para concluir: Teste passa após mudança e v1 continua compatível
  - Validador: qa-testing-standard
-
  - ID: MT-02
  - Título: Aplicar Task Contract v2
  - Resumo: Atualizar templates, docs e skills
  - Skill executora: dev-implementation-standard
  - Plugin: dev-implementation-standard
  - Capability: documentation-implementation
  - Tool preferencial: repository-native-tooling
  - Depende de:
    - MT-01
  - Referências:
    - REF-01
    - REF-02
  - Paths permitidos:
    - README.md
    - docs/**
    - plugins/**
  - Checklist:
    - templates
    - referências
    - pipeline
    - skills
    - README
    - testes
  - Entregáveis:
    - Task Contract v2
  - Condição para concluir: Suíte e validação das skills passam
  - Validador: qa-testing-standard

<!-- /contract-field: microtasks -->

<!-- contract-field: sectors -->
## Matriz e contratos dos setores

- database:
  - Owner: dev-implementation-standard
  - Aplicabilidade: N/A
  - Motivo: Sem banco
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- backend:
  - Owner: dev-implementation-standard
  - Aplicabilidade: N/A
  - Motivo: Sem backend
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- frontend:
  - Owner: dev-implementation-standard
  - Aplicabilidade: N/A
  - Motivo: Sem frontend
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- ui_ux:
  - Owner: ui-ux-standard
  - Aplicabilidade: N/A
  - Motivo: Sem UI
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- qa:
  - Owner: qa-testing-standard
  - Aplicabilidade: REQUIRED
  - Motivo: Regressão estrutural
  - Depende de:
    - documentation
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - REF-01
    - REF-02
  - Validações obrigatórias:
    - full-test-suite
- security:
  - Owner: security-standard
  - Aplicabilidade: N/A
  - Motivo: Sem superfície de segurança
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- devops:
  - Owner: devops-standard
  - Aplicabilidade: N/A
  - Motivo: Sem infraestrutura
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- observability:
  - Owner: devops-standard
  - Aplicabilidade: N/A
  - Motivo: Sem instrumentação
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - Nenhum.
- documentation:
  - Owner: dev-implementation-standard
  - Aplicabilidade: REQUIRED
  - Motivo: Artefato principal
  - Depende de:
    - Nenhum.
  - Microtarefas:
    - MT-01
    - MT-02
  - Fontes obrigatórias:
    - REF-01
    - REF-02
  - Validações obrigatórias:
    - documentation-review
- harness:
  - Owner: dev-workflow-standard
  - Aplicabilidade: REQUIRED
  - Motivo: Reconciliação final
  - Depende de:
    - qa
    - documentation
  - Microtarefas:
    - Nenhum.
  - Fontes obrigatórias:
    - Nenhum.
  - Validações obrigatórias:
    - sector-reconciliation

<!-- /contract-field: sectors -->

<!-- contract-field: pipeline -->
## Ordem de execução

- collaborative_discovery_sdd
- publish_discovery_sdd_completed
- human_approval
- environment_capability_readiness
- implementation
- executor_tests
- independent_functional_qa
- independent_security_qa
- independent_ui_ux_qa
- devops_observability_validation
- rework_retest
- pull_request_gate
- harness_final_gate
- human_acceptance_merge
- separately_authorized_deploy

<!-- /contract-field: pipeline -->

<!-- contract-field: gates -->
## Gates

- Discovery / SDD colaborativo: Published DISCOVERY_SDD_COMPLETED comment and human approval
- implementation: Approved microtasks, executor tests and current receipts
- independent_validation: Every REQUIRED sector validated by its owner
- pull_request: Issue, JSON, specs, revision and evidence reconciled
- harness_final: All REQUIRED sectors current and no unresolved blocker
- merge: Explicit human acceptance
- deploy: Fora do escopo desta task. Eventual deploy exige autorização humana separada.

<!-- /contract-field: gates -->

<!-- contract-field: required_tests -->
## Testes obrigatórios

-
  - ID: TEST-01
  - Tipo: unit
  - Comando: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
  - Resultado esperado: exit 0
-
  - ID: TEST-02
  - Tipo: skill-validation
  - Comando: quick_validate.py <skill-folder>
  - Resultado esperado: Sete skills válidas. Resolver o validador equivalente no host.
-
  - ID: TEST-03
  - Tipo: diff-validation
  - Comando: git diff --check
  - Resultado esperado: exit 0

<!-- /contract-field: required_tests -->

<!-- contract-field: acceptance_criteria -->
## Critérios de aceite

-
  - ID: AC-01
  - Descrição: Card e JSON v2 têm equivalência normativa e revisão compartilhada.
  - Validação: TEST-01
-
  - ID: AC-02
  - Descrição: Referências, design e microtarefas são campos de primeira classe.
  - Validação: TEST-01
-
  - ID: AC-03
  - Descrição: Pipeline inclui implementação e todas as validações independentes.
  - Validação: TEST-01
-
  - ID: AC-04
  - Descrição: Comentários materiais registram publicação, superfície alterada e tokens.
  - Validação: TEST-01
-
  - ID: AC-05
  - Descrição: Sete skills consumidoras aplicam o mesmo modelo.
  - Validação: TEST-01
-
  - ID: AC-06
  - Descrição: Contratos v1 existentes continuam legíveis e testes passam.
  - Validação: TEST-01

<!-- /contract-field: acceptance_criteria -->

<!-- contract-field: stop_conditions -->
## Condições de parada

- architecture_change_required
- scope_expansion_required
- mandatory_reference_missing
- source_of_truth_conflict
- human_task_json_divergence
- authorization_required

<!-- /contract-field: stop_conditions -->

<!-- contract-field: execution_prompt -->
## Prompt de ignição para o executor

- Instrução: Read this JSON, verify TASK-011 revision 1 and normative equivalence with its linked Issue, load routed skills and REF-01/REF-02, execute only allowed paths, collect receipts, publish material comments, and do not merge or deploy without explicit authorization.
- Checkpoints materiais:
  - DISCOVERY_SDD_COMPLETED
  - RUNNING
  - VALIDATING
  - REWORK
  - BLOCKED
  - COMPLETED

<!-- /contract-field: execution_prompt -->

<!-- contract-field: reporting -->
## Regras dos comentários

- Comentário na Issue obrigatório: true
- Evidência de publicação exigida: returned comment URL or identifier
- Campos de tokens:
  - input_tokens
  - output_tokens
  - total_tokens
  - measurement_source
- Campos da superfície alterada:
  - changed_files
  - issue_changes
  - json_spec_reference_changes
  - remote_mutations
  - code_changed
  - branch
  - commit
  - pull_request
- Valor quando indisponível: NOT_AVAILABLE
- Regra de armazenamento: Actual token counts, changed surface and publication evidence live in Issue comments and receipts, not in this normative contract.

<!-- /contract-field: reporting -->

<!-- contract-field: discovery -->
## Discovery / SDD colaborativo

- Perguntas e respostas:
  - O card é completo para humanos e o JSON contém as mesmas especificações para a LLM: confirmado pelo usuário.
  - Referências exatas, Design Guide e skills/plugins por microtarefa: confirmados pelo usuário.
- Pesquisa realizada:
  - Inspeção dos templates, skills, README, pipeline e testes do repositório.
- Decisões consolidadas:
  - Novas tasks usam v2; contratos v1 inativos não são migrados em massa.
  - Issue é o card humano; JSON é sua representação normativa estruturada.
  - Resultados e evidência mutável ficam nos comentários e receipts.
- Hipóteses abertas:
  - Nenhum.
- Aprovação: Aprovação do usuário registrada na conversa: aprovado, pode aplicar e alterar as skills. Para novas tasks, publicar Discovery antes de solicitar aprovação.

<!-- /contract-field: discovery -->

## Registro de execução

O usuário aprovou a implementação na conversa. A publicação do Discovery foi
registrada retrospectivamente nesta entrega; isso não comprova a ordem exigida
para novas tasks. O checkpoint inicial passou por correções na revisão.

- Relatório: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/34#issuecomment-5841283600
- Contagem de tokens: NOT_AVAILABLE, runtime sem medição exposta.
- Revisão independente: achados corrigidos; ver receipt para evidências e limites.
- Receipt: `docs/receipts/TASK-011-validation.json`.
- Merge e instalação global: não executados nesta entrega.
