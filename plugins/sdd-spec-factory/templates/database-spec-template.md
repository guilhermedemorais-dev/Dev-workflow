# SPEC: Banco de dados - Nome do escopo

> Spec é contrato do que deve ser construído. Não é PR, não é task.
> Crie apenas quando houver impacto em banco. Não invente schema existente (`HIPÓTESE:`).

## Status
Rascunho | Em revisão | Aprovada

## Objetivo
Que dado este escopo precisa armazenar/alterar e por quê.

## Contexto
Módulo/feature e specs relacionadas.

## Resultado dos gates
| Gate | Status | Evidência / motivo |
| --- | --- | --- |
| Ambiguity Gate | PASS/BLOCKED | Perguntas bloqueantes ou motivo de aprovação. |
| Spec Completeness Gate | PASS/BLOCKED | Schema, migração, privacidade e testes cobertos. |
| Security Spec Contract Gate | PASS/BLOCKED/N/A | Isolamento/dados sensíveis cobertos ou motivo de N/A. |
| Traceability Gate | PASS/BLOCKED | Requisitos ligados a testes e aceite. |

## Tabelas/coleções
Para cada tabela (nova ou alterada):

- **Nome:** `tabela`
- **Tipo de mudança:** nova | alteração | remoção (justificar remoção).
- **Colunas/campos:** nome, tipo, nulo?, default, descrição.
- **Chave primária:** ...
- **Chaves estrangeiras:** ... e ação ON DELETE/UPDATE.
- **Índices:** quais e por quê.
- **Constraints/checks:** unicidade, validação no nível do banco.

## Relacionamentos
Como as entidades se relacionam (1:1, 1:N, N:N).

## Migrações
Estratégia: criação, alteração, backfill, ordem e reversão (down).

## Compatibilidade e dados existentes
Impacto em dados atuais, migração de dados, breaking changes.

## Multi-tenant / isolamento
Como o dado é isolado por tenant/usuário, quando aplicável.

## Matriz de propriedade e acesso
| Entidade/tabela | Dono do dado | Escopo de acesso | Regra de isolamento | Quem pode ler | Quem pode escrever | Teste negativo |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Segurança e privacidade
Dados pessoais/sensíveis, criptografia, retenção, mascaramento (validar com security-standard).

## Classificação de dados
| Campo/dado | Classificação | Base legal/finalidade | Retenção | Mascaramento/criptografia | Exportável? | Auditável? |
| --- | --- | --- | --- | --- | --- | --- |
|  | público/interno/sensível/PII |  |  |  | sim/não | sim/não |

## Performance
Volume esperado, crescimento, particionamento/índices.

## Observabilidade
Auditoria, soft delete, timestamps, rastreamento de alterações.

## Testes
Validação de migração, rollback e integridade referencial.

## Riscos
Perda de dados, lock, downtime, regressão.

## Decisões pendentes
Decisões abertas aguardando humano (numeradas).

## Critérios de aceite
Critérios objetivos e testáveis do banco.

## Matriz de rastreabilidade
| Requisito/RN | Tabela/campo | Migração/constraint | Teste/evidência | Critério de aceite |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
