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

The bootstrap selects pnpm when `pnpm-lock.yaml` exists and uses
`pnpm install --frozen-lockfile --ignore-scripts`, even when launched through
`npm run bootstrap`. Otherwise it requires `package-lock.json` and uses
`npm ci --ignore-scripts`. A missing lockfile or an explicit manager that
conflicts with the selected lockfile fails before installation. Install the
required package manager beforehand; bootstrap never installs it globally.

The bootstrap verifies the committed tarball SHA-256 before installation. It does
not fetch `rea-agents` from npm or GitHub. Transitive Node dependencies and
optional external analysis engines remain normal environment dependencies.

The LLM should not receive all 130 REA tool schemas. It asks the Harness for a reverse-engineering capability; the gateway selects/invokes the lower-level runtime surface.

The upstream runtime is MIT. The repository vendors the published executable
package, checksum, package inventory, skill/reference license and provenance.
Updating REA is an explicit vendoring operation; normal execution no longer
depends on the upstream REA repository or the `rea-agents` package remaining
available remotely.

## Native process launch and prerequisites

Bootstrap and the gateway execute JavaScript entrypoints through the current Node
executable with `shell: false`. Windows `.cmd` wrappers are not executed.
Install a supported Node/npm distribution, then run `node install-local-runtime.mjs`.
With an existing trusted pnpm installation, set `DEV_WORKFLOW_PACKAGE_MANAGER_JS`
to its absolute `pnpm.cjs` entrypoint before bootstrap. This selects an existing
package manager matching the committed lockfile; it does not install a global package manager or modify Codex MCP
configuration. Dependency lifecycle scripts remain disabled.

REA is not Windows-only. Analysis availability depends on target and installed
providers: JavaScript static analysis requires no native decompiler; native
analysis requires a compatible selected Ghidra/IDA/Hopper provider; Android code
analysis requires JADX/Java; firmware extraction uses Linux Binwalk/Unblob.
Installing this skill alone does not install these providers or connect MCP.
Observed behavior supports an independent specification, not an automatic
plagiarism-free rewrite of arbitrary software.

## One-time provider configuration

For a prepared portable Ghidra installation, save machine-specific paths once in
`runtime-state/providers.json` next to this gateway. This ignored local file is
configuration only; provider health is always obtained from REA, not cached here.
Explicit environment variables override these paths. Only existing absolute
`GHIDRA_INSTALL_DIR` and `JAVA_HOME` directories are accepted:

```json
{
  "schema_version": 1,
  "paths": {
    "GHIDRA_INSTALL_DIR": "C:\\Tools\\ghidra_12.1.4_PUBLIC",
    "JAVA_HOME": "C:\\Tools\\jdk-21"
  }
}
```

REA 4.1.0 requires exactly Ghidra 12.1.4 and JDK 21. Download portable archives
from the official NSA Ghidra release and a trusted JDK vendor, verify published
checksums before extraction, and preserve their separate licenses. Do not bundle
machine-specific directories, provider binaries, or local configuration into a
plugin update. Check readiness with `node reverse-context-gateway.mjs cli doctor
--provider ghidra --json`. Hopper has no Windows version; IDA is separately
licensed and is not installed by this plugin.

This Windows preparation has observed JavaScript and managed .NET static analysis.
Native Ghidra support must be assessed through actual target analysis, not only a
passing installation/doctor check. No automatic universal reconstruction is claimed.

Observed native Windows validation: REA + Ghidra 12.1.4 analyzed a self-authored x64
PE fixture and recovered pseudocode `return 0x2a` (42). This establishes the tested
native path, not every executable format. Upstream Windows Ghidra P0 supports
approved native x86-64 PE applications on Windows 10+, local NTFS and the packaged
x64 native addon. DLL, managed, hostile, sensitive and mutable-path targets are
outside that provider's admitted boundary. Managed .NET inspection uses the
separate REA managed static provider. These limits must remain visible in reports.

## Supplemental Cutter/Rizin fallback

Cutter 2.5.0 and its bundled Rizin 0.9.1 are optional supplemental local tools.
They are registered in the specialist tool-registry, not advertised as REA provider
IDs. Prefer the REA gateway for its admitted target; use Rizin static inspection
when that concrete supplemental capability is needed. Cutter executable `--version` was
verified; GUI behavior was not validated.

Prepare an official portable Windows x64 Cutter release once, check its GitHub
release SHA256 before extraction, and detect `cutter` and `rizin` through the existing
Harness tool-state helper. Retain the resulting specialist runtime-state on updates.
To reuse the saved portable executable, prepend its known directory to PATH only
for the invoked process and call tool-state resolve/run. This preserves executable
identity checks; it does not globally change PATH, reinstall or ask for approval
on every task. A stale/moved installation still needs explicit repair.

Verified static Rizin sequence on an owned x64 PE fixture (never use `-d` here):

```text
rizin.exe -A -q -c "e scr.color=0;s 0x140001000;pd 2" <owned-fixture.exe>
```

Its bundled rz-ghidra plugin requires its portable Sleigh directory explicitly:

```text
rizin.exe -A -q -c "e ghidra.sleighhome=<portable-directory>/lib/rizin/plugins/rz_ghidra_sleigh;s 0x140001000;pdg" <owned-fixture.exe>
```

Both produced the owned fixture's return value 42. `pdg` is the plugin's command;
`pdd` is not supported. Archive version and tested binary formats do not establish
all Rizin/Cutter capabilities or Linux/macOS validation. Cutter is GPL-3.0; Rizin
uses LGPL-3.0 with separately licensed components. Keep each tool's license and
provenance. No provider binaries are redistributed in this plugin.

IDA Free exists but is non-commercial and lacks IDAPython/SDK, so it is not a
replacement for licensed IDA automation in this business workflow. Hopper's demo
is for macOS/Linux and has no Windows build. Neither is installed by this preparation.

On this portable Windows build, verify Cutter with the native Qt environment.
Do not force `QT_QPA_PLATFORM=offscreen` or `minimal` for `--version`: those probes
hang in the tested package, while the normal Windows platform exits immediately.
