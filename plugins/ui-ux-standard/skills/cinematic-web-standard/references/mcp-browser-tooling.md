# MCP and Browser Tooling

Use this reference when an agent needs browser automation, exploratory QA, or performance diagnostics.

## Selection Rule

Prefer the repo's existing test tooling first. Add MCP only when the agent benefits from an interactive browser loop.

### Playwright Tests / CLI

Prefer for repeatable acceptance checks, CI, deterministic regression tests, and high-throughput coding-agent workflows.

### Playwright MCP

Use when the agent benefits from persistent browser context and structured page interaction during exploratory work.

Official package/repo:

- https://github.com/microsoft/playwright-mcp
- npm package: `@playwright/mcp`

Generic MCP config example:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

The Playwright project itself notes that CLI + skills can be more token-efficient for coding agents, while MCP is useful for persistent exploratory loops. Choose based on the task rather than habit.

### Chrome DevTools MCP

Use for:

- performance traces
- network inspection
- console/source-map debugging
- runtime screenshots/inspection
- browser performance diagnostics

Official repo:

- https://github.com/ChromeDevTools/chrome-devtools-mcp

Generic MCP config example:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

For basic headless usage, the upstream server also documents a slim/headless configuration. Do not assume slim mode exposes every performance tool.

## Security Rule

A browser MCP can inspect page content, console/network data, cookies/session-visible content, and authenticated pages depending on how it is launched. Do not expose secrets or personal/client data to an MCP session unless the environment and authorization model explicitly allow it.

## Do Not Duplicate Tooling

Do not run Playwright MCP and Chrome DevTools MCP for the same simple navigation/assertion task. Use:

- Playwright for interaction flows and repeatable UI acceptance
- Chrome DevTools for deep performance/network/runtime diagnostics

## Building a Custom MCP

Only build a project-specific MCP server when stable project capabilities need to be exposed as agent tools/resources/prompts. Do not create one merely to wrap shell commands.

Official TypeScript SDK:

- https://github.com/modelcontextprotocol/typescript-sdk

As of the 2026-07-28 MCP specification line, the official TypeScript SDK v2 uses split packages including `@modelcontextprotocol/server` and `@modelcontextprotocol/client`.

## Suggested Cinematic QA Loop

1. Start page with cold cache.
2. Use Playwright (test/CLI/MCP) to traverse the full narrative forward and backward.
3. Exercise desktop and mobile viewports.
4. Toggle reduced motion.
5. Use Chrome DevTools MCP for a performance trace on the heaviest chapter.
6. Inspect frame/media requests and confirm progressive loading.
7. Inspect console errors and memory growth.
8. Save evidence in the task/PR report.
