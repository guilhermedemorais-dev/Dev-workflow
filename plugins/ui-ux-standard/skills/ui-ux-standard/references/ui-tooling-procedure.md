## Registry and MCP Policy

Own browser, visual, and accessibility tooling through
`references/tool-registry.json`. Follow the shared `skill-owned-tools.md`
protocol: consult ignored per-skill runtime state, use its compatible fast
path, or detect, install from an official supported source when required,
verify, and persist. Revalidate after a failed visual check or fix. A cached
Playwright CLI does not prove browser binaries or the project's runtime are
ready; validate those in the active workspace before claiming coverage.

When a shadcn-compatible project is detected, prefer registry-aware discovery
instead of generating JSX from memory.

- If shadcn MCP is already available, use it to browse and search configured
  registries before installing candidate components.
- If MCP is unavailable, use official documentation, the project's shadcn CLI,
  or public source repositories as discovery fallback.
- Do not silently modify global MCP configuration or install a new global tool.
  Propose that environment change separately when it is actually needed.
- Treat community registries as third-party code. Inspect source and license
  before adoption.
- When `components.json` defines registries, inspect those project-approved
  registries before unrelated public sources.
