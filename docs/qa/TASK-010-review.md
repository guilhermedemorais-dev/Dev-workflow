# QA Review: TASK-010 GitHub Repository Governance

## Scope and independence
Owner `qa-testing-standard`, reviewer `sector_sdd`, mode change-validation.
Branch `feat/github-governance-bootstrap`, base
`44718fe5faa49cdfde790a51ae6e63ce6c18c050` plus task working-tree changes.
Reviewer authored SDD acceptance artifacts, not the helper, skill/reference or
implementation tests. This is independent implementation verification, not a
blind requirements evaluation. GitHub remote governance is outside this run.

## SKILL_RECEIPT
- skill: qa-testing-standard
- path: plugins/qa-testing-standard/skills/qa-testing-standard/SKILL.md
- references_loaded: references/test-strategy.md; references/bug-report.md
- applied_rules: risk-adaptive independent testing; no product edits; planned
  cases are not executed; error classification; preserve owner-specific PASS
- status: LOADED, complete skill and planning reference read

## Sources loaded and purpose
- `docs/execution/TASK-010.json`: resolve QA sector, scope and dependencies.
- `docs/tasks/TASK-010-github-governance.md#qa`: QA assignment and expected evidence.
- `docs/specs/github-governance/module-spec.md`: approved architecture/boundaries.
- `docs/specs/github-governance/validation-rules.md`: RN-01–RN-12 and T01–T20 oracles.
- Active QA skill/reference above: select meaningful checks and report limitations.
Conditional implementation sources activated after DevOps handoff: full helper
`plugins/devops-standard/skills/devops-standard/scripts/github_governance.py`
and `tests/test_github_governance.py`, to inspect/execute behavior independently.
Bug-report reference read completely before confirming and returning defects.

## Planning strategy
Functional risk HIGH: administrative mutations, idempotency, partial failures,
credential-sensitive errors and false readiness. Use deterministic isolated
fake-gh/unit/integration tests, never a live account for the standard suite.

QA_GUARDRAILS:
- No external mutation, login, installer, push, merge or deployment during QA.
- Do not edit author tests or weaken assertions to obtain green.
- Track initial failures and reruns; classify fixture/tool failures separately.
- A fake API PASS is not live GitHub capability or production readiness.
- Security candidates go to Security; QA does not certify that sector.

TEST_SCENARIOS, prioritized:
| Group | Preconditions and action | Required observation | Level |
| --- | --- | --- | --- |
| P1 Read-only | Fake gh call ledger and filesystem snapshot; execute diagnose/propose/verify across happy/error branches | No write/mutation/workflow/Git side effect, including GraphQL mutation over POST | Isolated integration |
| P2 Approval binding | Create proposal; change target, desired hash, current state or operation payload; attempt confirmed apply | Stop before first mutation; new review required, not arbitrary proposal command execution | Unit/integration |
| P3 Missing authority | Missing gh, no auth, inaccessible repo, no admin, Project access failure | Distinct actionable statuses, no repetition of denied writes or credential output | Unit/integration |
| P4 Idempotency | Stateful fake remote/local apply; refresh/propose/apply again | Resource counts unchanged; NO CHANGE REQUIRED, current IDs reused | Stateful integration |
| P5 Partial failure | Inject failure after one approved mutation; inspect result and resume with refreshed proposal | No PASS, accurate partial ledger, no duplicate first resource or hidden rollback | Stateful integration |
| P6 Discovery completeness | Existing resource on second page; ambiguous title; existing labels/options with cosmetic differences | No duplicate creation, ambiguous matching blocked, statuses preserved | Unit/integration |
| P7 Capability limits | Distinguish plan-supported, evidenced plan limitation and ambiguous 403/404 | No guessed plan downgrade; fallback approval distinct from observed completion | Unit |
| P8 CI/readiness | Generated workflow but no run; stale/failed/foreign check; missing manual evidence | No false READY or enforcement assertion; required check names derive actual evidence | Unit/integration |
| P9 Local safety | Conflicting file, traversal and symlink to external temporary target | No unauthorized overwrite/escape; original content preserved | Isolated filesystem |
| P10 Error hygiene | Synthetic secret marker in auth/API/stderr/exception values | No sensitive/raw traceback output; useful bounded classification | Unit/integration |
| P11 Lifecycle/docs | Inspect README, eight stages, existing templates and owner boundaries | Validation/Awaiting Final Approval present; Done only human merge; no new owner/receipt/installer | Structural review |

