# SPEC: API/Backend - Nome do recurso/serviço

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Crie apenas quando houver backend. Não invente endpoints existentes (`HIPÓTESE:`).

## Status
Rascunho | Em revisão | Aprovada

## Objetivo
O que este serviço/endpoint resolve.

## Contexto
Módulo/feature e specs relacionadas.

## Resultado dos gates
| Gate | Status | Evidência / motivo |
| --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED | Perguntas bloqueantes ou motivo de aprovação. |
| Spec Completeness Gate | PASS/BLOCKED | Contratos, erros, dados e testes cobertos. |
| Backend Contract Gate | PASS/BLOCKED | Entry points abaixo completos. |
| Security Spec Contract Gate | PASS/BLOCKED/N/A | Superfícies e controles cobertos ou motivo de N/A. |
| Traceability Gate | PASS/BLOCKED | Requisitos ligados a testes e aceite. |

## Endpoints
Para cada endpoint:

- **Método e rota:** `GET /recurso/:id`
- **Descrição:** o que faz.
- **Autenticação/Autorização:** quem pode chamar.
- **Parâmetros:** path, query, headers.
- **Request body:** schema/campos, tipos, obrigatoriedade.
- **Response:** schema de sucesso e exemplos.
- **Códigos de status:** 200/201/400/401/403/404/409/422/500 e quando ocorrem.
- **Erros:** formato de erro e mensagens.
- **Idempotência / paginação / rate limit:** quando aplicável.

## Matriz de contratos backend
Incluir endpoints, jobs, webhooks, filas, imports/exports, pagamentos,
uploads/downloads e integrações externas.

| ID | Entry point | Ator/sistema | Authz | Request/evento | Validação | Banco/efeito | Transação/idempotência | Response/erro | Logs/auditoria | Testes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BE-01 |  |  |  |  |  |  |  |  |  |  |

## Contratos e tipos
Modelos de dados de entrada/saída (DTOs).

## Contrato de erros
Formato padrão de erro, códigos, mensagens expostas ao usuário, mensagens
internas proibidas, correlação/log id e comportamento de retry.

## Regras de negócio aplicadas
Referência às RN do validation-rules-spec.

## Banco
Tabelas/coleções lidas e gravadas. Detalhe no database-spec. `N/A` + motivo.

## Integrações externas
Serviços de terceiros, webhooks, filas.

## Concorrência, consistência e idempotência
Regras para chamadas repetidas, race conditions, locks, transações, filas,
ordenação de eventos, retries, timeouts e compensação/rollback.

## Segurança
Authz/authn, validação de input, dados sensíveis, segredos (validar com security-standard).

## Contrato de segurança backend
| Superfície | Ator/abuso | Controle obrigatório | Teste negativo/evidência | Bloqueia release? |
| --- | --- | --- | --- | --- |
|  |  |  |  | sim/não |

## Observabilidade/logs
Logs, métricas, tracing e auditoria esperados.

## Testes
Casos obrigatórios: sucesso, erro, autorização, borda.

## Performance
Latência esperada, volume, caching.

## Riscos
Quebra de contrato, regressão, compatibilidade.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Critérios objetivos e testáveis do backend.

## Matriz de rastreabilidade
| Requisito/RN | Entry point | Banco/API/serviço | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
