# TASK-041: Studio PRD, planejamento e guia visual vivo

Status: In Progress. Tipo: feature. Prioridade: alta. Revisão: 1.

Resumo: Studio PRD e templates de planejamento; Integração SDD e biblioteca visual viva; Packaging, roteamento e documentação

## Objetivo

Aplicar o briefing e planejamento aprovados ao Engineering Harness

## Estado atual

Portal na main, correções runtime em branch e especificações Studio locais ainda não implementadas

## Resultado esperado

Plugin Studio e integrações verificáveis, publicáveis e instaláveis

## Requisitos e critérios de aceite

- [ ] REQ-01 / AC-01: Studio PRD conduz briefing adaptativo com até três perguntas, pesquisa prévia, atores/jornadas/regras e inventário autorizado de software existente; sugestões não são requisitos aprovados.
- [ ] REQ-02 / AC-02: PRD explicita quantidade, IDs e limites dos módulos; uma task completa por módulo, sem fragmentar por camada, especialista ou tokens; sem redução automática a MVP.
- [ ] REQ-03 / AC-03: Planejamento interno separado em MD e JSON com mesma revisão e decisões, etapas, urgência versus dependências, esforço versus calendário, recursos, riscos, capacidade e incerteza explícita.
- [ ] REQ-04 / AC-04: Cada task no plano possui prompt curto específico com links reais; contrato inexistente indica especificação, não implementação. SDD mantém template completo e JSON equivalente; aguarda autorização por módulo.
- [ ] REQ-05 / AC-05: Guia visual vivo no projeto atendido: Markdown, HTML navegável, tokens e fontes, componentes identificados por revisão, estados e fixtures rotuladas; catálogo não prova backend pronto.
- [ ] REQ-06 / AC-06: Harness, SDD, UI, implementação e QA compartilham roteamento e gates; comentários da Issue registram evidência, superfícies e tokens apenas medidos.
- [ ] REQ-07 / AC-07: Adicionar plugin nos marketplaces, atualizar README/pipeline, incorporar correção de metadata/runtime existente, preservar credenciais e verificar instalação separadamente do carregamento.
- [ ] REQ-08 / AC-08: Portal somente regras já existentes de fonte externa para docs/portal; não construir portal, hospedar, configurar banco ou publicar dados privados.

## Fontes e contrato

Contrato: [TASK-041.json](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/execution/TASK-041.json). Specs: [studio-prd.md](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/specs/studio-prd.md). Documentação: README.md e docs/workflow-pipeline.md.

REF-01: docs/specs/studio-prd.md#requisitos, Escopo aprovado e aceites.

REF-02: plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md#sources-of-truth-and-ownership, Preservar contratos, setores e equivalência.

## Microtarefas e prompts

### MT-01: Studio PRD e templates de planejamento

Skill/plugin: dev-implementation-standard. Capacidade: skill-authoring. Ferramenta: apply_patch. Validador: qa-testing-standard.