REGRESSION_TARGETS: twenty requested helper cases T01–T20; full repository suite;
README and structural validators; existing gh registry/Environment integration;
legacy sector routing and receipts. Check coverage by behavior, not test count.

VALIDATION_REQUIREMENTS: released helper/relevant author receipt; independent
suite execution with command/exit/result; targeted negative probes where author
tests omit a material branch; initial failures and corrected-revision retest.
Remote private test-repo procedure must be documented but remains NOT VALIDATED.

## Twenty-case acceptance map
All are planned, not executed: T01 missing gh; T02 auth; T03 repo access;
T04 admin; T05 Project permission; T06 configured NOOP; T07 Project reuse;
T08 partial labels; T09 rules supported; T10 plan limitation; T11 read-only;
T12 apply confirmation; T13 idempotency; T14 drift; T15 dynamic IDs;
T16 existing status; T17 missing status; T18 failed mutation;
T19 secret-free output; T20 observed readiness.

## Findings, commands and results
Initial author suite independently executed: `PYTHONDONTWRITEBYTECODE=1 python3
-m unittest discover -s tests -p test_github_governance.py -q`, exit 0,
27 tests PASS in 0.095 seconds. This did not establish complete acceptance:
independent negative probes below found missed branches.

All probes used synthetic markers, temporary directories and fake clients;
no live GitHub invocation. Temporary QA artifacts were created with apply_patch
outside the checkout at `/tmp/task010-qa-wDyE10/`; no helper/author test edits.
The reproduction descriptions below remain durable even when temporary files
are later removed. Initial observed helper SHA-256:
`f1995e8c2132a16410ca8c6cea6d0957a66e99e3f3f0a4b8187166c5c2eed4f6`.

### Q01: Local change certified by unrelated remote CI
CONFIRMED_BUG, HIGH functional impact, deterministic 1/1, confidence HIGH.
Target: `verify` + `observe`, initial working-tree helper over base44718fe.
Preconditions: fake remote main SHA A has successful `quality`; local package
test script differs from the remote artifact; local generated workflow matches
the desired content; other requirements are disabled with fixture reasons.
Reproduction: generate local workflow from the changed package, return remote
snapshot with quality success at A, call verify. Expected: no READY until the
local governance/CI inputs are bound to verified remote revision/content.
Actual: `READY`, with no local/remote identity comparison.
Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/probes.py`,
exit 0, `P-dirty-local-vs-remote-CI: READY`.
Regression: committed and uncommitted workflow/config changes, local head not
equal remote head, dirty stack inputs and correctly matching happy path.
Owner DevOps, REWORK_REQUESTED; retest NOT_VALIDATED.

### Q02: Unknown capability waived by generic exception
CONFIRMED_BUG, HIGH functional impact, deterministic 1/1, confidence HIGH.
Target: verify exception filtering. Preconditions: rules enabled, observation
reports `rules/NOT_VALIDATED` due to API failure, desired exception for rules
contains only generic fallback reason; no observed fallback controls supplied.
Reproduction: inject that snapshot with no other drift and call verify.
Expected: unknown mandatory capability cannot become ready from an unsupported
attestation; fallback decision and observed fallback evidence remain distinct.
Actual: `READY_WITH_LIMITATIONS`. Probe command above, exit 0:
`P-unknown-capability-exception: READY_WITH_LIMITATIONS`.
Regression: unavailable API versus evidenced plan restriction, approved fallback
with observed controls versus unverified reason string. Owner DevOps,
REWORK_REQUESTED; retest NOT_VALIDATED.

### Q03: Existing confidential file content leaks into proposal
CONFIRMED_BUG for output contract; SECURITY_CANDIDATE sent to Security for its
classification, not an independently asserted vulnerability finding.
HIGH functional confidentiality impact, deterministic 1/1, confidence HIGH.
Target: make_proposal local unified diff. Preconditions: generated local files
enabled, existing CONTRIBUTING contains a synthetic ghp-prefixed marker.
Reproduction: propose replacement content and inspect serialized proposal.
Expected: no credential-like existing content appears in printed diff/output.
Actual: full marker appears in removed unified-diff line.
Probe command above, exit 0: `P-sensitive-old-diff-exposed: True` (the report
does not store a real token). Regression: sensitive old content in every governed
file, API descriptions/errors and local path metadata. Owner DevOps, Security
informed; REWORK_REQUESTED; retest NOT_VALIDATED.

### Q04: Malformed API row bypasses structured error handling
CONFIRMED_BUG, MEDIUM impact, deterministic 1/1, confidence HIGH.
Target: GH.pages and main exception boundary. Preconditions: fake gh returns
valid JSON `["malformed-row"]` instead of label objects.
Reproduction: real helper CLI subprocess `diagnose`, fake executable first in
PATH, isolated Git repository and call ledger. Expected: bounded JSON failure,
nonzero exit, no raw traceback. Actual: exit 1, empty stdout, traceback stderr
from unhandled AttributeError on row.get.
Evidence: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/cli_probe.py`,
exit 0 for probe harness, output `malformed_API_exit=1 json_output=False
traceback_exposed=True`. Regression: wrong dict/list/scalar shapes at API edges,
no exception detail leakage; Owner DevOps, REWORK_REQUESTED; retest NOT_VALIDATED.

