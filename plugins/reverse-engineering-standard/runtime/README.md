# Reverse Context Runtime

This directory keeps the reverse-engineering execution surface out of the LLM prompt.

- `rea-capability-catalog.json` mirrors the context-producing REA 4.1.0 tool families.
- `reverse-context-gateway.mjs` is the small Harness-facing gateway.
- `rea-agents` 4.1.0 is stored as a vendored tarball inside this repository and is the execution engine.
- The canonical specialist methodology remains `reverse-engineering-standard`.

Bootstrap the vendored runtime inside this directory with the Environment Bootstrap only after approval:

```bash
npm run bootstrap
node reverse-context-gateway.mjs probe
```

The bootstrap verifies the committed tarball SHA-256 before installation. It does
not fetch `rea-agents` from npm or GitHub. Transitive Node dependencies and
optional external analysis engines remain normal environment dependencies.

The LLM should not receive all 130 REA tool schemas. It asks the Harness for a reverse-engineering capability; the gateway selects/invokes the lower-level runtime surface.

The upstream runtime is MIT. The repository vendors the published executable
package, checksum, package inventory, skill/reference license and provenance.
Updating REA is an explicit vendoring operation; normal execution no longer
depends on the upstream REA repository or the `rea-agents` package remaining
available remotely.
