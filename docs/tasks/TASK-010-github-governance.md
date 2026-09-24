# TASK-010: Bootstrap idempotente de governança GitHub

## Identidade
Status visual: Concluída tecnicamente; Kanban: Awaiting Final Approval
(pacote local, sem PR publicado); checkpoint COMPLETED, não Done.
SDD aprovada pelo Harness em 2026-09-24, conforme autorização de implementação
do pedido. Nenhuma autorização de aplicação remota é inferida.
Tipo DevOps/Feature; COMPLEX; prioridade P1.
Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/30
Branch `feat/github-governance-bootstrap`; base `44718fe5faa49cdfde790a51ae6e63ce6c18c050`.
PR não criado, não autorizado nesta entrega. Responsável Harness; owners na matriz.
Pronto para Project como contrato, sem presumir vínculo/alterar board remoto.

## Objetivo e escopo
Evoluir DevOps existente com helper diagnose/propose/apply/verify, desired JSON,
readiness e onboarding. Sem aplicação de governança remota nesta task.

## Fontes globais / Specs / Docs obrigatórios
- REQUIRED [module-spec](../specs/github-governance/module-spec.md): arquitetura e limites.
- REQUIRED [validation-rules](../specs/github-governance/validation-rules.md): oráculos e testes.
- REQUIRED [AGENTS](../../AGENTS.md): governança vigente.
- REQUIRED [README](../../README.md) e [pipeline](../workflow-pipeline.md): coerência pública.
Contrato: [TASK-010.json](../execution/TASK-010.json).

## Estado encontrado e resultado esperado
Main sincronizada, base/branch acima; working tree inicial limpa. gh já catalogado
DevOps, Environment/receipts reutilizáveis, sem helper canônico equivalente achado.
Resultado: implementação local testada e revisável, não repo GitHub remotamente pronto.

## Fora do escopo / locked_paths
Não alterar governança remota do Dev-workflow, root `.github` ou settings/Projects;
sem push/merge/deploy/global install/auth automático; sem nova skill ou OAuth;
sem mudanças em scripts Environment/tool-state.py e registries de outros owners.
Paths permitidos no contrato. Expansão exige Harness antes de editar.

<a id="acceptance"></a>
## Critérios de aceite
- [x] RN-01–RN-12 e T01–T20 + negativos evidenciados no escopo offline.
- [x] Read-only comprovado; apply confirmado vinculado à proposta sem drift.
- [x] Idempotência fake-gh, sem duplicação ou falsas alegações de enforcement.
- [x] Security/QA independentes PASS, suíte/validators/README/diff check PASS.
- [x] README fases0–10, oito Kanban stages, Done reservado ao merge humano.
- [x] Gate libera commit local após PASS; integração remota NOT VALIDATED.

## Matriz de Validação por Setor
| Setor / ID | Aplicável | Owner | Status | Dependência final ou motivo N/A |
| --- | --- | --- | --- | --- |
| Banco / database | N/A | dev-implementation-standard | N/A | Sem schema/persistência app |
| API/Backend / backend | N/A | dev-implementation-standard | N/A | Helper operacional pertence DevOps, sem API app |
| Frontend / frontend | N/A | dev-implementation-standard | N/A | Sem UI |
| UI/UX / ui_ux | N/A | ui-ux-standard | N/A | Sem tela/design |
| QA/Testes / qa | REQUIRED | qa-testing-standard | PASS | Receipt independente e 539 testes |
| Segurança / security | REQUIRED | security-standard | PASS | Receipt independente, achado corrigido |
| DevOps/Infraestrutura / devops | REQUIRED | devops-standard | PASS | Helper e 47 regressões, escopo local |
| Observabilidade / observability | N/A | devops-standard | N/A | Relatório/receipt coberto DevOps, sem telemetria nova |
| Documentação / documentation | REQUIRED | dev-implementation-standard | PASS | Roadmap, referências e testes |
| Gate Final / harness | REQUIRED | dev-workflow-standard | PASS | Receipts reconciliados, sem produção |

