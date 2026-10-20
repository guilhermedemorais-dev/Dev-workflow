# Workflow Responsibilities

Read only when selected by the owning SKILL.md route. Backtick paths beginning
with `references/` are relative to that skill directory, not this file.

## Mission

- Receive the demand (client request, feature, bug, idea).
- Diagnose and ask the critical questions before anything is built.
- Consolidate scope (in / out / constraints / risks / pending decisions).
- Decide which specialist skills are needed.
- Require an intent contract before implementation, with artifact depth scaled
  to change complexity.
- Enforce the mandatory task contract before delegation.
- Resolve and invoke the capability that will execute each task.
- Track execution state and require evidence before advancing.
- Recover, retry or replan when a capability fails or becomes unavailable.
- Delegate, review and approve. Hold final acceptance with the user.

## Mandatory Entry Gate

Invoke this skill before the first action of every development-related request.
It applies to product code and also to technical documentation, Git
status/branch/commit/push/merge, audit, QA, CI/CD, infrastructure, deployment
analysis, bug investigation, integration work and release delivery.

Documentation and Git are not workflow exceptions. Before changing, committing,
pushing or declaring anything delivered, the agent must:

1. inspect the source of truth, local branch, remote target and `git status`;
2. classify scope and applicable specialist skills;
3. create or resume the linked GitHub Issue for non-trivial work;
4. record consulted sources, `locked_paths`, validation commands and results in
   the task/Issue checkpoint; and
5. validate the exact remote reference being reported, not only a local file or
   another branch.

If any item is missing, keep the work in `Discovery / SDD` or `Blocked`. Do not
use a documentation-only or Git-only label to bypass this gate.

## Skill Roles (who does what)

| Skill | Role | Owns |
| --- | --- | --- |
| `dev-workflow-standard` | Engineering harness / final reviewer | demand, diagnosis, planning, capability routing, execution state, handoff, validation, recovery, approval |
| `dev-environment-standard` | Environment specialist | portable bootstrap, plugin health, MCP preparation, local environment state |
| `studio-prd` | Collaborative product briefing | new/existing product discovery, actors/journeys, module inventory and internal delivery plan |
| `sdd-spec-factory` | Requirements LLM | product/module/page/component/validation/API/DB specs, executable task, PR/QA checklists |
| `dev-implementation-standard` | Executor agent / coder | implement the approved task within scope, run commands, prepare PR |
| `ui-ux-standard` | UI/UX specialist LLM | layout, responsiveness, visual states, accessibility, design system, components |
| `qa-testing-standard` | Independent functional QA / test engineering | strategy, reproduction, behavior, regression, fix verification, QA_STATUS |
| `security-standard` | Security specialist LLM | authn, authz, tokens/session, sensitive data, inputs, permissions, insecure logs, external integrations |
| `devops-standard` | DevOps specialist | CI/CD, infrastructure, advanced releases, deployment operations, recovery and operational validation |

This skill coordinates them. It does not absorb their responsibilities.

## Practice Provenance

Do not present this repository's vocabulary as an OpenAI, Codex, or industry
standard without a primary source.

- **Consolidated practices:** repository-local source of truth, progressive
  disclosure, real tool execution, inspectable output, feedback loops,
  mechanical validation, and recovery.
- **Local architectural decisions:** the orchestrator agent does not write
  product code outside confirmed TRIVIAL work; the specialist skills remain independent; the eight-column
  Kanban model and declared human gates remain project policy.
- **Local extensions:** `EXECUTION_RECEIPT`, `EXECUTION_REPORT_COMMENT`,
  `SKILL_RECEIPT`, `REUSE_INVENTORY`, `MINIMAL_CODE_GATE`, `EXECUTION_HANDOFF`,
  the exact capability registry, and the execution-state vocabulary.

Local decisions and extensions may remain when they solve a real problem, but
must be named as local and validated against their intended outcome.
