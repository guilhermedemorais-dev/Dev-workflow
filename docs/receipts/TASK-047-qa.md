# TASK-047 independent QA execution receipt

- Owner/sector: `qa-testing-standard` / `qa`.
- Task/list/revision: `TASK-047`, `MT-02/checklist`, `contract_revision: 3`.
- Phase/mode: validation / change-validation.
- QA_STATUS: **PASS**, bounded to consultative instructions, routing, source preservation and structural regression.
- State: COMPLETED for this QA checkpoint only. Application execution, fiscal approval, installed-host behavior, remote CI enforcement, Harness reconciliation and human merge acceptance are outside this attestation.
- Invocation evidence: independent QA agent invoked by Harness with canonical JSON path, list ID, revision and dependency receipts. No product/skill/test changes, publication, merge, installation or production effects performed by QA.

## Preconditions and skill receipt

`SKILL_RECEIPT`: canonical `plugins/qa-testing-standard/skills/qa-testing-standard/SKILL.md` read completely; `references/test-strategy.md` loaded for risk-based selection and result interpretation. Status LOADED. Rules applied: JSON-only specialist input, current comparison/revision before execution, independent evidence, no product fixes or another owner's PASS, local instruction scope separate from application validation.

The initial comparison receipt lacked the observed Issue update time and said remote readback remained pending. QA requested refreshed Harness evidence before validation. Harness supplied the updated receipt: revision 2 VERIFIED, remote Issue #47 body matches its published mirror; observed `updated_at: 2026-10-11T08:35:37Z`. This preflight deficiency is resolved, not silently waived. QA relied on the Harness comparison and did not read Human Task prose as execution input.

Inputs used / sources_loaded, each for its purpose:

- `docs/execution/TASK-047.json`: exact selected list, normative scope, AC-01..07, TEST-01..03, path restrictions and dependencies.
- `docs/receipts/TASK-047-harness-comparison.md`: current equivalence/revision evidence.
- `docs/receipts/TASK-047-implementation.md`: documentation dependency, authored outputs and explicitly unverified boundaries.
- `AGENTS.md`, `README.md`, `docs/workflow-pipeline.md`: repository map, native validation and lifecycle ownership.
- `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md`: REF-02 transport/equivalence/sector preservation.
- `plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md`: entry point and selective SDD routing.
- `plugins/sdd-spec-factory/skills/sdd-spec-factory/references/technical-knowledge-router.md`: REF-03 selection, missing-knowledge procedure, stop rules and evidence boundaries.
- Its six `technical-{architecture,data-concurrency,auth-sessions,apis-jobs,quality-operations,fiscal}.md` references: affected instruction inventory plus triggered scenario consultation, not all-domain default loading for a client task.
- `plugins/dev-workflow-standard/skills/dev-workflow-standard/references/{capability-registry,skill-owned-tools,continuous-improvement}.md`: shared Python capability ownership, research fallback and durable learning/promotion boundaries.
- Discoverable specialist `references/tool-registry.json` metadata (Implementation, Harness, DevOps, Reverse Engineering, Security, SEO, UI/UX) and Environment `references/mcp-library.json`: inventory matching only; no unrelated methodology execution or capability activation.
- `tests/test_technical_knowledge_library.py` and current diff: structural oracle and source-preservation review.

Conditional topics activated in the consultation: data/concurrency for last-unit purchase; auth/sessions for refresh; fiscal plus APIs/jobs for uncertain invoice submission; data/concurrency and knowledge-gap procedure for the hypothetical absent SQLite detail. Contract has no additional `conditional_sources` entries. No optional capability was installed.

## Actual commands and validation evidence

Environment: Python 3.12.14; branch `feat/technical-knowledge-routing-20261011`; starting HEAD `b728e2c18b8ac4248c6aae81557755e51c8292c8`. Validation includes current uncommitted/untracked authored files, not only HEAD.

