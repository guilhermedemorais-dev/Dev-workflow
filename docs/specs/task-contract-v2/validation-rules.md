# Task Contract v2: validation rules

## TC2-01, identidade e revisão

`task_id`, Issue e `contract_revision` devem coincidir entre card e JSON.

## TC2-02, equivalência normativa

Escopo, exclusões, requisitos, regras, referências, design, microtarefas,
setores, testes, critérios e stop conditions não podem divergir.

## TC2-03, referências específicas

Toda referência obrigatória informa propósito, arquivo do projeto e seção. A
microtarefa aponta o ID correto. Fonte obrigatória ausente bloqueia execução.

## TC2-04, design

Quando UI/UX for REQUIRED, Design Guide, tokens, biblioteca de componentes,
referências visuais e mockup devem ser resolvidos. N/A exige motivo verificado.

## TC2-05, publicação do Discovery

`DISCOVERY_SDD_COMPLETED` só é PUBLISHED quando a operação retorna URL ou
identificador. Se a capability ligada à Issue existe e falha, não avançar para
Ready for Dev.

## TC2-06, tokens

Contagem exata só pode vir do runtime/API. Sem fonte, usar `NOT_AVAILABLE` em
input, output, total e measurement source. Nunca promover estimativa a medição.

## TC2-07, superfície alterada

Todo comentário material registra arquivos, mudanças em Issue/card,
JSON/spec/referências, mutações remotas, indicador de código e branch/commit/PR.

## TC2-08, independência

Testes do implementador não substituem QA funcional, Security QA, UI/UX QA ou
DevOps/observabilidade REQUIRED. Falha retorna ao owner e à mesma validação.
