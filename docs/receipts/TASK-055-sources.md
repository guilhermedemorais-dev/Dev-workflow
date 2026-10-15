# TASK-055 official-source research

Contract revision: 1. Checked 2026-10-14. Research only; no runtime PASS,
installation, active configuration migration or publication by this researcher.

| Integration | Verified package/entry point | Requirement and Windows constraint |
| --- | --- | --- |
| Microsoft Playwright MCP | `@playwright/mcp` current npm `0.0.83`, `cli.js`; existing pin `0.0.82` | MCP engines Node >=18. Current Playwright system requirements list Windows11+, Server2019+ or WSL, not Windows10. Pin0.0.82 depends on Playwright1.64.0-alpha-1789764292000; 0.0.83 depends on alpha1790635538000. Native Windows10 operation must be locally proven and distinguished from official platform support. |
| Google Chrome DevTools MCP | `chrome-devtools-mcp` npm1.10.1, `build/src/bin/chrome-devtools-mcp.js` | Node ^20.19.0 OR ^22.12.0 OR >=23; README recommends LTS. Official browsers Chrome and Chrome for Testing. Chrome supports Windows10; MCP Codex Windows example names Windows11. Edge/other Chromium cannot be called officially supported. |
| Community n8n MCP | `czlonkowski/n8n-mcp`, npm `n8n-mcp`2.93.0, `dist/mcp/stdio-wrapper.js` | Node>=20. This is not the MCP server supplied by n8n itself. stdio env MCP_MODE=stdio, LOG_LEVEL=error, DISABLE_CONSOLE_OUTPUT=true. Optional better-sqlite3 may need native build tools; documented sql.js fallback. Documentation tools do not establish authenticated n8n management. |
| Anthropic Claude Code | Native `claude.exe mcp serve`; npm latest2.1.300 engines>=22 | Official Windows10 1809+, x64/ARM64,4GB RAM. Prefer native installer, `%USERPROFILE%\.local\bin\claude.exe`; Git for Windows currently optional, PowerShell supported. Native Windows Claude sandbox unavailable. MCP serve exposes tools, not Claude model calls; client owns individual tool confirmation. |

Primary sources, actually fetched:
- https://github.com/microsoft/playwright-mcp and https://playwright.dev/docs/intro
- https://github.com/ChromeDevTools/chrome-devtools-mcp and its `docs/client-configurations.md`
- https://support.google.com/chrome/a/answer/7100626?hl=en
- https://github.com/czlonkowski/n8n-mcp/blob/main/docs/SELF_HOSTING.md and `DATABASE_CONFIGURATION.md`
- https://code.claude.com/docs/en/setup and https://code.claude.com/docs/en/mcp
- https://developers.openai.com/codex/mcp and https://developers.openai.com/codex/config-reference
- https://developers.openai.com/plugins/build/plugins
- https://github.com/nodejs/node/blob/v24.x/BUILDING.md
- npm registry exact/current metadata endpoints for the four named packages.

Context7 resolved `/microsoft/playwright-mcp` and queried Windows requirements and
browser executable-path configuration. This supplemental index does not override
current upstream system requirements or prove actual machine compatibility.

Codex: `enabled=false` is documented; plugin server on/off control is under
`plugins.<plugin>.mcp_servers.<server>.enabled`. Plugin owns transport command.
No consulted official source establishes process startup only on first tool call.
Tool search and startup grace are not proof of lazy startup; explicit selection
is the documented fallback. Global/project/plugin definitions must be inventoried.

Native design: reuse persistent external Node/browser installations, install
selected package versions in a user-controlled prefix, launch node.exe plus JS
entry point directly rather than npx caches or Codex internal paths. Claude native
exe is separate. Preserve arguments, env precedence, secrets and browser/profile
preferences. Do not add sandbox bypass or change trust boundaries automatically.

Node24 platform table includes Windows10, but its EOL-vendor policy overrides
table entries. Record OS edition/build and qualify support separately from a
successful local runtime probe. Never silently choose WSL to mask this constraint.

Active config read-only identity observation: the four global MCP registrations
launch `wsl.exe`, distro `kali-linux`, executables under
`/home/teste/.local/share/gaeva-mcp`. Playwright/Chrome browser path is Linux-only.
Environment values were not printed. No process duplication inferred from this.
