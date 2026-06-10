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
```

Cada plugin mantem uma unica skill canonica e manifestos adaptadores para
Codex, Claude Code e Antigravity. Isso evita que as regras das tres plataformas
evoluam de forma diferente.

## Dev Workflow Standard

Plugin principal de desenvolvimento.

Responsabilidades:

- Estrutura padrao de documentacao por projeto.
- Fluxo de PRD, pesquisa, especificacao, implementacao e revisao.
- Delegacao obrigatoria de implementacao nao trivial para Claude Code, dividida em checkpoints pequenos.
- Uso opcional de CLIs auxiliares apos health check.
- Pesquisa tecnica com codigo local, documentacao oficial, Context7, Firecrawl e `grep.app`.
- Teste seguro de APIs e webhooks antes de producao.
- Pesquisa e uso de plugins/skills apenas quando faltar uma capacidade real.
- Criacao de skill/plugin quando a capacidade necessaria nao existir e for reutilizavel.
- QA, seguranca, testes e relatorio por camada: Banco, API/Backend e Frontend/UI.
- Validacao de fluxos web e UI com Playwright quando houver ambiente executavel.

### Plugin principal

O `dev-workflow-standard` e o responsavel principal por administrar e desenvolver
o software de ponta a ponta. Ele conduz descoberta, PRD, pesquisa, arquitetura,
planejamento, implementacao, revisao, testes, QA, seguranca, documentacao e
entrega. Claude Code executa os checkpoints de implementacao nao trivial, mas o
plugin principal continua responsavel por dividir o trabalho, controlar escopo,
revisar cada diff e executar a validacao.

Para economizar o contexto e os tokens do Codex, o workflow nao envia o projeto
inteiro nem a conversa completa ao Claude. Cada chamada recebe apenas objetivo,
caminhos das fontes de verdade, modulo permitido, restricoes e de um a tres
criterios de aceite. Banco, API/Backend, Frontend/UI, testes e documentacao sao
separados quando puderem ser revisados de forma independente.

Antes da primeira delegacao, o Codex verifica `claude --version` e
`claude auth status`, registra `CLAUDE_STATUS` e avisa qual checkpoint sera
delegado. Se Claude Code estiver indisponivel numa tarefa em que a delegacao e
obrigatoria, o Codex deve parar antes de implementar em vez de consumir sozinho
o orcamento de implementacao. O protocolo completo esta em
[`claude-delegation.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/references/claude-delegation.md).

Em workspaces com rede restrita, `claude auth status` pode funcionar enquanto
`claude -p` falha por DNS, conexao ou timeout. Nesse caso, o workflow registra
`CLAUDE_STATUS=SANDBOX_NETWORK_BLOCKED` e repete exatamente o mesmo checkpoint
pela execucao externa aprovada da plataforma. Se a segunda tentativa funcionar,
continua como `AVAILABLE_EXTERNAL`; se falhar, para e informa o erro sem assumir
a implementacao no Codex.

Ele nao deve procurar outro plugin para tarefas que ja consegue executar com
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

- Codex: planejamento tecnico, arquitetura, coordenacao, revisao e validacao.
- Claude Code: implementacao pesada ou repetitiva, quando disponivel.
- Gemini, Blackbox, Qwen, Goose ou outras CLIs: consultas auxiliares e tarefas
  limitadas, somente depois de um health check.

As ferramentas auxiliares nao substituem PRD, documentacao, testes nem revisao.
Codex e Claude Code nao devem editar os mesmos arquivos simultaneamente.

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
```

Para testar uma copia local antes de publicar:

```bash
claude --plugin-dir ./plugins/dev-workflow-standard \
  --plugin-dir ./plugins/ui-ux-standard \
  --plugin-dir ./plugins/security-standard
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

Use `dev-workflow-standard` como cockpit principal de desenvolvimento.

Use `ui-ux-standard` sempre que a tarefa envolver telas, mockups, design system,
assets visuais, prompts de imagem/video, responsividade, acessibilidade ou
validacao visual.

Use `security-standard` para revisoes de seguranca, threat modeling, validacao
de vulnerabilidades, remediacao e gates de release proporcionais ao risco.

Para conhecer todas as regras, consulte diretamente:

- [`dev-workflow-standard/SKILL.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md)
- [`ui-ux-standard/SKILL.md`](plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md)
- [`security-standard/SKILL.md`](plugins/security-standard/skills/security-standard/SKILL.md)
