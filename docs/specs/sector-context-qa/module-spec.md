# MODULE SPEC: Contexto por setor e QA independente

## Status
Aprovada pelo Engineering Harness em 2026-09-24, derivada do pedido explícito do usuário.

## Product Spec relacionado
Intenção de produto existente: [README](../../../README.md), [pipeline](../../workflow-pipeline.md)
e pedido do usuário, seções 1–76. Este módulo evolui o Harness, não cria aplicação.
Page/component specs: N/A, não há telas nem componentes de produto.

## Objetivo
Human Task mostra o todo; Execution Contract roteia contexto; especialistas
executam somente seu setor; Harness reconcilia evidências. Adicionar QA funcional
independente sem absorver Implementation, Security, UI/UX ou DevOps.

## Diagnóstico
- Claro: matriz com dez setores, fontes com propósito, owners exclusivos e QA independente.
- Verificado em `59e6275`: task/contract/templates e receipts existem; QA dedicado não foi
  encontrado em `plugins`; QA genérico está distribuído nas referências e templates.
- `tests/test_execution_contract.py` verifica contratos v1; não foi encontrado parser
  runtime de Execution Contract. Parsers de estado Environment não são esse contrato.
- Lacuna não bloqueante: redução quantitativa de tokens não foi medida.
- Perguntas críticas: nenhuma; arquitetura e escopo foram explicitamente solicitados.

## Escopo incluído
Templates Task/contract/QA/review/PR; routing/receipts/handoff do Harness; integração
SDD e boundaries dos especialistas; bundle QA nos três adaptadores e marketplaces;
testes estruturais, cenários, documentação e commit local após PASS.

## Fora de escopo
Push/PR remoto/merge/deploy; instalar plugins ou ferramentas; alterar configuração
global; scanner/policy engine/servidor/parser customizado; datasets; novos receipts;
importe automático de branches locais anteriores Security/UI; migração em massa.

## Arquitetura do contrato
Manter `schema_version: 1`: extensão aditiva opcional, não renomear/remover campos
existentes. `sectors` é um mapa por identificador estável. `global_acceptance_refs`
aponta critérios relevantes, não duplica seu texto.

Cada setor possui `owner`, `applicability` (`REQUIRED` ou `N/A`), `depends_on`,
`task_sections`, `required_sources`, `conditional_sources`, `required_validations`.
Fontes REQUIRED: `path` e `purpose`. CONDITIONAL: acrescentar `condition`.
OPTIONAL não carrega automaticamente e pode ser representada por `optional_sources`.
N/A exige `reason`, não precisa de seção detalhada. Estado, logs, receipts, segredos
e instalação nunca entram nesse índice.

`depends_on` governa validação final. Planejamento antecipado usa pré-requisitos
próprios, explicitados na Task; se necessário no JSON, `planning_depends_on`
aditivo. Não criar grafo de execução próprio nem segunda máquina de estados.
Ausência de `sectors`: v1 legado continua válido; Harness resolve contexto
proporcional e documenta a decisão ao retomar, sem migrar históricos inativos.

## Matriz e estados
Dez setores padrão: Banco, API/Backend, Frontend, UI/UX, QA/Testes, Segurança,
DevOps/Infraestrutura, Observabilidade, Documentação, Gate Final do Harness.
Extensões só para domínio material. Todo setor padrão fica visível, inclusive N/A
com motivo. Tasks triviais usam matriz compacta; não exigem dez especialistas.

Reutilizar PENDING, READY, RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
PASS é resultado com evidência, mapeado a COMPLETED; NOT_VALIDATED/PARTIAL não
concluem setor obrigatório. N/A é aplicabilidade, não sucesso. REWORK_REQUESTED
é solicitação ao owner, não mutação unilateral do resultado de outro setor.

