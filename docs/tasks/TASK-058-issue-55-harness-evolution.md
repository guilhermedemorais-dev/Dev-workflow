# TASK-058: Issue #55, evolução verificável do Engineering Harness

Status: Implementação concluída, handoff de validação atualizado para contract_revision 2. QA e Segurança estão sendo executados independentemente sobre a PR #56. Branch `codex/issue-55-harness-evolution`, base `ef0dce3a123e192cac8330161ea8c0c2e3317051` (`feat/ui-library-routing`). Issue humana: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/55.

## Objetivo e autorização

Implementar os itens obrigatórios da Issue #55 neste repositório. Autorização direta do usuário em 2026-10-15. A orientação antiga da Issue para não implementar na máquina de origem foi substituída por essa instrução explícita. A aceitação final permanece com o usuário.

## Escopo e critérios de aceite

1. Reconciliar o Harness, contratos, roteamento, receipts e validação existentes; corrigir apenas lacunas concretas dos requisitos da Issue #55, sem duplicar motores ou estado. Registrar os novos entrypoints nos catálogos autoritativos de Linux, Windows e macOS, separando validação executada de plataforma apenas declarada. Vincular mutações remotas a alvo/head/revisão; reconsultar antes de repetir escrita ambígua; nunca alegar lease ou concorrência isolada sem executá-la.
2. Entregar um piloto opt-in de contexto derivado menor que suas fontes, com seleção determinística de trechos canônicos, referências e SHA-256 das fontes/plano, casos de recuperação positivos e negativos, controle de remoção de exceção e inversão de negação, invalidação por mudança e fallback para o original. Não afirmar equivalência semântica por hash ou schema.
3. Entregar preenchimento determinístico de templates existentes, com campos explicitamente permitidos, validação de dados, escape para o destino, texto fixo e critérios aprovados preservados, falha sem saída parcial e escrita atômica.
4. Testar texto fixo byte a byte, Unicode, caracteres especiais, repetição, campos ausentes/extras/inválidos, fonte alterada, remoção de exceção e inversão de negação.
5. Documentar limites, adoção opt-in, método de medição e fallback. Não alegar economia sem medição.
6. Preservar distinção Windows nativo/WSL/Linux e não alterar configurações ativas, caches instalados, credenciais, outros repositórios ou dados externos.
7. Rodar testes estruturais do repositório e `git diff --check`; anexar resultados e pendências reais.

## Fora de escopo e gates

Não fazer merge, deploy, release, automerge, migração de configuração ativa, instalação global, publicação de edição ou gasto recorrente. Não incorporar Rig, Agentics, gh-aw, Evergreen, Goal, Autoloop, Crane, CAO ou WikiKB como dependência. Experimentos externos só ficam recomendados/NOT VALIDATED. Não alterar critérios aprovados para obter PASS.

## Superfícies e validação

- API/backend: N/A, utilitários locais sem serviço persistente.
- Banco/dados: N/A, fontes e artefatos em arquivos locais selecionados pelo usuário.
- UI: N/A.
- Segurança: validar caminhos, conteúdo, campos e escrita atômica; não imprimir segredos.
- Testes: testes unitários/estruturais focados e suíte completa do repositório.
- Observabilidade: resultados e medições explícitos, sem declarar execuções não realizadas.
- Revisão independente: obrigatória para Security/QA conforme os requisitos aplicáveis; se não houver capacidade de especialista disponível nesta sessão, registrar pendência em vez de autoatribuir aceite.

## Fontes normativas

- Issue #55, revisão remota observada em 2026-10-15.
- `AGENTS.md`, `docs/workflow-pipeline.md`.
- `plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md` e referências `harness-execution.md`, `context-routing.md`, `minimal-code-gate.md`.
- `plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md`.
- `plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md` e template de Task.

## Decisão de reuso

Estender `plugins/dev-workflow-standard/scripts/` que já contém utilitários de contexto. Manter os dois pilotos opt-in e sem serviço/daemon. O renderer deve ser usado por uma fixture/template governado do próprio Harness. Não modificar a tarefa distinta TASK-055.
