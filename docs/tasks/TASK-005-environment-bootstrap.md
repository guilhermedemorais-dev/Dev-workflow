# TASK-005: Environment Bootstrap / Plugin Health

## Adendo autorizado: resolver conflitos PR #23

Usuário autorizou integrar a main `aa389d9` na branch `feat/environment-bootstrap`
após PR #25, preservando ambas as entregas. Complexidade NORMAL, continuidade
da mesma task/Issue #22, sem nova feature. Sete conflitos identificados antes
da execução; não usar ours/theirs indiscriminadamente, force push ou merge na main.
Preservar descoberta dinâmica/read-only/quiet/cache do Environment, o owner
DevOps, workspace inválido e exit codes; preservar MCPs e biblioteca de APIs.
Escopo: resolução nos arquivos compartilhados, correção de documentação que
ficaria contraditória e testes de regressão/integridade combinada. Locked paths:
configurações globais, infraestrutura, dados e novas funcionalidades fora dessas
duas entregas. Aceite: suíte combinada passa, plugins/marketplaces válidos,
nenhum marcador, HEAD remoto confirmado e PR #23 sem conflito.
Estado: validação local concluída; publicação da branch e estado remoto são
confirmados separadamente no checkpoint da Issue #22.

Evidências da integração PR #23 / PR #25, 2026-09-23:
- Executor aplicou o contrato TASK-005 e a skill de implementação canônica;
  Harness e DevOps conduziram revisão e preservação dos gates.
- Sete conflitos resolvidos sem descartar nenhuma entrega. Helper preserva
  descoberta dinâmica, cache sanitizado, read-only/quiet, workspace e exit codes.
- Suíte combinada: 441 testes passaram, incluindo quatro novos testes reais
  de integração Environment/registro DevOps, sem infraestrutura externa.
- Validadores dos dois plugins e das duas skills: exit 0.
- Doctor/status/prepare dry-run: exit 0, sem instalações; health DEGRADED,
  status ready=false/refresh_required=true pela ausência de evidência de runtime.
- Hostinger/AWS/WordPress preservados em USER_ACTION_REQUIRED; biblioteca de
  APIs gratuitas para validação/testes preservada. Nenhuma autenticação inferida.
- Revisão encontrou IDs Mermaid duplicados no README; separados Environment
  e DevOps. Documentação operacional atualizada sem reescrever auditorias históricas.
- Sem merge na main, force push, instalação global ou operação de infraestrutura.

## Adendo autorizado: biblioteca de pesquisa de APIs

Correção textual autorizada pelo usuário: tornar explícita na biblioteca,
SDD, Harness e README a prioridade por APIs gratuitas ou faixa gratuita adequada
para validar funcionalidades e testar a aplicação, quando pertinente. Confirmar
limites, usar dados sintéticos e manter testes locais/mocks quando suficientes.
Escopo TRIVIAL, sem alterar runtime, instalar ou chamar APIs externas.
Validação da correção: regra textual confirmada nos quatro documentos;
suíte unittest 399 PASS, exit 0; git diff --check exit 0.

