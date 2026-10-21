# Task #59 — eficiência do Engineering Harness

This report records revision `1c33d80`. The subsequent decision/UX/Apple HIG
continuation and current limits are recorded in `evidence-design-delivery.md`.

Task: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/59
PR: https://github.com/guilhermedemorais-dev/Dev-workflow/pull/60
Base V1: `af94e8022eaec3e4eedfb4a2a62e13c6b349b9c4`.
Branch publicada: `fix/trivial-workflow-efficiency`. Data: 2026-10-20.

## Plano executado

- [x] Corrigir o caminho TRIVIAL nos contratos do Harness e executor.
- [x] Separar contrato permanente de procedimentos por fase.
- [x] Mapear todas as 21 seções anteriores e verificar origem/destino por hash.
- [x] Substituir inventário global obrigatório por descoberta direcionada.
- [x] Reutilizar evidência compatível de ferramentas, runtime e contexto.
- [x] Referenciar specs externas aprovadas sem gerar uma spec equivalente.
- [x] Referenciar uma evidência pelos artefatos de governança, sem copiar logs.
- [x] Implementar e executar CLI de verificação de escopo de Compose.
- [x] Executar regressão, validators, edição real isolada e teste adversarial.
- [ ] Homologar instalação/descoberta no host do proprietário.
- [ ] Medir consumo em tarefas reais NORMAL/COMPLEX comparáveis.

## Implementação e decisões locais

O SKILL.md permanente caiu de 38.885 bytes/678 linhas na main V1 para
10.975 bytes/163 linhas. Isso mede texto do arquivo, não tokens do modelo,
custo por Task ou qualidade. A primeira correção intermediária tinha
41.600 bytes/719 linhas. O conteúdo restante fica em cinco referências:

| Referência | Responsabilidade |
| --- | --- |
| workflow-responsibilities.md | missão, entrada, papéis e proveniência |
| workflow-planning.md | fluxo de produto, onboarding e gatilhos setoriais |
| workflow-governance.md | Task, contratos, Kanban, templates e review |
| workflow-execution.md | execução, delegação, disponibilidade e recuperação |
| workflow-context.md | contexto, evolução local e referências técnicas |

Todas as seções anteriores têm destino em `workflow-section-migration.json`.
Os testes comparam o mapa com o commit intermediário publicado
`f850909df24eeb371195fe5ead29f80d373fbbd0`, e não apenas com uma lista manual.
Hashes normalizam somente whitespace ao final da seção. Revisões intencionais
em Harness Contract e Delegation Rules removem repetição de descoberta/leitura;
as demais diferenças são correções de links relativos por mudança de diretório.
Nenhuma metodologia especializada foi resumida para simular economia.

TRIVIAL confirmado mantém objetivo, caminhos permitidos, aceite, validação e
resultado real, no mesmo agente quando possível. JSON v2, SDD, matriz setorial,
executor externo e receipts separados não são obrigatórios nesse caminho.
Regra mais estrita do projeto e contratos aprovados existentes continuam válidos.
Bugfix funcional, UI, pagamentos e infraestrutura não recebem essa exceção.

NORMAL/COMPLEX mantêm JSON v2, equivalência com a Issue e gates aplicáveis.
Specs existentes, incluindo Spec Kit, são fontes por caminho, revisão e propósito;
SDD cobre lacunas reais. Isso não instala nem migra o motor para Spec Kit.
Os campos obrigatórios de receipts permanecem; evidência detalhada pode ser
referenciada pelo mesmo caminho/revisão no receipt, relatório, Issue e PR.

Descoberta começa na seleção da Task e no estado compatível já disponível.
Inventário completo continua disponível para lacunas, falha ou seleção obsoleta.
Fonte carregada na mesma revisão/contexto não precisa ser relida em cada lista;
perda de contexto exige reconstrução das fontes normativas selecionadas.
O executor pode ser reutilizado entre listas compatíveis; isso não satisfaz
revisão independente por outro owner.

## Verificador de Compose

Implementação canônica no bundle DevOps:
`plugins/devops-standard/skills/devops-standard/scripts/compose-scope.py`.

```bash
python3 plugins/devops-standard/skills/devops-standard/scripts/compose-scope.py \
  --before baseline.json --after proposed.json --allow-services api
```

Compara JSON renderizado da mesma versão/contexto de Compose. Exige nomes exatos
permitidos para alterações de services, volumes, networks, secrets, configs e
campos globais. Rejeita alterações não declaradas, duplicatas e dados inválidos.
Exit 0: WITHIN_SCOPE; exit 1: OUT_OF_SCOPE; exit 2: INVALID_INPUT.
Não imprime valores interpolados; inclui nomes, hashes e mudanças.

