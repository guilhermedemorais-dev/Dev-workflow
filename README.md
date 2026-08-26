# Dev Workflow

Plugins publicos para padronizar planejamento, pesquisa tecnica,
desenvolvimento, UI/UX, seguranca, documentacao, QA e validacao em projetos de software.

O objetivo e manter uma rotina reutilizavel entre projetos sem substituir as
regras locais, o PRD, a arquitetura existente ou a aprovacao humana.

## Plugins

```text
plugins/
  dev-workflow-standard/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    plugin.json
    skills/dev-workflow-standard/SKILL.md
  ui-ux-standard/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    plugin.json
    skills/ui-ux-standard/SKILL.md
  security-standard/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    plugin.json
    skills/security-standard/SKILL.md
  sdd-spec-factory/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    plugin.json
    skills/sdd-spec-factory/SKILL.md
    templates/
  dev-implementation-standard/
    .codex-plugin/plugin.json
    .claude-plugin/plugin.json
    plugin.json
    skills/dev-implementation-standard/SKILL.md
    templates/
```

Cada plugin mantem uma unica skill canonica e manifestos adaptadores para
Codex, Claude Code e Antigravity. Isso evita que as regras das tres plataformas
evoluam de forma diferente.

## Arquitetura das skills

As skills tem papeis separados. A principal orquestra; as demais sao
especialistas acionados sob demanda.

| Skill | Papel |
| --- | --- |
| `dev-workflow-standard` | Agente orquestrador / revisor final |
| `sdd-spec-factory` | LLM de requisitos: specs e task executavel |
| `dev-implementation-standard` | Agente executor / coder |
| `ui-ux-standard` | LLM especialista em UI/UX |
| `security-standard` | LLM especialista em seguranca |

Pipeline de ponta a ponta:

```text
Ideia / demanda
  -> dev-workflow-standard diagnostica (perguntas criticas, riscos)
  -> dev-workflow-standard consolida escopo
  -> sdd-spec-factory gera specs
  -> sdd-spec-factory gera task executavel
  -> aprovacao humana
  -> skills obrigatorias carregadas + SKILL_RECEIPT
  -> REUSE_INVENTORY + MINIMAL_CODE_GATE
  -> dev-implementation-standard implementa (somente o escopo da task)
  -> Pull Request
  -> ui-ux-standard / security-standard / QA conforme aplicavel
  -> dev-workflow-standard aprova ou solicita rework
  -> merge / deploy (somente apos PR aprovado)
```

Regras invariantes:

- `dev-workflow-standard` nunca escreve codigo de produto, nunca pula specs e
  nunca cria task sem specs suficientes.
- `dev-implementation-standard` nunca implementa sem task aprovada e nunca altera
  fora do escopo sem registrar justificativa.
- `ui-ux-standard` e obrigatoria quando houver UI.
- `security-standard` e obrigatoria quando houver auth, autorizacao, tokens,
  sessao, dados sensiveis, uploads, pagamentos ou integracoes externas.
- Toda task aponta para specs obrigatorias.
- Todo PR aponta para task, issue, branch e specs seguidas.
- Skill mencionada nao e skill aplicada: toda skill obrigatoria gera `SKILL_RECEIPT`.
- Nenhum novo codigo e aceito sem `REUSE_INVENTORY` e `MINIMAL_CODE_GATE`.
- Se um LLM ficar sem tokens ou indisponivel, outro assume pelo `EXECUTION_HANDOFF`.
- Nenhum deploy e aprovado sem PR aprovado.

O pipeline completo, com gates e gatilhos, esta em
[`docs/workflow-pipeline.md`](docs/workflow-pipeline.md).

## Dev Workflow Standard

Skill do agente orquestrador. E a unica skill que aprova a passagem de um gate para
o proximo e nunca escreve codigo de produto diretamente.

Responsabilidades:

- Receber a demanda, diagnosticar e fazer as perguntas criticas.
- Consolidar escopo (incluido, fora de escopo, restricoes, riscos, decisoes).
- Decidir quais skills especialistas usar.
- Exigir specs antes de tasks e tasks antes da implementacao.
- Delegar a criacao de specs para `sdd-spec-factory`.
- Delegar a implementacao para `dev-implementation-standard`.
- Acionar `ui-ux-standard` quando houver UI.
- Acionar `security-standard` quando houver auth, autorizacao, tokens, sessao,
  dados sensiveis, uploads, pagamentos ou integracoes externas.
- Revisar o PR contra specs, task e criterios de aceite.
- Aprovar ou solicitar rework; relatar status por Banco, API/Backend e Frontend/UI.
- Nunca implementar codigo de produto diretamente.

