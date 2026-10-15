# TASK-056 security receipt, revision1

SECURITY_STATUS: PASS for the bounded local lifecycle change. This is not human
acceptance, production approval, publication or desktop-client certification.

## Authority, methodology and scope

Execution contract: `docs/execution/TASK-056.json`, revision1,
`lifecycle-security`. Harness directly attested current local Human Task/JSON
normative equivalence and unchanged acceptance criteria. User approved local
implementation/validation; active configuration, installed caches, credentials,
existing servers and remote publication are protected. No protected state changed
by this reviewer. Only this receipt was written.

SKILL_RECEIPT: security-standard read fully. Loaded review-pipeline,
false-positive-validation, finding-standard, stack-profiles and Harness
context-routing. Mode CHANGE_REVIEW; risk HIGH because the change launches local
executables, handles environment credentials and terminates owned descendants.
Reviewed Environment lifecycle module, its native-owner prime/plan/apply linkage,
CLI dispatch/private writer, lifecycle instructions, behavioral tests and final
runtime receipt/evidence. Existing unrelated TASK-054/TASK-055 changes and
third-party vulnerability auditing are excluded.

## Compact threat model and control review

Assets: user secrets/settings, client tool approval context, cache inventory,
unrelated processes, host availability and integrity of mutating calls.
Boundaries: client JSON-RPC to known tool; private reviewed manifest to native
transport; subprocess to owned JobObject/process group; shared leases to cleanup.
The model can select a published tool and arguments, not a command, arbitrary PID,
manifest path or executor approval. Same-user compromise of configuration and
checkout together is outside this local adapter's trust model.

- Tool schemas/names/annotations are copied unchanged; front-end controls have
  distinct names and do not confer tool, model, Security or executor authority.
  Tools-only protocol advertises no roots/sampling/elicitation capability.
  Unsupported upstream requests fail explicitly, never silently authorize.
- Private atomic creation reuses protected DACL handling. Manifest reads reject
  symlinks/unsafe size/nonprivate permissions, then verify the approved byte digest.
  Source/executable/arguments/effective environment and canonical native owner are
  bound. Operational configuration drift and enabled global/plugin identity
  collisions block launch, including generated proxies under arbitrary aliases.
- Inherited credentials are provider-specific and owner-derived; other providers'
  secrets are absent. Explicit env/env_vars remain intentional user settings.
  Errors are sanitized and upstream stderr discarded; no environment or protocol
  payload logging was introduced. Successful tool content remains its requested
  result and is not claimed to be a universal secret-redaction layer.
- Windows creates suspended, assigns a private kill-on-close JobObject before
  resume and fails closed on containment error. Cleanup takes no arbitrary PID.
  Owned descendants terminate; unrelated processes survive. POSIX code uses a
  newly owned process group, with actual POSIX execution unvalidated here.
- Serialized calls, bounded admission, shared leases, final-release drain and idle
  checks preserve active work. Client closure blocks queued mutations. Failed or
  partially applied calls are never replayed. Tool-change notifications trigger an
  exact inventory recheck before further calls; real drift invalidates the cache,
  including previously queued mutations. An operation already applied before a
  disconnect/drift may require reconciliation; a failed response is not rollback.

Review iterations corrected privacy inspection, configuration/cache binding,
metadata invalidation race, bounded cleanup/admission, alias duplicate detection
and cross-provider credential inheritance. These were implementation review
candidates resolved before delivery, not externally published vulnerabilities.
No unresolved confirmed security finding remains in this bounded change.

## Independently executed validation

Command: bundled QA-only Python3.12.14, `-m unittest discover -s tests -p
test_mcp_lifecycle.py`. Final independent run: **26 tests PASS, 8.169 seconds,
exit0**. The bundled interpreter was not placed in production configuration.

Negative/behavioral coverage includes private manifest permission/digest rejection,
runtime/env drift, cross-provider credential isolation and explicit overrides,
unrecognized tools/leases, actual owned Windows descendant cleanup and unrelated
process preservation, shared/in-flight/idle behavior, partial-mutation no-replay,
concurrent failure, unsupported sampling request, metadata drift versus harmless
notification, queued closed/invalidated mutations and global/plugin proxy aliases.

Reviewed final `TASK-056-runtime.md` and `TASK-056-runtime-evidence.json` from
Harness: all four actual Windows-native transports passed cached metadata with
zero heavy child, real representative calls, same-workflow PID reuse and explicit
finish with zero remaining observed owned PIDs. No owned WSL child; active config
hash unchanged. Those provider runs were executed by Harness, not this reviewer.
The independent full structural suite remains owned by QA.

## Frozen artifacts, SHA256

- mcp_lifecycle.py: `244707ee30eb3178daf821b7446b2c98426a1ae452a8e744214e18de3dec501b`
- native_mcp.py: `0f73bb2cb2c5bd52690d85fd4739101d45f295455eb664db1470f822ca66841f`
- environment.py: `a32df9c365f3c64831975b093cdd1a872f0ffe7a154222266a19f009e3b5f1f0`
- test_mcp_lifecycle.py: `16cb48b9cd6f8e9658c06ce25edbbb754098df2a3433aa1d706566a79dccb7a0`
- TASK-056-runtime-evidence.json: `3be446c66c49937bf860ba7b48564bc8f8cf53202b5fecebd1e3fee0f5227a6c`

## Layer coverage and residual limits

Banco: NOT_APPLICABLE, no database changes. API/Backend: PASS for internal
local JSON-RPC/control boundary. Frontend/UI: NOT_VALIDATED for actual desktop
approval UI; no frontend changes. Infra/DevOps: PASS for bounded Windows owned
process controls; POSIX/macOS runtime NOT_VALIDATED. Dependencias/Supply Chain:
no new dependency; source/pin reuse inspected, broad dependency advisory audit
NOT_PERFORMED.

The lightweight front-end remains alive for its MCP connection. Actual desktop
host migration/approval UX, external n8n API/Claude model authentication, production
deployment and whole-machine memory savings remain NOT_VALIDATED. Stable external
Python3.11+ is required for future application. MCP tools-only limitations and
state loss after stop are documented. No merge/push/install/application authorized
by this PASS. Exact next human decision: separately authorize applying the reviewed
configuration migration when desired; mandatory executor controls still apply.