| Command/check | Exit | Observed result |
| --- | --- | --- |
| `python3 -m unittest discover -s tests -v > /tmp/TASK-047-independent-qa-tests-rev3.log 2>&1` | 0 | `Ran 595 tests in 4.452s`, `OK`; independent full run, no failures/errors |
| `git diff --check && git diff origin/main --check` | 0 | No whitespace diagnostics; repeated after the suite |
| `git diff origin/main --name-status`, `git status --short`, `git diff origin/main -- .../SKILL.md` | 0 | Only scoped tracked additions/edits; new topic/test/task records included separately in review |
| Python stdlib check against `git show origin/main:<skill>` and current contents | 0 | Every preexisting SDD/Harness skill line retained in original order; no removal |
| Python JSON + `fnmatch` check of changed and untracked paths against TASK-047 allowed/protected paths | 0 | 17 changed/new paths at final revision 3 inspection; all allowed, zero protected paths changed |
| `rg -n 'SQLite\|BEGIN IMMEDIATE\|SQLITE_BUSY_SNAPSHOT' .../technical-*.md` | 0 | Only SQLite limitation found; specific WAL snapshot-promotion detail absent |
| Available-tool name/metadata inspection for Context7/Firecrawl/Grep and web search | successful | No Context7/Firecrawl/Grep callable in active inventory; web source reader available |
| Web `open https://www.sqlite.org/isolation.html` | successful | Original official document read, not search snippet; source page last-update 2022-04-18; retrieved 2026-10-11 |

The final revision 3 suite includes 9 new structural library tests, in addition to 586 existing tests. It validates routing/link/schema-related fixtures; it cannot prove a future agent always follows instructions or a client application behaves correctly.

## Independent consultation scenarios

These are executed **instruction consultations** and derived **application test plans**. No product facts, DB engine, provider, tax regime or API were supplied; none is invented here.

| Scenario | Selected route/owner | Needed decisions before product execution | Derived verification and expected evidence |
| --- | --- | --- | --- |
| Checkout can sell last unit twice | SDD -> data/concurrency; database/backend Implementation; independent QA; Security for affected payment surface | Inspect actual schema/engine/version/isolation and transaction boundary; confirm backorder policy and reserved/paid states; compare atomic conditional update, row lock, optimistic check or serialization against invariant; establish idempotency and payment reconciliation | After approved no-backorder stock=1, race two independent real-DB transactions with synchronization; exactly one committed reservation, no negative stock, other purchase rejected. Replay winner, crash after commit/before response, late payment result and cancellation/reconciliation. Engine-specific evidence required; sequential mocks or SQLite substitute do not prove another production DB |
| Simultaneous refresh requests | SDD -> auth/sessions; Security owns control/replay decisions; Implementation owns state transitions; QA independently checks provider boundary | Discover real identity provider/client/token store and documented rotation/sender constraints. Decide atomic consumption/family replay behavior and legitimate-client coordination; no invented grace window or assertion that both succeed | Race independent refresh requests on synthetic account; assert documented provider result and approved replay response; valid new token, consumed token replay, expiry/revocation/logout and cross-user/tenant denial. Record mocks separately from provider sandbox; absent provider semantics block affected spec |
| Invoice submission times out | SDD -> fiscal plus APIs/jobs; accountant/domain owner establishes rules; Implementation integration, QA technical scenarios, Security certificates/data and DevOps operational target retain ownership | Determine actual model/jurisdiction/effective release/provider, schemas and approved numbering/key/protocol lifecycle. Treat timeout as uncertain outcome; establish authoritative query/reconciliation and duplicate-safe resend rules. NF-e is a hypothesis, not an asserted product fact | Approved synthetic homologation flow: timeout after acceptance, query/status reconciliation before unsafe resend, duplicate attempt without unintended issuance, schema/provider rejection, certificate expiry and model-permitted cancellation/contingency. Official protocol proves authorization, PDF alone does not. No real production issuance/cancellation; fiscal manuals and schemas remain NOT VERIFIED in this upgrade |
| Pattern missing from library | SDD -> selected topic + router knowledge-gap procedure; existing project reference owner; Harness for normative/review changes | Example unanswered question: if an actual project uses SQLite WAL, what happens when a read snapshot becomes stale before write promotion? This is hypothetical scope, not its stack. Inspect actual SQLite version/journal/shared-cache configuration before applicability; no plugin install/new registry | Search existing topic before research; use original official source; record source/section/version/date/claim/limits. Save/update the existing project reference and route exact section through Task/JSON; preserve prior provenance on conflict. Reuse next time only after stack/freshness applicability check. Only project-matched two-connection runtime evidence would validate its concurrency behavior |

