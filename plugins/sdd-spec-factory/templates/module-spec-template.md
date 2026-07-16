# MODULE SPEC: Nome do módulo

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Deriva de um Product Spec. Gera page/feature specs.

## Status
Rascunho | Em revisão | Aprovada

## Product Spec relacionado
Link para o product spec pai (ou marcar `HIPÓTESE:` se ainda não existir).

## Objetivo
O que este módulo entrega dentro do produto.

## Resultado dos gates
| Gate | Status | Evidência / motivo |
| --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED | Perguntas bloqueantes ou motivo de aprovação. |
| Spec Completeness Gate | PASS/BLOCKED | Escopo, superfícies, regras e testes cobertos. |
| Security Spec Contract Gate | PASS/BLOCKED/N/A | Superfícies de risco cobertas ou motivo de N/A. |
| Traceability Gate | PASS/BLOCKED | Specs filhas ligadas a aceite. |

## Escopo incluído
Funcionalidades e telas que pertencem a este módulo.

## Fora de escopo
O que não pertence a este módulo.

## Páginas/telas previstas
Lista de páginas/features que derivam deste módulo (cada uma vira page-spec).

## Mapa de superfícies do módulo
| Superfície | Tipo | Risco | Specs filhas | Owner | Status |
| --- | --- | --- | --- | --- | --- |
|  | UI/API/Banco/job/webhook/integração | baixo/médio/alto/crítico |  |  | pendente/revisado/bloqueado |

## Componentes compartilhados
Componentes reutilizados em várias telas (cada um vira component-spec).

## Regras de negócio do módulo
Regras transversais ao módulo (detalhes em validation-rules-spec).

## Banco
Impacto no modelo de dados. Detalhe em database-spec. `N/A` + motivo se não houver.

## API/Backend
Serviços/endpoints do módulo. Detalhe em api-spec. `N/A` + motivo se não houver.

## Frontend/UI
Padrões de UI do módulo, design system e mockups aprovados a seguir.

## Testes
O que precisa de cobertura no nível do módulo.

## Segurança
Authz/authn, limites de tenant, dados sensíveis (validar com security-standard).

## Matriz de papéis e permissões
| Papel | Pode acessar | Pode criar | Pode alterar | Pode excluir | Pode exportar | Observações |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Observabilidade/logs
Eventos, métricas e auditoria esperados.

## Dependências
Outros módulos, integrações ou serviços.

## Riscos
Riscos técnicos, de dados e de regressão.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Critérios objetivos e testáveis do módulo.

## Matriz de rastreabilidade
| Objetivo/requisito | Spec filha | Task esperada | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Hipóteses
Liste explicitamente cada suposição (`HIPÓTESE:`).