### Papel do agente orquestrador

O `dev-workflow-standard` administra o ciclo de ponta a ponta como coordenador.
Ele conduz descoberta, escopo, delegacao, gates e aprovacao, mas nao absorve as
responsabilidades das skills especialistas. A criacao de specs e da task fica com
`sdd-spec-factory`; a implementacao fica com o agente executor usando
`dev-implementation-standard`. O orquestrador divide o trabalho,
controla escopo, revisa cada diff/PR e executa a validacao final.

O orquestrador nunca escreve codigo de produto. Depois que as specs e a task
estao aprovadas, ele delega a implementacao para `dev-implementation-standard`,
que pode usar qualquer LLM autorizado como meio de execucao. Para economizar
contexto e tokens, o orquestrador nao envia o projeto inteiro nem a conversa
completa: cada delegacao recebe a task, as specs obrigatorias, o modulo
permitido, restricoes e os criterios de aceite. Banco, API/Backend, Frontend/UI,
testes e documentacao sao separados quando puderem ser revisados de forma
independente.

Quando Claude Code for o transporte escolhido, o agente orquestrador verifica
`claude --version` e `claude auth status` e registra `CLAUDE_STATUS`. Se esse LLM
ficar sem tokens, contexto, autenticacao ou rede, o estado e persistido em
`EXECUTION_HANDOFF` e outro LLM autorizado continua a mesma task sem reiniciar
ou duplicar a implementacao. O adaptador de terminal visivel esta em
[`claude-delegation.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/references/claude-delegation.md).

Esse transporte e apenas o meio de execucao do `dev-implementation-standard`; a
divisao do trabalho, o controle de escopo e a revisao de cada diff/PR continuam
com o orquestrador.

Ele nao deve procurar outro plugin para tarefas que ja consegue coordenar com
suas regras, ferramentas e recursos atuais.

### MCPs disponiveis no ambiente do Guilherme

O ambiente Codex atual foi configurado com estes servidores MCP habilitados:

| MCP | Uso principal no workflow |
| --- | --- |
| `chrome-devtools` | Console, rede, renderizacao e performance do navegador. |
| `context7` | Documentacao atual de bibliotecas, SDKs e exemplos de API. |
| `figma` | Contexto de designs, frames, tokens e componentes aprovados. |
| `firecrawl-mcp` | Descoberta e extracao direcionada de conteudo web publico. |
| `grep-mcp` | Pesquisa de padroes em codigo publico indexado pelo `grep.app`. |
| `hf-mcp-server` | Modelos, datasets, Spaces e documentacao do Hugging Face. |
| `node_repl` | Execucao JavaScript limitada e orquestracao oferecida pelo runtime Codex. |
| `playwright` | QA de paginas, interacoes, estados, responsividade e fluxos e2e. |

Os plugins tratam essa lista como inventario do ambiente, nao como dependencia
obrigatoria para outros usuarios. Antes de depender de um MCP, devem confirmar o
estado real com `codex mcp list`, selecionar apenas os servidores relevantes e
aplicar fallback quando houver falha, falta de autenticacao ou rate limit.

Nenhum segredo, configuracao de `~/.codex/config.toml`, codigo privado, cookie,
dado de cliente ou credencial de producao deve ser enviado ou versionado por
causa desses MCPs. PRD, codigo local, arquitetura, mockup aprovado e
documentacao oficial continuam sendo as fontes de verdade.

### Melhoria continua controlada

Somente quando identifica uma capacidade necessaria que realmente nao possui, o
workflow pesquisa primeiro skills e plugins instalados e depois marketplaces
confiaveis. Se nao existir uma solucao adequada e a necessidade for recorrente,
ele propoe criar uma skill ou plugin focado. Exemplos de lacunas:

- Erro ou correcao que se repete.
- Processo manual recriado em varios projetos.
- Falta de capacidade para cumprir um criterio de aceite.
- Skill instalada que ficou obsoleta, instavel ou cara em tokens.

O ciclo e:

1. Registrar a lacuna e uma meta mensuravel.
2. Verificar primeiro as capacidades que ja estao instaladas.
3. Pesquisar marketplaces oficiais e depois fontes comunitarias mantidas.
4. Auditar codigo, manifestos, hooks, scripts, MCPs, permissoes e dependencias.
5. Criar score de relevancia, qualidade, manutencao, seguranca, compatibilidade,
   eficiencia, testabilidade e reversibilidade.
6. Pedir aprovacao humana antes de instalar ou habilitar codigo de terceiros.
7. Testar no menor escopo possivel e comparar com o baseline.
8. Promover com versao fixada ou fazer rollback.
9. Se nenhuma capacidade adequada existir, propor criar uma skill ou plugin.
10. Registrar o aprendizado e remover capacidades que nao compensam seu custo.

Nao existe instalacao autonoma silenciosa. Plugins podem executar scripts,
hooks, binarios ou servidores MCP e, por isso, toda nova capacidade passa por
aprovacao e validacao antes de entrar no fluxo global.

O protocolo completo esta em
[`continuous-improvement.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/references/continuous-improvement.md).

