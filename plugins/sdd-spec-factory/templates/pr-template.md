# Pull Request

> PR é a entrega revisável. Só é mergeado após review/QA aprovados.
> Deploy só acontece depois do PR aprovado.

## Task
Link da task (TASK-XXX) que originou este PR.

## Issue
Link da issue rastreada.

## Branch
Branch de origem -> branch de destino.

## Specs seguidas
Links das specs que este PR implementa (o contrato).

## O que foi feito
Resumo objetivo das mudanças.

## Fora do escopo respeitado
Confirmar que o que estava fora de escopo não foi alterado.

## Como testar
Passos para revisar/testar manualmente.

## Evidências
Screenshots, gravações, logs ou saídas que comprovam o resultado.

## Matriz de rastreabilidade entregue
| Requisito/RN/mockup | Implementação | Teste/evidência | Status |
| --- | --- | --- | --- |
|  |  |  |  |

## Comandos executados
Build, testes, lint e migrações executados.

## Resultado dos testes
Resumo dos testes (passou/falhou) com evidência.

## Checklist de code review
- [ ] Código segue as specs e os critérios de aceite.
- [ ] Matriz de rastreabilidade foi implementada item a item.
- [ ] Matriz de interações UI foi implementada quando aplicável.
- [ ] Contrato backend/API/job/webhook foi implementado quando aplicável.
- [ ] Sem código fora do escopo da task.
- [ ] Nomes, padrões e estilo consistentes com o repositório.
- [ ] Sem segredos, tokens ou dados sensíveis versionados.
- [ ] Tratamento de erros adequado.
- [ ] Banco / API/Backend / Frontend/UI revisados separadamente.

## Checklist de QA
- [ ] QA funcional: fluxos principais e de erro validados.
- [ ] Cada botão/ação/estado especificado tem evidência.
- [ ] QA visual: telas conferem com o mockup aprovado (ui-ux-standard).
- [ ] Estados cobertos: loading, vazio, erro, sucesso, sem permissão.
- [ ] Responsividade e acessibilidade verificadas.

## Checklist de segurança
- [ ] Security Spec Contract seguido ou `N/A` justificado.
- [ ] Authz/authn corretos (security-standard).
- [ ] Validação de input no servidor.
- [ ] Testes negativos de acesso, tenant, input e abuso executados quando aplicável.
- [ ] Dados sensíveis protegidos e isolamento de tenant respeitado.
- [ ] Sem novas vulnerabilidades introduzidas.

## Riscos
Riscos desta entrega e plano de mitigação/rollback.

## Pendências
Itens conhecidos em aberto e follow-ups.