### CLI interface evidence already observed
The same isolated fake-gh CLI probe ran diagnose/propose/verify separately.
All returned exit 0 in the minimal explicit-N/A fixture, the repository file
snapshot remained byte-identical, and the call ledger contained 18 reads and
zero mutations. Apply without proposal/confirmation returned exit 1 with zero
additional gh calls and unchanged filesystem. These are verified narrow
read-only/confirmation paths, not all remote capability paths.

## EXECUTION_RECEIPT
- task_id: TASK-010
- sector: qa
- phase: validation
- capability: functional-qa / test-strategy
- provider_or_runtime: local specialist agent
- executor: sector_sdd
- state: COMPLETED
- invocation_evidence: delegated QA planning request, full skill/reference load
- inputs_used: sources and purposes above
- outputs_produced: test plan, five reproducible findings, two retest cycles and bounded final acceptance
- changed_files_or_artifacts: docs/qa/TASK-010-review.md only
- commands_and_results: final 47 focused and 539 full-suite tests PASS; isolated module/CLI probes below
- validation_evidence: Q01–Q05 corrected in final reviewed helper hash; T01–T20 local coverage mapped below
- blockers: none for bounded local delivery; live integration remains NOT_VALIDATED
- next_safe_action: Harness reconciles Security and QA receipts before any separately authorized commit/publication

## Cycle 1 retest, release candidate
RC helper SHA-256:
`082d4ef8b3d9467378763b79fda958529d53351f8fda0fecbb9ec272c5267628`.
- Independent focused suite: 45 tests PASS in 4.697 seconds, exit 0.
- Independent full suite: 537 tests PASS in 15.608 seconds, exit 0.
- Original Q01 probe now BLOCKED; original Q02 probe now BLOCKED.
- Original Q03 proposal now rejects sensitive material with VALIDATION_FAILED
  and no marker exposure; arbitrary removed lines are omitted from printed diff.
- Original Q04 real CLI probe now returns bounded JSON, exit 1, no traceback.
- Read-only CLI rerun: filesystem unchanged, 18 read calls, zero mutations;
  unconfirmed apply exit 1 with no extra gh calls. Verify appropriately BLOCKED
  for the unpublished/minimal local fixture rather than falsely READY.
- `local.generate=false` with required files missing is now explicitly blocked
  by `local_governance`, covered in author test45 and independently inspected.
Q02/Q03/Q04 FIXED for these reproduced cases. Q01 original path corrected,
but the following related ignored-file path still blocks acceptance.