## Context Routing
Harness lê Task completa e contrato. Handoff: task_id, execution_contract_path,
sector, revisão e receipts de dependências relevantes. Especialista lê seu SKILL
completo, seção própria, fontes obrigatórias com propósito, condicionais ativadas,
código relevante e receipts materiais. Não lê toda Task por padrão.
Fonte obrigatória ausente ou conflito com spec/código bloqueia. Contexto
insuficiente solicita expansão com motivo, fonte e claim bloqueado ao Harness.
Se fonte normativa exigir leitura adicional, disclosure não a dispensa.

## QA Architecture
Criar `qa-testing-standard` porque não há owner equivalente. Modos: Change
Validation, Scoped QA, Repository Regression Audit quando solicitado, Bug
Reproduction, Fix Verification. Escolher profundidade LOW/MEDIUM/HIGH/CRITICAL
por risco funcional e menor nível de teste que prove comportamento.
QA produz estratégia/casos/regressões, reprodução, reteste e gate funcional;
Implementation escreve/corrige produto e testes de desenvolvimento. QA não
corrige produto silenciosamente. Candidato de segurança vai a Security;
fidelidade visual vai a UI; operação/runtime vai a DevOps; Environment prepara.
QA usa owners existentes de ferramentas; nenhum registry QA vazio/duplicado.
Bases de bugs públicas são opcionais; não são evidência deste projeto nem
requisito para QA normal. Não criar registry de conhecimento sem valor atual.

## Reuse Inventory e Minimal Code Gate
EXTEND templates SDD, execution/handoff/receipt/capability do Harness, boundaries
e marketplaces. REUSE Python unittest, tool-state.py, Environment, pytest e
Hypothesis sob Implementation, Playwright sob UI. CREATE somente bundle QA,
referências proporcionais, testes e artifacts desta task, exigidos pelo pedido.
Não remover QA developer tests: sobreposição de ferramentas é deliberada,
responsabilidades de implementação e verificação independente são diferentes.
Gate de planejamento: PASS, sujeito à revisão do Harness; sem abstração especulativa.

## Practice Provenance
- [OFFICIAL PRACTICE]: somente afirmações sustentadas por documentação primária
  verificada, não atribuir matriz/receipt local a OpenAI ou outra organização.
- [ECOSYSTEM CONVENTION]: testes proporcionais ao risco, regressão, reprodução
  e progressive disclosure; fontes primárias no relatório da entrega.
- [PROJECT CHOICE]: especialistas independentes, aprovação humana, v1 aditivo.
- [LOCAL EXTENSION]: Sector Validation Matrix, Context Routing e campos exatos
  reutilizando SKILL_RECEIPT/EXECUTION_RECEIPT existentes.

## Banco
N/A: sem persistência/schema/migração de aplicação.

## API/Backend
N/A para endpoints/serviços; contratos de agente são documentação e JSON, não API.

## Frontend/UI
N/A: não há interface renderizada. UI skill recebe somente ajuste de boundary.

## Testes
38 verificações estruturais e dez cenários detalhados na
[validation-rules](validation-rules.md), suíte completa e validators de bundle.
Testes de texto/fixture não comprovam execução futura de agentes nem runtime de aplicação.

## Segurança
Preservar candidate versus finding, autorização de execução e publicação; exemplos
sintéticos. QA não confirma vulnerabilidade, não publica logs sensíveis.

## Observabilidade/logs
Reutilizar ledger humano, receipts e comentários Issue. Sem telemetria nova.

## Dependências
Templates e skills existentes; QA final depende da implementação revisável.
Planejamento QA pode anteceder implementação. Ferramenta indisponível bloqueia
somente validação que a exige, sem ser confundida com bug de produto.

## Riscos
Contexto insuficiente, ciclos de dependências, PASS cruzado, ruptura v1,
duplicação de tool owner e falsa evidência runtime. Mitigar com fontes explícitas,
revisão independente e testes negativos. Caches instalados podem continuar antigos.

## Decisões pendentes
Aceite humano final e eventual publicação/instalação, fora desta entrega local.

## Critérios de aceite
Regras RN-01–RN-12 atendidas; 38 checks e dez cenários evidenciados; documentação
atualizada; zero blocker obrigatório; commit somente após PASS local.
