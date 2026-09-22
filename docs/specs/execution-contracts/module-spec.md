# Lean execution contracts

## Objective

Separate human task tracking from the minimum machine-readable contract needed
to start execution in a fresh session, while preserving specs, governance,
traceability, validation, and evidence.

## Architecture

```text
Spec -> Human Task -> Execution Contract -> Executor
                                      -> Execution Receipt -> Validation
```

- Spec: detailed functional and technical source of truth.
- Human Task: status, ownership, scope summary, checkpoints, blockers, result.
- Execution Contract: lean operational index with repository paths and bounded
  execution constraints.
- Prompt: short bootstrap pointing to the contract.
- Execution Receipt: output evidence produced after real execution.

## Contract requirements

New executable tasks must have `docs/execution/TASK-XXX.json` containing:

- `schema_version`
- `task_id`
- `task_path`
- `goal`
- `specs`
- `docs`
- `allowed_paths`
- `out_of_scope`
- `requirements`
- `acceptance_criteria`
- `required_tests`
- `required_skills`
- `stop_conditions`

The JSON stores concise values and paths. It must not contain full specs, long
prompts, conversation transcripts, secrets, or execution evidence.

## Progressive disclosure

The executor loads the contract first, validates it, then opens only the
referenced skills, specs, docs, and code needed for the active scope. A path
marked mandatory must be loaded before changing the area it governs. The human
task is consulted for mutable status, blockers, handoff, and results rather than
being injected wholesale.

## Legacy compatibility

- New executable task: contract required.
- Legacy task without a contract: remains readable and is not silently broken.
- When a legacy task re-enters execution, normalize it by generating and
  validating a contract before code changes.
- Do not mass-migrate historical tasks.

## Layers

- Banco: N/A, documentation/plugin workflow only.
- API/Backend: N/A, no runtime service.
- Frontend/UI: N/A, human-facing Markdown structure only.
- Security: JSON must not embed secrets or untrusted executable instructions.
- Tests: structural unittest coverage and JSON parsing.
- Observability: validation commands and exit codes persisted in TASK-002.

## Acceptance criteria

1. The task template links an Execution Contract and contains a short prompt.
2. A valid reusable JSON template exists.
3. SDD produces task plus contract for new executable work.
4. The executor starts from the contract and uses progressive disclosure.
5. Harness delegation prefers IDs and paths over duplicated bodies.
6. `EXECUTION_RECEIPT` is documented and tested as output, not input.
7. `EXECUTION_HANDOFF` preserves `execution_contract_path`.
8. Legacy fallback is explicit and non-destructive.
9. Existing governance and specialist gates remain intact.
