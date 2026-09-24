# TASK-009: Matriz de setores, Context Routing e QA independente

## Identidade e Status visual
- Status visual: 🟢 Concluída no escopo local; Kanban local: Done; estado: COMPLETED.
- Aceite humano pendente; nenhum board remoto foi alterado.
- Tipo: Feature; complexidade: COMPLEX; prioridade: P1.
- Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28
- Branch: `feat/sector-context-qa`; base verificada: `59e627519b83c0ec30d16c81dbeebd788b5e0b19`.
- PR: não criado; publicação fora deste escopo; preparar pacote revisável local.
- Responsável: Harness coordena, Implementation executa, QA revisa independentemente.
- Pronto para GitHub Projects: sim como contrato, sem presumir associação a board.

## Objetivo
Evoluir Task/contract para execução por setores com contexto mínimo completo,
adicionando QA/Test Engineering independente e reconciliação final evidenciada.

## Escopo e Resultado esperado
Extensão aditiva de templates/skills/handoffs; bundle QA integrado; testes,
cenários e documentação. Arquitetura definida na spec, não repetida aqui.

## Fora do escopo
Push/PR/merge/deploy, instalação global, runtime de aplicação, migração histórica,
policy engine/novo parser/novo receipt, datasets, importação de branches Security/UI.

## Fontes globais da verdade / Specs obrigatórias / Docs obrigatórios
- REQUIRED [module-spec](../specs/sector-context-qa/module-spec.md): arquitetura e limites.
- REQUIRED [validation-rules](../specs/sector-context-qa/validation-rules.md): regras/38 checks/dez cenários.
- REQUIRED [AGENTS](../../AGENTS.md): governança do repositório.
- REQUIRED [README](../../README.md): produto e integração pública.
- REQUIRED [pipeline](../workflow-pipeline.md): gates existentes.

## Execution Contract
[TASK-009.json](../execution/TASK-009.json). v1 com routing setorial aditivo,
normalizado após aprovação dos templates; status/evidências continuam nesta Task.

## Estado atual encontrado
Branch limpa criada da main sincronizada. QA distribuído sem especialista
dedicado; contract v1 sem parser runtime; owners de tools já definidos.
Branches locais anteriores Security e UI preservadas, não incorporadas aqui.

## Arquivos e módulos permitidos
Paths em `allowed_paths` do contrato. `locked_paths`: tool-state.py, registries
existentes, scripts Environment, configurações globais e branches anteriores.
Alteração necessária em path bloqueado exige voltar ao Harness antes de executar.

<a id="acceptance"></a>
## Critérios de aceite
- [x] T01–T38 e S01–S10 evidenciados, limitações explícitas.
- [x] Contract v1 legado compatível; fontes propósito/condição e owners verificáveis.
- [x] QA independente, sem duplicação de ferramentas/receipts.
- [x] README/pipeline/templates e marketplaces coerentes.
- [x] Suíte e validators PASS; review independente; zero REQUIRED pendente.
- [x] Gate PASS para commit local; sem ações externas fora do escopo.

## Matriz de Validação por Setor
`governance` estende a matriz para a metodologia/contratos do Harness, sem
fingir alteração de endpoints de aplicação.

| Setor / ID | Aplicável | Responsável | Status | Dependências finais / motivo N/A |
| --- | --- | --- | --- | --- |
| Banco / database | N/A | dev-implementation-standard | N/A | Sem schema/persistência |
| API/Backend / backend | N/A | dev-implementation-standard | N/A | Sem API/serviço de produto |
| Frontend / frontend | N/A | dev-implementation-standard | N/A | Sem UI renderizada |
| UI/UX / ui_ux | N/A | ui-ux-standard | N/A | Boundary textual, sem design/validação visual |
| QA/Testes / qa | REQUIRED | qa-testing-standard | COMPLETED | governance; planning pode preceder implementação |
| Segurança / security | N/A | security-standard | N/A | Boundary textual preserva candidate/finding; sem nova superfície AppSec |
| DevOps/Infraestrutura / devops | N/A | devops-standard | N/A | Sem CI/runtime/container/infra |
| Observabilidade / observability | N/A | devops-standard | N/A | Sem telemetria ou operação; evidências no ledger existente |
| Documentação / documentation | REQUIRED | dev-implementation-standard | COMPLETED | governance |
| Gate Final / harness | REQUIRED | dev-workflow-standard | COMPLETED | governance, qa, documentation |
| Governança/contratos / governance | REQUIRED | dev-implementation-standard | COMPLETED | Specs aprovadas |

