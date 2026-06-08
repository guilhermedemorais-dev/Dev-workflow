# Dev Workflow

Plugins publicos para padronizar planejamento, pesquisa tecnica,
desenvolvimento, UI/UX, documentacao, QA e validacao em projetos de software.

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
```

Cada plugin mantem uma unica skill canonica e manifestos adaptadores para
Codex, Claude Code e Antigravity. Isso evita que as regras das tres plataformas
evoluam de forma diferente.

## Dev Workflow Standard

Plugin principal de desenvolvimento.

Responsabilidades:

- Estrutura padrao de documentacao por projeto.
- Fluxo de PRD, pesquisa, especificacao, implementacao e revisao.
- Delegacao controlada para Claude Code.
- Uso opcional de CLIs auxiliares apos health check.
- Pesquisa tecnica com codigo local, documentacao oficial, Context7 e `grep.app`.
- Teste seguro de APIs e webhooks antes de producao.
- Roteamento sob demanda para plugins e skills especializados.
- Melhoria controlada apenas quando existe uma lacuna real de capacidade.
- QA, seguranca, testes e relatorio por camada: Banco, API/Backend e Frontend/UI.

### Orquestrador leve e especialistas sob demanda

O plugin principal nao deve tentar conter ou executar sozinho todo conhecimento
de arquitetura, backend, frontend, QA, seguranca, DevOps e design. Ele atua como
orquestrador:

1. Classifica a tarefa.
2. Consulta apenas o indice ou metadados das skills/plugins instalados.
3. Seleciona uma ferramenta principal e, normalmente, no maximo uma de apoio.
4. Envia somente objetivo, arquivos relevantes, restricoes e criterios de aceite.
5. Exige retorno estruturado com evidencias, validacoes, riscos e incertezas.
6. Confere as alegacoes no codigo, documentacao oficial, testes ou runtime.
7. Mantem no contexto apenas a conclusao aceita e descarta o restante.

Isso reduz contexto, consumo de tokens e perda de foco. Tambem diminui
alucinacoes, mas nao elimina a necessidade de verificacao: plugins continuam
sendo agentes/ferramentas e podem errar.

O workflow nunca deve carregar todas as skills para decidir qual usar. Quando o
`skill-router-orchestrator` estiver instalado, ele usa um indice local leve e
ativa apenas a skill selecionada.

O protocolo completo esta em
[`capability-routing.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/references/capability-routing.md).

### Melhoria continua controlada

Somente quando o roteamento nao encontra uma ferramenta adequada, ou quando uma
ferramenta ativa falha repetidamente, o workflow pode pesquisar skills,
plugins, MCPs, hooks e ferramentas nas lojas e repositorios. Exemplos:

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
9. Registrar o aprendizado e remover capacidades que nao compensam seu custo.

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
```

Para testar uma copia local antes de publicar:

```bash
claude --plugin-dir ./plugins/dev-workflow-standard \
  --plugin-dir ./plugins/ui-ux-standard
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

Para conhecer todas as regras, consulte diretamente:

- [`dev-workflow-standard/SKILL.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md)
- [`ui-ux-standard/SKILL.md`](plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md)
