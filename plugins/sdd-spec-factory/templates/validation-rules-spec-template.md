# SPEC: Regras de validação e de negócio

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Centraliza regras transversais referenciadas por page/component specs.

## Status
Rascunho | Em revisão | Aprovada

## Contexto
Módulo/tela/feature ao qual estas regras se aplicam.

## Resultado dos gates
| Gate | Status | Evidência / motivo |
| --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED | Perguntas bloqueantes ou motivo de aprovação. |
| Spec Completeness Gate | PASS/BLOCKED | Regras, camadas, mensagens e testes cobertos. |
| Security Spec Contract Gate | PASS/BLOCKED/N/A | Regras de autorização/privacidade cobertas ou motivo de N/A. |
| Traceability Gate | PASS/BLOCKED | Regras ligadas a testes e aceite. |

## Regras de negócio
Lista numerada. Para cada regra:

- **RN-XX:** descrição clara da regra.
  - Condição / gatilho.
  - Resultado esperado.
  - Exceções.

## Regras de validação de entrada
Por campo: formato, obrigatoriedade, limites, máscara e normalização.

## Matriz de regras executáveis
| ID | Regra | Gatilho | Entrada | Camada fonte da verdade | Resultado válido | Resultado inválido | Mensagem | Teste |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RN-01 |  |  |  | Banco/API/Frontend |  |  |  |  |

## Mensagens
Texto exato de erro/sucesso por regra, quando aplicável.

## Camada de aplicação
Onde cada regra é aplicada e validada:

- **Banco** (constraints, checks). `N/A` + motivo se não houver.
- **API/Backend** (validação de servidor, fonte de verdade).
- **Frontend/UI** (validação imediata, não substitui o backend).

## Casos de borda
Valores limite, vazios, duplicados, concorrência, fuso/locale.

## Testes
Casos obrigatórios para cobrir cada regra (válido e inválido).

## Segurança
Regras com impacto em autorização, privacidade ou integridade de dados.

## Regras negativas obrigatórias
Casos que devem falhar: sem permissão, tenant errado, objeto de outro usuário,
entrada malformada, duplicidade, replay, concorrência, tentativa de burlar limite
ou manipular estado.

## Riscos
Conflitos de regras, ambiguidades e regressões possíveis.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Como verificar que as regras foram implementadas corretamente.

## Matriz de rastreabilidade
| RN | Tela/API/Banco afetado | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- |
|  |  |  |  |