### Q05: Disabled generation omits existing governance files from publication binding
CONFIRMED_BUG, HIGH functional impact, deterministic 1/1, confidence HIGH.
Affected RC is the hash above. Owner DevOps; REWORK_REQUESTED, cycle 2.
Preconditions: all required governance files exist, generation disabled,
CONTRIBUTING.md ignored/untracked, other files committed, local HEAD equals the
fake remote default SHA, git status clean, CI/Project/rules N/A with reasons.
Reproduction: create these fixtures in isolated Git repo; change ignored
CONTRIBUTING content; run real verify CLI against fake gh returning matching SHA.
Expected: publication cannot be certified because required governance content is
absent from the remote revision and differs locally outside tracked state.
Actual: exit 0, `READY`, empty limitations. `observe` inventories generated
artifacts, workflow and stack inputs, but does not inventory the required local
governance files when generation is disabled.
Evidence: `PYTHONDONTWRITEBYTECODE=1 python3
/tmp/task010-qa-wDyE10/ignored_governance_probe.py`, exit 0:
`ignored_governance_verify_exit=0 readiness=READY limits=[]`.
Regression: include all required governance files in snapshot and publication
binding independent of generation setting; cover ignored/untracked differences,
proposal hash drift and correctly committed matching governance.
Retest: FIXED in cycle 2 below.

## Cycle 2 final independent retest
Helper SHA-256:
`7fa330927f7136bdfda0d34c6da98ad5bc1bf1be60c83c9b55d36850cb32c46f`.
Commands run from repository root, exit 0 unless noted:

- `python3 -m unittest discover -s tests -p test_github_governance.py -q`:
  47 tests PASS, 19.462 seconds.
- `python3 -m unittest discover -s tests -q`: 539 tests PASS,
  42.256 seconds. These are local tests, not live GitHub integration.
- `git diff --check`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/probes.py`:
  Q01 and Q02 BLOCKED; Q03 VALIDATION_FAILED, marker exposure false.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/cli_probe.py`:
  read-only commands preserve filesystem, 18 gh reads and zero mutations;
  unconfirmed apply exit 1 with no extra gh calls; malformed API exit 1,
  structured JSON and no traceback. Unpublished minimal fixture verify BLOCKED.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/ignored_governance_probe.py`:
  original Q05 now helper exit 1, BLOCKED, publication limitation. Required local
  governance inventory is independent of generation; author regression46 also
  exercises this condition. Q01–Q05 closed for reproduced local paths.
- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/task010-qa-wDyE10/supplemental.py`:
  six probes PASS: unauthenticated, inaccessible repository, denied Project,
  complete Status NOOP, strong effective rules NOOP/READY, explicit plan limit
  with approved fallback and revision-bound manual evidence READY_WITH_LIMITATIONS.
  Same fallback without evidence BLOCKED. All observations are synthetic.
  First supplemental run used an invalid fake gh version, correctly rejected
  GH_BROKEN; QA corrected its fixture, not product code (TEST_BUG).

### Requirement coverage, bounded to offline behavior
| Required cases | Executed evidence |
| --- | --- |
| T01–T05 environment/access | author11/24/30, supplemental auth/repo/Project denials |
| T06–T08 existing resources | author19/25/37/43, reuse dynamic Project and partial labels |
| T09–T10 rules and limitations | author14/33/41 plus supplemental strong rules and evidenced fallback; Q02 negative |
| T11–T14 read-only, confirmation, rerun, drift | author12/16/21/22/23/32/37/43/46; independent CLI ledger and Q01/Q05 |
| T15–T17 IDs/options | author05/06/25, supplemental complete options; REST15 and GraphQL27 pagination |
| T18–T19 partial failure and sensitive output | author30/34/36/38/40/44; independent Q03/Q04 |
| T20 fresh readiness | author26/31/32/33/45/46; independent publication, rules and fallback probes |

Additional negative coverage includes traversal/symlink/injection, malformed
schema/API, target/hash tampering, concurrent local edit, unknown stack and pinned
workflow generation. Test47 verifies unsupported local-write platforms block
before any remote mutation. No claim of successful native Windows execution.
Existing-project/pagination tests exercise mocked observations, not a live owner.
Manual-evidence tests check schema, target/revision and decision behavior; they
do not prove that a real linked observation or branch enforcement exists.
Temporary probe paths are local QA artifacts, not installed components or a
portable committed test package. Durable author regressions retain Q01–Q05.

## Result
QA_STATUS: PASS for the reviewed hash and executed local scope only.
Independent of helper implementation; this reviewer authored the acceptance
specification, so the exercise is informed, not a blind evaluation.
No live GitHub mutation, actual permissions verification, installation, CI run,
Project/ruleset enforcement or production readiness was performed or certified.
The authorized disposable-private-repository procedure in validation-rules.md
remains NOT_VALIDATED and is required before claiming operational remote readiness.
