# SPEC: Regras de contexto por setor e QA

## Status e contexto
Aprovada pelo Harness em 2026-09-24, vinculada à [module-spec](module-spec.md), TASK-009.

## Regras de negócio
- RN-01: dez setores visíveis, REQUIRED/N/A explícito, owner sempre; N/A com motivo.
- RN-02: owner só atesta seu resultado; Harness reconcilia, não fabrica PASS externo.
- RN-03: Task completa para Harness; especialistas recebem menor contexto completo.
- RN-04: REQUIRED path/purpose; CONDITIONAL path/condition/purpose; OPTIONAL sob demanda.
- RN-05: ausência REQUIRED ou source_of_truth_conflict bloqueia; expansão justificada.
- RN-06: dependências finais não bloqueiam planejamento com pré-requisitos próprios.
- RN-07: required setor incompleto, sem receipt/evidência, PARTIAL ou NOT_VALIDATED
  impede Task COMPLETED. N/A justificado não bloqueia.
- RN-08: QA independente não implementa produto nem assume outros domínios.
- RN-09: CONFIRMED_BUG exige esperado/atual/reprodução/ambiente/revisão/evidência/
  impacto/reprodutibilidade; severidade separada de confiança.
- RN-10: fix exige reteste; quando viável regressão falha antes e passa depois.
  NOT_REPRODUCED não autoriza inventar causa/correção. ACCEPTED/DEFERRED requerem
  decisão autorizada registrada, não equivalem a FIXED.
- RN-11: TOOL_FAILURE, ENVIRONMENT_FAILURE, TEST_BUG e FLAKY_TEST não são
  automaticamente PRODUCT_BUG. QA PASS exige escopo obrigatório executado.
- RN-12: compatibilidade v1, nenhuma tool duplicada, nenhuma máquina de estados,
  receipt paralelo, instalação/global state ou policy engine novo.

## Validação de entrada e camada de aplicação
Verificar JSON válido, campos antigos preservados, ids de setor únicos, owners
resolvíveis, referências existentes, dependencies conhecidas sem autociclo/ciclo,
motivos N/A e fontes com propósito/condição. Execução via checks estruturais
de teste e revisão do executor/Harness; não criar validador runtime genérico.
Banco: N/A, sem constraints. API/Backend: N/A, sem endpoint. Frontend/UI: N/A,
sem formulário. Mensagens: usar stop conditions existentes e motivo acionável.

## Testes estruturais obrigatórios
IDs correspondem às seções 67–68 do pedido. Cada teste deve apontar evidência,
não apenas declarar que foi planejado.

| ID | O que provar |
| --- | --- |
| T01 | Task template contém Sector Validation Matrix |
| T02 | REQUIRED/N/A explícitos e motivo para N/A |
| T03 | owner em cada setor |
| T04 | dependencies suportadas |
| T05 | REQUIRED source com purpose |
| T06 | CONDITIONAL source com condition e purpose |
| T07 | contrato roteia setores |
| T08 | contrato permanece índice enxuto |
| T09 | sem corpos de specs/checklists no JSON |
| T10 | Harness compreende visão global |
| T11 | especialista não lê Task inteira por padrão |
| T12 | handoff resolve task sections |
| T13 | handoff resolve required sources |
| T14 | OPTIONAL não carrega automaticamente |
| T15 | CONDITIONAL respeita condição |
| T16 | owner não marca outro setor PASS |
| T17 | todo REQUIRED precisa fechar com evidência |
| T18 | N/A justificado não bloqueia |
| T19 | fonte REQUIRED ausente bloqueia |
| T20 | source_of_truth_conflict bloqueia |
| T21 | receipts existentes continuam obrigatórios |
| T22 | README coerente com nova arquitetura |
| T23 | QA dedicado existe sem equivalente duplicado |
| T24 | registry resolve functional QA / test engineering |
| T25 | QA não escreve produto |
| T26 | QA solicita REWORK ao owner |
| T27 | QA não substitui Security |
| T28 | QA não substitui UI |
| T29 | QA não substitui DevOps |
| T30 | test failure não confirma product bug |
| T31 | bug reproduction suportado |
| T32 | fix verification suportado |
| T33 | regression validation suportada |
| T34 | QA_STATUS PASS/PARTIAL/BLOCKED/NOT_VALIDATED |
| T35 | execução ausente nunca PASS |
| T36 | bug confirmado tem reprodução e evidência |
| T37 | bugfix relevante exige reteste |
| T38 | QA planning produz cenários antes da implementação |

## Cenários e casos de borda
| ID | Entrada | Resultado esperado |
| --- | --- | --- |
| S01 | Docs-only | Docs e Harness REQUIRED; demais oito N/A com motivo; sem especialistas irrelevantes |
| S02 | Botão visual sem mudança funcional | Frontend/UI REQUIRED; QA proporcional ou N/A motivado; Security/DevOps N/A |
| S03 | Cadastro | Frontend/UI/QA REQUIRED; Backend se API; Security conforme dados/auth; fontes QA relevantes |
| S04 | Duplo envio | QA reproduz/confirma; Implementation corrige + regressão; QA retesta antes de PASS |
| S05 | Endpoint multi-tenant | Backend/QA/Security REQUIRED, comportamento versus exploração separados |
| S06 | QA encontra cross-tenant | SECURITY_CANDIDATE para Security; QA não decide CVE/severidade de segurança |
| S07 | Frontend completo, Backend PENDING | QA final dependente dos dois não PASS; planning pode continuar |
| S08 | Tool QA falha | TOOL_FAILURE, sem PRODUCT_BUG automático nem PASS obrigatório |
| S09 | Handoff Security | Contrato/seção/fontes Security + receipt/código backend relevante; não UI/QA/DevOps sem motivo |
| S10 | Fonte de persistência condicional | Spec Banco só carrega se mudança de persistência ocorrer |

Acrescentar casos negativos para fonte ausente, dependência desconhecida/cíclica,
N/A sem motivo e v1 legado sem sectors; testes não devem criar engine paralelo.
Registrar se cenários foram review informado ou avaliação cega; não inventar
runtime nem porcentagem de economia de tokens.

## Segurança
Dados sintéticos; receipts sem segredos. Security classifica candidato próprio.

## Observabilidade/logs
Ledger aponta comando/exit code/resultado/artefato; output grande não entra no contrato.

## Riscos
Testes de strings são cobertura estrutural, não prova de enforcement automático.

## Decisões pendentes
Aceite humano final, publicação e instalação não autorizadas neste escopo.

## Critérios de aceite
T01–T38 e S01–S10 com resultado observado; suíte baseline sem regressão;
revisão independente e final gate do Harness sem REQUIRED pendente.