<a id="devops"></a>
## DevOps / Infraestrutura
Owner devops-standard, PASS local; final sem dependências setoriais. Objetivo: helper,
template e referência oficiais, reutilizando gh existente.
- REQUIRED module-spec e validation-rules: implementar contrato e oráculos.
- REQUIRED registry DevOps existente: ampliar capabilities sem duplicar gh.
- CONDITIONAL fontes oficiais registradas em github-governance.md: ao persistir
  comandos/API/limites, confirmar fonte/revisão atual; não depender de memória.
- Fazer: TDD fake-gh, readonly guard, proposta/aprovação/drift, idempotência,
  permissions/plan capability/CI/Project com limites, verificação fresca.
- Evidência esperada: diff, comandos/resultados, fontes oficiais e EXECUTION_RECEIPT.
- Resultado: PASS local, helper SHA-256 registrado no relatório de entrega.

<a id="security"></a>
## Segurança
Owner security-standard, PASS local; validation depende DevOps concluído.
- REQUIRED module-spec: fronteiras e autorização.
- REQUIRED validation-rules: cadeia input/paths/CLI/response e falhas.
- CONDITIONAL helper/testes retornados: quando DevOps entregar, auditar execução.
- Fazer: revisar permissões, segredo/output, injeção, path confinement, proposal
  tampering/drift e ausência de mutação não aprovada; devolver REWORK ao owner.
- Evidência esperada: finding/disposition/contraprovas e receipt; não scanner inventado.
- Resultado: [PASS independente](../security/reviews/TASK-010-github-governance.md).

<a id="qa"></a>
## QA / Testes
Owner qa-testing-standard, PASS local; final depende DevOps concluído.
- REQUIRED validation-rules: T01–T20 e negativos.
- REQUIRED module-spec: arquitetura e limites de escopo.
- CONDITIONAL testes/helper retornados: quando DevOps entregar, executar regressão.
- Fazer: fake-gh independente, read-only, idempotência, drift e erros/readiness;
  distinguir comportamento mock versus operação GitHub real.
- Evidência esperada: comandos/exit codes/observações, bugs/retestes, QA_STATUS/receipt.
- Resultado: [PASS independente](../qa/TASK-010-review.md), Q01–Q05 retestados.

<a id="documentation"></a>
## Documentação
Owner dev-implementation-standard, PASS; depende DevOps concluído.
- REQUIRED README/pipeline: onboarding e lifecycle.
- REQUIRED module-spec: limites/proveniência/decisões.
- CONDITIONAL referência DevOps: quando pronta, conferir links e comandos do roadmap.
- Fazer: roadmap fases0–10, quatro operações/auth segura/gates/readiness, oito estados,
  capabilities, limitações, manual test e relatório final sem duplicar manual API.
- Evidência: docs/diff, 34 testes README e 18 testes DevOps PASS.

<a id="harness"></a>
## Gate Final do Harness
Owner dev-workflow-standard, PASS local; todos REQUIRED reconciliados.
- REQUIRED Task completa + contrato: reconciliação de owners, escopo, evidência.
- REQUIRED receipts dos owners: não inferir execução nem PASS.
- Fazer: confirmar gates, fontes oficiais, revisão/testes/docs e commit após PASS.
- Evidência: revisão do diff e receipts, 539 testes PASS; gate permite commit local.

## Banco / API / Frontend
N/A de aplicação conforme matriz; nenhum schema, endpoint ou tela implementado.

## Target_environment e rollback_strategy
Checkout local e fake-gh/temporários isolados. Nenhuma operação remota autorizada.
Reverter somente diff próprio após revisão; não descartar trabalho de outros.
Para uso futuro helper: partial apply para e reporta, rollback mutante requer
aprovação independente; README não promete rollback atômico.

## Ordem de execução e validações
1. [x] Estado real/Issue/SDD registrados.
2. [x] Harness aprova specs; DevOps pesquisa fontes oficiais e inicia TDD.
3. [x] Security e QA independentes validam; dois ciclos consolidados e retestes.
4. [x] Docs/README/pipeline e testes completos; setores reconciliados.
5. [x] Commit autorizado após PASS local; Awaiting Final Approval, não Done.
Comandos: suíte unittest completa/focada, git diff --check, validators estruturais
existentes e README tests. DevOps dono execução; QA/Security donos conclusões.

