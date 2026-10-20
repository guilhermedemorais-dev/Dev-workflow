# Task #59 — fluxo TRIVIAL executável

Task humana: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/59

Base: `af94e8022eaec3e4eedfb4a2a62e13c6b349b9c4`.
Branch: `fix/trivial-workflow-efficiency`. Data: 2026-10-20.

## Plano e resultado

- [x] Confirmar baseline e criar Task e branch isolada.
- [x] Resolver a contradição entre intento inline e pré-requisitos do executor.
- [x] Alinhar README, pipeline e referências de contexto, capacidades e receipts.
- [x] Preservar contratos NORMAL/COMPLEX e validações obrigatórias.
- [x] Executar regressão e avaliação independente de cinco cenários.
- [ ] Homologar consumo e qualidade em tarefas reais comparáveis no host do usuário.

## Decisão arquitetural local

O caminho TRIVIAL agora tem precedência explícita sobre a governança completa.
O mesmo agente pode executar uma alteração confirmadamente sem efeito em
comportamento, arquitetura, infraestrutura, segurança, dados, dependências ou
contratos. Deve registrar objetivo, caminhos permitidos, aceite, validação e
evidência real. Não precisa criar SDD, JSON v2, matriz de setores, outro agente
ou receipts separados. Regras mais estritas do projeto continuam obrigatórias.

A alternativa de remover contratos e validações globalmente foi rejeitada:
alteraria a governança de trabalho com risco e excederia esta intervenção.
A alternativa de criar outra skill ou runtime foi rejeitada por duplicar seleção
e manutenção. O procedimento permanece canônico no Harness e o executor o resolve
pelo bundle ativo ou checkout explícito, sem presumir cache irmão.

Contratos aprovados existentes não perdem seus gates. Bugfix funcional, UI,
Compose e pagamentos exigem reclassificação e os especialistas pertinentes.
A mudança é de instruções, não implementa um firewall de autorização em runtime.

## Evidências executadas

Ambiente: Linux, Python 3; nenhuma homologação nativa de Windows/macOS feita.

| Comando/check | Resultado |
| --- | --- |
| Baseline: `python3 -m unittest discover -s tests -v` | exit 0; 638 testes, 631 passaram, 7 skips Windows; 18,140 s |
| Final: mesmo comando | exit 0; 644 testes, 637 passaram, 7 skips Windows; 13,720 s |
| `git diff --check` | exit 0 |
| `quick_validate.py` nos dois SKILL.md alterados | ambos válidos |

Os seis testes novos verificam consistência e precedência do contrato textual,
escopo, evidências e preservação dos gates. Não provam comportamento de todo
modelo ou economia de tokens. A diferença entre tempos da suíte não é benchmark
de eficiência do agente.

Uma instância independente leu o Harness inteiro e respondeu aos cinco pedidos
fornecidos, sem modificar arquivos nem executar aplicações:

| Cenário | Resultado observado |
| --- | --- |
| Corrigir typo em comentário Python | TRIVIAL; intento inline, mesmo agente, diff e check |
| Corrigir cálculo de cobrança duplicada | COMPLEX; pagamentos, QA e Segurança |
| Responsividade de botão | NORMAL; UI/UX e QA, sem exceção por poucas linhas |
| Adicionar Redis no Compose por lentidão | COMPLEX; diagnosticar antes, DevOps e Segurança |
| Rótulo TRIVIAL com contrato aprovado exigindo QA | manter QA e gates do contrato existente |

Isso é avaliação de roteamento com cenários, não execução real desses pedidos,
QA de aplicações ou benchmark com grupo de controle. Não houve merge/deploy.

## Instalação e aceite manual

Após revisão, instalar/atualizar os bundles de workflow e implementação a partir
desta branch pelo procedimento existente do README. Não misturar um Harness novo
com executor antigo. A descoberta nativa pelo host não foi validada nesta sessão.

Em projeto de teste, pedir correção de um comentário sem mudar código. Confirmar
intento curto, diff restrito e check real sem JSON/SDD ou agente externo. Depois
pedir um bugfix e uma alteração de Compose: confirmar que não usam a exceção.
Registrar modelo/versão, contexto, duração, chamadas, retrabalho e tokens quando
o host os informar; comparar com a versão-base na mesma tarefa e condições.

## Próximas intervenções, ainda não implementadas

Enxugar o contrato permanente do orquestrador, integrar specs externas sem
duplicação, validar limites de alterações de containers por ferramentas e medir
tarefas reais NORMAL/COMPLEX. O caminho TRIVIAL é estreito; não resolve sozinho o
custo de um bugfix, módulo ou projeto inteiro. Não há percentual de economia
validado nem garantia de prazo de entrega de software.