Pedido do usuário: usar inventario-apis-gratuitas e PublicAPIs.io como biblioteca
de pesquisa durante planejamento/spec, inclusive para APIs de validação.
Contrato NORMAL documental, mesma Issue 22/PR 23. Owner da referência canônica:
sdd-spec-factory; Harness roteia planejamento para ela. Não copiar catálogos,
criar crawler/plugin novo, instalar MCPs ou consumir serviços externos.
Locked paths: referência api-research-library.md da SDD, SKILL.md SDD/Harness,
README, esta task, spec environment e tests/test_api_research_library.py.
Aceite: URLs das duas fontes; gatilho condicional em planejamento/spec;
distinção API/MCP/mock; verificação primária de auth/custo/limites/licença/dados;
registro de candidato/decisão/plano de validação e NOT VALIDATED quando não testado;
sem pesquisa obrigatória irrelevante, segredos ou aprovação automática.
Validação: testes estruturais da referência/roteamento, suíte completa e
git diff --check. Banco/UI/runtime: N/A, apenas contrato de pesquisa.
REUSE_INVENTORY: seção de pesquisa do README, referências on-demand e fluxos SDD
existentes; MINIMAL_CODE_GATE: uma referência Markdown, sem novo serviço.
Status: validado, In Review no PR #23.
EXECUTION_RECEIPT: referência canônica criada e ligada às skills SDD/Harness;
README atualizado antes do commit. Testes novos: 5 PASS. Suíte completa:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`, 399 PASS,
exit 0; quick_validate nas duas skills e git diff --check, exit 0.
SECURITY_STATUS=PASS para o diff documental; observação de portabilidade tratada
com resolução da skill SDD ativa, sem presumir pastas vizinhas no cache.
APIs externas e ativação nos caches globais NOT VALIDATED/não executadas.

## Adendo autorizado: Hostinger, AWS e WordPress

Pedido posterior do usuário: incluir os três MCPs na mesma entrega/PR #23.
Escopo NORMAL, extensão do catálogo existente sem mudar engine, auth ou schema.
IDs `hostinger`, `aws`, `wordpress`; PROJECT_SPECIFIC / OFFICIAL;
AUTH_REQUIRED com host_handoff, sem configuração executável ou credenciais.
AWS corresponde ao AWS API MCP Server; WordPress ao MCP Adapter para site próprio,
não ao conector WordPress.com. Fontes primárias em mcp-source-audit.md.

Locked paths do adendo: mcp-library.json, tests/test_environment_bootstrap.py,
README, operations.md, esta task e docs/specs/environment-bootstrap/**.
Aceite: três entradas válidas, nenhuma seleção padrão, seleção/requisito exige
handoff mesmo com approvals; não instalar/conectar/provisionar nem operar conta/site.
Validar suíte completa, catálogo real e git diff --check; atualizar README antes
de commit/push na branch existente. Status do adendo: validado, In Review no PR #23.

SKILL_RECEIPT: Harness/environment e referências lidos; executor canônico
dev-implementation-standard invocado em environment_runtime. REUSE_INVENTORY:
reutilizar entradas AUTH_REQUIRED/host_handoff e fixtures existentes.
MINIMAL_CODE_GATE: sem engine, wrapper ou novo instalador.

Evidências do adendo: 65 testes environment PASS, suíte completa 394 PASS,
git diff --check exit 0. Smoke CLI com os três --select e --dry-run: exit 0,
USER_ACTION_REQUIRED para cada entrada, executed=false. Revisão independente
security-standard PASS no diff; registrou que AWS API MCP foi substituído pelo
AWS MCP oficial. Catálogo/docs mostram esse ciclo de vida e orientam avaliar o
sucessor antes de novo setup. Nenhuma instalação/auth/operação externa validada.
O relatório original abaixo é histórico da entrega de 13 entradas; este adendo
eleva o catálogo para 16, sem modificar os resultados observados anteriormente.

## Status e rastreabilidade

- Status: Implementado e validado localmente; aguardando revisão humana do PR.
- Status visual: 🟡 Em revisão. Status Kanban: In Review.
- Responsável: Engineering Harness / Codex.
- Bloqueios: nenhum para revisão do código; conexão/auth MCP não validadas no host.
- Milestone: N/A. Labels sugeridas: feature.
- Pronto para GitHub Projects: sim; nenhum board foi associado.
- Tipo: Feature. Prioridade: Alta.
- Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/22
- Branch: `feat/environment-bootstrap`, baseline `83e1c72`.
- PR: entrega única de `feat/environment-bootstrap` para `main`, vinculada à Issue 22; sem merge automático.
- Responsáveis: dev-workflow-standard orquestra; dev-implementation-standard
  executa; security-standard revisa; usuário aceita entrega final.

## Objetivo e escopo

Entregar ambiente portátil com doctor, prepare, repair e status, health baseado
em evidências, Library MCP pública, preferências/custom MCPs privados e preparação
seletiva. Reutilizar helper tool-state e ownership especialistas. Seguir todas as
regras e 30 cenários na spec, sem incorporar DevOps.

## Specs e docs obrigatórios

- `docs/specs/environment-bootstrap/module-spec.md`
- `docs/specs/environment-bootstrap/mcp-source-audit.md`
- `AGENTS.md`, `README.md`, `docs/workflow-pipeline.md`
- `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/skill-owned-tools.md`
- `plugins/dev-workflow-standard/scripts/tool-state.py`
- Skills canônicas afetadas e respectivos tool registries.

## Execution Contract

`docs/execution/TASK-005.json`

## Arquivos e módulos permitidos / locked_paths

Nova skill/plugin environment e seus scripts/references; helper tool-state e
testes; manifests/marketplaces; agents metadata mínimos faltantes; README,
AGENTS, pipeline e roteamento/references afetados. Contrato JSON delimita paths.
Owners exclusivos: executor tool_helper no helper e sua suite; executor
environment_runtime no CLI e sua suite; Harness em catálogo, docs, manifests e
integração. Reviewer independente somente lê/testa. Nenhum executor edita os
mesmos arquivos ao mesmo tempo.

## Estado atual encontrado / resultado esperado

Baseline main 83e1c72, working tree limpa, 318 testes PASS. Três registries e
13 tools, sem environment capability. Resultado: preparação portátil seletiva,
estado privado e health com evidências, conforme 30 critérios da spec.

## Regras obrigatórias / condições de parada

Reutilizar helper; não duplicar registries; respeitar políticas/consentimento;
doctor/status/dry-run somente leitura; README antes de commit. Parar ação
afetada quando exigir privilégio, credencial, política não aprovada, fonte
desconhecida, contrato conflitante ou alteração fora de escopo.

## Diagnóstico, recibo e reúso

SKILL_RECEIPT: sdd-spec-factory lida integralmente em sua fonte canônica; templates
module/task/execution-contract/PR/QA/review lidos. Pedido integral, AGENTS,
TASK-004/contrato e helper existente inspecionados. Saída desta skill: spec,
task e contrato, sem implementar código de produto.

REUSE_INVENTORY: estender tool-state.py; consumir registries das skills sem cópia;
reutilizar manifests/marketplaces, capability routing, receipts, runtime-state
ignorado e testes stdlib. O helper atual tem owners fixos e detecção que escreve,
portanto requer extensão para probe read-only e discovery dinâmico.

MINIMAL_CODE_GATE: um script stdlib environment.py, um catálogo MCP, referências
necessárias e extensões pequenas ao helper. Sem framework, daemon, camada paralela
de instalação ou adaptação fictícia de host. Requisito arquitetural explícito
justifica plugin novo; implementação autorizada, revisão do contrato pelo Harness.

## Banco

N/A para banco/migração; JSON operacional privado/ignorado com schema validado.

## API/Backend

CLI local quatro operações; tool-state reutilizado; host medeia transporte/auth.

## Frontend/UI

N/A para UI de produto; saída CLI humana/JSON e diálogo pelo host.

## Segurança

Sem secrets persistidos/impressos, sudo, comandos de fontes desconhecidas ou
alteração global/destrutiva silenciosa. Aprovação de implementação não equivale a
seleção de opcionais. COMMUNITY exige consentimento; UNKNOWN nunca automático.

## Observabilidade/logs

HEALTH_REPORT e receipts com evidência, comandos seguros/exit/result; distinguir
instalado, conectado, autenticado e efetivamente executado.

## Decisões pendentes e riscos

Sem bloqueio para implementação. Escolha de opcionais/custom/auth pertence ao
bootstrap real. Host sem introspecção, estado inválido e checks não executados
devem resultar em estado conservador, nunca falso HEALTHY.

## Critérios de aceite e testes

Todos os 30 cenários numerados da spec cobertos; preservação da suíte existente,
testes adicionais de exit-code/cwd/resolução local/lockfile/dry-run. README e
referências portáteis atualizados antes do commit. Health nunca supera evidência.

Validações planejadas:

- dev-implementation-standard / python-unit-testing / python-unittest:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
- dev-implementation-standard / environment-health / environment-cli:
  smoke doctor, status e prepare dry-run com comandos finais documentados.
- dev-workflow-standard / repository-integrity / git-diff-check:
  `git diff --check`, JSON/manifests, README gate e inspeção completa do diff.
- security-standard / local-bootstrap-security / code-review:
  revisão de consentimento, processos, paths, estado, auth e output.
- QA visual: N/A, nenhuma UI de produto alterada.

## Checklist PR / QA / review

- [x] Spec/30 critérios conferidos com evidência e casos negativos.
- [x] Banco, API/Backend e Frontend/UI revisados separadamente, N/A justificado.
- [x] Smoke real doctor/status e dry-run, sem instalar opcionais no host.
- [x] Suíte, sintaxe, manifests, JSON e diff check passam.
- [x] Segurança revisada, falhas tratadas, nenhum secret/path pessoal versionado.
- [x] README corresponde à implementação; gate preservado.
- [x] Issue/branch/receipts coerentes; review de segurança aprovado para revisão humana.
- [x] Relatório abaixo cobre as seções obrigatórias; Git final no PR e na entrega.

## Fora do escopo

DevOps completo conforme spec, produto, install-all, configuração global não
necessária, merge/deploy automático ou instalações opcionais sem escolha.

## Prompt para o executor

Execute TASK-005 usando `docs/execution/TASK-005.json`. Siga o Engineering Harness
e registre resultado e evidências nesta task e checkpoints materiais na Issue.

## Continuidade e relatórios humanos

- Executores: tool_helper e environment_runtime, usando dev-implementation-standard;
  contrato conferido/aprovado pelo Harness antes da delegação. environment_spec
  entregou SDD; environment_review usa security-standard para revisão independente.
- EXECUTION_HANDOFF obrigatório ao trocar executor.
- Checkpoints Issue: RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
- Checkpoint VALIDATING: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/22#issuecomment-5801239020

## Resultado da execução

### Audit Summary

Baseline: main `83e1c72`, seis plugins, três registries/13 tools e 318 testes.
Não havia bootstrap canônico; README/security continham inventário pessoal.
O helper tinha owners fixos, resolução local/cwd insuficientes e CLI mascarando
exit code da tool. Corrigidos com regressões, sem recriar a camada de tools.

### Architecture

```text
Engineering Harness
  -> dev-environment-standard
     -> Plugin Health / MCP Library / Runtime Discovery
     -> registries especialistas via tool-state.py
     -> Environment State privado
  -> Capability Router
  -> Specialist Skills
