# TASK-009: Sector Validation Matrix, Context Routing e QA

## Audit Summary

Data: 2026-09-24. Fonte canônica: checkout Dev-workflow. Estado inicial:
`feat/security-lifecycle`, HEAD `b10b46e0a6fc7c767d8931bcf8470a802fa86446`, limpo.
Fetch e pull fast-forward com URL HTTPS aplicada somente ao comando confirmaram
`origin/main` em `59e627519b83c0ec30d16c81dbeebd788b5e0b19`. Nova branch
`feat/sector-context-qa` parte dessa main. Commits anteriores Security e UI
permanecem em branches separadas, sem merge implícito nem perda de trabalho.

Baseline: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`,
441 testes, exit 0, 9.908s. Não havia QA dedicado equivalente no catálogo/skills.
Já existiam template QA, v1 Execution Contract, receipts, handoff seletivo e
owners de ferramentas. Não foi encontrado parser runtime do Execution Contract;
parsers de estado Environment não cumprem essa função.

Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28.
RUNNING publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818418747.
Nenhum Project vinculado na consulta; não foi escolhido board arbitrário.

## Consolidated Practice Check

Fontes primárias verificadas em 2026-09-24:

| Mudança | Classificação | Base e aplicação |
| --- | --- | --- |
| Contexto just-in-time por identificadores/paths | OFFICIAL PRACTICE do fornecedor, não padrão universal | [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): suporte à leitura sob demanda |
| Testar comportamento observável e isolar testes | OFFICIAL PRACTICE da ferramenta | [Playwright](https://playwright.dev/docs/best-practices): referência para QA, não adoção obrigatória de E2E |
| Investigar falha intermitente, estado e isolamento | OFFICIAL PRACTICE da ferramenta | [pytest](https://docs.pytest.org/en/stable/explanation/flaky.html): falha não prova automaticamente bug do produto |
| Reprodução, regressão e teste proporcional | ECOSYSTEM CONVENTION | Usar menor nível que prove o comportamento |
| QA independente, v1 aditivo e aceite humano | PROJECT CHOICE | Fronteiras explícitas deste repositório |
| Matriz, campos de routing e extensões dos receipts | LOCAL EXTENSION | Não atribuir schema/nomenclatura à OpenAI ou outro fornecedor |

## Task Architecture

Antes: Task humana com camadas e QA genérico; fontes flat no JSON; handoff por
paths, mas sem setor ou propósito por fonte. Depois: Task é painel completo com
matriz e ledger; JSON é índice setorial, specs mantêm detalhes, receipt prova
execução. Harness lê o todo; cada especialista lê a menor fatia completa.

## Sector Validation Matrix

Dez IDs: database, backend, frontend, ui_ux, qa, security, devops,
observability, documentation, harness. Cada um tem owner e REQUIRED/N/A.
N/A mantém motivo curto e pode ficar somente na matriz. Domínio material pode
estender a lista, como governance nesta mudança de metodologia.
Estado e evidência ficam na Task. PASS é resultado que permite COMPLETED
somente com evidência do owner; não é nova máquina de estados.

## Context Routing

Contrato v1: `sectors`, `global_acceptance_refs` opcionais. Setor: owner,
applicability, depends_on, task_sections, required_sources, conditional_sources,
required_validations; N/A adiciona reason. OPTIONAL é sob demanda.
Fonte REQUIRED tem path/purpose; CONDITIONAL acrescenta condition.

Handoff leva task_id, execution_contract_path, sector, phase, revisão e receipts
materiais. SKILL.md ativo é lido inteiro; Task inteira não é obrigatória para
todo especialista. Global constraints e critérios relevantes continuam valendo.
Fonte ausente/conflito/condição material desconhecida bloqueia o claim.
Pedido de expansão usa motivo, fonte necessária e claim bloqueado.

`depends_on` rege validação final; `planning_depends_on` rege planejamento.
Planejamento não encerra validação. Receipts devem corresponder ao owner, escopo
e revisão, com revalidação após mudança material. Não há roteador executável ou
enforcement automático novo: o protocolo orienta agentes e é revisado/testado.

## Human Task Example

Exemplo completo: [TASK-EXAMPLE](examples/sector-context-qa/TASK-EXAMPLE.md),
com [spec sintética](examples/sector-context-qa/feature-spec.md).
A Task real é [TASK-009](tasks/TASK-009-sector-context-qa.md).
Exemplos sintéticos não serão registrados como implementação de aplicação.

## Execution Contract Example

Contrato real: [TASK-009.json](execution/TASK-009.json). Não armazena specs,
checklists inteiros, logs, status de execução ou estado de instalação.
O [contrato do exemplo](examples/sector-context-qa/execution-contract.json)
corresponde aos anchors/owners da Task ilustrativa, sem autorizar produto real.

## QA Architecture

Novo owner: qa-testing-standard, porque a auditoria não encontrou equivalente.
Implementation escreve produto/TDD/testes de desenvolvimento e corrige;
QA planeja estratégia, reproduz, explora comportamento e verifica correção;
UI valida experiência/design; Security valida vulnerabilidade/abuso;
DevOps valida operação; Environment prepara capacidades; Harness reconcilia.
QA não substitui esses owners nem marca seus setores PASS.

## QA Workflow

Planning define guardrails/casos/regressões. Reproduction exige esperado/atual,
ambiente, revisão, reprodução e evidência antes de CONFIRMED_BUG. Validation
executa casos aplicáveis; Regression seleciona os alvos relevantes;
Fix Verification retesta a correção feita por Implementation. Sem reprodução,
NOT_REPRODUCED, não causa ou correção inventada. Candidato de segurança é
encaminhado a Security, não publicado por QA como vulnerabilidade.

QA_STATUS: PASS, PARTIAL, BLOCKED, NOT_VALIDATED. Falha é classificada entre
PRODUCT_BUG, TEST_BUG, ENVIRONMENT_FAILURE, FLAKY_TEST e TOOL_FAILURE.
PASS não significa software sem bugs nem dispensa aceite humano.

## Capability Integration

Registry do Harness resolve functional QA / test engineering para
qa-testing-standard sem fallback silencioso ao implementador. REQUIRED quando
há comportamento/bugfix/fluxo/API/regra/estado/integração material; N/A motivado
para docs/metadata sem impacto funcional. Nesta mudança, a metodologia do agente
tem impacto comportamental: QA da metodologia é REQUIRED, runtime de app é N/A.

## Tool Ownership

pytest, pytest-cov, Hypothesis e python-unittest permanecem com Implementation;
Playwright com UI. QA pode consumir capabilities compartilhadas e interpretar
comportamento funcional sem copiar registries. Environment já descobre skills
sem registry, portanto nenhum novo registry, CLI ou instalador foi necessário.
SWE-bench, Defects4J e BugsInPy foram considerados referências opcionais; sem
consumidor concreto nesta entrega, não há registry nem download desses datasets.

## Scenario Tests

[Revisão independente completa](qa/TASK-009-review.md): S01–S10 PASS procedural,
com resultado individual e evidência. H01 revisão desatualizada, H02 owner errado
e H03 condição desconhecida produziram as decisões de bloqueio esperadas.
S01–S10 foram informados; H01–H03 não receberam resposta esperada. Nenhum deles
é benchmark de agentes ou execução de aplicação real.

## Context Economy

Antes, referências flat podiam induzir repetição da Task e specs não pertinentes.
Depois, o especialista recebe contrato, seção própria, critérios relevantes,
fontes REQUIRED/condicionais ativadas, código e receipts materiais. Security não
carrega docs UI/QA/DevOps sem motivo. Harness reavalia a visão global quando o
contrato muda, não mantém uma leitura antiga como autoridade eterna.
Não medimos tokens nem latência; nenhuma porcentagem de economia é alegada.

## Migration / Compatibility

| Responsabilidade anterior | Nova localização |
| --- | --- |
| QA genérico no SDD | Setor QA + especialista; demais gates retêm seus owners |
| Required skills/specs/docs flat | Preservados para v1, routing setorial nas novas Tasks |
| Camadas Banco/API/UI | Matriz explícita, seções detalhadas só para REQUIRED |
| Handoff de arquivos amplos | Identificadores, setor/fase, revisão e receipts pertinentes |
| Progresso/resultado | Ledger da Task e receipts existentes, nunca no JSON |

Sem setores, contrato legado continua válido. Retomada normaliza apenas quando
necessário; nenhum histórico foi migrado. Consumidor antigo que ignora campos
novos não comprova routing. Atualização de fonte não atualiza caches instalados;
revalidar suporte no host antes de depender da nova garantia.

## Tests

Baseline: 441 testes. Validação integrada: **490 testes PASS**, exit 0,
14.469s no Harness e 15.362s na execução independente de QA.
Reexecução final após consolidar receipts: 490 PASS, 9.731s, exit 0.
Todos os 45 arquivos conferidos contra allowed_paths, paths protegidos
preservados e JSONs alterados parseáveis: PASS.

| Verificação executada pelo Harness | Resultado |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q` | 490 PASS, exit 0 |
| `git diff --check` | PASS, exit 0 |
| System plugin-creator `validate_plugin.py plugins/qa-testing-standard` | PASS, exit 0 |
| System skill-creator `quick_validate.py` para QA, Harness, SDD, Implementation, UI, Security e DevOps | Sete PASS, exit 0 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_dev_implementation_skill.py -q` | 70 PASS, exit 0 |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_readme.py -q` | 32 PASS, exit 0 |
| `python3 plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py doctor --repo-root . --workspace . --json` | Inicial exit 2, faltava agents/openai.yaml QA; após correção exit 0, blockers=[], dez checks QA PASS |

