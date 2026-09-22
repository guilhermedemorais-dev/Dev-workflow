# Human Execution Reporting

## Objective

Add a concise chronological human report to the GitHub Issue linked to an
executing task without replacing repository evidence or the Project workflow.

## Artifact boundaries

- `TASK.md`: persistent technical task record.
- `execution-contract.json`: lean operational input for an executor.
- `EXECUTION_RECEIPT`: structured evidence produced after execution.
- `EXECUTION_REPORT_COMMENT`: human-readable checkpoint report published to the
  linked GitHub Issue when commenting is available.
- GitHub Project/Board: visual workflow state.
- PR: reviewable delivery.

## Checkpoint policy

Publish only for material state or outcome changes: `RUNNING`, `VALIDATING`,
`REWORK`, `BLOCKED`, and `COMPLETED`. Consolidate multiple small operations in
one comment and do not publish an identical report twice.

The report may derive facts from the task, receipt, diff, and command results.
It must contain concise, verifiable technical rationale, never private
chain-of-thought.

## Publication contract

- Resolve the real linked Issue before publishing.
- Record the returned comment URL or identifier as publication evidence.
- Never claim publication from a prepared body or attempted command.
- When the Issue or comment capability is unavailable, persist the report in
  the Human Task and record `NOT PUBLISHED` with the reason.
- Absence of a remote comment does not replace validation or make unvalidated
  work valid.

## State-specific content

- `RUNNING`: started scope, method, reuse target, next material checkpoint.
- `VALIDATING`: delivered scope, commands/results, unvalidated areas.
- `REWORK`: failed criterion, evidence, known cause, correction strategy.
- `BLOCKED`: concrete blocker, impact, completed scope, required decision, safe
  next step.
- `COMPLETED`: delivery, method, decisions, validation, residual risks,
  out-of-scope items, branch/commit/PR when available.

## Layer impact

- Banco: N/A, no data model.
- API/Backend: N/A, no product runtime.
- Frontend/UI: N/A, no interface change.
- Security: GitHub publication must never include secrets or private reasoning.
- Observability: Issue comment URL/identifier is publication evidence.

## Acceptance criteria

1. Harness and executor distinguish comment from receipt.
2. Task and receipt remain mandatory sources of truth.
3. Publication requires returned remote evidence.
4. Material checkpoints and anti-spam behavior are explicit.
5. REWORK, BLOCKED, and COMPLETED have useful required content.
6. Technical rationale is concise and verifiable; chain-of-thought is excluded.
7. Issue, Project, task, PR, and existing execution-contract behavior remain intact.
8. README and structural tests describe and enforce the final architecture.
