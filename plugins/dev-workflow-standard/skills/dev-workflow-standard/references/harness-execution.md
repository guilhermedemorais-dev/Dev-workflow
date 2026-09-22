# Engineering Harness Execution Contract

This reference defines how `dev-workflow-standard` turns an approved plan into
verified execution.

## Execution States

Use exactly these states for each delegated checkpoint:

- `PENDING`: task exists but prerequisites are incomplete.
- `READY`: task contract, specs, scope and capability are resolved.
- `RUNNING`: the selected capability has actually been invoked.
- `VALIDATING`: execution returned and evidence is being checked.
- `REWORK`: execution ran but validation failed and correction is required.
- `BLOCKED`: no safe capable path can continue without user input or an external dependency.
- `COMPLETED`: execution evidence exists and all required validation passed.

Do not use `ASSIGNED` as a completion state.

## Mandatory Execution Loop

For every executable checkpoint:

1. Confirm task/spec/source-of-truth prerequisites.
2. Resolve the required capability via `capability-registry.md`.
3. Verify the preferred capability is available in the current runtime.
4. Invoke the capability. Naming it, planning for it, or drafting a prompt is not invocation.
5. Set `RUNNING` and execute the bounded checkpoint.
6. Inspect the returned output, diff, files, commands, artifacts or specialist findings.
7. Complete an `EXECUTION_RECEIPT` from that observed result.
8. Set `VALIDATING` and check acceptance criteria and mandatory specialist rules.
9. If validation passes, mark `COMPLETED`.
10. If validation fails, mark `REWORK` and invoke the responsible capability again.
11. If the capability fails or becomes unavailable, select an approved fallback or create an `EXECUTION_HANDOFF`.
12. Mark `BLOCKED` only when no safe capable path remains.

## EXECUTION_RECEIPT

Every invoked capability must return or be represented by this evidence. The
receipt may be opened while state is `RUNNING`, but it is not complete until the
execution result and command evidence have been observed:

```text
EXECUTION_RECEIPT
- task_id:
- capability:
- provider_or_runtime:
- executor:
- state: RUNNING | VALIDATING | REWORK | BLOCKED | COMPLETED
- invocation_evidence:
- inputs_used:
- outputs_produced:
- changed_files_or_artifacts:
- commands_and_results:
- validation_evidence:
- blockers:
- next_safe_action:
```

A task without `invocation_evidence` is `NOT EXECUTED`.

A task without `validation_evidence` cannot be `COMPLETED`.

`EXECUTION_RECEIPT` is a local Engineering Harness extension. It adapts the
consolidated practice of retaining inspectable tool output and validation
evidence; this name and schema are not claimed as an OpenAI or industry standard.

## Invocation Evidence

Valid evidence depends on the capability:

- skill/specialist: canonical `SKILL.md` loaded plus specialist output
- code executor: process/tool invocation plus resulting diff/files
- MCP/plugin/tool: actual tool call plus returned result
- script: command plus exit status/output
- reviewer: concrete findings tied to files/specs/criteria

The orchestrator must not fabricate evidence from intended actions.

## Handoff Contract

Each capability receives only the minimum complete context:

- `task_id`
- `execution_contract_path`
- current branch/revision when code is involved
- relevant prior receipts
- relevant prior handoff, when resuming another executor

The executor validates the contract first and loads the Human Task, mandatory
specs, source-of-truth files, and code on demand. Do not paste those bodies into
the bootstrap prompt. An `EXECUTION_RECEIPT` is produced after execution from
observed evidence; it is never treated as an implementation input for the same
checkpoint. The output of one capability becomes explicit input to the next
only when there is a dependency. Conversation memory alone is not a source of
truth.

## Recovery

When an invocation fails:

1. record the failure in the receipt;
2. classify the failure as capability unavailable, provider unavailable, invalid
   output, validation failure, scope conflict or source-of-truth conflict;
3. retry only when the failure is transient and retrying is safe;
4. otherwise use an approved fallback from the capability registry;
5. if switching executor/provider, create or update `EXECUTION_HANDOFF`;
6. never restart completed work merely because the provider changed.

## Completion Gate

The harness may mark a checkpoint `COMPLETED` only when all are true:

- selected capability actually ran;
- required skill receipts exist;
- expected output exists;
- acceptance criteria were checked;
- mandatory tests/reviews passed or are explicitly marked not applicable;
- no unresolved blocker remains;
- evidence is inspectable from repository/tool state.
