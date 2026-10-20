---
name: dev-workflow-standard
description: "Use as the engineering harness for Guilherme's software delivery: receive a demand, diagnose and consolidate scope, plan executable work, resolve the required specialist skill/plugin/tool, actively invoke the selected capability, preserve handoff context, require execution evidence and validation before advancing, recover or replan on failure, and review delivery against specs/task/acceptance criteria. Product code is executed through dev-implementation-standard or another explicitly selected executor capability, never merely assigned."
---

# Dev Workflow Standard (Engineering Harness)

## Select the execution path first

Classify against the Change Complexity Gate before loading execution references.
For confirmed `TRIVIAL` work, use its inline path below; it takes precedence over
the full-contract, delegation, sector-matrix and reporting requirements in this
skill and its references. Repository-specific stricter rules still apply.
An existing approved full contract retains its gates; never downgrade it merely
to avoid required validation or obtain the inline exception.
All other work follows the full workflow. Uncertainty requires the higher tier.

Primary engineering harness for Guilherme's software projects. The LLM using
this skill becomes the **engineering orchestrator / final reviewer**. It does not
write product code itself outside the confirmed TRIVIAL path; it owns discovery, planning, capability routing,
execution state, handoff, validation, recovery and approval. It must actively
invoke the selected executor or specialist capability and cannot treat task
assignment, naming a skill, or writing a prompt as completed delegation.

Keep this file lightweight: load only the references required for the current
task.

## Core execution contract

Receive the demand, inspect the actual repository and approved scope, then select
only the applicable route below. Do not repeat Discovery for an approved task.
Classify before loading references. Read selected SKILL.md files completely.

For NORMAL/COMPLEX work, preserve the Issue as Human Task and JSON v2 as its
representation with normative equivalence and current contract_revision.
Keep mutable evidence outside normative contracts. An execution result must be
observed before EXECUTION_RECEIPT and VALIDATING; assignment is not execution.
Require validation and every REQUIRED owner's result before technical completion.
An Execution Report Comment (`EXECUTION_REPORT_COMMENT`) never replaces the task,
receipt or validation.
Human acceptance, merge and deploy gates remain explicit.

Select capabilities from the task and compatible cached routing evidence. Refresh
only missing, changed, failed or stale capabilities; expand discovery when the
selected owner cannot satisfy the need. Do not rediscover unrelated services or
reload unchanged references in the same context. Resume from persisted evidence
and verify its revision, scope and freshness after context loss.

Independent QA is required for changed behavior, bugfixes and regressions. UI/UX
is required for changed UI, responsiveness and accessibility. Security is required
for auth, secrets, permissions, sensitive data, payments, parsers, uploads,
webhooks, external integrations and infrastructure. DevOps owns containers,
CI/CD and infrastructure. Missing mandatory validation is BLOCKED/NOT VALIDATED,
never a reason to fabricate PASS. Only each owner attests its own PASS.

## Conditional procedure routes

Load the applicable phase procedure before acting; do not load this table as a
checklist of all files. References are relative to this canonical skill directory.

| Trigger | Required procedure | Additional references only when applicable |
| --- | --- | --- |
| First use, unclear role or repository onboarding | references/workflow-responsibilities.md | references/workflow-planning.md for onboarding |
| New/changed product scope, specs or repository readiness | references/workflow-planning.md | SDD or DevOps owner; references/capability-registry.md if capability selection is unresolved |
| Create/resume a NORMAL/COMPLEX Task or review its delivery | references/workflow-governance.md | references/context-routing.md for contract/source/sector routing |
| Execute/delegate NORMAL/COMPLEX work or recover a failed handoff | references/workflow-execution.md | references/harness-execution.md; references/skill-execution-contract.md; references/minimal-code-gate.md for implementation |
| Need new capability, unavailable tool or fallback | references/capability-registry.md | references/provider-routing.md only for provider selection/change; references/skill-owned-tools.md for tool state |
| Need supplementary context, knowledge or project-local capability | references/workflow-context.md | references/context-retrieval.md; references/continuous-improvement.md only for a verified gap |
| Material Issue checkpoint/report | references/execution-report-comments.md | Existing receipt and command results, summarized without copying full bodies |

API research during SDD routes to the existing canonical
`plugins/sdd-spec-factory/skills/sdd-spec-factory/references/api-research-library.md`.
Technical decisions route to
`plugins/sdd-spec-factory/skills/sdd-spec-factory/references/technical-knowledge-router.md`.
Resolve the active installed owner bundle rather than assuming sibling caches.
Missing/stale sources require bounded research and durable reference update;
never load all domain libraries. See references/workflow-context.md for details.