### Missing-pattern research and reuse exercise

Actual primary-source read: `https://www.sqlite.org/isolation.html`, sections “Isolation And Concurrency” and “No Isolation Between Operations On The Same Database Connection”, checked 2026-10-11. Bounded supported claim: in WAL mode, a reader holds a snapshot; promoting an outdated snapshot to a writer can fail with `SQLITE_BUSY_SNAPSHOT`. The source describes ending that snapshot and starting another transaction, and `BEGIN IMMEDIATE` as an alternative for an intended writer. Same-connection operation visibility is a separate boundary.

The document explicitly dates WAL support to SQLite 3.7.0; the supplied scenario has no actual engine release. Therefore the source is verified research, while application/version applicability and test execution are NOT VALIDATED. No universal transaction policy is adopted from this example. The source's update date is provenance, not a fabricated expiry TTL.

Fallback reason: registry metadata includes Context7/Firecrawl/Grep candidates, but no corresponding callable was exposed; available bounded web reader retrieved the original official page without installation. Documentation metadata/source is not evidence those MCPs executed.

Durable-update review exercise: the router requires updating the existing client project reference record, routing it by purpose/version, then reusing compatible evidence. QA may write only this receipt, so it records the source/claim here and returns the proposed owning-reference action to Harness; it did not pretend to update a nonexistent client's library, change installed caches, or promote rules globally. No application uses this hypothetical pattern in this upgrade. Cross-project promotion remains the existing reviewed plugin-source process. Conflict/unavailable-source branches explicitly preserve provenance or mark NOT VERIFIED and block only dependent decisions.

## Findings, acceptance and limits

No unresolved blocking instruction/routing defect found. Initial comparison receipt deficiency was resolved before execution. No product bug/security finding was inferred from documentation.

- AC-01: existing skill bodies and protected contracts/manifests/templates/runtime/workflows preserved; no second registry/runtime introduced.
- AC-02: six consultative topic records have explicit provenance/decision/verification boundaries; fiscal index pointers deliberately do not claim manuals/schemas were read.
- AC-03: SDD and Harness point to one canonical router, select triggered topics, and use existing reference/list/sector fields with v1 compatibility.
- AC-04: three critical consultations above yield bounded decisions and test plans, explicitly separated from application execution.
- AC-05: independent full regression/whitespace/preservation completed. Remote Quality Gate observation and human acceptance remain Harness-owned, outside this QA PASS.
- AC-06: missing-pattern consultation exercises local gap search, original-source research, provenance/applicability, durable-owner update routing, reviewed promotion and later compatible reuse; no unverified rule is promoted.

Outputs_produced / artifacts: this receipt only. validation_evidence: actual commands/results above and reviewed-source SHA-256 identities below. Bug disposition: none requiring rework. Remote mutations by QA: none. Tokens: NOT_AVAILABLE.

Reviewed instruction/test content identities (SHA-256):