### Pesquisa tecnica e grep.app

O plugin usa [grep.app](https://grep.app/) para pesquisar implementacoes reais
em repositorios publicos. Ele e especialmente util para encontrar:

- Uso real de bibliotecas, SDKs, hooks, componentes e funcoes.
- Padroes avancados que nao aparecem em exemplos basicos da documentacao.
- Integracoes semelhantes, tratamento de erros e estrategias de testes.
- Alternativas de implementacao adotadas por projetos mantidos.
- Exemplos para comparar APIs antigas e atuais durante migracoes.

O `grep.app` e uma fonte de referencia, nao uma fonte de verdade. O plugin nao
deve copiar codigo encontrado sem revisar licenca, contexto, versao,
dependencias, seguranca e compatibilidade com o projeto.

### Ordem das fontes

A pesquisa segue esta prioridade:

1. PRD, arquitetura, regras e codigo do proprio projeto.
2. Documentacao oficial da biblioteca, framework, SDK ou servico.
3. Context7 para consultar documentacao atual e exemplos da API.
4. `grep.app` para localizar padroes usados em codigo publico real.
5. Decisao tecnica manual, com riscos e justificativa documentados.

Quando a pesquisa influencia arquitetura ou codigo compartilhado, o resultado
deve ser registrado em `docs/modules/<modulo>/research.md`, incluindo:

- Consulta realizada e problema investigado.
- Fontes e versoes relevantes.
- Alternativas encontradas.
- Solucao aceita e motivo.
- Solucoes rejeitadas e motivo.
- Riscos, testes e impactos esperados.

### Context7

Context7 e usado para confirmar sintaxe atual, configuracao, migracoes e
comportamento documentado de bibliotecas e SDKs. Ele complementa a
documentacao oficial e reduz o risco de implementar APIs obsoletas.

Exemplos publicos encontrados no `grep.app` nunca devem prevalecer sobre a
documentacao oficial ou sobre os contratos existentes no projeto.

### Firecrawl

Firecrawl e uma ferramenta opcional para descobrir e extrair conteudo de sites
publicos quando a documentacao local, oficial e o Context7 nao forem
suficientes. Ele pode ajudar em documentacao fragmentada, release notes e
pesquisa estruturada em varias paginas.

O workflow deve preferir buscas e extracoes direcionadas antes de crawls
amplos, limitar escopo e profundidade e confirmar afirmacoes tecnicas nas
fontes oficiais. Firecrawl nao e fonte de verdade e sua indisponibilidade nao
deve bloquear o desenvolvimento normal. Chaves de API ficam somente na
configuracao local ou em variaveis de ambiente; nunca no repositorio.

### Playwright

Playwright e a ferramenta preferencial para validacao reproduzivel de paginas
renderizadas e fluxos do usuario quando o projeto possui uma aplicacao web em
execucao. Ele cobre navegacao, formularios, autenticacao, permissoes, estados de
loading/empty/error, responsividade, screenshots e fluxos e2e criticos.

O plugin deve reutilizar a configuracao Playwright e o ambiente canonico do
projeto. Se Playwright estiver indisponivel, pode usar outra ferramenta de
navegador aprovada, mas deve reportar a validacao de runtime como nao realizada
quando nenhuma alternativa for executada.

### APIs e webhooks

Para novas integracoes, o workflow recomenda mocks, ambientes sandbox/staging
e, quando adequado, [Webhook.site](https://webhook.site/) para inspecionar
requisicoes de teste antes de apontar o fluxo para producao.

Devem ser validados metodo HTTP, headers, autenticacao, payload, timeout,
retries e tratamento de erros. Nunca envie segredos, tokens, cookies, dados de
clientes, dados financeiros, dados de saude ou payloads reais ao Webhook.site.
URLs temporarias do Webhook.site tambem nao devem permanecer no codigo ou na
configuracao versionada.

### Agentes e CLIs

O modelo operacional recomendado e:

- agente orquestrador usando `dev-workflow-standard`: diagnostico, escopo,
  delegacao, gates e revisao.
- LLM de requisitos usando `sdd-spec-factory`: specs e task executavel.
- agente executor usando `dev-implementation-standard`: implementa a task
  aprovada com qualquer LLM autorizado e disponivel.
- LLMs auxiliares: consultas limitadas, somente depois de um health check.

As ferramentas auxiliares nao substituem PRD, specs, documentacao, testes nem
revisao. O orquestrador e o executor nao devem editar os mesmos arquivos
simultaneamente.

## UI/UX Standard

Plugin especializado em design e validacao visual.

Responsabilidades:

- Descoberta de UI existente.
- `design.json` e `design-tokens.json`.
- Mockup-first workflow.
- Padrao de componentes.
- PRDs de prompts para imagens e videos.
- Validacao visual, responsividade, acessibilidade e estados da UI.

## Security Standard

Plugin especializado em seguranca de aplicacoes e integrado ao ciclo principal.

Responsabilidades:

- Revisao de seguranca proporcional ao risco para diffs e pull requests.
- Auditoria por modulo, integracao ou repositorio com escopo explicito.
- Threat modeling baseado na arquitetura real do projeto.
- Validacao de achados para reduzir falsos positivos.
- Correcao minima, testes de regressao e verificacao de comportamento legitimo.
- Relatorio por Banco, API/Backend, Frontend/UI, Infra e Supply Chain.

O plugin e uma implementacao original e independente. Ferramentas e plugins de
terceiros podem ser usados como segunda opiniao, mas seus textos, scripts,
templates e fluxos proprietarios nao sao copiados ou redistribuidos.

## SDD Spec Factory

Plugin especializado em Spec-Driven Development (SDD). Transforma um pedido de
cliente, feature, ideia ou problema em specs detalhadas e em uma task pequena e
executavel, sem implementar codigo de produto.

Funcao:

- Diagnosticar o pedido e levantar perguntas criticas antes de especificar.
- Consolidar escopo (incluido, fora de escopo, restricoes, riscos, decisoes).
- Gerar specs por camada: product, module, page/feature, component, regras de
  validacao, banco e API/backend, alem de frontend/UI quando houver tela.
- Separar sempre Banco, API/Backend, Frontend/UI, Testes, Seguranca,
  Observabilidade/logs, Decisoes pendentes, Riscos e Criterios de aceite.
- Produzir uma task executavel ligada a specs, issue, branch e PR.
- Entregar checklists de PR, code review e QA.

Quando usar:

- Sempre que um pedido novo precisar virar contrato antes de implementar.
- Quando faltar clareza de escopo e for preciso fechar specs e perguntas.
- Para quebrar uma feature grande em tasks pequenas e revisaveis.

Hierarquia imposta:

```text
Product Spec -> Module Spec -> Page/Feature Spec -> Component Specs ->
Task -> Branch -> Pull Request -> Review/QA -> Merge/Deploy
```

Distincao mantida pelo plugin:

- Spec nao e PR; spec e o contrato do que deve ser construido.
- Task e a ordem de execucao.
- PR e a entrega revisavel.
- Issue e o rastreamento.
- Review e aprovacao/reprovacao.
- Deploy so acontece depois do PR aprovado.

Integracao com os outros plugins:

- `dev-workflow-standard` e o CTO/orquestrador. O SDD Spec Factory alimenta esse
  fluxo com specs e a task executavel; a implementacao fica com
  `dev-implementation-standard`, sob revisao do orquestrador.
- `ui-ux-standard` valida as specs de tela e componente contra mockups
  aprovados, design system, acessibilidade e responsividade.
- `security-standard` valida a dimensao de seguranca de cada spec e o checklist
  de seguranca de cada PR antes do gate de release.

Os templates ficam em `plugins/sdd-spec-factory/templates/` (product, module,
page, component, validation-rules, api, database, task, pr, qa-review e review).

## Dev Implementation Standard

Skill executora / coder. Transforma uma task aprovada em codigo, estritamente
dentro do escopo. Nao planeja, nao escreve specs e nao detem a aprovacao final.

Funcao:

- Ler a task aprovada e todas as specs obrigatorias vinculadas.
- Implementar somente o escopo da task, na branch sugerida.
- Nao avancar para outra task.
- Nao alterar arquitetura sem aprovacao.
- Rodar os comandos obrigatorios e coletar evidencias.
- Atualizar o resultado da execucao na task.
- Preparar o PR vinculado a task, issue, branch e specs.

Pre-condicoes (nao inicia sem elas):

- Existe uma task aprovada.
- A task vincula specs obrigatorias e criterios de aceite.
- A branch sugerida esta definida.

Se faltar qualquer pre-condicao, ou se as specs forem ambiguas/contraditorias, ou
se a task exigir mudanca de arquitetura, a skill para e escala de volta para
`dev-workflow-standard` / `sdd-spec-factory`. Qualquer alteracao fora do escopo
precisa ser registrada com justificativa no resultado da task.

O template de relatorio de execucao fica em
`plugins/dev-implementation-standard/templates/execution-report-template.md`.

## Instalacao

### Codex

Adicionar este repositorio como marketplace:

```bash
codex plugin marketplace add guilhermedemorais-dev/Dev-workflow --ref main
```

Instalar os plugins:

```bash
codex plugin add dev-workflow-standard@guilherme-dev-workflow
codex plugin add ui-ux-standard@guilherme-dev-workflow
codex plugin add security-standard@guilherme-dev-workflow
codex plugin add sdd-spec-factory@guilherme-dev-workflow
codex plugin add dev-implementation-standard@guilherme-dev-workflow
```

### Claude Code

Adicionar o marketplace:

```text
/plugin marketplace add guilhermedemorais-dev/Dev-workflow
```

Instalar os plugins:

```text
/plugin install dev-workflow-standard@guilherme-dev-workflow
/plugin install ui-ux-standard@guilherme-dev-workflow
/plugin install security-standard@guilherme-dev-workflow
/plugin install sdd-spec-factory@guilherme-dev-workflow
/plugin install dev-implementation-standard@guilherme-dev-workflow
```

Para testar uma copia local antes de publicar:

```bash
claude --plugin-dir ./plugins/dev-workflow-standard \
  --plugin-dir ./plugins/ui-ux-standard \
  --plugin-dir ./plugins/security-standard \
  --plugin-dir ./plugins/sdd-spec-factory \
  --plugin-dir ./plugins/dev-implementation-standard
```

### Antigravity

O Antigravity reconhece skills e plugins no workspace. Depois de clonar este
repositorio, copie ou vincule os plugins desejados para:

```text
<projeto>/.agents/plugins/
```

Para uso global em todos os workspaces:

```text
~/.gemini/config/plugins/
```

O `plugin.json` na raiz de cada bundle identifica o plugin, e a skill canonica
continua dentro de `skills/<nome>/SKILL.md`.

### Copia local manual

Copiar para a pasta local de plugins:

```bash
mkdir -p ~/plugins
cp -a plugins/dev-workflow-standard ~/plugins/
cp -a plugins/ui-ux-standard ~/plugins/
cp -a plugins/security-standard ~/plugins/
cp -a plugins/sdd-spec-factory ~/plugins/
cp -a plugins/dev-implementation-standard ~/plugins/
```

O uso via marketplace e preferivel porque oferece descoberta e atualizacao
versionada. A copia manual e util para desenvolvimento e testes locais.

## Compatibilidade

| Plataforma | Manifesto/catalogo | Skill compartilhada |
| --- | --- | --- |
| Codex | `.codex-plugin/plugin.json` e `.agents/plugins/marketplace.json` | `skills/<nome>/SKILL.md` |
| Claude Code | `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` | `skills/<nome>/SKILL.md` |
| Antigravity | `plugin.json` na raiz do bundle | `skills/<nome>/SKILL.md` |

Hooks, MCPs e permissoes nao devem ser compartilhados cegamente entre as
plataformas, pois os esquemas e modelos de seguranca sao diferentes.

## Uso recomendado

Use `dev-workflow-standard` como CTO/orquestrador: ele recebe a demanda,
diagnostica, consolida escopo, exige specs, delega e revisa.

Use `sdd-spec-factory` quando um pedido novo precisar virar specs detalhadas e
uma task executavel antes da implementacao, garantindo o fluxo
spec -> component spec -> task -> issue -> branch -> PR -> review/QA -> deploy.

Use `dev-implementation-standard` para executar uma task ja aprovada, dentro do
escopo, na branch sugerida, rodando os comandos obrigatorios e preparando o PR.

Use `ui-ux-standard` sempre que a tarefa envolver telas, mockups, design system,
assets visuais, prompts de imagem/video, responsividade, acessibilidade ou
validacao visual.

Use `security-standard` para revisoes de seguranca, threat modeling, validacao
de vulnerabilidades, remediacao e gates de release proporcionais ao risco.

Para conhecer todas as regras, consulte diretamente:

- [`dev-workflow-standard/SKILL.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md)
- [`sdd-spec-factory/SKILL.md`](plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md)
- [`dev-implementation-standard/SKILL.md`](plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md)
- [`ui-ux-standard/SKILL.md`](plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md)
- [`security-standard/SKILL.md`](plugins/security-standard/skills/security-standard/SKILL.md)
- [`workflow-pipeline.md`](docs/workflow-pipeline.md)