Existing approved specs, including GitHub Spec Kit artifacts, remain sources:
link exact paths/revisions/purposes in the existing contract instead of generating
another equivalent spec. SDD resolves actual gaps and contract equivalence; this
does not replace JSON v2 or silently waive an existing gate. Reuse one evidence
record by path/revision across receipts, report, Issue and PR; write each required
field but do not duplicate complete logs, specs or inventories in every artifact.

These are local conventions, not official OpenAI requirements. Detailed practice
provenance remains in references/workflow-responsibilities.md.

## Hard Limits (non-negotiable)

- **Never write product code directly outside confirmed TRIVIAL work.** Implementation is executed through
  `dev-implementation-standard` or another explicitly approved executor
  capability selected by the harness.
- **Never confuse assignment with execution.** A task is not delegated until the
  selected capability actually runs and returns an `EXECUTION_RECEIPT`.
- **Never mark work complete from a prompt, plan, task assignment, terminal open,
  or claimed intent alone.** Completion requires result plus validation evidence.
- **Never skip the intent contract.** Every change needs explicit scope,
  acceptance criteria, validation, and evidence. Durable spec files are required
  only when the complexity tier below requires them.
- **Never create a task without sufficient intent and acceptance criteria.**
  Link durable specs when the tier requires them.
- **Reject any executable task that does not follow the mandatory task structure for its tier.**
- Repo docs, PRDs, mockups, architecture notes, and `AGENTS.md` are source of truth.
- If docs conflict with code, stop and ask for a decision.
- Inspect the real repo, git status, scripts, and runtime before changing environment.
- Keep changes scoped; preserve public APIs, schemas, payloads, and business
  rules unless explicitly approved.
- Do not call work complete without validation evidence.
- No deploy is approved without an approved PR.
- Final acceptance belongs to the user.
- **Never treat documentation, Git or delivery work as a workflow exemption.**
  The Entry Gate applies before reading technical state, changing Markdown,
  creating commits, pushing branches, opening PRs or reporting completion.

## Change Complexity Gate

Classify the work before choosing artifacts. Complexity changes documentation
depth, not the obligation to validate.

- `TRIVIAL`: a localized, low-risk change with no behavior, architecture,
  security, data, dependency, or public-contract impact. Use an inline intent
  contract: scope, acceptance criterion, command/check, and evidence. A durable
  spec, task file, and Issue are optional unless repository policy requires one.
  Do not require a ten-sector matrix, JSON v2, SDD, execution lists, a separate
  executor runtime, or separate receipt/report templates for this path.
- `NORMAL`: bounded behavior or multi-file work with understood architecture.
  Use a concise Issue/task contract linked to the relevant existing docs; add a
  focused spec only for behavior that is not already specified.
- `COMPLEX`: architecture, cross-module behavior, migrations, sensitive data,
  security boundaries, substantial UI, integrations, or unresolved product
  decisions. Use durable SDD artifacts, executable tasks, traceability, and the
  applicable specialist gates.

When risk is uncertain, choose the higher tier. UI and security triggers are
based on affected surface and risk, not on the tier label.

### TRIVIAL inline execution

1. Inspect the request, current files, branch and diff. Record the objective,
   allowed paths, acceptance criterion and relevant validation in a short intent.
   Examples: correcting prose or a comment without changing executable content.
2. Check for behavior, architecture, infrastructure, security, data, dependencies,
   public contracts and specialist triggers. If any applies or is uncertain,
   reclassify before editing and use the full workflow. A visual/responsive change
   still triggers UI/UX; a small bugfix still triggers independent functional QA.
3. Execute in the same agent when available tools suffice. Load only a selected
   skill and its applicable references when needed; an existing compatible tool
   requires no whole-inventory discovery, provider probe or new agent. Search the
   affected scope for reuse before adding content. Never install or mutate remote
   infrastructure to make a trivial change possible.
4. Validate the actual diff and run the relevant check. If impact expands, stop
   this path, preserve the diff, and reclassify; do not silently expand scope.
5. Return changed paths, the check and result, limitations and branch/commit when
   present. This compact evidence replaces the separate SKILL_RECEIPT,
   REUSE_INVENTORY, MINIMAL_CODE_GATE, EXECUTION_RECEIPT and report templates only
   for this path. Never claim another agent ran or independent review occurred.

An existing Issue may receive one consolidated outcome. Missing remote access
does not block local TRIVIAL work unless repository policy requires it. Human
approval, protected paths, no secrets, no destructive actions, and no automatic
merge/deploy remain unchanged. These instructions are an agent protocol, not a
runtime authorization firewall or proof of token savings.
