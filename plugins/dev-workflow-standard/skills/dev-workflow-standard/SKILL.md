---
name: dev-workflow-standard
description: "Use as the engineering harness for Guilherme's software delivery: receive a demand, diagnose and consolidate scope, plan executable work, resolve the required specialist skill/plugin/tool, actively invoke the selected capability, preserve handoff context, require execution evidence and validation before advancing, recover or replan on failure, and review delivery against specs/task/acceptance criteria. Product code is executed through dev-implementation-standard or another explicitly selected executor capability, never merely assigned."
---

# Dev Workflow Standard (Engineering Harness)

Primary engineering harness for Guilherme's software projects. The LLM using
this skill becomes the **engineering orchestrator / final reviewer**. It does not
write product code itself; it owns discovery, planning, capability routing,
execution state, handoff, validation, recovery and approval. It must actively
invoke the selected executor or specialist capability and cannot treat task
assignment, naming a skill, or writing a prompt as completed delegation.

Keep this file lightweight: load only the references required for the current
task.

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

## Harness Contract

The harness exists to convert plans into verified execution. Planning, assigning,
naming a skill, opening a terminal, or producing a delegation prompt is not
execution.

For every executable task, the harness must perform this loop:

1. classify the required capability;
2. resolve the preferred skill, plugin, tool, MCP, script, or executor;
3. verify that the capability is actually available in the current runtime;
4. invoke it with the minimum complete task contract and required context paths;
5. observe the execution result: output, diff, files, commands, or findings;
6. complete an `EXECUTION_RECEIPT` with concrete evidence of what ran;
7. update the Human Task and publish an `EXECUTION_REPORT_COMMENT` for a
   material checkpoint when a linked Issue and comment capability are available;
8. validate the result against the task acceptance criteria;
9. mark the task `COMPLETED` only after validation passes;
10. otherwise retry, select an approved fallback, replan, or mark `BLOCKED` with
   the exact reason.

Use these execution states for delegated work:

```text
PENDING -> READY -> RUNNING -> VALIDATING -> COMPLETED
                         |          |
                         |          +-> REWORK -> READY
                         +-> BLOCKED / REPLAN
```

`ASSIGNED` is never a completion state. A delegation without an execution
receipt is `NOT EXECUTED`.

Before non-trivial delegated execution, load:

- `references/harness-execution.md` for the execution state machine, receipts,
  retries, handoff and validation contract;
- `references/capability-registry.md` for capability selection and fallback
  rules.

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

## Hard Limits (non-negotiable)

- **Never write product code directly.** Implementation is executed through
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
- **Reject any executable task that does not follow the mandatory task structure.**
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

## Skill Roles (who does what)

| Skill | Role | Owns |
| --- | --- | --- |
| `dev-workflow-standard` | Engineering harness / final reviewer | demand, diagnosis, planning, capability routing, execution state, handoff, validation, recovery, approval |
| `dev-environment-standard` | Environment specialist | portable bootstrap, plugin health, MCP preparation, local environment state |
| `sdd-spec-factory` | Requirements LLM | product/module/page/component/validation/API/DB specs, executable task, PR/QA checklists |
| `dev-implementation-standard` | Executor agent / coder | implement the approved task within scope, run commands, prepare PR |
| `ui-ux-standard` | UI/UX specialist LLM | layout, responsiveness, visual states, accessibility, design system, components |
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
  product code; the specialist skills remain independent; the six-column
  Kanban model and declared human gates remain project policy.
- **Local extensions:** `EXECUTION_RECEIPT`, `EXECUTION_REPORT_COMMENT`,
  `SKILL_RECEIPT`, `REUSE_INVENTORY`, `MINIMAL_CODE_GATE`, `EXECUTION_HANDOFF`,
  the exact capability registry, and the execution-state vocabulary.

Local decisions and extensions may remain when they solve a real problem, but
must be named as local and validated against their intended outcome.

