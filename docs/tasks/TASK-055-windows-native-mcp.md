# TASK-055: Windows-native MCP lifecycle

Revision1, authorized by direct user request2026-10-14. Local-only delivery;
do not migrate active notebook Codex configuration, update installed caches,
publish/merge, remove Linux distributions/data or stop existing servers.
Base7f36b78; preserve every existing TASK054 uncommitted change.

Scope: Windows-native discovery/install plans/config generation and staged
migration with backup/rollback, MCP proof, platform-specific launch and dedup
global/plugin registrations. Detect Windows native vs WSL vs Linux, preserve
Linux/WSL routes and explicit selections. Verify official package identity and
requirements; upstream support and actual Windows10 validation are distinct.
Reuse stable runtimes/browser; reject transient/Codex internal runtime defaults.
Explicit selected MCPs only; no promise that Codex lazily starts server processes.
Preserve credential/env/preferences without printing values. WSL fallback requires
technical justification or explicit user choice. Configuration application must
be separate, explicit, fingerprint-bound, backed up and reversible.

Allowed: dev-environment-standard owner SKILL/references/environment.py and one
internal native adapter module; MCP library metadata; relevant environment tests,
new tests/test_windows_native_mcp.py, migration docs and TASK055 records/CHANGELOG.
Protected: active Codex/plugin caches/settings/credentials, other tasks/plugins,
existing TASK054 work, Linux data and external systems. No remote publication.

Read-only diagnosis may read sanitized command identity/parent topology and
memory. Isolated native validation may prepare selected package/runtime assets
in a persistent user-scoped validation prefix and run owned temporary MCP/browser
processes; no PATH/registry/global config changes or control of existing PIDs.
Only public package downloads and self-owned fixture/documentation operations;
no secrets transferred or external n8n/Claude account calls without authorization.

Acceptance: official support/requisites recorded per package; native launch
uses real Windows executables/paths, no wsl.exe or /home; generated config preserves
existing env/preferences and detects duplicate integration across host/plugin;
apply requires explicit approval, source fingerprint and backup, rollback rejects
later unrelated edits. Selection and unsupported/conditional compatibility explicit.
Behavioral tests cover platform detection, native command, stable discovery,
dedup/selection, secret preservation/redaction, migration stale/backup/rollback,
legacy Linux/WSL behavior. Actual Windows10 handshake+representative operation
per runnable tool, owned-process topology and comparable memory observations;
all missing runtime proof is NOT_VALIDATED. Active config digest unchanged.
Independent QA/security and full structural suite plus diffcheck required.

Contract docs/execution/TASK-055.json revision1; Harness attests local scope
equivalence. Status VALIDATED_LOCAL_ONLY. Issue/Projects NOT_PUBLISHED_USER_SCOPE.

Final evidence: docs/receipts/TASK-055-harness.md reconciles owner receipts.
28 focused tests and683 full-suite tests PASS43.263s; QA/Security independent
PASS; actual generated native MCP commands passed all four representative
operations. Active Codex config hash unchanged. Production RAM savings, active
rollout, external n8n API/Claude model authentication and fresh Linux/WSL
handshakes NOT_VALIDATED. Existing TASK054 changes preserved. No commit/push.
