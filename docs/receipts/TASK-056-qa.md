# TASK-056 independent QA receipt

EXECUTION_RECEIPT: task TASK-056, contract revision 1, list lifecycle-qa,
sector QA, phase validation, mode change-validation. QA_STATUS: PASS bounded to
the local approved adapter and executed evidence below. State: COMPLETED for this
QA checkpoint only; no publication, installed-cache change or active migration.

## Invocation, sources and guardrails

Harness delegated independent QA and attested current local Task/JSON normative
equivalence, with direct user authorization for implementation and validation.
No remote Issue was invented. Inputs used: docs/execution/TASK-056.json revision1;
canonical Environment SKILL, scripts/native_mcp.py and scripts/mcp_lifecycle.py;
QA SKILL in the installed bundle and references/test-strategy.md, read fully;
canonical Harness references/minimal-code-gate.md; developer tests/receipt;
docs/receipts/TASK-056-runtime.md and TASK-056-runtime-evidence.json.
SKILL_RECEIPT: qa-testing-standard LOADED; applied independent execution,
risk-based behavioral oracles, mock/real boundary separation, minimal-code review
and evidence-bounded acceptance. No conditional unrelated source was required.

QA did not implement or weaken product tests. Early findings went to the owner:
initialize source validation, persisted partial-mutation no-replay counter,
in-flight idle retention, protocol-version negotiation and inventory notification
behavior. Existing TASK-054/055 work and real clients remained preserved.

## Independently executed final checks

Windows commands used the existing bundled Python3.12 QA interpreter only:
`C:/Users/teste/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`.
This is not a generated production interpreter path.

| Arguments / command | Result | Duration |
| --- | --- | ---: |
| -m unittest discover -s tests -p test_mcp_lifecycle.py | 26 tests PASS, exit0 | 8.681s |
| -m unittest discover -s tests -p test_windows_native_mcp.py | 28 tests PASS, exit0 | 0.609s |
| -m unittest discover -s tests | 709 tests PASS, exit0 | 56.566s |
| git diff --check | PASS, exit0 | not material |

Earlier complete 703/705/707 green suites were intermediate snapshots, not final
acceptance. They were rerun after actual-provider findings and source changes;
the 709-test result supersedes them. Historical runtime failures remain described
in the runtime receipt, rather than erased by later success.

Behavioral oracles cover: cached metadata without heavy launch and exact upstream
schemas/annotations; lazy first call and related-call PID reuse; owner-child and
descendant termination; unrelated-process survival; default/shared workflow final
release; release during active call; idle expiration with no in-flight termination;
unknown/expired sessions; stale runtime/environment/manifest refusal; private cache
integrity; partial mutation persisted exactly once across disconnect; queued-call
failure isolation and no replay; disconnected/invalidated queued mutation rejected;
unsupported server approval request refusal; harmless notification exact-inventory
recheck versus actual inventory invalidation; newer protocol negotiation; aliased
global/plugin duplicate refusal; provider credential isolation and explicit env
override/env_vars preservation. These fixture checks prove those local invariants,
not an external service integration.

## Actual native evidence independently reviewed

Harness executed real selected-provider prime and stdio proxy operations on
Windows10 Home Single Language 22H2 build19045.6466 with Node24.22.0, Edge155,
PlaywrightMCP0.0.83, ChromeDevToolsMCP1.10.1, n8nMCP2.93.0 and ClaudeCode2.1.300.
QA inspected the sanitized JSON and runtime receipt, distinct from independently
running the suites. All four records show cached initialize/list/status with zero
heavy children, workflow PID reuse, STOPPED after finish, no remaining observed
owned heavy PIDs and no owned WSL process. Operations were owned-loopback browser
navigation/snapshot, public n8n documentation/search and Claude Read of an owned
fixture file. No model request or external n8n instance mutation was claimed.

Source hashes before/after the real proof match the independently tested files:

- mcp_lifecycle.py: 244707ee30eb3178daf821b7446b2c98426a1ae452a8e744214e18de3dec501b
- native_mcp.py: 0f73bb2cb2c5bd52690d85fd4739101d45f295455eb664db1470f822ca66841f
- test_mcp_lifecycle.py: 16cb48b9cd6f8e9658c06ce25edbbb754098df2a3433aa1d706566a79dccb7a0

Active configuration SHA before/after was identical. Front-end plus conhost stayed
approximately32MiB per connected integration; heavy subtrees were removed after
finish. Scoped working-set snapshots are not a controlled whole-machine savings
benchmark and do not attribute existing vmmem to this adapter.

## Minimal-code review and disposition

The change extends Environment's four actual native consumers, reusing native
provider definitions, install/config/backup/rollback owner and private state helper.
One shared stdlib front-end supplies a capability direct transports lacked.
No parallel installer, new dependency, unrelated deletion or global daemon added.
Direct routes and required permission boundaries remain; full suite includes
native/Linux/WSL routing regressions. Security owns its separate review receipt.

Outputs produced: this independent QA receipt and executed check results.
No blocking functional finding remains in the tested local scope. Intentional
limits: lightweight front-end persists for discovery; explicit workflow completion
and bounded idle fallback control heavy lifetime; state is lost after stop;
cross-client process sharing is not implemented. Unsupported callbacks fail closed.

NOT_VALIDATED: active Codex-client migration/approval UI, external stable production
Python setup, macOS/POSIX real lifecycle execution, authenticated n8n instance,
Claude model/auth and whole-machine RAM savings. Playwright/Edge Windows10 support
remains conditional local evidence, not vendor certification. No installed plugin
was changed. Next safe action: Harness reconcile required owner receipts and
deliver the local update; application/publication requires separate authorization.
