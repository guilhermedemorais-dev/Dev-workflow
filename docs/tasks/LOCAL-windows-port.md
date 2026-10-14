# Authorized native Windows port and reverse runtime repair

Revision5. User directly requested fixing all native Windows failures and investigating/repairing installed reverse-engineering capability on 2026-10-12. Earlier local preparation was authorized while GitHub was disconnected. On 2026-10-13 the user explicitly authorized commit and push of the tested changes. Publish a review branch and PR; do not merge or create a release.

Goal: native Windows10 supported execution rather than catalogs alone. Baseline595 has24 failures13 errors, current605 same failures. Preserve Linux regression. Existing platform routing work remains intact.

Execution list windows-tools: inspect all baseline failure identities, distinguish POSIX-only fixtures from runtime defects. Make authored Python tools and tests natively portable, preserving security invariants, existing APIs and shared canonical scripts. Implement safe Windows filesystem governance protections rather than removing race/symlink guards. Provide platform-appropriate mock executables and permissions tests; do not skip failures merely to pass. Allowed scripts/tool-state.py, github_governance.py, environment.py as required, related tests, Windows catalog entries and support docs AFTER evidence. Do not touch REA runtime (separate list).

Execution list reverse-runtime: read reverse-engineering-standard SKILL, rea-integration and vendor REA SKILL; inspect pinned source, runtime providers and requirements. Test Windows bootstrap/probe and real benign owned synthetic artifact analysis; compare Linux bootstrap when useful. Repair Node process launching/dependency execution safely on Windows. Allowed reverse-engineering-standard runtime/refs/docs/tests and catalog REA entries AFTER evidence. Do not port all third-party tools or pretend universal reconstruction; state installed, executing, authenticated and optional providers separately. No real third-party target analysis.

Acceptance: full native Windows suite zero failures/errors; Linux no regressions; reverse runtime actually bootstraps/probes and performs meaningful harmless synthetic analysis or exact verified blocker. Scoped install dependencies authorized by direct user request, never blanket install all providers. Independent QA/security review required. No proprietary code copying, secrets in repo or claims automatic rewrite prevents plagiarism. Local report/patch/readme/changelog reflect exact verified coverage, not generic certification.

Normative sectors: backend CLI/cache/filesystem/processes REQUIRED; tests REQUIRED; security REQUIRED (safe file mutation and subprocess launching); docs/observability REQUIRED; DB/UI/devops N/A (no infrastructure). Required sources: AGENTS.md, README.md, baseline/final logs in chat outputs, original platform contract and tools registries. Architecture limited to OS adapters in existing helpers, no duplicate runtime/framework. Runtime/behavior evidence tied to source/version. Human acceptance remote pending.

## Revision2 approved extension

User expressly requested adding native providers to Windows and confirmed no commercial licenses. Prepare portable official Ghidra12.1.4 and a suitable officialJDK21 under this task work/tools, validate official downloadchecksums/license/provenance, integrate into REA4.1 runtime and execute native static analysis on self-authored harmless PE fixture (do not execute target). No HopperWindows version exists; no IDAlicense/purchase. REA/MIT and Ghidra/Apache2 are separate licenses. Optional preexisting.NET compiler may build harmless owned managed fixture for static inspection. Download footprint about775MB from officialsources accepted within explicit installationrequest; no globalPATH/Java mutation. No newframework or optionalprovider blanketinstallation. Supportcatalog/docs promoted only after observednative evidence, upstreamWindowsGhidra remainsexperimental until integration proven. Outputreport distinguishes installation, probe, analysis and agentMCP registration.

## Revision3 bounded completeness

The user's request to fix all our Windows tools also covers authored SEO runtime bootstrap/probe. Inspect and verify the existing vendored BeyondSEO package with scoped native Python dependencies; no browser optional installation, no crawl of real websites. Fix only an observed compatibility bug. Runtime probe validates the local engine boundary, not all SEO operations or external websites. Add WINDOWS_SUITE routing status for observed Windows helpers, preserving exact OS/capability evidence. Local installed-plugin refresh from the validated checkout may use supported Codex CLI temporary source overrides after review/tests, preserving configured remote marketplace and all unrelated settings; backup affected artifacts first. No remote publication. Do not distribute machine-specific provider paths/dependencies as versioned source.


## Revision4 approved extension

User explicitly requests portable official Cutter/Rizin Windows preparation and free
IDA/Hopper options verification. Download official Cutter v2.5.0 Windows x64 under
work/tools, verify release SHA256 before extraction, run version and static analysis
on existing owned PE fixture, never execute target or launch GUI without need.
Add canonical reverse tool-registry and runtimeREADME supplemental CLI/GUI routing;
Cutter/Rizin are not REA provider IDs. Preserve prior revision3 Windows/SEO/local
installed-refresh scope. No purchases/accounts/proprietary-license acceptance.
Report exact local support and optional capabilities; independent QA remains required.

## Revision5 publication checkpoint

Publish the already-tested platform routing, native Windows fixes, REA/Ghidra and supplemental Cutter/Rizin integration, UTF8 fixtures, README and changelog through the authenticated GitHub connector. The local filesystem is writable again. Git CLI push credentials remain unavailable; publish through the authenticated GitHub connector and synchronize the local branch afterwards. Preserve code bytes except normal Git LF normalization. No new product implementation. Validation: Windows10 626 tests PASS, no failures/errors/skips, PythonUTF8mode0 cp1252; Ubuntu24.04.5 WSL2 native filesystem 626 tests PASS,16 skips(7 Windows-specific,9 Node unavailable). Independent bounded QA/Security receipts revision4 PASS. Never upload runtime-state, node_modules, provider binaries, tokens or local dependencies. Locked paths: main, configured desktop marketplace settings, secrets and third-party runtime artifacts. Final acceptance/merge remains with user. Previous revision notes describe historical local-only authorization and are superseded for branch publication by this checkpoint.
