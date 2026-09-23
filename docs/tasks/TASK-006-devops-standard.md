# TASK-006: Integrar especialista DevOps ao Engineering Harness

## Status, tipo e prioridade

Implementação e validação local concluídas; em revisão para decisão humana.
Feature/DevOps. Prioridade alta. Complexidade COMPLEX.
Escopo de implementação autorizado pelo usuário; merge/deploy não autorizados.

## Status visual

- Status visual: 🟡 Em andamento
- Status Kanban: In Review
- Responsável: Engineering Harness e executores especializados
- Bloqueios: nenhum para o pacote local; Environment futuro NOT VALIDATED
- Branch sugerida: feat/devops-standard
- Issue criada / vinculada: #24
- Pronto para GitHub Projects: sim; nenhum Project foi alterado
- Milestone: N/A
- Labels sugeridas: feature

## Tipo

Feature / Infra

## Prioridade

P1

## Specs obrigatórias

`docs/specs/devops-standard/module-spec.md`

## Execution Contract

`docs/execution/TASK-006.json`

## Arquivos e módulos permitidos

Allowlist em TASK-006.json. `locked_paths`: outros plugins, configurações globais,
PR #23/feat/environment-bootstrap, dados e infraestrutura de clientes.

## Estado atual encontrado

Main sincronizada por fetch/pull ff-only, base 83e1c72, inicialmente limpa.
318 testes baseline passaram. Helper suportava três owners, ignorava cwd e
retornava exit0 para ferramenta executada com falha. Cache instalado do Harness
difere da fonte canônica; esta entrega não altera a instalação global.

## Resultado esperado

Plugin DevOps funcional como skill, integrado ao pacote e revisável em PR,
com catálogo oficial, evidência e aprovação humana nas operações de risco.

## Regras obrigatórias da implementação

Escopo, segurança, proveniência e critérios da module-spec são vinculantes.
Não operar infraestrutura para comprovar funcionamento deste pacote de skills.

## Checklist de execução

1. Ler fontes e skills, registrar preflight.
2. Gerar spec/task/contract e resolver capacidades.
3. Implementar pacote, docs e extensão mínima do helper.
4. Testar fixtures, suite, JSON e validadores de skill/plugin.
5. Revisar segurança e interpretação com agentes independentes.
6. Atualizar README/evidências, commit/push/PR sem merge.

## Condições de parada

Conflito de fonte de verdade, expansão de escopo, validação obrigatória falhando,
ausência de skill obrigatória ou necessidade de autoridade de produção.

## Testes obrigatórios

Suíte unittest completa, testes de pacote/integração e helper em processos
temporários, parse JSON, quick_validate, validate_plugin e git diff --check.

## Evidências esperadas no PR

Relatório completo, receipts, review de segurança, comandos/exit codes, fonte
pinada/notices, critérios mapeados e limitações de infraestrutura real.

## Critérios de aceite

Vinte critérios da module-spec e trinta itens do pedido mapeados no relatório
de entrega, com distinção entre teste automático e avaliação comportamental.

## Rastreabilidade

- Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/24
- Branch: `feat/devops-standard`, base `83e1c7296497c34267d85105f352b460136a09a7`.
- PR: abrir após validação; vincular TASK-006/Issue24, sem merge automático.
- Responsáveis: Harness orquestra; SDD especifica; executor implementa;
  security-standard revisa segurança e Harness revisa entrega.
- Spec: [module-spec.md](../specs/devops-standard/module-spec.md).
- Contract: [TASK-006.json](../execution/TASK-006.json).
- Checklist: [review-checklist.md](../specs/devops-standard/review-checklist.md).

## Objetivo, escopo e arquivos

Entregar `devops-standard` como especialista nativo, com conhecimento upstream
reutilizável auditado e revisão original baseada no pedido. Criar plugin,
manifestos, referências/templates, registry de 20 tools, integração Harness/SDD,
testes e documentação. Reutilizar helper e receipts atuais.
Arquivos: `plugins/devops-standard/**`, docs do Harness/SDD/implementation/security,
marketplaces, `plugins/dev-workflow-standard/scripts/tool-state.py`, tests,
README, AGENTS e pipeline. Extensões mínimas, sem subsistema paralelo.

## Docs obrigatórios

AGENTS.md, README.md, docs/workflow-pipeline.md, referências Harness
capability-registry, harness-execution, skill-owned-tools,
skill-execution-contract e execution-report-comments, além da spec acima.
Antes de adaptar fonte, carregar ORIGIN/notices resultantes da auditoria.

