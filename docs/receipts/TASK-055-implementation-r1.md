# TASK-055 implementation receipt, revision 1

SKILL_RECEIPT: canonical Implementation and Environment SKILL read fully; AGENTS,
current TASK-055 native-implementation list, operations/state-and-consent and
Minimal Code Gate loaded. Authority is local implementation only. No cache,
active notebook config, remote repository or TASK-054 block was modified.

REUSE_INVENTORY: searched environment.py discovery/registered/plan/configure/
prepare/main and private atomic writer, library, existing environment tests.
Decision EXTEND Environment owner with internal native_mcp.py (no entrypoint/
CLI/shebang, no new external dependencies). Reuse existing private atomic helper,
CLI and consent lifecycle; retain Linux/WSL owner paths. Explicit architecture
requirement is a shared adapter for four integrations and five lifecycle operations.

MINIMAL_CODE_GATE: scoped cleanup N/A, no obsolete owner removed. Platform ladder
uses stdlib, existing Node/npm/browser; no dependency added to plugin. Shared root
is global config generation and native installation, not compatibility labels.
Affected consumers CLI prepare/operations/Skill and behavioral tests updated.
No arbitrary cached executable commands accepted; commands come from reviewed
pinned providers. Preserve credentials, validation and architecture. Exceptions
and installer stdout are sanitized. Unknown/complex wrapper/config cases require
manual normalization. Official native Claude installer is manual handoff; MCP
runtime proofs are independently owned. Active migration explicitly not performed.

Developer validation: 28 native behavioral tests PASS on Windows, including CRLF
byte-exact backup/rollback, secret sentinel preservation/non-disclosure, global/
plugin alias dedup, fingerprints, late-edit rollback, exact selected installation,
Chrome browser/engine constraints, conditional Playwright, Linux/WSL detection,
secret-bearing shell wrapper rejection and backup symlink rejection, structured inline environment precedence, browser-path
replacement with preserved flags and unknown wrapper positional-option refusal.
Existing Environment Bootstrap regression suite: 65 tests PASS.
Full suite, independent QA/Security and actual MCP runtime proof are pending owner
receipts. No remote mutations, no merge/deploy/publication, no installed cache edit.

Review REWORK addressed: actual WSL -- delimiter, empty environment tables,
exact reviewed n8n bin, runtime/browser/entrypoint byte fingerprints, durable
explicit executable/browser overrides and conditional Chrome Edge candidate.
28 targeted tests PASS after fixes; final full-suite/QA/Security remains pending.

Final review fixes: strict known executable aliases recognized across WSL wrappers;
Claude executable replacement invalidates approval; rollback rechecks config after
backup read. Tests reproduce all three failures. Check/replace race requires
serialized writers and is documented, not claimed impossible.

Final discovery routing: invalid explicit Node override fails closed; Windows
legacy plan now emits native-plan marker/method instead of npx configure action;
doctor reports sanitized configured transport separately from native readiness.

Integration REWORK: Chrome real dual-bin metadata selects known MCP key; n8n
./ relative entrypoint is normalized safely. Owner-bundled migration policy
replaces root-only Skill dependency; root documentation links canonical policy.
