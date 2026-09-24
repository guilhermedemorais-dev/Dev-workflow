# TASK-EXAMPLE: Consultar pedido com isolamento de tenant

Exemplo ilustrativo completo em PT-BR. NÃO EXECUTADO, sem aplicação neste
repositório, Issue real, PR, aprovação ou autorização de produção.

## Identidade
Status visual: A fazer. Kanban: Discovery / SDD. Tipo Feature, prioridade média.
Responsável: Harness coordena; owners na matriz. Issue/branch/PR: N/A, exemplo.
Contrato: [execution-contract.json](execution-contract.json).

<a id="global"></a>
## Objetivo, escopo e restrições
Entregar consulta de pedido via tela e adaptador API dentro do tenant autenticado.
Hipóteses: sessão e serviço tenant-aware já existem no projeto didático, conforme
[escopo da spec](feature-spec.md#scope). Confirmar antes de trabalho real.
Fora do escopo: novas queries, persistência, cadastro, alteração, deploy e cobrança.
Path `docs/examples/sector-context-qa/**` neste contrato só autoriza manter o
exemplo documental, nunca criar produto fora dele.

## Fontes globais da verdade
- REQUIRED [escopo](feature-spec.md#scope): entender hipóteses e limites.
- REQUIRED [aceite](feature-spec.md#acceptance): critérios comuns aos owners.
Detalhes ficam nas fontes; cada setor recebe só os necessários ao seu claim.

<a id="criterios-de-aceite"></a>
## Critérios de aceite
AC1: consulta legítima e erros seguem API/DTO. AC2: isolamento entre tenants
verificado no servidor. AC3: UI acessível com estados revisados. AC4: QA executa
cenários e regressões. AC5: docs coerentes e gates reconciliados com evidência.

## Matriz de Validação por Setor
| Setor / ID | Aplicável | Owner | Status | Dependências finais / motivo |
| --- | --- | --- | --- | --- |
| Banco / database | N/A | dev-implementation-standard | N/A | Serviço/query/persistência existentes inalterados, não só ausência de migração |
| API / Backend / backend | REQUIRED | dev-implementation-standard | PENDING | nenhum setor final |
| Frontend / frontend | REQUIRED | dev-implementation-standard | PENDING | backend |
| UI / UX / ui_ux | REQUIRED | ui-ux-standard | PENDING | frontend |
| QA / Testes / qa | REQUIRED | qa-testing-standard | PENDING | backend, frontend |
| Segurança / security | REQUIRED | security-standard | PENDING | backend |
| DevOps / devops | N/A | devops-standard | N/A | Sem alteração CI/runtime/deploy |
| Observabilidade / observability | N/A | devops-standard | N/A | Nenhuma nova telemetria operacional requerida |
| Documentação / documentation | REQUIRED | dev-implementation-standard | PENDING | backend, frontend |
| Gate Final / harness | REQUIRED | dev-workflow-standard | PENDING | backend, frontend, ui_ux, qa, security, documentation |

<a id="backend"></a>
## API / Backend
Owner dev-implementation-standard, status PENDING; final depende de nenhum setor.
Objetivo: adaptador com autorização/DTO sobre serviço didático existente.
- REQUIRED [API](feature-spec.md#api): contrato/erros e boundary servidor.
- REQUIRED [Security](feature-spec.md#security): preservar isolamento.
- CONDITIONAL [persistência](feature-spec.md#persistence): se query ou contrato de
  persistência mudar, conferir invariantes e solicitar revisão do escopo ao Harness.
Fazer: verificar hipótese do serviço; implementar adaptador e testes no projeto
real somente depois de autorização, sem modificar query.
Evidência esperada: diff e unit/integration negativos na revisão entregue.
Resultado: NOT_VALIDATED, nenhum produto/teste executado.

<a id="frontend"></a>
## Frontend
Owner dev-implementation-standard; PENDING; final depende de backend.
Objetivo: formulário e estados sem duplo envio.
- REQUIRED [UI](feature-spec.md#ui): estados e interação.
- REQUIRED [API](feature-spec.md#api): consumo do contrato/erros.
Fazer: implementar integração e testes de estado no projeto real autorizado.
Evidência esperada: diff/testes e artefato renderizável.
Resultado: NOT_VALIDATED. Fontes condicionais: nenhuma identificada.

<a id="ui_ux"></a>
## UI / UX
Owner ui-ux-standard; PENDING; final depende de frontend; planning sem dependência
de conclusão de setor, mas exige escopo e direção aprovados antes de implementar.
Objetivo: direção visual e validação de estados, foco, responsividade e acesso.
- REQUIRED [UI](feature-spec.md#ui): orientar e verificar interface.
Fazer: planning visual; após implementação, revisar renderização real.
Evidência esperada: revisão visual por estado/viewport e receipt do owner.
Resultado: NOT_VALIDATED. Fontes condicionais: nenhuma identificada.

<a id="qa"></a>
## QA / Testes
Owner qa-testing-standard; PENDING; final depende de backend e frontend;
planning sem dependências de conclusão, mantendo fontes e critérios obrigatórios.
Objetivo: verificar comportamento independentemente do implementador.
- REQUIRED [QA](feature-spec.md#qa): casos e regressões.
- REQUIRED [API](feature-spec.md#api): esperado para erro/sucesso.
Fazer: QA_GUARDRAILS para retry/duplo envio; TEST_SCENARIOS para AC1/AC4;
REGRESSION_TARGETS consulta/envio único; VALIDATION_REQUIREMENTS integração e UI
funcional. Reproduzir bug, devolver REWORK à Implementation e retestar correção.
Evidência esperada: revisão/build, passos/comandos, esperado/observado, bugs e
disposição, regressão e QA_STATUS no EXECUTION_RECEIPT existente.
Resultado: NOT_VALIDATED. Fontes condicionais: nenhuma identificada.

<a id="security"></a>
## Segurança
Owner security-standard; PENDING; final depende de backend; planning sem
dependência de conclusão. Objetivo: validar isolamento e privacidade.
- REQUIRED [Security](feature-spec.md#security): controles e contraprovas.
- REQUIRED [API](feature-spec.md#api): traçar contexto servidor até efeito.
Fazer: guardrails no planning, review/negativos na validation. Receber candidato
de QA e validar pelo evidence contract; não inferir CONFIRMED do relato isolado.
Evidência esperada: revisão exata, path/mitigações/testes e SECURITY_STATUS.
Resultado: NOT_VALIDATED. Sem carregar UI/QA/DevOps docs por padrão.
- OPTIONAL [UI](feature-spec.md#ui): consultar somente se o tracing exigir
  entender entrada/controle de navegador além do escopo API, registrando motivo.

<a id="documentation"></a>
## Documentação
Owner dev-implementation-standard; PENDING; final depende de backend/frontend.
Objetivo: registrar comportamento/limites sem divulgar candidatos sensíveis.
- REQUIRED [spec](feature-spec.md): alinhar instruções com escopo e contrato.
Fazer: atualizar instruções após evidência, linkar receipts e limitações.
Evidência esperada: diff documental e revisão de links/contratos.
Resultado: NOT_VALIDATED. Fontes condicionais: nenhuma identificada.

<a id="harness"></a>
## Gate Final do Harness
Owner dev-workflow-standard; PENDING; depende de todos os outros REQUIRED.
Fonte REQUIRED: Task completa e contrato para reconciliação, não replicados JSON.
Fazer: conferir AC1–AC5, aplicabilidade, dependências, receipts atuais, PR/docs.
Evidência esperada: registro do resultado de cada owner; nenhuma atribuição de
PASS por outro setor. Resultado NOT_VALIDATED até validação real.

## Ordem de Execução
Planning UI/QA/Security pode começar com escopo resolvido. Backend precede
Frontend e validação Security; Frontend precede UI final; Backend+Frontend
precedem QA final e docs. Harness fecha depois de todos REQUIRED.
Conclusão de planning nunca é evidência de validation concluída.

## Registro de Evidências
Vazio intencionalmente: nenhum SKILL_RECEIPT ou EXECUTION_RECEIPT fictício.
Resultados de todos REQUIRED: NOT_VALIDATED. Campos futuros: setor, fase,
owner, revisão/artefato, fontes carregadas, comando/resultado, receipt, limites.

## Gate do PR e Aceite Humano
PR não criado. Exigir revisão/Task/specs/receipts consistentes; humanos decidem
aceite e autorização de release. Este exemplo não concede nenhuma autorização.

## Riscos e Condições de parada
Hipóteses não verificadas, mandatory_reference_missing, source_of_truth_conflict,
mudança de query/arquitetura/escopo ou dependência final sem evidência interrompem
o checkpoint. Revisão nova exige reavaliar receipts e retestar impacto material.

## Prompt para o especialista
TASK-EXAMPLE, contrato `docs/examples/sector-context-qa/execution-contract.json`,
setor/fase/revisão do handoff. Execute apenas se autorizado no projeto-alvo.