```text
5458475770685dcf956dd8407cd7bac594dc157b3d587444da9d7a8243e8a9bd  Harness SKILL.md
d3821261934235d2aa0dc4b1b6ec48a0ed3970987f11e6839797972660a4c021  SDD SKILL.md
b092a50fc4ecc45360bf6757db1f5cb010e027cc4a0ecd0094439c84053ff57e  technical-knowledge-router.md
28931e53fd0d2ff1178c8c871a53eee62aee27d711d7a10846b67d4e222b3570  technical-apis-jobs.md
bebabb5b80d74755f07a53a31e3a09cf9a159b6f2dc44676f9bc864acc491b92  technical-architecture.md
bfb7ffc8cb25fbdc070b291ee2ceb19b44f846b7a54f083e5ac3184b39419e5e  technical-auth-sessions.md
7006485f0d3bcfe864d656e18e13b1886f372de5611020c1c322c3cd6fa3f0d9  technical-data-concurrency.md
8cc966a34e90550f3130dffdc64c7dde897de61e83b11102254f2c68dd7e65f0  technical-fiscal.md
8c1f17d5e391e52025f7d544bc2904a16731b43fc48283f6a832bc5b9d074c21  technical-quality-operations.md
d817f94aa991ef87221576a125e331057ce3d98f432bb2079981fdb682893807  test_technical_knowledge_library.py
```

## Revision 3 revalidation and catalog consultation

Harness explicitly handed off revision 3 of the same list. QA verified the canonical JSON now includes REQ/AC-07, REF-04 with purpose/section, corresponding list action, continued receipt-only write scope and the expanded global permitted surface. Refreshed comparison is VERIFIED with remote body match and observed Issue `updated_at: 2026-10-11T08:40:08Z`; implementation receipt also names revision 3. No new stop or application requirement is inferred.

Prior inventory/refresh/fiscal/missing-pattern consultations remain applicable: their instruction sources have unchanged content hashes, and the added catalog pointers change discovery leads only. Source applicability still requires a real client stack/model; reuse does not claim application execution. Full suite and whitespace were rerun for revision 3, rather than reusing only the revision 2 594-test run.

REF-04 `continuous-improvement.md` was read completely, then its new source section/diff inspected. Baseline lines retained in order, no existing approval/candidate audit rule removed; an intermediate duplicate WordPress heading was reported and removed by the owner before this validation. No blocking defect remains. Final content SHA-256: `0ce065a4aae533c38b15481ebf4ce322ae16a1a69cfecd0ae3183fc72b6b0499`.

Independent web original-source reads on 2026-10-11:

- `https://github.com/google/skills` and the linked Google Cloud announcement: identify skills for Google products/technologies and official-source authority, not a generic engineering guarantee.
- `https://github.com/google-labs-code/stitch-skills`: README prerequisites explicitly require configured/running Stitch MCP; catalog presence does not show this runtime has it.
- `https://antigravity.google/docs/skills`: host skill format/discovery guidance; no catalog adoption or installation executed.
- `https://github.com/sickn33/antigravity-awesome-skills`: readback redirected to `https://github.com/sickn33/agentic-awesome-skills`; community catalog authority remains distinct from Google's official source.

AC-07 consultation: a verified capability gap selects relevant catalog metadata, then a pinned candidate's full instructions/references/scripts/license/permissions. Existing specialist ownership and evaluation gates determine whether adoption is appropriate. Sources are bounded discovery leads; no bulk import, installer, activation, replacement control plane, global promotion, or candidate runtime approval is implied. This procedure is coherent with the existing Harness architecture and user-requested researched library updates. Individual candidates remain NOT VALIDATED.

Final independent native run: 595 tests, 4.452s, exit 0, OK. Post-run `git diff --check && git diff origin/main --check`: exit 0. Final allowed/protected check: 17 paths allowed, zero protected paths changed. Contract identity/list owner/REF-04 resolution checks: exit 0. One additional structural test covers discovery-source authority/adoption boundaries; it was reviewed and included in the independent full run.

Next_safe_action: Harness reconciles this bounded owner receipt with documentation evidence and remote Quality Gate facts, presents results and pending limitations for explicit human acceptance. Revalidate materially changed instruction/test content; do not infer merge/deploy authorization from this PASS.