```

Um CLI stdlib, catálogo público de 13 componentes, estado local ignorado,
manifests Codex/Claude e marketplaces existentes. Metadata agents faltante
adicionada às cinco skills legadas afetadas. Nenhuma responsabilidade DevOps.

### MCP Library / Optional MCPs

O smoke leu apenas nomes/enabled da configuração Codex. "Não validado" abaixo
não significa servidor comprovadamente quebrado ou pacote comprovadamente ausente.

| MCP | Provider | Classification | Capability | Status observado |
| --- | --- | --- | --- | --- |
| GitHub | GitHub | CORE / OFFICIAL | repositórios, Issues, PRs | não registrado pelo ID canônico; conexão não validada |
| Context7 | Upstash | CORE / OFFICIAL | documentação | registrado; conexão não validada |
| Playwright | Microsoft | CORE / OFFICIAL | browser QA/e2e | registrado; conexão não validada |
| Chrome DevTools | Chrome DevTools | RECOMMENDED / OFFICIAL | console/rede/performance | registrado; conexão não validada |
| Docker Gateway | Docker | RECOMMENDED / OFFICIAL | lifecycle/isolamento MCP | não validado |
| Docker Registry | Docker | RECOMMENDED / OFFICIAL | catálogo/discovery | catálogo, não servidor |
| Figma | Figma | OPTIONAL / OFFICIAL | design/frames/tokens | registrado; conexão não validada |
| Firecrawl | Firecrawl | OPTIONAL / OFFICIAL | extração web | não validado |
| Hugging Face | Hugging Face | OPTIONAL / OFFICIAL | modelos/datasets/Spaces | não validado |
| Sentry | Sentry | OPTIONAL / OFFICIAL | erros da aplicação | não validado |
| Supabase | Supabase | PROJECT_SPECIFIC / OFFICIAL | backend do projeto | não validado |
| grep-mcp | maintainer declarado por PyPI | COMMUNITY / UNKNOWN | pesquisa pública | registrado; origem não verificada, instalação bloqueada |
| node_repl | host atual | RUNTIME_PROVIDED / UNKNOWN | JavaScript do host | não validado; nunca instalar como servidor externo |

RECOMMENDED, OPTIONAL e PROJECT_SPECIFIC continuam opcionais, sem aprovação
implícita. Docker não é obrigatório. Auditoria das fontes em mcp-source-audit.md.

### Custom MCP Support

Intake local valida identidade, fonte, documentação, capacidades, instalação,
transporte, permissões, auth e riscos. Metadata privada participa do catálogo
efetivo e resolução `--require`; conexão/auth só por evidência recente do host.
Setup custom é MANUAL_ONLY, sem executar texto arbitrário. Sem promoção automática
ao catálogo público. Preferências e ofertas não solicitadas persistem sem repetir
perguntas a cada sessão.

### Specialist Tools

| Skill | Registered Tools | Installed | Missing | Broken confirmado |
| --- | --- | --- | --- | --- |
| dev-implementation-standard | 6 | python-unittest | pytest, pytest-cov, hypothesis, ruff, mypy | 0 |
| security-standard | 6 | 0 detectadas | semgrep, trivy, gitleaks, zap, bandit, pip-audit | 0 |
| ui-ux-standard | 1 | 0 detectadas | playwright CLI local | 0 |
| environment, workflow, sdd, parceiro global | sem registry | N/A | N/A | 0 |

"Missing" significa não detectada no workspace/PATH desta execução, não ausência
em todos os ambientes da máquina. Playwright MCP não comprova CLI local disponível.

### Environment / Plugin Health

- Runtimes detectados: Git 2.43.0, Python 3.12.3, Node 22.22.2.
- Managers disponíveis por resolução: npm, npx, pip, pnpm, uv; pipx/yarn ausentes.
- Nenhum lockfile de dependências do projeto foi encontrado; deps NOT VALIDATED.
- Chrome/Firefox encontrados no PATH; Chromium/WebKit em cache sem launch validado.
- Doctor real: DEGRADED, zero bloqueios estruturais. Sem importar evidência,
  tests-and-validators é NOT VALIDATED mesmo tendo executado a suíte separadamente.
- Status com snapshot: refresh_required=false, ready=false, sem discovery completo.
  Faltam evidências CORE/conexão/auth e validação importada para READY total.

### Installations / Authentication Required

Nenhuma instalação real de MCP, scanner, runtime, browser ou dependência.
Smoke prepare sem approvals gravou somente observações locais privadas e cache
do helper; nenhuma ação de instalação/configuração executada. Config global
preservada. Nenhuma pendência de auth confirmada por desafio real: auth não
testada, não inferida do catálogo nem da autenticação `gh`.

### Tests / Execution Receipt

Comandos a partir da raiz; `ENVCLI` abaixo abrevia
`plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py`.
Smoke usou `--repo-root . --workspace . --host codex --state-dir <temporário> --json`.

| Command | Exit code | Result |
| --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q` | 0 | 391 PASS, baseline 318; 62 environment e 24 helper |
| `python3 .../plugin-creator/scripts/validate_plugin.py plugins/dev-environment-standard` | 0 | Plugin validation passed |
| `python3 .../skill-creator/scripts/quick_validate.py plugins/dev-environment-standard/skills/dev-environment-standard` | 0 | Skill is valid |
| `git diff --check` | 0 | sem erros |
| `python3 ENVCLI doctor` + flags acima | 0 | DEGRADED, zero blockers, sem escrita |
| `python3 ENVCLI prepare --dry-run` + flags | 0 | plano sem execução e sem escrita |
| `python3 ENVCLI status` antes de prepare | 0 | ready=false, refresh_required=true; sem escrita |
| `python3 ENVCLI prepare` sem approvals | 0 | zero ações executadas, estado local persistido |
| `python3 ENVCLI status` após prepare | 0 | ready=false, refresh_required=false; sem escrita |

