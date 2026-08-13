# TASK-XXX: Nome da task

> Task é ordem de execução. Aponta para specs (o contrato), issue, branch e PR.
> Deve ser pequena, revisável e executável em um único PR.

## Status
A fazer | Em andamento | Em revisão | Concluída | Bloqueada

## Tipo
Feature | Bugfix | Refactor | Chore | Spike | DevOps | Docs

## Prioridade
Alta | Média | Baixa

## Issue GitHub
Obrigatório: toda task tem issue registrada no GitHub. Cole o número/URL da issue.
Sem issue registrada a task fica `blocked`/`needs-info` e não entra em Ready for Dev.

## Branch sugerida
`feat/<modulo>-<resumo>` | `fix/<modulo>-<resumo>` | `chore/<resumo>`

## PR
PR esperado (ou "abrir PR após primeiro checkpoint"). Aponta para esta task e a issue.

## Responsável
Quem executa (dev/IA) e quem revisa.

## Atribuição de execução / Executor LLM
Obrigatório antes de Ready for Dev. A task deve dizer quem executa, quem revisa
quais arquivos ficam bloqueados para outros executores, e qual contrato o modelo
de IA deve seguir.

- Executor LLM primário: Codex | Claude Desktop | Claude Code | Humano | A definir
- Executor secundário/revisor: Codex | Claude Desktop | Claude Code | Humano | N/A
- Motivo da atribuição:
- Pode rodar AFK: sim/não. Se sim, checkpoint máximo:
- Modo de handoff: task manual | Codex local | Claude Desktop manual | Claude Code CLI | outro
- Status da claim: unclaimed | claimed | in_progress | blocked | done
- Claim por:
- Claim em:
- `locked_paths`:
  -
- Conflitos conhecidos com outras tasks:

Regras:

- `A definir`, `unclaimed` sem dono antes da execução ou `locked_paths` vazio
  bloqueiam Ready for Dev, salvo task puramente docs sem arquivo-alvo.
- Duas LLMs não podem executar a mesma task nem editar o mesmo `locked_path` ao
  mesmo tempo.
- Se a task estiver atribuída a `Claude Desktop`, Codex só pode preparar,
  revisar ou reatribuir com autorização explícita; não pode implementar os
  arquivos bloqueados.
- Se o executor precisar alterar arquivo fora de `locked_paths`/permitidos, deve
  parar e registrar bloqueio.

## Contrato do executor IA
Obrigatório para qualquer task executada por Codex, Claude Desktop, Claude Code
ou outro agente. Sem este bloco completo, a task não entra em Ready for Dev.

- Modelo/ambiente autorizado: Codex Desktop local | Claude Desktop | Claude Code CLI | Humano | outro
- Diretório/branch/worktree obrigatório:
- Prompt obrigatório para colar/rodar:
  ```text
  Leia esta task inteira e as specs obrigatórias antes de codar.
  Confirme o branch/worktree atual, `git status`, `locked_paths`, conflitos
  conhecidos e arquivos permitidos.
  Execute somente o escopo desta task.
  Pare e devolva bloqueio se faltar spec, issue, permissão, arquivo permitido,
  contrato de UI/API/segurança, teste obrigatório ou validação.
  ```
- Pode fazer:
  -
- Não pode fazer:
  - Não salvar arquivos fora do repo/caminho canônico da task.
  - Não usar worktree temporário como fonte final sem commit/PR.
  - Não inventar arquivos, endpoints, tabelas, permissões, payloads ou regras.
  - Não editar fora de `locked_paths`.
  - Não sobrescrever trabalho de outro executor.
  - Não avançar para outra issue/task.
- Comandos obrigatórios antes de codar:
  - `git status --short --branch`
  - leitura completa da task e specs obrigatórias
- Comandos obrigatórios de validação:
  -
- Formato obrigatório da resposta final:
  - Banco:
  - API/Backend:
  - Frontend/UI:
  - Validação:
  - Riscos/Lacunas:
  - Arquivos alterados:
- Evidência obrigatória:
  -
- Checkpoint máximo para AFK:
- Condição de parada específica desta task:
  -

## Objetivo da task
O que esta task entrega, em uma a três frases.

## Tipo de slice
Vertical behavior slice | Refactor mecânico | Infra/DevOps | Spike | Docs

Se não for `Vertical behavior slice`, justificar por que UI/API/Banco/Testes não
precisam ser entregues juntos nesta task.

## Contexto
Por que esta task existe e o que o executor precisa saber.

## Specs obrigatórias
Links das specs que são contrato desta task (product/module/page/component/validation/database/api).

## Docs obrigatórios
PRD, arquitetura, mockups aprovados e demais documentos a seguir.

## Resultado dos gates
| Gate | Status | Evidência / motivo | Bloqueio |
| --- | --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED |  |  |
| Spec Completeness Gate | PASS/BLOCKED |  |  |
| UI Interaction Contract Gate | PASS/BLOCKED/N/A |  |  |
| Backend Contract Gate | PASS/BLOCKED/N/A |  |  |
| Security Spec Contract Gate | PASS/BLOCKED/N/A |  |  |
| Traceability Gate | PASS/BLOCKED |  |  |