## Banco

N/A: sem schema, migração ou restauração real.

## API/Backend

N/A para API de aplicação. Helper existente pode receber suporte mínimo ao novo
owner, execução no workspace e propagação do exit code real, cobertos por
fixtures sem rede/infraestrutura. Não portar toda a feature Environment.

## Frontend/UI

N/A: sem superfície visual. ui-ux-standard não é owner DevOps.

## Regras de negócio e aceite

Cumprir integralmente as regras e 20 critérios da module-spec. Cobrir pelo menos
30 verificações relevantes do pedido: bundle/skill/manifests/marketplace,
proveniência/notices, registry/fontes/ownership, routing aplicável e não
aplicável, contrato compacto, gates destrutivos, IaC/K8s sem apply automático,
produção gated, rollback, caminhos de validação CI/Docker/IaC/K8s/Ansible,
findings contextualizados, fail/fix/revalidate, receipts, README e integração
Environment condicionada à sua existência real.

## Fora do escopo

Merge/deploy, instalação global/cache, produção, mudanças em cloud/servidores,
segredos, duplicação Environment/MCP/scanners e cópia de `devops-review`
restricted. PR #23 não está nesta base; preservar seus trabalhos separadamente.

## TDD / Testes obrigatórios

- Criar testes estruturais e fixtures temporárias, incluindo sucesso/falha do
  helper e negativos de roteamento/gates. Não apenas busca de palavras.
- Executar `python3 -m unittest discover -s tests -v` e `git diff --check`.
- Executar validators de plugin/skill e parse JSON. Inspecionar diff final.
- Registrar comandos, códigos e resultados. Não executar produção para testes.

## Validações e tools previstas

| Owner | Capability | Preferred tool |
| --- | --- | --- |
| dev-implementation-standard | python-unit-testing | python-unittest |
| dev-implementation-standard | plugin-structure-validation | validator local de plugin/skill |
| security-standard | operational-safety-review | revisão contextual das mudanças |

Ferramentas DevOps são o catálogo entregue, não dependências obrigatórias desta
task documental. Validators de infra sem ambiente/fixture adequado permanecem
NOT VALIDATED; não instalar 20 CLIs para aparentar validação.

## Segurança

Revisar fontes/notices, ausência de secrets, gates humanos, rollback, comandos
de templates, runtime-state ignorado e single ownership. Aprovação desta task
não autoriza apply/destroy/deploy/force push/restores ou outras operações reais.

## Observabilidade/logs

Preservar receipts existentes, comandos/exit codes e evidência local sanitizada.
Issue recebe checkpoints materiais, não logs extensos. Nenhum DEVOPS_RECEIPT.

## Decisões pendentes e riscos

Environment Bootstrap: integração pendente NOT VALIDATED nesta base, sem
duplicação. Revisão humana do PR e eventual integração futura continuam abertas.
Ferramentas externas/produção não testadas não recebem PASS.

## Prompt para o executor

Execute TASK-006 pelo contrato `docs/execution/TASK-006.json`, seguindo o
Engineering Harness. Registre resultado e evidências nesta task.

## Continuidade entre LLMs

- Executor: agente delegado usando dev-implementation-standard.
- Disponibilidade: resolvida pelo Harness por checkpoint.
- Contrato: `docs/execution/TASK-006.json`.
- EXECUTION_HANDOFF obrigatório ao trocar executor.

## Relatórios humanos na Issue

- Checkpoints: RUNNING, VALIDATING, REWORK, BLOCKED ou COMPLETED conforme prova.
- Publicação deste checkpoint de especificação: NOT PUBLISHED pelo agente SDD;
  orquestrador consolida/publica para evitar duplicação.
- Evidência remota: pendente de publicação pelo Harness.

## Resultado da execução

### Especificação

SKILL_RECEIPT: sdd-spec-factory, LOADED; SKILL canônica completa, templates de
module/task/contract/PR/QA/review e skill-execution-contract lidos. Aplicado:
separação de dimensões, contrato enxuto e rastreabilidade antes de implementação.
Arquivos gerados: spec, checklist, esta task e contrato. Nenhum código de produto
ou infraestrutura executado pelo agente SDD.

### Implementação e validação

Pacote implementado; 356 testes PASS (318 baseline + 38 novos), plugin validator
PASS, cinco skills alteradas válidas e 32 JSON parseados. Compose config real
PASS na fixture, sem criar container. Correções do helper comprovadas por
processos temporários, incluindo fail/fix/revalidate e workspace inválido.

