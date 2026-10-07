# REA Integration

REA (morluto/rea, MIT) is the preferred external reverse-engineering runtime
for this skill. It is not vendored into the Engineering Harness.

## Boundary

The Harness and this skill own:
- target authorization and scope;
- methodology and evidence interpretation;
- distinction between observation, inference and unknown;
- Task/sector ownership;
- reconstruction decisions;
- receipts and final validation.

REA owns its own MCP/CLI implementation and analysis adapters.

## Capability discovery

Do not assume every REA tool is available. Detect the installed CLI first:

```bash
rea --version
```

Use scoped diagnostics only when needed:

```bash
rea doctor --client codex --json
rea doctor --provider ghidra --json
```

Do not run full diagnostics before every investigation when the required
capability is already known healthy.

## Routing

Prefer the smallest matching REA surface:

- extracted JavaScript/Electron/ASAR: static JavaScript application analysis;
- native binary/library: native provider through REA;
- managed .NET assembly: managed artifact inspection;
- Android APK: Android package inspection;
- firmware image: firmware region inspection/extraction when explicitly needed;
- browser/Electron runtime: passive runtime observation only when static evidence
  is insufficient and the target is authorized.

Provider/engine selection belongs to the concrete target and host. Do not install
or select Hopper, Ghidra or IDA merely because REA supports them.

## Evidence contract

Every conclusion must be classified:

- OBSERVED: directly supported by returned REA Evidence or inspected artifact;
- INFERRED: reasoned from observed facts;
- UNKNOWN: not established by current evidence.

Record relevant REA evidence identifiers, target revision/hash when available,
provider/tool actually used, limitations and unresolved gaps in the existing
Engineering Harness EXECUTION_RECEIPT.

Static analysis must never be described as runtime observation.

## Reconstruction handoff

When the objective is to reproduce a feature in the user's own software:

```text
reverse-engineering-standard
  -> observed behavior + evidence + unknowns
  -> sdd-spec-factory
  -> dev-implementation-standard
  -> qa-testing-standard
  -> security/ui/devops gates as applicable
```

Do not copy proprietary source text or assets. Reconstruct behavior from observed
interfaces, behavior, protocol, state transitions and independently written code.