Casos `test_01` a `test_30` mapeiam critérios numerados; mais 32 regressões.
Fixtures testam configuração Claude/Codex, subprocesses aprovados, repair seletivo,
cache, expiração, consentimento, credentials, falhas e recuperação externa.
Smoke comparou hashes de estado/config nos três fluxos read-only.

### Security Review

SECURITY_STATUS=PASS para revisão humana, risk HIGH pelo limite instalação/config.
Reviewer independente leu security-standard e referências, executou 61 testes
environment +24 helper, reproduziu entradas de segredo e retries genéricos.
A suíte consolidada do Harness inclui o 62º caso de recuperação externa.

Falhas corrigidas: snapshot vencido liberando READY; origem/política descartada;
credenciais CLI/Basic; consentimento COMMUNITY truthy; Chrome privilegiado;
fingerprint incompleto; pendências apagadas por prepare subsequente.
Banco: N/A. API/Backend/JSON/processos revisados. Frontend/UI: N/A.

### README / Git / Remaining Risks

README atualizado antes do commit: arquitetura, quatro operações, Library/tiers,
custom/preferências, políticas, evidências, estados, health, limites e instalação.
Branch `feat/environment-bootstrap`, baseline `83e1c72`; SHA final identificado
pelo commit que inclui esta task e pelo PR. Issue continua aberta até merge.

Riscos/limites concretos: transportes/auth MCP e instaladores externos não
exercitados no host real; mocks/fixtures não substituem QA desses serviços.
Evidência importada depende da honestidade do executor autorizado, não é prova
criptográfica. Filtros de credenciais são defensivos, não reconhecem todo segredo.
Setup custom/host-specific exige handoff. Falha genérica requer reparo manual e
check identificado por component, posterior à execução; não apagar o estado todo.
Plugins foram alterados no checkout, não reinstalados nos caches globais.
Nenhum merge, deploy ou encerramento automático de Issue executado.