Relatório completo com audit summary, fontes/revisões/notices, tabela das 20
tools, validações por domínio, forward tests, 30 critérios e comandos/exit:
[devops-standard-delivery.md](../devops-standard-delivery.md).
Revisão independente: [TASK-006 security review](../security/reviews/TASK-006-devops-standard.md).
Nenhuma instalação global, merge, deploy ou operação de produção.

## Validação

Skill principal: 112 linhas, progressive disclosure. Três manifestos e dois
marketplaces corretos. Sem novo Harness/installer/MCP/scanner. Pipeline/SDD/
owners e README atualizados. Avaliação independente: quatro cenários SDD e
sete cenários DevOps, mais walkthrough de segurança, sem infraestrutura real.

## SKILL_RECEIPT e evidência de invocação

- Harness canônico LOADED pelo orquestrador: referências harness-execution,
  capability-registry, skill-execution-contract, minimal-code-gate,
  skill-owned-tools e execution-report-comments. Aplicado: contratos antes da
  implementação, delegação real, receipts, revisão e sem merge/deploy.
- SDD LOADED por devops_spec: templates module/task/contract/PR/QA/review.
  Output: spec, task, contrato e checklists antes da liberação dos executores.
- Implementation LOADED por devops_sources e devops_tools: task/contrato/spec,
  fronteiras e minimal gate. Outputs reais: refs/templates/registry/helper/testes.
- Security LOADED por revisor independente devops_spec: pipeline/coverage/
  finding/false-positive/stack-profiles/report-template; relatório com cobertura.
- plugin-creator e skill-creator LOADED pelo orquestrador: scaffold via script,
  metadados gerados, progressive disclosure e validadores do pacote/skill.
- readme LOADED: exploração do repo e instruções de instalação/uso refletindo
  a estrutura entregue, sem presumir aplicação ou deploy de infraestrutura.
- UI lida na inspeção de fronteiras; execução UI N/A, não há tela alterada.

## REUSE_INVENTORY / MINIMAL_CODE_GATE

Buscas em skills, registries, helper/tests, marketplace e docs confirmaram
owners existentes e ausência de DevOps na main. REUSE: receipts, schema JSON,
diretórios de task/spec e convenções de marketplace. EXTEND: helper e router,
sem segundo instalador. CREATE: referências/templates do especialista aprovado,
registry próprio e testes. Gate PASS, sem abstração de runtime nova. Os
bytecodes gerados pelos testes foram ignorados, sem remover bytecodes históricos.

## EXECUTION_RECEIPT

- task_id: TASK-006
- capability: implementação e integração DevOps no Harness
- provider_or_runtime: agentes autorizados nesta sessão, shell local e GitHub CLI
- executor: devops_sources (knowledge), devops_tools (registry/helper),
  orquestrador (integração/documentação/packaging/validação)
- state: COMPLETED para implementação/verificação local; revisão humana pendente
- invocation_evidence: delegações executadas, patches presentes, subprocessos
  de testes e validadores observados; referências no relatório de entrega
- inputs_used: docs/execution/TASK-006.json, spec e fontes pinadas em ORIGIN
- outputs_produced: bundle nativo, integração, docs/testes e review independente
- changed_files_or_artifacts: diff da branch feat/devops-standard
- commands_and_results: tabela no relatório de entrega, incluindo RED e GREEN
- validation_evidence: 356 testes, validadores, Compose config fixture, review
- tool_evidence: Git2.43.0 detectado/cacheado, Compose5.5.1 detectado; tools já
  existentes, installation_performed=false; registry/test fixtures não alegam
  funcionamento real das 20 ferramentas
- blockers: nenhum para revisão do pacote; Environment/runtime/prod NOT VALIDATED
- next_safe_action: revisar PR; nenhuma permissão de merge/deploy inferida

## EXECUTION_REPORT_COMMENT

Publicados pelo Harness, retornos confirmados:

- RUNNING: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/24#issuecomment-5802224591
- VALIDATING: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/24#issuecomment-5802342726

## Riscos/Lacunas

Gates são instruções, não sandbox. Produção/deploy/restore/cloud auth e execução
real de CLIs ausentes NOT VALIDATED. Environment permanece fora da base, sem
integração simulada. PR #23 segue preservado e poderá exigir resolução de
conflitos após revisão. Instalação global/cache não realizada. UI/Banco/APIs
de aplicação N/A. Nenhum segredo ou dado de cliente usado.
