# TASK-XXX: Nome da task

> Task é a interface humana para ordem de execução e acompanhamento. Aponta
> para specs, Execution Contract, issue, branch e PR. Deve ser pequena,
> revisável e executável em um único PR.
> A matriz mostra o todo; somente o Harness lê a Task completa por padrão.
> Especialistas recebem setor, fase, revisão, referências e receipts necessários.
> Substitua todos os placeholders. N/A exige motivo verificado; o exemplo JSON
> inicial é docs-only, não um default para dispensar setores de outras mudanças.

## Status
A fazer | Em andamento | Em revisão | Concluída | Bloqueada

## Status visual
- Status visual: A definir | 🟡 Em andamento | 🔴 Bloqueada | 🟢 Concluída
- Status Kanban: Backlog | Discovery / SDD | Ready for Dev | In Progress | Validation | In Review | Awaiting Final Approval | Done
- Pronto para GitHub Projects: sim/não

## Tipo
Feature | Bugfix | Refactor | Chore | Spike | DevOps | Docs

## Prioridade
Alta | Média | Baixa

## Issue GitHub
Link da issue (ou "criar issue: <título sugerido>").

## Branch sugerida
`feat/<modulo>-<resumo>` | `fix/<modulo>-<resumo>` | `chore/<resumo>`

## PR
PR esperado (ou "abrir PR após primeiro checkpoint"). Aponta para esta task e a issue.

## Responsável
Quem executa (dev/IA) e quem revisa.

## Objetivo da task
O que esta task entrega, em uma a três frases.

## Resumo do escopo
O que está incluído, em linguagem adequada para acompanhamento humano.

## Specs obrigatórias
Links das specs que são contrato desta task (product/module/page/component/validation/database/api).

## Docs obrigatórios
PRD, arquitetura, mockups aprovados e demais documentos a seguir.

## Fontes globais da verdade
Liste somente fontes globais necessárias, com path/link e propósito. Specs
detalhadas permanecem nas fontes. O Harness distribui os critérios globais
relevantes para cada setor; não manda todos os documentos a todo especialista.

## Execution Contract
`docs/execution/TASK-XXX.json`

## Escopo
O que está incluído nesta task.

## Fora do escopo

<!-- Conditional: for operational infrastructure include devops-standard and
target_environment, impact, rollback_strategy, validation plan and human gates.
Omit this DevOps addition for unrelated work; keep installation state out. -->
O que NÃO deve ser feito aqui (evita PR inchado).

## Arquivos prováveis
Caminhos prováveis a alterar (marcar `HIPÓTESE:` quando não confirmado).

## Matriz de Validação por Setor
Sector Validation Matrix: preencher todos os dez setores, inclusive em TRIVIAL.
Setores N/A ficam apenas nesta matriz, com motivo; detalhar somente REQUIRED.
Substitua owners genéricos por uma skill concreta. Extensões materiais têm ID,
owner e justificativa explícitos, sem criar especialistas por cerimônia.

| Setor / ID | Aplicável | Responsável | Status | Dependências finais | Motivo N/A |
| --- | --- | --- | --- | --- | --- |
| Banco / database | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| API / Backend / backend | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| Frontend / frontend | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| UI / UX / ui_ux | REQUIRED ou N/A | ui-ux-standard | PENDING ou N/A | definir | se N/A, justificar |
| QA / Testes / qa | REQUIRED ou N/A | qa-testing-standard | PENDING ou N/A | definir | se N/A, justificar |
| Segurança / security | REQUIRED ou N/A | security-standard | PENDING ou N/A | definir | se N/A, justificar |
| DevOps / Infraestrutura / devops | REQUIRED ou N/A | devops-standard | PENDING ou N/A | definir | se N/A, justificar |
| Observabilidade / observability | REQUIRED ou N/A | definir skill de instrumentação/operação | PENDING ou N/A | definir | se N/A, justificar |
| Documentação / documentation | REQUIRED ou N/A | dev-implementation-standard | PENDING ou N/A | definir | se N/A, justificar |
| Gate Final do Harness / harness | REQUIRED | dev-workflow-standard | PENDING | todos os demais REQUIRED | não se aplica |

Reutilizar PENDING, READY, RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
PASS exige evidência do owner; PARTIAL/NOT_VALIDATED não fecham REQUIRED.
N/A é aplicabilidade. Um owner solicita retrabalho, nunca atesta PASS de outro.

## Bloco de setor REQUIRED
Repita este bloco somente para cada setor REQUIRED, com âncora HTML única e ID
correspondente ao contrato (`database`, `backend`, `frontend`, `ui_ux`, `qa`,
`security`, `devops`, `observability`, `documentation`, `harness`).

