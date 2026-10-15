# TASK-056: Start, use and release tool processes on demand

Revision1, direct user approval2026-10-14. Local implementation/isolated tests
only; preserve TASK054/TASK055 work, active config/cache/credentials and existing
processes. No publication or active notebook migration.

Implement lightweight MCP front-end for the selected native stdio integrations.
Cached verified tool schemas allow initialize/tools-list without starting heavy
servers. Explicit prime discovers schemas outside client startup and stops its
owned child. First actual tool call starts its server lazily. Retain one server
per owned front-end during a workflow, preserve browser state between calls,
explicitly release on workflow completion, with bounded idle cleanup as fallback.
Multiple active session leases cannot terminate each other's work. Never kill
by executable name or external PID, interrupt an in-flight call, silently restart
mutating calls, bypass approval, weaken schemas or hide unsupported MCP features.

Native Windows Job ownership or equivalent verified owned subtree cleanup;
Linux process groups without WSL wrappers. No heavy process during front-end
initialize/catalog inspection. Lightweight front-end necessarily stays available
while its client connection is alive; it is not zero total process overhead.
Defaults: no heavy integrations auto-start, essential set explicit/empty unless
selected. No unsupported claim that Codex itself provides lazy spawn/stop.
Reuse current native definitions and stable external runtime; no temporary/Codex
runtime path in generated production defaults. Approval/provenance retained.

Allowed: Environment internal lifecycle/proxy modules and existing native adapter
integration, owner SKILL/references/operations, targeted lifecycle tests, TASK056
docs/receipts/CHANGELOG. If new script entrypoint is necessary, route it through
existing owner/platform inventory with candid validation flags. No other edits.

Acceptance: process-count-zero heavy startup, lazy first-call, same PID/state
within workflow, shared lease last-user release, call-drain safety, idle cleanup,
crash/restart explicit, cache/source drift refusal, child/browser cleanup on exit,
permission annotations/source schemas preserved, no secrets in protocol/logs.
Run real native MCP workflow proof on Windows10 plus mock-fixture behavioral
tests and full suite; independent QA/security. Mark untested platforms/features.
Record actual process/evidence and remaining prerequisites; no production RAM claim.

Contract docs/execution/TASK-056.json revision1. Harness attests scope equivalence
and delegated local implementation/validation. Status LOCAL_UPDATE_TECHNICALLY_ACCEPTED:
709 full tests,26 lifecycle tests,28 native tests, independent QA/Security and
four source-bound Windows10 native lifecycle proofs passed. See
docs/receipts/TASK-056-harness.md for criterion-specific evidence and limitations.
Active configuration/cache application and publication were not performed.