Caminhos: plugins/studio-prd/**, tests/test_studio_prd.py. Fontes: REF-01, REF-02. Dependências: nenhuma.

- [ ] Inspecionar fontes e reuso
- [ ] Implementar recorte aprovado
- [ ] Executar testes e relatar limitações

Entrega: Studio PRD e templates de planejamento. Conclusão: Critérios aprovados cobertos e testes do recorte passam.

Prompt: leia [TASK-041.json](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/execution/TASK-041.json), lista MT-01/checklist; respeite restrições, fontes, critérios e testes globais.

### MT-02: Integração SDD e biblioteca visual viva

Skill/plugin: dev-implementation-standard. Capacidade: skill-authoring. Ferramenta: apply_patch. Validador: qa-testing-standard.

Caminhos: plugins/ui-ux-standard/**, plugins/sdd-spec-factory/**, plugins/dev-implementation-standard/**, plugins/qa-testing-standard/**, tests/test_live_design_guide.py. Fontes: REF-01, REF-02. Dependências: nenhuma.

- [ ] Inspecionar fontes e reuso
- [ ] Implementar recorte aprovado
- [ ] Executar testes e relatar limitações

Entrega: Integração SDD e biblioteca visual viva. Conclusão: Critérios aprovados cobertos e testes do recorte passam.

Prompt: leia [TASK-041.json](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/execution/TASK-041.json), lista MT-02/checklist; respeite restrições, fontes, critérios e testes globais.

### MT-03: Packaging, roteamento e documentação

Skill/plugin: dev-implementation-standard. Capacidade: skill-authoring. Ferramenta: apply_patch. Validador: qa-testing-standard.

Caminhos: README.md, AGENTS.md, docs/**, .agents/plugins/marketplace.json, .claude-plugin/marketplace.json, plugins/dev-workflow-standard/**, plugins/dev-environment-standard/**, tests/**, plugins/studio-prd/.codex-plugin/plugin.json, plugins/studio-prd/.claude-plugin/plugin.json. Fontes: REF-01, REF-02. Dependências: nenhuma.

- [ ] Inspecionar fontes e reuso
- [ ] Implementar recorte aprovado
- [ ] Executar testes e relatar limitações

Entrega: Packaging, roteamento e documentação. Conclusão: Critérios aprovados cobertos e testes do recorte passam.

Prompt: leia [TASK-041.json](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/execution/TASK-041.json), lista MT-03/checklist; respeite restrições, fontes, critérios e testes globais.

## Matriz de setores

### Lista QA/checklist

Owner: qa-testing-standard; fase validation; depende de documentation.
Fontes REF-01/REF-02, critérios AC-01..08 e testes TEST-01/02.
Caminhos permitidos tests/** e docs/receipts/**; mesmas restrições globais.
Entrega: QA_STATUS com evidências e limitações; sem divergências materiais abertas.

- [ ] Executar cenários representativos e suíte completa.
- [ ] Revisar equivalência, links e gates.
- [ ] Relatar defeitos e retestes.

Prompt: leia [TASK-041.json](https://github.com/guilhermedemorais-dev/Dev-workflow/blob/feat/studio-prd-delivery/docs/execution/TASK-041.json), lista QA/checklist,
herdando restrições globais e aguardando a evidência da implementação.

- database: N/A; dev-implementation-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- backend: N/A; dev-implementation-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- frontend: N/A; dev-implementation-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- ui_ux: N/A; ui-ux-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- qa: REQUIRED; qa-testing-standard; Autoria, regressão e reconciliação do protocolo. Dependências: documentation. Validação: full-test-suite.
- security: N/A; security-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- devops: N/A; devops-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- observability: N/A; devops-standard; Sem aplicação, dados, infraestrutura ou interface de produto nesta entrega; regras para futuros projetos não são sua execução. Dependências: nenhuma. Validação: N/A.
- documentation: REQUIRED; dev-implementation-standard; Autoria, regressão e reconciliação do protocolo. Dependências: nenhuma. Validação: documentation-review.
- harness: REQUIRED; dev-workflow-standard; Autoria, regressão e reconciliação do protocolo. Dependências: documentation, qa. Validação: sector-reconciliation.

## Limites e gates

Caminhos permitidos: plugins/studio-prd/**, tests/test_studio_prd.py, plugins/ui-ux-standard/**, plugins/sdd-spec-factory/**, plugins/dev-implementation-standard/**, plugins/qa-testing-standard/**, tests/test_live_design_guide.py, README.md, AGENTS.md, docs/**, .agents/plugins/marketplace.json, .claude-plugin/marketplace.json, plugins/dev-workflow-standard/**, plugins/dev-environment-standard/**, tests/**, plugins/studio-prd/.codex-plugin/plugin.json, plugins/studio-prd/.claude-plugin/plugin.json, plugins/reverse-engineering-standard/**, plugins/seo-standard/**. Protegidos: credenciais, runtime-state/**. Fora do escopo: Aplicação portal; Deploy de projeto cliente; Alterar credenciais; Migração em massa de tasks históricas.

Parar: source_of_truth_conflict, human_task_json_divergence, authorization_required, scope_expansion_required.

Aprovar PRD não autoriza implementar projetos clientes. Esta mudança do plugin foi autorizada na conversa. QA independente e reconciliação antes do PR; merge exige autorização e checks; deploy fora do escopo.

## Testes e evidências

- [ ] TEST-01: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`, esperado exit 0.
- [ ] TEST-02: `git diff --check`, esperado exit 0.

Relatar arquivos, comandos, resultados, limitações e tokens NOT_AVAILABLE quando não medidos em comentários da Issue. Resultado: execução em andamento, nenhum PASS antecipado.