O doctor permanece DEGRADED para saúde geral sem comprovação de todo o runtime;
não foi convertido artificialmente em HEALTHY. QA corretamente aparece sem
registry próprio. Operação read-only, nenhuma instalação/configuração aplicada.
O autor acrescentou teste de regressão do metadata, observou RED e depois GREEN.
Na integração, um teste legado esperava conclusão da Task pelo implementador;
foi atualizado para exigir conclusão somente do setor e reconciliação pelo
Harness. Não se removeu exigência de evidência para obter verde.
Uma rodada intermediária executou 489 testes e falhou em 13 asserts legados
do Harness sobre template duplicado/leitura integral da Task. Os asserts foram
adaptados à fonte SDD canônica e ao routing setorial, mantendo as exigências.
O bundle QA teve RED/GREEN estrutural; alterações documentais de integração
não são apresentadas como TDD de comportamento runtime.
R01 metadata, R02 gate circular entre checkpoints e R03 fonte obrigatória
classificada como opcional foram corrigidos e retestados independentemente.

## README / Workflow

README registra setores, fontes, compatibilidade, QA/boundaries e instalação;
pipeline registra matrix → routing → especialistas → reconciliation → gates.
A skill readme orientou documentação operacional e limites, sem inventar
stack/deploy de aplicação para um repositório de plugins.

