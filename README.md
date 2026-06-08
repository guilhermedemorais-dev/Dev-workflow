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
    skills/dev-workflow-standard/SKILL.md
  ui-ux-standard/
    .codex-plugin/plugin.json
    skills/ui-ux-standard/SKILL.md
```

## Dev Workflow Standard

Plugin principal de desenvolvimento.

Responsabilidades:

- Estrutura padrao de documentacao por projeto.
- Fluxo de PRD, pesquisa, especificacao, implementacao e revisao.
- Delegacao controlada para Claude Code.
- Uso opcional de CLIs auxiliares apos health check.
- Pesquisa tecnica com codigo local, documentacao oficial, Context7 e `grep.app`.
- Teste seguro de APIs e webhooks antes de producao.
- QA, seguranca, testes e relatorio por camada: Banco, API/Backend e Frontend/UI.

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

## Instalacao local

Copiar para a pasta local de plugins:

```bash
mkdir -p ~/plugins
cp -a plugins/dev-workflow-standard ~/plugins/
cp -a plugins/ui-ux-standard ~/plugins/
```

Depois, registre/atualize os plugins no marketplace local do Codex conforme o
fluxo usado na maquina.

## Uso recomendado

Use `dev-workflow-standard` como cockpit principal de desenvolvimento.

Use `ui-ux-standard` sempre que a tarefa envolver telas, mockups, design system,
assets visuais, prompts de imagem/video, responsividade, acessibilidade ou
validacao visual.

Para conhecer todas as regras, consulte diretamente:

- [`dev-workflow-standard/SKILL.md`](plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md)
- [`ui-ux-standard/SKILL.md`](plugins/ui-ux-standard/skills/ui-ux-standard/SKILL.md)
