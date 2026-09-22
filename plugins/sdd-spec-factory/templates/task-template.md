# TASK-XXX: Nome da task

> Task é a interface humana para ordem de execução e acompanhamento. Aponta
> para specs, Execution Contract, issue, branch e PR. Deve ser pequena,
> revisável e executável em um único PR.

## Status
A fazer | Em andamento | Em revisão | Concluída | Bloqueada

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

## Execution Contract
`docs/execution/TASK-XXX.json`

## Escopo
O que está incluído nesta task.

## Fora do escopo
O que NÃO deve ser feito aqui (evita PR inchado).

## Arquivos prováveis
Caminhos prováveis a alterar (marcar `HIPÓTESE:` quando não confirmado).

## Banco
Mudanças de schema/migração. `N/A` + motivo se não houver.

## API/Backend
Endpoints/serviços a criar ou alterar. `N/A` + motivo se não houver.

## Frontend/UI
Telas/componentes a criar ou alterar. `N/A` + motivo se não houver.

## Regras de negócio
RN aplicáveis (referência ao validation-rules-spec).

## Critérios de aceite
Lista objetiva e testável do que define "pronto".

## TDD / Testes obrigatórios
Testes que devem existir/passar (unit, integração, e2e) e cobertura mínima.

## Segurança
Pontos de atenção de segurança (validar com security-standard).

## Observabilidade/logs
Eventos, métricas e logs que devem ser adicionados.

## Prompt para o executor
Execute a TASK-XXX usando o contrato:
`docs/execution/TASK-XXX.json`

Siga o Engineering Harness e registre resultado e evidências nesta task.

## Continuidade entre LLMs
- LLM executor atual:
- Estado de disponibilidade:
- Execution Contract: `docs/execution/TASK-XXX.json`
- `EXECUTION_HANDOFF`: obrigatório ao trocar de LLM

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
