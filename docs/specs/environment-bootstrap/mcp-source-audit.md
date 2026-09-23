# MCP source audit, 2026-09-23

Scope: portable development bootstrap, not CI/CD or production infrastructure.
The repositories below were opened before implementation. Runtime availability,
connection and authentication must be discovered per host; this table is not an
installed inventory. No server was installed by this audit.

| MCP/component | Provider/source | Tier | Trust | Preparation decision |
| --- | --- | --- | --- | --- |
| GitHub | https://github.com/github/github-mcp-server | CORE | OFFICIAL | Prefer supported host connector or remote HTTP endpoint; host manages OAuth/PAT and permissions. |
| Context7 | https://github.com/upstash/context7 | CORE | OFFICIAL | Documentation capability; remote endpoint and host authentication, no embedded API key. |
| Playwright | https://github.com/microsoft/playwright-mcp | CORE | OFFICIAL | Official npm package, Node prerequisite, project/user preparation only after approval; prepare only selected browser. |
| Chrome DevTools | https://github.com/ChromeDevTools/chrome-devtools-mcp | RECOMMENDED | OFFICIAL | Explicit selection; browser access and telemetry need disclosure; vendor supports Chrome, not every Chromium derivative. |
| Docker MCP Gateway | https://github.com/docker/mcp-gateway | RECOMMENDED | OFFICIAL | Optional MCP lifecycle/isolation alternative when supported Docker tooling already exists. Do not install Docker as a mandatory dependency. |
| Docker MCP Registry | https://github.com/docker/mcp-registry | RECOMMENDED | OFFICIAL | Catalog/discovery source, not a standalone MCP server; do not fabricate a connection or install command. |
| Figma | https://github.com/figma/mcp-server-guide | OPTIONAL | OFFICIAL | Vendor guide and remote endpoint; explicit selection and host authentication. |
| Firecrawl | https://github.com/firecrawl/firecrawl-mcp-server | OPTIONAL | OFFICIAL | External extraction service; API key remains in host secret storage. |
| Hugging Face | https://github.com/huggingface/hf-mcp-server | OPTIONAL | OFFICIAL | Host connector or remote HTTP; authentication evidence is separate from discovery. |
| Sentry | https://github.com/getsentry/sentry-mcp | OPTIONAL | OFFICIAL | Application errors/debugging only; explicit selection and safe host OAuth. |
| Supabase | https://github.com/supabase/mcp | PROJECT_SPECIFIC | OFFICIAL | Recommend only with Supabase project evidence; restrict project and read-only access where supported. |
| grep-mcp | https://pypi.org/pypi/grep-mcp/json | COMMUNITY | UNKNOWN | Installed configuration names `uvx grep-mcp`. PyPI 1.0.3 declares `galperetz/grep-mcp`; GitHub API and public repository URL both returned 404. Maintainer/repository availability is unverified. Never auto-install. |
| node_repl | Host-provided runtime | RUNTIME_PROVIDED | UNKNOWN | Detect only if the current host exposes it; no external MCP package is asserted. |

## Transport and evidence

Official documented remote endpoints inspected: GitHub
`https://api.githubcopilot.com/mcp/`, Context7 `https://mcp.context7.com/mcp`,
Figma `https://mcp.figma.com/mcp`, Hugging Face `https://huggingface.co/mcp`,
Sentry `https://mcp.sentry.dev/mcp`, Supabase `https://mcp.supabase.com/mcp`.
An endpoint or configured launcher does not prove connectivity. Context7's
current manual configuration documents API-key authentication. Auth requirements
are provider knowledge, not proof of this developer's login status.

Playwright documents `@playwright/mcp`; Chrome DevTools documents
`chrome-devtools-mcp`. Before an approved install, resolve/review and retain an
exact release instead of silently updating arbitrary latest versions. Chrome
DevTools documents usage statistics enabled by default and an opt-out flag.
Do not connect a browser containing private sessions without the user's scope.

Docker Gateway can consolidate discovery and secret handling, but its supported
host prerequisites and added runtime make it optional. Docker Registry remains
discovery metadata. There is no DevOps provisioning in this implementation.

## Existing implementation audit

- Source of truth synchronized to main `83e1c7296497c34267d85105f352b460136a09a7`.
- Six canonical plugin bundles; three tool registries, 13 entries total.
- Existing `tool-state.py` owns per-skill persistence and installation verification.
- Baseline suite: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`,
  318 tests, exit 0.
- No existing environment/doctor/bootstrap capability was found in this checkout.
- Reuse requires a non-persisting tool probe for doctor and dynamic owners.
- Existing helper ignores workspace cwd, misses project-local executables and
  returns CLI success for failed executed tools. These must be corrected at the
  shared helper boundary, with regressions, before bootstrap relies on it.
- Runtime state is already ignored under `plugins/*/skills/*/runtime-state/`.
- README and security skill contain a developer-specific MCP inventory. Replace
  the assertion of availability with library routing and runtime evidence.

## Data and authority boundary

Versioned library metadata is public knowledge. Host config, authenticated
sessions, local executable paths, developer preferences and custom MCPs stay
local. Diagnostics must not echo host config or credentials. Configuration
presence, installed package, available host tool, successful connection and
authentication are separate observations. Unverified capabilities cannot make
the environment READY.