## API/Backend
N/A conforme matriz; não há endpoint nem serviço de aplicação alterado.

<a id="governance"></a>
## Governança/contratos
Responsável: dev-implementation-standard. Status COMPLETED. Objetivo: templates,
contratos, routing, QA bundle e boundaries. Banco e endpoints: N/A, como na matriz.
- REQUIRED [module-spec](../specs/sector-context-qa/module-spec.md): decisões e caminhos.
- REQUIRED [validation-rules](../specs/sector-context-qa/validation-rules.md): implementar contrato verificável.
- CONDITIONAL `plugins/dev-implementation-standard/skills/dev-implementation-standard/references/tool-registry.json`:
  quando usar capability de teste, confirmar ownership.
- Fazer: TDD estrutural, estender mecanismos existentes, preservar v1 e locked_paths.
- Evidência esperada: diff, testes antes/depois, skill/execution receipts.
- Resultado: PASS: bundle, routing, templates e boundaries entregues; suíte 490 PASS.

## Frontend/UI
N/A conforme matriz; nenhum artefato visual a validar.

<a id="qa"></a>
## QA / Testes
Responsável: qa-testing-standard, resolver skill canônica criada antes da execução.
Status COMPLETED. Planning: estratégia/casos podem anteceder implementação.
Validation: depende de governance revisável, não aceitar só claim do implementador.
- REQUIRED [validation-rules](../specs/sector-context-qa/validation-rules.md): oráculo dos checks/cenários.
- REQUIRED [module-spec](../specs/sector-context-qa/module-spec.md): limites e compatibilidade.
- CONDITIONAL `tests/test_sector_context_routing.py`: quando Governance entregar,
  executar e avaliar cobertura de routing.
- CONDITIONAL `tests/test_qa_testing_standard.py`: quando bundle QA existir,
  executar e avaliar fronteiras e regressões.
- Fazer: T01–T38, S01–S10, negativos e regressão; distinguir teste/ambiente/produto.
- Evidência esperada: comandos/exit codes, casos observados, bugs/disposição/reteste,
  QA_STATUS e EXECUTION_RECEIPT independente. Runtime de app N/A.
- Resultado: PASS no escopo de metodologia/contratos; [QA independente](../qa/TASK-009-review.md).

## Segurança
N/A AppSec runtime conforme matriz; invariantes de boundary exigidas por T27/S06.

## Observabilidade/logs
N/A runtime; reaproveitar registro de evidências abaixo, sem output sensível.

<a id="documentation"></a>
## Documentação
Responsável dev-implementation-standard; Status COMPLETED; depende de governance.
- REQUIRED [README](../../README.md): atualizar arquitetura, instalação e limites.
- REQUIRED [pipeline](../workflow-pipeline.md): explicitar setores/routing/gates.
- REQUIRED [module-spec](../specs/sector-context-qa/module-spec.md): não contradizer decisões.
- CONDITIONAL `.agents/plugins/marketplace.json` e `.claude-plugin/marketplace.json`:
  quando bundle QA existir, conferir paths/adaptadores.
- Fazer: docs públicas, Migration Matrix, exemplos PT-BR Task/JSON, economia qualitativa.
- Evidência esperada: revisão de links/diff/validadores e relatório final.
- Resultado: PASS; README, pipeline, exemplos e [relatório](../sector-context-qa-delivery.md) atualizados.