Os catálogos existentes de plataforma incluem o script. Linux registra testes
estáticos executados; Windows e macOS permanecem NOT VALIDATED para esta tool.
Não há instalador, hook ou execução automática de Docker.

Este CLI verifica somente diferença contra o escopo fornecido. Não valida schema
Compose completo, origem/autenticidade da baseline nem a segurança de uma mudança
explicitamente permitida. Não bloqueia outras ferramentas de executar Docker.
Não autoriza build, restart, prune ou deploy. Security/DevOps continuam exigidos.
Snapshots podem conter segredos: guardar em estado local ignorado com permissões
restritas e nunca publicar seu conteúdo. Não ampliar allow-list para obter verde.

## Testes e evidências

Ambiente observado: Linux, Python 3.12.14. Docker ausente.

| Verificação | Resultado |
| --- | --- |
| Baseline V1: unittest discover | 638 testes, 631 passaram, 7 skips Windows; exit 0 |
| Primeira correção TRIVIAL | 644 testes, 637 passaram, 7 skips Windows; exit 0 |
| Revisão completa: unittest discover | 661 testes, 654 passaram, 7 skips Windows; exit 0 |
| quick_validate.py: workflow e DevOps | ambos válidos |
| git diff --check | exit 0 |
| Edição real em repositório descartável | somente README alterado, substituição exata e diff check aprovados |
| CLI adversarial independente | 13 casos executados e retestados após correção |

A edição real usou o novo Harness: corrigiu `recieve` para `receive`, sem commit,
rede ou instalações. Inspeções reais de HEAD/diff e teste de igualdade confirmaram
que somente o arquivo autorizado mudou. Para essa execução, leu somente SKILL.md;
referências adicionais foram lidas depois para explicar os cenários hipotéticos
Redis e cobrança, que não foram executados em aplicações.

O teste independente do CLI reproduziu dois defeitos antes da correção:
Python confundia true/1 em comparação recursiva, e JSON não padrão com NaN/Infinity
era aceito. Ambos foram corrigidos e receberam regressões. Presença de grupo vazio
também passou a ser tratada como mudança explícita. Reteste dos 13 casos:

| Caso | Exit final |
| --- | --- |
| api isolado autorizado | 0 |
| api + redis; remoção de data; nome do projeto | 1 em cada caso |
| JSON truncado; serviço duplicado; chave aninhada duplicada | 2 em cada caso |
| x-policy true→1; 1→true fora do escopo | 1 em cada caso |
| NaN fora/dentro de api; Infinity em api | 2 em cada caso |
| adicionar networks vazio não autorizado | 1 |

Os testes antigos de conteúdo agora inspecionam a união das referências roteadas.
Isso preserva a cobertura de regras sem obrigar o agente a carregar essa união.
Novos testes verificam limite do contrato permanente, mapa completo e hashes,
links relativos, gates preservados, JSON estrito e CLI com subprocessos reais.
Testes estruturais não provam obediência de todo modelo ou economia de tokens.

## Instalação e aceite manual

Após revisão, atualizar os bundles workflow, implementação, ambiente e DevOps
com os arquivos desta branch pelo instalador/procedimento existente do README.
Não misturar bundles antigos com o novo contrato. Nenhum merge/deploy foi feito.

1. Em projeto descartável, corrigir somente comentário sem mudar código. Conferir
   intento curto, caminhos, diff e check, sem criação de JSON/SDD ou outro agente.
2. Pedir bugfix funcional e mudança de Compose. Conferir que mantêm os gates
   obrigatórios, sem tratar poucas linhas como risco trivial.
3. Renderizar baseline/proposta Compose em contexto controlado. Autorizar somente
   api e verificar que inclusão de redis ou alteração de data retorna exit 1.
4. Registrar modelo, versão dos bundles, contexto, duração, chamadas, retrabalho
   e tokens quando o host os fornecer. Comparar mesmas tarefas e critérios com V1.

## Limitações e pendências

Tokens de entrada/saída/cache e custo: NOT_AVAILABLE. Não houve benchmark
end-to-end de bugfix, backend ou módulo, nem promessa de redução percentual.
A comparação textual não inclui os bytes das referências condicionais necessárias
para cada tarefa. O fluxo NORMAL/COMPLEX continua tendo custo de governança.
Não é garantia de impedir todo desvio de agente ou de entregar projeto em prazo.

Instalação nativa no host, renderer/daemon Docker, Windows10/11 e macOS não foram
homologados nesta sessão. A Task aguarda revisão e aceite, sem merge/deploy.
