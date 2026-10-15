# TASK-056 implementation receipt, revision1

Scope: approved local lifecycle-implementation list in
`docs/execution/TASK-056.json`; no active configuration/cache migration or remote
publication. CODE_COMPLETE is not independent QA/Security acceptance.

## Skill receipt and reuse inventory

Read completely: repository AGENTS, implementation SKILL, Environment SKILL,
Minimal Code Gate, required native_mcp.py owner and active contract. Read repository
README/workflow pipeline and existing Environment private atomic writer.
Reuse searched: native transport definition/install/prepare/apply/rollback,
existing global/plugin identity check, atomic/private permissions, owned runtime
route/catalog and existing tests. Decision EXTEND Environment's approved native
owner; CREATE one internal stdlib MCP front-end because the existing direct
transport cannot answer metadata while leaving its heavy process stopped.
No third-party dependency or independent installer/catalog entrypoint added.

## Implemented behavior

- Native CLI opt-in prime/plan/apply; ordinary direct routes unchanged.
- Explicit selected native provider priming validates initialize/tools/list once,
  closes owned tree and writes private cache. Generation never primes at startup.
- Cache-bound lightweight stdio initialize/list; upstream schemas/annotations
  unchanged, control tools distinct. Lazy first real tools/call starts upstream;
  related workflow calls retain PID/browser state.
- Default workflow and random explicit shared leases; final release waits for
  in-flight calls, then closes only owned processes. Idle fallback expires
  abandoned leases, never kills active calls. EOF rejects queued mutations.
- Windows suspended creation, NO_WINDOW, private JobObject assignment before
  resume, kill-on-job-close descendants; POSIX own process-group fallback.
  Stdio closes first with bounded grace period. No arbitrary PID input.
- Private cache ACL/symlink/size/digest validation, streaming runtime hashes,
  approved native source/options/config/environment binding and dynamic
  global/plugin redundancy checks. Sanitized errors and discarded upstream stderr.
- Bounded16 concurrent admissions; serialized upstream requests, no automatic
  replay of failed or partially mutating calls. Unsupported callbacks fail closed.
  Inventory notifications trigger read-only exact schema recheck; harmless
  unchanged snapshots retain state, changed snapshots require explicit re-prime.
  Pending notifications are checked before the next mutation. Newer clients
  negotiate the supported 2024-11-05 protocol, client acceptance remains required.

## Developer evidence

Windows command (bundled interpreter is QA-only, never generated production path):

`C:/Users/teste/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -m unittest discover -s tests -p test_mcp_lifecycle.py -v`

Latest run on current implementation:
26 tests, OK, exit0,7.646s. Scenarios include owned child/descendant cleanup,
unrelated process preservation, original schema/arguments, same workflow PID,
shared final release, in-flight drain/idle, abandoned lease, runtime/environment
drift, private ACL/digest, persisted partial-mutation no-replay counter, concurrent
failure plus queued call, unsupported sampling request, inventory invalidation,
and blocked pre-admitted closed/invalidated mutation, harmless listChanged with
persisted counter no replay, and actual stdio newer-protocol negotiation with
metadata discovery retaining STOPPED heavy process state.
Generated lifecycle transports are recognized through their canonical internal
module and reviewed provider manifest even under arbitrary global/plugin aliases;
both duplicate routes fail before launch. Malformed owned transports fail closed.
Inherited provider credentials are restricted through the canonical provider
mapping. Browser providers do not inherit n8n/Claude secrets; explicit approved
env/env_vars are retained, relevant credential drift invalidates the binding,
and unrelated provider credential drift does not.

Existing direct-native suite:28 tests, OK, exit0,0.537s before subsequent lifecycle
changes; Harness/QA must repeat full suite on final source. `git diff --check`
passed on the tested snapshot. Real per-provider protocol/workflow proof is owned
by Harness/independent QA and is not claimed by these simulated fixtures.

## Minimal-code gate

Reused/extended: NativeMCP and Environment action/consent/config owner; private
atomic/permission helper. New unit: one internal stdio front-end shared by four
concrete reviewed providers. No duplicate source/config policy. No code deleted
outside scope. Preserved direct routes, pinned native provider validation,
credentials/settings and backup/rollback authorization boundaries. Streaming
hashing avoids large temporary executable buffers. Cleanup criteria concern only
newly owned trees, never existing servers/distributions. Meaningful behavioral
tests verify mutations/processes, not prose mirrors.

Intentional limits: lightweight Python process remains; cached tools-only
protocol2024-11-05, optional resources/prompts not exposed, no runtime approval
callbacks/sampling/tasks translation; no cross-client shared process daemon.
Context/session/browser handles do not survive stop. Source/environment drift
requires approved explicit reprime. Production needs stable external Python3.11+;
no runtime install/migration was performed. Desktopclient end-to-end, external
API/model auth, macOS and generalized RAM-saving claims remain NOT VALIDATED here.

Changed files: Environment scripts/native_mcp.py, scripts/environment.py,
scripts/mcp_lifecycle.py, SKILL.md, references/tool-lifecycle.md; docs/tool-lifecycle.md,
this receipt and tests/test_mcp_lifecycle.py. Other owners update shared Task,
CHANGELOG and independent receipts. Remote changes none, code changed yes,
publication NOT_PUBLISHED. Runtime/API token usage: NOT_AVAILABLE.