## Git

Branch feat/sector-context-qa, base 59e6275; gate local PASS para commit desta
entrega. O SHA final é confirmado após o commit, não embutido no próprio commit.
Sem push, PR, merge, deploy ou atualização de plugin instalado nesta entrega.

## Remaining Risks

Conformidade de agentes futuros exige receipts/revisão; testes estruturais não
são firewall de execução. Exemplos não comprovam QA de aplicação real. Caches
globais permanecem inalterados. Branches locais Security/UI precisam de decisão
separada de publicação/integração; mudanças sobrepostas exigirão review de merge.

## Receipts and minimal change

SKILL_RECEIPT do Harness: skills canônicas Harness, SDD, Implementation, UI,
Security, DevOps, Environment; referências obrigatórias de execução, capacidade,
skill contract, tools, minimal gate, handoff e comentários lidas; templates SDD
e relatório lidos. System skill-creator, plugin-creator e readme lidas por inteiro.
QA e suas duas referências lidas após criação; referência openai_yaml e skill
TDD lidas para a validação/correção de metadata. Não foi escrito runtime novo.
Aplicação: scope por owner, contexto proporcional, gates/evidência, pacote local.

REUSE_INVENTORY: templates v1, receipts, estados, registries e Environment
reutilizados. CREATE apenas bundle QA, referências de routing/QA, exemplos e
testes exigidos. MINIMAL_CODE_GATE: sem novo runtime/parser/policy engine.
MINIMAL_CODE_GATE: PASS. Sem parser, engine, receipt, registry ou instalador novo.

### EXECUTION_RECEIPT: governance
- owner: dev-implementation-standard; executores: qa_bundle, security_sources e root.
- sector: governance; phase: implementation; state: COMPLETED; result: PASS.
- inputs_used: spec aprovada, validation-rules, contrato, skills/templates canônicos.
- outputs_produced: bundle QA, routing, templates, boundaries e testes.
- invocation_evidence: delegações com paths exclusivos e retornos dos autores;
  QA bundle 21 testes, routing 27, Harness 103 e contracts 6 PASS.
- validation_evidence: suíte integrada e validators acima; revisão QA independente.
- revision: worktree desta branch sobre 59e6275; fingerprints no relatório QA.
- blockers: none; runtime de aplicação não executado.

### EXECUTION_RECEIPT: documentation
- owner: dev-implementation-standard; executor: root; sector: documentation.
- phase: implementation; state: COMPLETED; result: PASS.
- inputs_used: spec, README, pipeline, marketplaces e exemplos.
- outputs_produced: README, pipeline, relatório, Task e fronteiras de integração.
- validation_evidence: revisão integral de diff/exemplos, 32 testes README PASS,
  validação estrutural e revisão independente dos documentos públicos.
- blockers: none; não implica instalação da versão documentada.

### EXECUTION_RECEIPT: QA e Harness
- QA: owner qa-testing-standard, executor sector_sdd, PASS conforme
  [receipt independente](qa/TASK-009-review.md#execution_receipt). Não é autoaprovação.
- Harness: owner dev-workflow-standard, executor root, sector harness,
  phase reconciliation, state COMPLETED, result PASS no escopo local.
- inputs_used: Task completa, contrato, retornos de implementação/documentação,
  report QA independente, comandos e diff final.
- validation_evidence: todos REQUIRED reconciliados; nenhum bloqueio aberto;
  demais setores N/A justificados, não artificialmente PASS.
- outputs_produced: pacote revisável e gate para commit local.
- next_safe_action: confirmar HEAD do commit e submeter entrega ao aceite humano.

Checkpoint VALIDATING publicado:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818634646.
Checkpoint COMPLETED local publicado, Issue aberta para aceite:
https://github.com/guilhermedemorais-dev/Dev-workflow/issues/28#issuecomment-5818693644.
