# SPEC: Nome da página/tela

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Deriva de um Module Spec. Referencia component specs.

## Objetivo
O que esta página/tela permite que o usuário faça.

## Usuário alvo
Quem usa esta tela e em que contexto/permissão.

## Fluxo principal
Passo a passo do caminho feliz.

## Resultado dos gates
| Gate | Status | Evidência / motivo |
| --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED | Perguntas bloqueantes ou motivo de aprovação. |
| Spec Completeness Gate | PASS/BLOCKED | Campos obrigatórios cobertos. |
| UI Interaction Contract Gate | PASS/BLOCKED/N/A | Matriz abaixo completa ou motivo de N/A. |
| Backend Contract Gate | PASS/BLOCKED/N/A | API/job/webhook especificado ou motivo de N/A. |
| Security Spec Contract Gate | PASS/BLOCKED/N/A | Superfícies e controles cobertos ou motivo de N/A. |
| Traceability Gate | PASS/BLOCKED | Requisitos ligados a testes e aceite. |

## Layout esperado
Estrutura visual macro. Referenciar mockup aprovado (ui-ux-standard), não inventar.

## Componentes obrigatórios
Lista de componentes usados (cada um deve ter component-spec).

## Matriz de interações da tela
Obrigatória para toda tela com ação do usuário. Incluir botões, links, menus,
tabs, filtros, campos, uploads, modais, cards clicáveis, ações de tabela,
paginação, bulk actions, empty-state CTAs, retry e confirmações destrutivas.

| ID | Elemento/ação | Visível para | Habilitado quando | Entrada/payload | Chama API/serviço | Sucesso | Loading/processando | Erro/forbidden | Toast/feedback | Navegação/efeito | Teste/evidência |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UI-01 |  |  |  |  |  |  |  |  |  |  |  |

## Estados da tela
Loading, vazio, com dados, erro, sem permissão, sucesso.

## Estados por permissão
| Papel/permissão | Pode ver | Pode criar | Pode editar | Pode excluir | Pode exportar | Restrições |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Regras de negócio
Regras que se aplicam nesta tela (detalhe em validation-rules-spec).

## Validações
Validações de entrada e de fluxo nesta tela.

## Navegação
De onde se chega, para onde vai, parâmetros e deep links.

## Banco
Dados lidos/gravados por esta tela. `N/A` + motivo se não houver.

## API/Backend
Endpoints consumidos, contratos e erros tratados. `N/A` + motivo se não houver.

## Dados e estado
Fonte de dados, cache, invalidação, atualização otimista/pessimista,
sincronização, concorrência e comportamento quando dados mudam enquanto a tela
está aberta.

## Frontend/UI
Comportamento de UI, responsividade e acessibilidade (detalhar com ui-ux-standard).

## Segurança
Permissões necessárias, dados sensíveis exibidos, limites de acesso.

## Contrato de segurança da tela
| Superfície | Ator/risco | Controle obrigatório | Teste negativo/evidência | Bloqueia release? |
| --- | --- | --- | --- | --- |
|  |  |  |  | sim/não |

## Observabilidade/logs
Eventos de uso, métricas e erros que devem ser registrados.

## Critérios de aceite
Critérios objetivos e testáveis da tela.

## Matriz de rastreabilidade
| Requisito/RN/mockup | Interação/entry point | Banco/API/Frontend | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Fora do escopo
O que esta tela explicitamente não cobre.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).