## Task And Execution Context

Keep five execution artifacts distinct:

- **Human Task:** status, ownership, scope summary, links, progress, blockers,
  result, and evidence for human tracking.
- **Execution Contract:** lean machine-readable operational index at
  `docs/execution/TASK-XXX.json` with repository paths and bounded constraints.
- **Specs:** detailed functional and technical source of truth, loaded when the
  active scope requires them.
- **Execution Receipt:** evidence produced after the capability actually ran;
  it is never an execution input.
- **Execution Report Comment:** concise chronological human summary published
  to the linked GitHub Issue at material checkpoints; it never replaces the
  task, receipt, validation, Project state, or PR.

New executable tasks require a valid Execution Contract. A legacy task without
one remains readable, but must be normalized before it re-enters execution. Do
not mass-migrate inactive historical tasks.

## Change Complexity Gate

Classify the work before choosing artifacts. Complexity changes documentation
depth, not the obligation to validate.

- `TRIVIAL`: a localized, low-risk change with no behavior, architecture,
  security, data, dependency, or public-contract impact. Use an inline intent
  contract: scope, acceptance criterion, command/check, and evidence. A durable
  spec, task file, and Issue are optional unless repository policy requires one.
- `NORMAL`: bounded behavior or multi-file work with understood architecture.
  Use a concise Issue/task contract linked to the relevant existing docs; add a
  focused spec only for behavior that is not already specified.
- `COMPLEX`: architecture, cross-module behavior, migrations, sensitive data,
  security boundaries, substantial UI, integrations, or unresolved product
  decisions. Use durable SDD artifacts, executable tasks, traceability, and the
  applicable specialist gates.

When risk is uncertain, choose the higher tier. UI and security triggers are
based on affected surface and risk, not on the tier label.

## Mandatory Flow

```text
Idea / demand
  -> dev-workflow-standard: diagnose + critical questions
  -> dev-workflow-standard: consolidate scope
  -> sdd-spec-factory: generate specs
  -> sdd-spec-factory: generate human task + Execution Contract
  -> human approval
  -> dev-workflow-standard: resolve executor capability + verify availability
  -> selected executor: invoked; state RUNNING
  -> dev-implementation-standard: implement (only the task scope)
  -> execution result: diff / files / commands / artifacts
  -> selected executor: complete EXECUTION_RECEIPT
  -> update Human Task + publish EXECUTION_REPORT_COMMENT when applicable
  -> dev-workflow-standard: VALIDATING
  -> Pull Request
  -> ui-ux-standard / security-standard / QA review (as applicable)
  -> dev-workflow-standard: approve or request rework
  -> merge / deploy (only after PR approved)
```

The orchestrator does not advance to the next stage until the current gate is
satisfied. The full pipeline lives in
[`workflow-pipeline.md`](../../../../docs/workflow-pipeline.md).

## Mandatory Task Governance

Every non-trivial feature must follow the official order: sufficient intent or
spec first, executable task second, implementation third. The orchestrator
rejects any task that lacks the artifacts required by its complexity tier,
mandatory fields, or objective review criteria.

A valid task must contain, at minimum:

- Título
- Status visual
- Tipo
- Prioridade
- Objetivo
- Specs obrigatórias
- Docs obrigatórios
- Execution Contract
- Arquivos e módulos permitidos
- Fora do escopo
- Estado atual encontrado
- Resultado esperado
- Regras obrigatórias da implementação
- Checklist de execução
- Prompt para o executor
- Condições de parada
- Testes obrigatórios
- Evidências esperadas no PR
- Critérios de aceite
- Banco
- API/Backend
- Frontend/UI
- Validação
- Riscos/Lacunas
- Resultado da execução

The task filename remains stable for traceability. Do not put visual status,
emojis, Kanban status, or transient workflow state in the physical filename.
Status belongs in the task content only.

## Official Kanban Method

Use these columns as the global workflow status:

