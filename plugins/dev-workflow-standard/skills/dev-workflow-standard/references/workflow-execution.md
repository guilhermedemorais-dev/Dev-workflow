# Workflow Execution

Read only when selected by the owning SKILL.md route. Backtick paths beginning
with `references/` are relative to that skill directory, not this file.

## Harness Contract

The harness exists to convert plans into verified execution. Planning, assigning,
naming a skill, opening a terminal, or producing a delegation prompt is not
execution.

For every executable task, the harness must perform this loop:

1. classify the required capability;
2. resolve the preferred skill, plugin, tool, MCP, script, or executor;
3. verify that the capability is actually available in the current runtime;
4. resolve the owner skill before selecting a provider/model; if an executor LLM
   is needed, reuse current compatible runtime verification or verify with the
   provider resolver when selecting/changing/recovering the runtime; do not
   equate configured credentials with availability;
5. invoke it with the minimum complete task contract and required context paths;
6. observe the execution result: output, diff, files, commands, or findings;
7. complete an `EXECUTION_RECEIPT` with concrete evidence of what ran;
8. update the Human Task and publish an `EXECUTION_REPORT_COMMENT` for a
   material checkpoint when a linked Issue and comment capability are available;
9. validate the result against the task acceptance criteria;
10. mark the task `COMPLETED` only after validation passes;
11. otherwise retry, select an approved fallback, replan, or mark `BLOCKED` with
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

Before non-trivial delegated execution, load applicable references not already
read at this revision in the active context:

- `references/harness-execution.md` for the execution state machine, receipts,
  retries, handoff and validation contract;
- `references/capability-registry.md` when capability selection/fallback is
  missing, stale or insufficient;
- `references/provider-routing.md` when an executor LLM/provider must be
  selected or changed;
- `references/context-retrieval.md` when supplemental project context beyond
  routed normative sources is needed.

## Delegation Rules

Use the Task's current owner/tool selection and compatible Environment evidence.
When selection is missing, stale or insufficient, consult the relevant owner
metadata through `references/capability-registry.md`; expand only for a real gap.

Before delegated execution, read `references/harness-execution.md` and
`references/skill-execution-contract.md` unless already loaded at this revision
in the active context. Read `references/minimal-code-gate.md` for implementation,
not unrelated read-only operations. Naming a skill is not activation, and
assigning a task is not execution. Resolve the canonical `SKILL.md`, require the
receiving LLM to read it completely and emit a `SKILL_RECEIPT` before work.
On context loss reload selected normative sources rather than trust memory.

Reuse an available authorized executor for compatible lists instead of spawning
one runtime per microtask. A role switch is not evidence of independent review:
required QA/Security/UI validations retain their actual owner and independence.

- **Specs and execution artifacts** -> delegate to `sdd-spec-factory` for NORMAL work that needs new
  behavior specification and for all COMPLEX work. Provide: demand summary,
  source-of-truth paths, consolidated scope, constraints, and the layers in play
  (Banco, API/Backend, Frontend/UI). Require the spec hierarchy, human task, and
  valid Execution Contract before approving implementation.
- **Implementation** -> delegate to `dev-implementation-standard` only after the
  task, Execution Contract, and mandatory specs are approved. Prefer a bounded
  list prompt linking the single Task JSON file, containing `task_id`, `list_id`,
  `execution_contract_path`, sector, phase, current
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
