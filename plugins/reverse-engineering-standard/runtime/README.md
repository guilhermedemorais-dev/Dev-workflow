# Reverse Context Runtime

This directory keeps the reverse-engineering execution surface out of the LLM prompt.

- `rea-capability-catalog.json` mirrors the context-producing REA 4.1.0 tool families.
- `reverse-context-gateway.mjs` is the small Harness-facing gateway.
- `rea-agents` is version-pinned to 4.1.0 as the execution engine.
- The canonical specialist methodology remains `reverse-engineering-standard`.

Install runtime dependencies inside this directory with the Environment Bootstrap only after approval:

```bash
npm install
node reverse-context-gateway.mjs probe
```

The LLM should not receive all 130 REA tool schemas. It asks the Harness for a reverse-engineering capability; the gateway selects/invokes the lower-level runtime surface.

The upstream runtime is MIT. The repository also vendors the upstream skill/reference license and provenance. A future full source mirror can replace the npm package without changing the gateway contract.
