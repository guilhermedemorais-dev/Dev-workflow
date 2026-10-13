# LOCAL-windows-port reverse-runtime receipt

Task/list: LOCAL-windows-port / reverse-runtime, contract revision 3. Local-only
implementation authorized; remote Issue/PR/publication pending. Independent bounded review recorded separately.

SKILL_RECEIPT: dev-implementation-standard; reverse-engineering-standard;
rea-integration.md; bundled vendor/rea/SKILL.md read completely. Required boundaries:
owned harmless target, static evidence, no third-party execution or rewrite claims.

REUSE_INVENTORY: existing install-local-runtime.mjs and gateway run helper extended.
MINIMAL_CODE_GATE: process-launch.mjs shared by bootstrap and gateway; no duplicated
REA implementation or global runtime. Canonical tarball unchanged.

Changes: direct Node JavaScript entrypoints replace npm.cmd/rea.cmd execution;
existing trusted npm entrypoint discovered beside Node/PATH; explicit trusted npm/pnpm
JS override supported; no shell interpolation. Bootstrap checks tarball checksum,
disables install scripts, installs locally. pnpm-lock.yaml records dependency integrity.
Probe distinguishes runtime_available from broad provider/environment healthy and
returns structured malformed/missing-runtime failures.

OBSERVED on win32 x64, Node 24.19.0: initial bootstrap failed npm absent. Restored via
existing scoped pnpm 11.25.0 entrypoint; 132 dependencies installed, no global install.
Tarball SHA256 d4859719e27cd405daea45f88aed60b5136df628da2290d9e5e299d09f7a711c.
MCP client/server 2.3.1 registry metadata both present; not an unavailable pin.

Owned synthetic JavaScript fixture (2 files) statically analyzed successfully through
the gateway. Provider rea-javascript-application, REA 4.1.0. One JS file parsed,
46 AST nodes visited, 2 findings, zero parse failures, no target execution/network.
Evidence ev_519e3f103dba30ac2e6630cbf6f15145c18ec5cb668b946304e4db8a1f6cefda.
Artifact SHA256 c87e8145fc0bc1474fc7d7875f63119313c2efc833083edf36c89451c13d76e2.
Raw result: chat outputs/rea-windows-owned-analysis.json.
Doctor actually launches; broad health false because optional Hopper/Ghidra/IDA and
client/skill registrations missing. JS analysis remains available. MCP was not
registered or authenticated by this work. Raw outputs/rea-windows-probe.json.

Developer tests: five process launch regression tests pass, including literal spaces/
metacharacters, malformed doctor JSON, missing runtime, direct package manager and
optional-provider failure vs runtime availability. outputs/rea-windows-launch-tests.txt.
Linux comparison: WSL startup returned CreateInstance/ERROR_TIMEOUT on this attempt;
no Linux regression or macOS verification claimed here. Parent owns full suite.

Primary sources checked: https://github.com/morluto/rea and npm registry package
metadata https://registry.npmjs.org/@modelcontextprotocol/client/2.3.1 and corresponding
server/2.3.1. REA is cross-platform with provider-dependent capability, not Windows-only.
Native binary decompilation, managed/APK/firmware, passive runtime observation are
unvalidated in this host; selected optional providers required. Independent review
pending. No merge/deploy/publish or installed plugin replacement. Token usage unavailable.

## Revision 2 provider extension

User expressly authorized native Windows provider preparation and has no commercial
licenses. No IDA or Hopper installed. Official portable Ghidra 12.1.4 and Eclipse
Temurin JDK 21.0.12.1+1 prepared under chat work/tools, not inside plugin distribution.
DownloadSHA256 checked before extraction; archive member paths constrained to tools root.
Ghidra archive569649598bytes SHA256ddac49f903da9d5bac833e5cc79395098b9c33cfd3279be5f31bd00387d2d4db.
Temurin archive205073461bytes SHA256f9d6e191ab098c0d416e7d588a24420a8621cd2f4720dab2459b8b7b2d2d8b4e.
Official sources https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest
and https://api.adoptium.net/v3/assets/latest/21/hotspot?architecture=x64&image_type=jdk&os=windows&vendor=eclipse.
Ghidra Apache2 and JDK license preserved in extracted archives; REA remains MIT.
REA source GhidraInstallation.js requires exactGhidra12.1.4+Java21, both observed.

Once-only config runtime-state/providers.json holds absolute provider paths; ignored,
not part of update, no healthcache or global environment mutation. Existing upstream
setup inspected: focuses agent registrations and optionalHopper, so it was not run.
Gateway validates configschema+allowedkeys+existingabsolutedirs, env explicitly wins.
Existing absolute Windows target arguments normalized with Node resolve because REA
native Win32 bridge rejects slash-drive paths. Initial target_unavailable and NTFS
boundary failure outputs superseded after compilation/pathcorrection; final outputs
retain successfulresults. Developer regressions now8/8pass (two configtests+pathtest).

Owned .NET fixture authored and compiled with preexisting Framework64csc (no execution).
inspect-managed-artifact returned ev_29d0bdb1f1484103977bee0ba8ca4b05c1e2f31a55fc5602fc4683c027fe1b06,
SHA813eb0adf9e5355548ead8fa23bfb365719d0095d8d563b83b5ba12ad0e326d6,
providerrea-dotnet-static. outputs/rea-windows-managed-analysis.json.

Owned minimal1024-byte nativePEx64 authored with entrypointmachinecode mov eax,42;ret,
never executed. Ghidraactuallyimportedandanalyzed it through authenticatedREAWindows
provider, exit0, ev_fd1e9e5f3eb8c6f451a03885250af8e1a0a9993cbb5330e95d230e8faac7cd60,
SHA6d3eea26039d6f7451a1af38995e334a664996330c8d36fb34316ae594014a3d.
outputs/rea-windows-ghidra-native-analysis.json and rea-windows-ghidra-doctor.json.
Scoped Ghidradoctorhealthytrue; broaddoctor stilldoesnotestablishagentMCPregistration.
Native support limited to this actualx64PE fixture, not fullWindows/Linux/macOSmatrix.

Focused native decompile also exit0, providerghidra12.1.4, operationprocedure_pseudo_code,
ev_730e1d9a1d20b52428427452746d85d2f9bedebd6d6576b53f6c11637a7187c0.
OBSERVED pseudocode entry(void) returns0x2a (42), matches selfauthoredfixture bytes.
outputs/rea-windows-ghidra-decompile.json. Do not call this originalsource.
Upstream returned limitations: WindowsGhidraP0 supports approved native x86-64 PE
apps, Windows10+, packagedx64addon/localNTFS; DLL/managed/hostile/sensitive/mutable
path targets unsupported. Separate.NETstatic provider alreadytested above.
Eightlaunchregressions pass. No optionallicensedtoolsinstalled, no target execution,
no systemwidePATH/config mutation, no agentMCP registration claimed.