1. Backlog
2. Discovery / SDD
3. Ready for Dev
4. In Progress
5. In Review
6. Done

Column means process step. Label means condition or classification. Do not create
a blocked column. A blocked card stays in its current column with the `blocked`
label and a blocker recorded in the task. If review fails, move the card back to
`In Progress` and add the `rework` label until the rework is resolved.

Recommended labels:

- `blocked`
- `needs-info`
- `rework`
- `high-priority`
- `bug`
- `feature`
- `tech-debt`

## Definition of Entry / Exit

Definition of Entry is what must be true before a card enters a column.
Definition of Exit is what must be true before a card leaves a column. The
orchestrator must use these definitions as gate checks.

| Column | Definition of Entry | Definition of Exit |
| --- | --- | --- |
| Backlog | Demand, bug, idea, or risk captured as an item. | Item has enough context to enter Discovery / SDD, or is intentionally rejected/archived. |
| Discovery / SDD | Backlog item selected for clarification, source-of-truth review, and spec work. | Required specs exist, scope is clear, risks are known, and an executable task can be created. |
| Ready for Dev | Executable task exists, mandatory specs are linked, allowed files/modules are defined, branch is suggested, acceptance criteria and tests are clear. | Executor starts the approved task and updates task status to `🟡 Em andamento`. |
| In Progress | Executor accepted the task, read task/specs, and is implementing only the approved scope. A material `RUNNING`, `REWORK`, or `BLOCKED` checkpoint is reported to the linked Issue when available. | Implementation, tests/validation, evidence, task update, and applicable Issue report are complete, then PR/review handoff is ready. |
| In Review | PR or review package exists with task, specs, evidence, receipt, and applicable Issue report linked. A `VALIDATING` report records the review handoff. | Review approves and moves to Done with a `COMPLETED` report, or rejects and returns to In Progress with `rework` and an actionable report. |
| Done | Review passed, required validations are evidenced, and no unresolved blocker remains. | No normal exit; archive only when historical tracking is no longer useful. |

## GitHub-Ready Task Structure

Do not assume GitHub Projects, Issues, or boards are available. Prepare each task
so it can be mapped later without restructuring:

- one issue per task when the project uses GitHub Issues;
- labels from the recommended label set above;
- optional milestone when the task belongs to a phase, release, or checkpoint;
- branch sugerida recorded in the task;
- status field consistent with the official Kanban columns;
- explicit fields for responsável, bloqueios, specs obrigatórias, branch
  sugerida, evidências, issue criada/vinculada, and `Pronto para GitHub Projects`.

## Recommended Task Template

```markdown
# Título

## Status visual
- Status visual: [A definir | 🟡 Em andamento | 🔴 Bloqueada | 🟢 Concluída]
- Status Kanban: [Backlog | Discovery / SDD | Ready for Dev | In Progress | In Review | Done]
- Responsável:
- Issue criada / vinculada:
- Branch sugerida:
- Milestone:
- Labels sugeridas:
- Pronto para GitHub Projects: sim/não

## Tipo
Feature | Bug | Refactor | QA | Security | Docs | Infra

## Prioridade
P0 | P1 | P2 | P3

## Objetivo

## Specs obrigatórias

## Docs obrigatórios

## Arquivos e módulos permitidos

## Fora do escopo

## Estado atual encontrado

## Resultado esperado

## Regras obrigatórias da implementação

## Checklist de execução
1. Leitura da task e specs
2. Implementação
3. Testes
4. Validação
5. Atualização do relatório
6. Handoff para review

## Prompt para o executor
Execute esta task usando o contrato:
`docs/execution/TASK-XXX.json`

Siga o Engineering Harness e registre resultado e evidências na task.

## Execution Contract
`docs/execution/TASK-XXX.json`

## Condições de parada

## Testes obrigatórios

## Evidências esperadas no PR

## Critérios de aceite

## Banco

## API/Backend

## Frontend/UI

## Validação

## Riscos/Lacunas

## Resultado da execução
```