<a id="harness"></a>
## Gate Final do Harness
Responsável dev-workflow-standard; Status COMPLETED; depende de todos REQUIRED.
- REQUIRED `docs/tasks/TASK-009-sector-context-qa.md` completa: reconciliar setores e autorização.
- REQUIRED `docs/execution/TASK-009.json`: conferir escopo e fontes.
- REQUIRED receipts retornados no registro abaixo: verificar execução real e não fabricar PASS.
- CONDITIONAL contexto adicional: se conflito, resolver antes de continuar.
- Fazer: revisão completa, critérios, docs, comandos, commit local só após PASS.
- Evidência esperada: decisão final e HEAD/status confirmados.
- Resultado: PASS; todos REQUIRED reconciliados, gate local aprovado. HEAD final confirmado após commit.

## Ordem de Execução e Checklist
1. [x] Sincronizar main e registrar estado, Issue, SDD.
2. [x] Harness aprova arquitetura/spec em 2026-09-24; delega implementação em paths exclusivos.
3. [x] Planning QA proporcional; implementar templates, routing e QA bundle.
4. [x] QA independente executa validação após dependências materiais.
5. [x] Documentação/relatório e reconciliação de todos REQUIRED.
6. [x] Gate PASS autoriza commit local; aceite humano permanece separado.

## Regras obrigatórias / Condições de parada
Sem PASS fora do owner; sem evidência não PASS; REQUIRED não opcional;
source_of_truth_conflict, mandatory_reference_missing, expansão de escopo,
arquitetura não aprovada ou ferramenta obrigatória indisponível param o checkpoint.

## TDD / Testes obrigatórios / Validação
Owner Implementation: unittest estrutural, validators de plugin/skill e diff check.
Owner QA: cenários/revisão independente e regressão. Comandos previstos:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`,
`git diff --check`, validators disponíveis do bundle e skill.
Estado/instalação de ferramenta não pertence ao contrato.

## Evidências esperadas no PR / Gate do PR
Pacote local deve vincular Task, Issue, specs, diff, testes, receipts, migration,
limites e bugs. PR não publicado neste escopo; isso não autoriza merge/deploy.

## Registro de Evidências / Resultado da execução
SDD: quatro artifacts escritos; nenhum código de produto implementado.
Implementation e Documentation: PASS, receipts por owner no
[relatório final](../sector-context-qa-delivery.md#receipts-and-minimal-change).
QA: PASS independente pelo executor sector_sdd, [receipt e fingerprints](../qa/TASK-009-review.md).
Harness: PASS local após conciliar esses resultados; sem bloqueios abertos.
Suíte root: 490 PASS / 14.469s; QA: 490 PASS / 15.362s; exit 0 em ambas.
Sete skills e bundle QA validados; diff check PASS. Doctor exit 0, blockers [],
saúde geral DEGRADED explicitamente não equivale a runtime completo validado.
S01–S10 e três casos adicionais revisados; R01–R03 corrigidos/retestados.
Revisão: worktree sobre 59e6275, fingerprints dos artefatos no receipt QA.
Commit contém este pacote; hash final verificado pelo Git após gravação.
Relatório VALIDATING publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818634646.
Relatório RUNNING publicado pelo Harness:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818418747.
Relatório COMPLETED local publicado, sem fechar a Issue:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818693644.
Reexecução final após consolidar os receipts: 490 PASS, 9.731s, exit 0.
Conferência dos 45 paths alterados, paths protegidos e JSONs: PASS.

## Riscos/Lacunas / Decisões pendentes
Testes estruturais não provam execução futura de agentes. Runtime de aplicação e
cache instalado fora do escopo. Aceite final humano e publicação aguardam decisão.

## Prompt para o executor
Execute TASK-009 usando `docs/execution/TASK-009.json`. Siga o Engineering Harness,
respeite o setor atribuído e registre evidências nesta Task.

## Aceite Humano
Pedido autoriza implementação especificada e commit após PASS local. Aceite da
entrega, push, PR, merge, deploy e instalação global não presumidos.
