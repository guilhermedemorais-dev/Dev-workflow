# Dev Workflow

Repositorio de plugins pessoais para padronizar planejamento, desenvolvimento,
UI/UX, documentacao, QA e validacao em projetos de software.

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
- Pesquisa tecnica com docs oficiais, Context7 e exemplos publicos quando util.
- QA, seguranca, testes e relatorio por camada: Banco, API/Backend e Frontend/UI.

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