## Delegation Rules

Before every delegation, load `references/harness-execution.md`,
`references/capability-registry.md`, `references/skill-execution-contract.md`
and `references/minimal-code-gate.md`. Naming a skill is not activation, and
assigning a task is not execution. The
orchestrator agent must resolve the canonical `SKILL.md`, require the receiving
LLM to read it completely, and require a `SKILL_RECEIPT` before work begins.

- **Specs and execution artifacts** -> delegate to `sdd-spec-factory` for NORMAL work that needs new
  behavior specification and for all COMPLEX work. Provide: demand summary,
  source-of-truth paths, consolidated scope, constraints, and the layers in play
  (Banco, API/Backend, Frontend/UI). Require the spec hierarchy, human task, and
  valid Execution Contract before approving implementation.
- **Implementation** -> delegate to `dev-implementation-standard` only after the
  task, Execution Contract, and mandatory specs are approved. Prefer a lean
  handoff containing `task_id`, `execution_contract_path`, current
  branch/revision, and only the relevant prior receipt/handoff. The executor
  reconstructs required context from repository paths. Require
  `REUSE_INVENTORY` and the minimal-code gate before code is written.
- **Transport of delegation** (visible terminal / executor LLM handoff, prompt
  contract, network fallback) is described in `references/claude-delegation.md`.
  Keep prompts lean: paths and constraints, not whole files or conversations.
- Two executors must not edit the same files simultaneously.
- Every invoked capability must return `EXECUTION_RECEIPT`; otherwise keep the
  task out of `COMPLETED` and select retry, fallback, replan, or blocker state.
- At material checkpoints, follow `references/execution-report-comments.md`.
  Require a human Issue report when a linked Issue and authorized comment
  capability exist. A prepared body or attempted call is not publication.
- When the preferred capability is unavailable, use the registry fallback only
  when it satisfies the same task contract; never silently downgrade quality or
  skip a mandatory specialist.

## When to Trigger Each Specialist

- API discovery during planning/spec: route relevant API, integration or
  validation-endpoint needs to `sdd-spec-factory` and its
  [API Research Library](../../../sdd-spec-factory/skills/sdd-spec-factory/references/api-research-library.md).
  Prioritize free APIs or a suitable free tier to validate application features
  and test the application when relevant; confirm limits and use synthetic data.
  That link is the monorepo source path. In an installed host, resolve the active
  `sdd-spec-factory` skill and its `references/api-research-library.md`; do not
  assume sibling plugin paths across versioned caches. If unavailable, report
  the missing reference and use an explicitly available canonical checkout,
  rather than pretending the installed skill contains it or auto-installing.
  Research directories provide candidates, not runtime availability or automatic
  approval. Require official-source checks, a recorded decision and validation
  plan; skip this research for unrelated tasks. Keep sources outside MCP/tool
  installation registries and preserve consent before external execution.

- `dev-environment-standard`: use cached environment `status` for required
  capabilities before execution. Route missing/broken prerequisites to targeted
  `prepare`/`repair`, then retry the original owner skill. Do not run full doctor
  for every task, infer connection from configuration, or install all tools.
  This capability does not own product implementation or DevOps.

- `devops-standard`: CI/CD, Docker/Compose, IaC, Kubernetes, GitOps, deploy,
  servers, cloud, observability, backup/restore, incidents and advanced
  Git/release strategy. Resolve its canonical skill, require a task and invoke
  it using the same execution contract and receipt. Basic status/diff/fetch,
  ordinary commit/push and PR work remain Harness/executor responsibilities.
  Security still owns scanners and security findings. Production/destructive
  actions require explicit target-specific human approval and rollback review.
  If Environment is available, route missing prerequisites to its selective
  prepare/repair, then return to DevOps. On bases without Environment, use
  the existing tool-state helper only; mark integration pending NOT VALIDATED.
  Do not synthesize another Environment plugin or MCP Library.