<!-- Exemplo de bloco a preencher, não é resultado executado. -->
<a id="documentation"></a>
## Documentação
- Status: PENDING
- Responsável: dev-implementation-standard
- Depende de (validação final): definir
- Pré-requisitos de planejamento: definir separadamente, quando houver

### Objetivo do setor
O que este owner precisa garantir dentro do escopo.

### Fontes obrigatórias
- REQUIRED `path#anchor`: propósito concreto da leitura.

### Fontes condicionais
- CONDITIONAL `path#anchor`: condição observável; propósito da leitura.
- OPTIONAL `path#anchor`: propósito de consulta complementar, sem carga automática.

### O que fazer
Checklist contextual, sem copiar a spec.

### Evidência esperada
Revisão/artefato, comandos e critérios que autorizam o resultado deste setor.

### Resultado
NOT_VALIDATED até execução. Links de SKILL_RECEIPT/EXECUTION_RECEIPT, revisão,
fontes carregadas e limitações; nunca inventar execução.

## Regras de negócio
RN aplicáveis (referência ao validation-rules-spec).

<a id="criterios-de-aceite"></a>
## Critérios de aceite
Lista objetiva e testável do que define "pronto".

## TDD / Testes obrigatórios
Testes que devem existir/passar (unit, integração, e2e) e cobertura mínima.

## Validação e tools previstas
- Skill responsável:
- Capability:
- Tool preferencial (se aplicável):

O estado de instalação é local ao runtime e não pertence à task.

## Ordem de Execução
Planning pode anteceder implementação conforme pré-requisitos próprios.
Validação final aguarda `depends_on` e receipts atuais; planejamento não fecha
o gate final do setor. Paralelizar somente sem conflito de paths/dependências.

## Checklist de execução
1. Leitura da fatia e fontes obrigatórias pelo owner; Task completa pelo Harness.
2. Execução do escopo.
3. Testes e validação material.
4. Evidências e resultado do próprio setor.
5. Reconciliação dos setores.
6. Handoff para review.

## Registro de Evidências
| Setor | Fase | Owner | Revisão/artefato | Receipt/evidência | Resultado/limites |
| --- | --- | --- | --- | --- | --- |
| preencher após execução | planning ou validation | owner real | revisão testada | link | resultado observado |

## Gate do PR
Task/Issue/specs/revisão consistentes; validações e documentação requeridas
evidenciadas. Sem publicação presumida a partir de Markdown local.

<a id="harness"></a>
## Gate Final do Harness
Responsável dev-workflow-standard; status PENDING; depende de todos REQUIRED.
Fonte REQUIRED: Task completa e contrato, para reconciliar escopo e owners.
O que fazer: conferir critérios, resultados, receipts atuais e bloqueios.
Evidência esperada: reconciliação de cada setor e decisão fundamentada.
Resultado: NOT_VALIDATED até execução. CODE_COMPLETE != TASK_COMPLETE;
NO_EVIDENCE != PASS. N/A motivado não bloqueia. Nenhum REQUIRED pendente,
BLOCKED, REWORK, PARTIAL ou NOT_VALIDATED permite concluir a Task.

## Aceite Humano
Decisão, responsável e evidência quando ocorrer; PASS não autoriza merge/deploy.

## Riscos/Lacunas
Contexto insuficiente, validação não executada e decisões pendentes explícitas.

## Prompt para o executor
Execute a TASK-XXX usando o contrato:
`docs/execution/TASK-XXX.json`

Setor/fase/revisão: definidos no handoff. Siga o Harness e registre evidências.

## Continuidade entre LLMs
- LLM executor atual:
- Estado de disponibilidade:
- Execution Contract: `docs/execution/TASK-XXX.json`
- `EXECUTION_HANDOFF`: obrigatório ao trocar de LLM

## Relatórios humanos na Issue
- Checkpoints materiais: RUNNING | VALIDATING | REWORK | BLOCKED | COMPLETED
- Último status de publicação: PENDING | PUBLISHED | NOT PUBLISHED | N/A
- Evidência remota (URL/identificador):
- Motivo quando não publicado:

## Resultado da execução

### Resumo
O que foi feito.

### Arquivos alterados
Lista de arquivos criados/alterados/removidos.

### Comandos executados
Comandos de build/teste/lint executados.

### Resultado dos testes
Saída/resumo dos testes (passou/falhou, evidência).

### Bloqueios
Impedimentos encontrados.

### Observações
Notas adicionais, decisões tomadas e follow-ups.