## Gate do PR / Aceite Humano
Pacote local com Issue/specs/diff/receipts/tests/limites. PR/push/merge não feitos.
Pedido autoriza implementar e commit após PASS, não aplicar governança remota.
Human merge e deployment gates permanecem separados da aprovação técnica.

## Registro de evidências / Resultado
SDD: quatro artifacts lidos e aprovados pelo Harness, receipt do owner recebido.
DevOps: core entregue para revisão intermediária, 27 testes do autor passaram;
isso não encerra QA nem Security. Rework ciclo 1 consolidado: falso READY por
revisão CI antiga/exceção desconhecida, resposta malformada fora do contrato JSON
e reflexão de marcador sensível no diff, confirmada pelo owner Security.
Autores corrigindo e adicionando regressões, sem aplicação em GitHub real.

Documentação: roadmap README, Harness/pipeline e templates alinhados às oito etapas.
Escopo do contrato ampliado pontualmente pelo Harness para o execution-report
template existente, necessário à mesma migração explícita; sem nova arquitetura.
Testes focados: README 34, Harness 103, Implementation 70, execution-report 64,
DevOps 18, todos exit 0 nas respectivas execuções verdes. Validadores das skills
Harness/DevOps exit 0. Suíte final e reconciliação ainda pendentes.

Checkpoint inicial publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/30#issuecomment-5822213186
Checkpoint REWORK ciclo 1 publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/30#issuecomment-5822466719
Checkpoint técnico COMPLETED / Awaiting Final Approval publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/30#issuecomment-5822649564
Comentários Issue só PUBLISHED com URL retornada. Histórico acima preserva os
checkpoints intermediários, não representa o estado final abaixo.

## EXECUTION_RECEIPT final reconciliado
- task_id: TASK-010; revision: base `44718fe` + diff desta entrega.
- state: COMPLETED, escopo técnico local, pronto para revisão humana.
- invocation_evidence: SDD executado por `sector_sdd`; DevOps por
  `security_sources`; QA independente por `sector_sdd`; Security independente
  por `qa_bundle`; documentação/integração e gate reconciliados pelo Harness.
- inputs_used: contrato, specs, Task e fontes com propósito acima; skills
  canônicas integralmente lidas pelos respectivos owners. README/skill-creator
  orientaram documentação e roteamento enxuto, sem nova skill.
- outputs_produced: helper, desired template, referência técnica, registry gh
  ampliado, README/fluxo/templates alinhados e 47 testes do helper.
- validation_evidence: Harness executou 539 testes em 43.010s, exit 0;
  QA executou independentemente 539 e 47 focados, além de seis probes extras;
  Security executou 47 e cinco canários independentes. Relatórios vinculados
  preservam comandos, hashes, achados/correções e limites.
- helper_sha256: `7fa330927f7136bdfda0d34c6da98ad5bc1bf1be60c83c9b55d36850cb32c46f`.
- rework: 2 ciclos, Q01–Q05 corrigidos nos cenários reproduzidos;
  SEC-2026-010 FIXED, nenhum achado confirmado aberto no escopo revisado.
- commands_and_results: [relatório de entrega](../github-governance-delivery.md#tests).
- blockers: nenhum para commit e entrega local. Integração remota, permissões
  reais, enforcement, CI remoto e instalação permanecem NOT_VALIDATED.
- next_safe_action: commit local autorizado; revisão humana e eventual ensaio
  separado em repo descartável, sem push/merge/deploy implícitos.

REUSE_INVENTORY / MINIMAL_CODE_GATE: reutilizados gh/Environment/registries e
receipts, um helper determinístico explicitamente pedido; constante de arquivos
obrigatórios compartilhada por validação e snapshot para não duplicar policy.
Sem novo framework, autenticação, instalação, runtime state ou skill.

## Riscos / Decisões pendentes / Condições de parada
API drift/permissão, proposal drift, side effects e false readiness. Parar em
source_of_truth_conflict, referência obrigatória ausente, expansão ou alvo ambíguo.
Integração remota manual aguarda autorização futura; nenhum bloqueio para testes locais.

## Prompt para o executor
Execute TASK-010 usando `docs/execution/TASK-010.json`, setor/fase do handoff.
Siga o Harness, respeite o escopo e registre evidências na Task.