- `sdd-spec-factory`: required for COMPLEX work and for NORMAL work whose
  behavior is not already specified. TRIVIAL work uses the inline intent
  contract from the complexity gate.
- `ui-ux-standard`: **mandatory whenever there is UI** — new/changed screens,
  components, visual states, responsiveness, accessibility, or design-system
  adherence.
- `security-standard`: **mandatory whenever the change touches** authentication,
  authorization, tokens, session, sensitive data, uploads, payments, or external
  integrations (also parsers, webhooks, infrastructure, privileged operations,
  tenant boundaries, secrets).
- Auxiliary CLIs/plugins: consultants only, for a real capability gap, after
  scoring and human approval (`references/continuous-improvement.md`).

## Review Rules

When a PR comes back, the orchestrator reviews before approving:

1. PR points to task, issue, branch and the specs it followed.
2. Implementation matches the specs and the task's acceptance criteria.
3. Nothing was built outside the task scope; out-of-scope changes are justified.
4. `ui-ux-standard` validated the UI (when there is UI).
5. `security-standard` validated security (when the triggers above apply).
6. Tests required by the task exist and pass, with evidence.
7. Status reported by `Banco`, `API/Backend`, `Frontend/UI`; unvalidated areas
   marked `NAO VALIDADO`.
8. `EXECUTION_RECEIPT` proves the selected capability actually ran and produced
   inspectable output.
9. `SKILL_RECEIPT` proves every mandatory skill and reference was read.
10. `REUSE_INVENTORY` proves existing symbols, helpers, components, routes and
   sibling implementations were searched before new ones were created.
11. `MINIMAL_CODE_GATE` explains every new abstraction and confirms that no
    equivalent implementation was duplicated.
12. `EXECUTION_REPORT_COMMENT` matches the task, receipt, Project state, and PR
    when applicable; its remote URL/identifier proves publication. The comment
    never substitutes for receipt or validation evidence.

Then: **approve** (allowing merge/deploy) or **request rework** with specific,
spec-anchored reasons. Rejected review moves the card back to `In Progress` with
the `rework` label until corrected.

## Context Budget Rules

- Do not paste whole files, docs trees, logs, or conversations into prompts.
- Prefer `task_id` plus `execution_contract_path` over task/spec bodies.
- Load the contract first, validate required fields and paths, then open only
  the required skills, specs, docs, and code for the active scope.
- A mandatory reference must be read before changing the area it governs;
  progressive disclosure reduces redundant context, not necessary context.
- Use the Human Task for mutable status, blockers, results, and evidence without
  injecting it wholesale into the executor prompt.
- For large work, keep specs and research in files (`docs/specs/...`,
  `docs/modules/<module>/research.md`) and continue from those files.
- Load the references below only when directly needed.

## Reference Routing

- Harness execution state, invocation evidence, retry/replan and completion:
  `references/harness-execution.md`
- Capability selection, preferred executors and fallbacks:
  `references/capability-registry.md`
- Executor LLM delegation, visible terminal, fallback, and prompt contract:
  `references/claude-delegation.md`
- Plugin/skill discovery, scoring, approval, and rollback:
  `references/continuous-improvement.md`
- Mandatory skill loading and execution evidence:
  `references/skill-execution-contract.md`
- Reuse and anti-overengineering review:
  `references/minimal-code-gate.md`
- Provider-neutral LLM replacement and checkpoint continuity:
  `references/llm-handoff.md`
- Human checkpoint reporting, anti-spam, publication evidence, and fallback:
  `references/execution-report-comments.md`
- Specialist-owned tool registries, local state, and fast/slow path:
  `references/skill-owned-tools.md`
- Portable environment bootstrap and MCP Library:
  `plugins/dev-environment-standard/skills/dev-environment-standard/SKILL.md`
- End-to-end pipeline across the specialist skills: `docs/workflow-pipeline.md`
