# Task Contract v2

## Resumo

O Task Contract v2 mantém duas representações sincronizadas da mesma ordem de
execução: a GitHub Issue completa para pessoas e um JSON estruturado para LLMs.
As duas compartilham `contract_revision` e equivalência normativa.

## Problema

O modelo anterior tratava o JSON como índice reduzido. Isso obrigava a LLM a
reconstruir requisitos dispersos e permitia que card e contrato expressassem
instruções diferentes. O card também não tornava referências, Design Guide,
microtarefas e toda a cadeia de validação suficientemente explícitos.

## Resultado esperado

- A Issue permite entender objetivo, escopo, referências, execução e gates sem
  depender de um arquivo Markdown local.
- O JSON contém as mesmas regras normativas, em campos estáveis e econômicos.
- Cada microtarefa roteia skill, plugin, capability, tool, referências, paths,
  checklist, entregáveis, condição de conclusão e validador.
- Discovery/SDD termina com comentário publicado antes de Ready for Dev.
- Comentários materiais registram tokens e superfície alterada.
- QA funcional, segurança, UI/UX e DevOps validam de modo independente quando
  seus setores forem REQUIRED.

## Fontes e bibliotecas

- Referências do projeto: `docs/biblioteca-referencias/`.
- Design Guide e biblioteca visual: `docs/design/` quando UI for aplicável.
- Contrato de roteamento: `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md`.
- Relatórios humanos: `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/execution-report-comments.md`.

## Regras de equivalência

1. Campos normativos do card e JSON descrevem a mesma entrega aprovada.
2. Toda alteração normativa incrementa `contract_revision` e atualiza ambos.
3. Evidência mutável, resultados, logs e discussão não são duplicados no JSON.
4. Divergência bloqueia execução com `human_task_json_divergence`.
5. V1 permanece legível; novas tasks usam v2.

## Pipeline obrigatório

Discovery/SDD colaborativo, comentário `DISCOVERY_SDD_COMPLETED`, aprovação
humana, prontidão do ambiente, implementação, testes do executor, validações
independentes, rework/reteste, gate do PR, gate final do Harness, aceite e merge
humanos. Deploy exige autorização separada.

## Critérios de aceite

- Templates de card, JSON e comentário representam o modelo aprovado.
- As sete skills consumidoras reconhecem equivalência e seus limites de owner.
- README e pipeline documentam o fluxo completo.
- Testes de contrato e suíte existente passam sem invalidar contratos v1.