Qualquer `BLOCKED`, `N/A` sem motivo verificável ou gate ausente impede Ready for
Dev.

## Escopo
O que está incluído nesta task.

## Fora do escopo
O que NÃO deve ser feito aqui (evita PR inchado).

## Arquivos prováveis
Caminhos prováveis a alterar (marcar `HIPÓTESE:` quando não confirmado).

## Arquivos e módulos permitidos
Lista objetiva dos arquivos, diretórios ou módulos que o executor pode alterar.
Se precisar sair da lista, parar e registrar bloqueio.

## Arquivos e módulos proibidos
Lista de áreas que não devem ser tocadas nesta task.

## Minimal Planning Review
Resumo das recomendacoes aprovadas pelo `minimal-implementation-gate`, ou `N/A`
com motivo. Registrar qualquer recomendacao rejeitada e a justificativa humana.

## Banco
Mudanças de schema/migração. `N/A` + motivo se não houver.

## API/Backend
Endpoints/serviços a criar ou alterar. `N/A` + motivo se não houver.

## Contrato backend/API/job/webhook
Obrigatório quando houver backend, integração, job, fila, webhook, upload,
pagamento, import/export ou efeito persistente.

| ID | Entry point | Request/evento | Authz | Validação | Banco/efeito | Response/erro | Idempotência/transação | Testes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-01 |  |  |  |  |  |  |  |  |

## Frontend/UI
Telas/componentes a criar ou alterar. `N/A` + motivo se não houver.

## Matriz de interações UI
Obrigatória quando houver UI. Cada linha deve ter implementação e evidência.

| ID | Tela/componente | Elemento/ação | Condição/permissão | Chamada/efeito | Estados | Erro/feedback | Teste/evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UI-01 |  |  |  |  |  |  |  |

## Regras de negócio
RN aplicáveis (referência ao validation-rules-spec).

## Critérios de aceite
Lista objetiva e testável do que define "pronto".

## Matriz de rastreabilidade
| Requisito/RN/mockup | Spec origem | Implementação esperada | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## TDD / Testes obrigatórios
Testes que devem existir/passar (unit, integração, e2e) e cobertura mínima.

## Testes negativos obrigatórios
Sem permissão, tenant/usuário errado, input inválido, estado inválido,
duplicidade, concorrência, erro de integração, rate limit/retry ou outro abuso
aplicável. `N/A` exige motivo.

## Segurança
Pontos de atenção de segurança (validar com security-standard).

## Security Spec Contract
Obrigatório quando houver auth, autorização, tenant, admin/support, dados
sensíveis, uploads/downloads, pagamentos, webhooks, integrações externas,
parsers, arquivos gerados, browser storage, dependências, infraestrutura, CI/CD,
secrets, logs, import/export, AI/LLM tools ou endpoint público.

| Superfície | Ator/abuso | Controle obrigatório | Teste/evidência | Bloqueia release? |
| --- | --- | --- | --- | --- |
|  |  |  |  | sim/não |

## Observabilidade/logs
Eventos, métricas e logs que devem ser adicionados.

## Instrução para IA/dev
Passos diretos para o executor atribuído, restrições e o que NÃO tocar. Antes de
codar, executar `Minimal Implementation Gate`, confirmar que o `Executor LLM
primário` corresponde ao agente atual, confirmar que o `Contrato do executor IA`
está completo, e respeitar o caminho minimo aprovado.

Instrução obrigatória: se qualquer gate estiver ausente, `BLOCKED`, ou se a
task/spec não definir comportamento de botão, endpoint, permissão, erro ou teste
necessário, pare antes de codar e devolva para `dev-workflow-standard` /
`sdd-spec-factory` como `blocked`/`needs-info`.

Instrução obrigatória de contrato IA: se o modelo/ambiente atual não for o
`Modelo/ambiente autorizado`, se o prompt obrigatório não foi fornecido, se o
branch/worktree estiver errado, ou se o executor não conseguir ler a task/specs,
não implemente. Registre bloqueio ou peça reatribuição explícita.

Instrução obrigatória de anti-colisão: se a task estiver atribuída a outra LLM,
ou se algum `locked_path` estiver reclamado por outra task/executor, não
implemente. Registre o bloqueio ou peça reatribuição explícita.

## Condições de parada
- Gate obrigatório ausente, `BLOCKED` ou `N/A` sem justificativa verificável.
- `Executor LLM primário` ausente, `A definir`, diferente do executor atual, ou
  sem reatribuição explícita.
- `Contrato do executor IA` ausente, incompleto, sem prompt obrigatório, sem
  proibições explícitas ou incompatível com o executor atual.
- `locked_paths` ausente, vazio sem justificativa, ou em conflito com outra task
  em andamento.
- Necessidade de alterar arquivo/módulo fora da lista permitida.
- Necessidade de criar endpoint, tabela, payload ou regra não especificada.
- Divergência entre spec, mockup, PRD, AGENTS.md ou código real.
- Falta de teste/evidência para comportamento crítico.

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
