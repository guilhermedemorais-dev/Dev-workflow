---
name: qa-testing-standard
description: Independently plan and verify functional behavior, reproduce bugs, investigate regressions and verify fixes for a task, diff, feature or scoped audit. Use for Test Engineering and functional QA, not product implementation or specialist security, visual or infrastructure approval.
---

# QA Testing Standard

Own functional correctness and Test Engineering. The Harness coordinates; QA
plans, executes and interprets behavior checks independently of the product
implementer. Tool execution and actual evidence, not a checklist, justify results.

## Context and activation

1. Receive `task_id`, `execution_contract_path`, `sector`, `revision` and relevant
   `dependency_receipts`. Read the contract; match the task and current revision.
2. Resolve your own sector and owner. For additive `schema_version: 1` contracts,
   load the minimal global goal/acceptance references, listed `task_sections`,
   `required_sources` (each with a `purpose`), relevant code and material receipts.
   Evaluate `conditional_sources` and read only when their condition occurs.
   OPTIONAL sources are not loaded automatically.
3. Read this SKILL completely and references required by the active mode.
   Record the existing `SKILL_RECEIPT`: skill, exact path, references_loaded,
   applied_rules and status LOADED or BLOCKED; sector/mode are contextual details.
4. The Harness reads the complete Human Task; QA does not by default. With a
   legacy contract without sectors, request a scoped handoff from the Harness,
   preserving its mandatory sources and existing gates. Do not invent a sector
   or silently omit a source required by another applicable instruction.
5. Missing required source or `source_of_truth_conflict` blocks the claim. For
   insufficient context request `CONTEXT_EXPANSION` with reason, required_source
   and blocking_claim; let the Harness resolve it before loading unrelated docs.

Read [test-strategy](references/test-strategy.md) when planning, selecting test
levels/categories, investigating failures/flakiness, or interpreting a run.
Read [bug-report](references/bug-report.md) when reproducing a candidate,
documenting a bug, requesting rework, or verifying a fix. Do not load both
automatically for a simple already-specified validation.

## Modes and phases

Use the smallest sufficient mode:

| Mode | Scope |
| --- | --- |
| `change-validation` | Current task/diff/PR behavior and affected regression |
| `scoped-qa` | Named feature, page, module or API |
| `repository-regression-audit` | Broader repository evaluation only when requested |
| `bug-reproduction` | Reproduce a reported problem and classify evidence |
| `fix-verification` | Retest a specified fix and affected regression |

In **planning**, produce strategy/scenarios before implementation when their own
prerequisites exist. Final `depends_on` dependencies do not forbid planning.
In **validation**, verify all material dependencies and the executable revision.
Frontend complete while required backend is PENDING cannot yield QA final PASS.
Planning completion is not validation PASS; keep validation NOT_VALIDATED until
executed. Report phase and scope so a planning receipt cannot close final QA.

Behavior changes, bugfixes, user flows, API behavior, business rules, persistence,
payments, tenants, integrations, imports/exports, concurrency, state machines and
reported regressions trigger QA. Docs/metadata/comments with no runtime impact
can be N/A with a reason agreed by the Harness. Pure visual changes still belong
to UI validation even when functional QA is N/A.

## Execution and ownership

- Do not write or fix product code. Implementation owns code fixes and developer
  regression tests via `dev-implementation-standard`. QA may prepare test cases
  and scoped test artifacts when explicitly allowed, but must not weaken or edit
  an oracle merely to obtain green. Both may run tests; their responsibility differs.
- Confirmed bug: supply reproduction evidence and `REWORK_REQUESTED` to the
  affected owner through the Harness; preserve its status until its owner acts.
  QA retests the returned fix. Never mark another sector PASS, fabricate its
  receipt, or substitute developer tests for mandatory independent QA.
- QA can detect a `SECURITY_CANDIDATE`; route it to `security-standard` for
  exploitation/impact validation. `CONFIRMED_BUG` is not
  `CONFIRMED_SECURITY_FINDING`. Do not assign CVEs/security severity or publish
  a candidate as a vulnerability. Security keeps confidentiality, integrity,
  availability and abuse review.
- `ui-ux-standard` owns design fidelity, visual hierarchy, accessibility design,
  responsive behavior and visual runtime QA. QA owns functional forms,
  navigation, transitions and error behavior, not visual approval.
- `devops-standard` owns CI/CD, deployment, infrastructure, operational runtime,
  health and rollback; `dev-environment-standard` prepares available tooling.
  QA interprets product behavior after prerequisites are ready, not environment
  or production readiness. No deployment, production mutation or destructive
  test is implied by a QA assignment.

## Shared tools, not duplicated ownership

Prefer project-native commands and the project's existing test configuration.
For external capabilities, resolve the original owner and follow the Harness
`skill-owned-tools.md` protocol through the existing helper:

- `dev-implementation-standard`: pytest, pytest-cov, Hypothesis, Python unittest.
- `ui-ux-standard`: Playwright browser runtime capability.

QA can execute an approved shared capability and interpret functional results;
that does not transfer its technical registry/install/state ownership. Read the
owner's registry/protocol when using it. If an owner or required tool is missing,
ask the Harness/Environment for preparation or an approved equivalent. Do not
duplicate a registry, installer or cache; do not silently install anything.
No new QA-exclusive tool or knowledge registry is needed for this bundle.

Use synthetic data and isolated environments. Review network, billing, email,
payment, mutation and cleanup effects before running tests. Obtain explicit
authorization for effects outside the approved scope; do not run production or
destructive fuzz/concurrency workloads as a routine validation shortcut.

## Evidence gate

Return `QA_STATUS` in the existing `EXECUTION_RECEIPT`, with sector, phase/mode,
revision, sources_loaded (path and purpose), conditional_sources_loaded,
validation_scope, commands/exit codes, scenarios executed, bug disposition,
artifacts, limitations and next_safe_action. Preserve its invocation_evidence,
inputs_used, outputs_produced, state and validation_evidence fields. Do not
invent another global receipt or put logs/status into the Execution Contract.

| QA_STATUS | Meaning |
| --- | --- |
| PASS | Required scope executed, mandatory cases passed, blocking bugs resolved, required regression verified, limitations recorded |
| PARTIAL | Useful checks ran but coverage is incomplete; cannot close required QA |
| BLOCKED | A mandatory dependency, tool, source or unresolved blocking bug prevents the gate |
| NOT_VALIDATED | No applicable validation was executed, including planning-only work |

No execution means no PASS. A tool version, build success, screenshot or unit
suite alone cannot prove a required user flow. PASS is bounded to executed
scope, never a claim that software has no bugs. A red test must be classified
before asserting a product defect. Unresolved mandatory checks cannot be waived
by relabeling the result PARTIAL or by accepting a bug informally.

Map evidence-backed QA PASS to the existing COMPLETED state only for your
completed validation checkpoint. The Harness reconciles all REQUIRED sectors
and final acceptance. Human approval, PR, merge and release remain separate.

## Provenance

Independent QA ownership and routing are [PROJECT CHOICE]; QA_STATUS and sector
receipt details are [LOCAL EXTENSION], not official platform standards.
Risk-based selection and regression reasoning are [ECOSYSTEM CONVENTION].
Tool-specific official guidance is linked in test-strategy when relevant.
