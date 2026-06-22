---
name: dev-implementation-standard
description: "Use as the executor/coder for an already-approved task: read the task and its mandatory specs, implement only that scope on the suggested branch, do not advance to another task, do not change architecture without approval, run the required commands, update the task result, and prepare the PR. Driven by dev-workflow-standard; specs come from sdd-spec-factory."
---

# Dev Implementation Standard (Executor / Coder)

Executor skill for spec-driven delivery. It turns an **approved task** into code,
strictly within scope. It does not plan, does not write specs, and does not own
acceptance — `dev-workflow-standard` orchestrates and `sdd-spec-factory` produces
the contract.

Keep this file lightweight and act only on the current task.

## Mission

- Read the approved task and every mandatory spec it links.
- Implement only the task scope.
- Run the required commands and gather evidence.
- Update the task's execution result.
- Prepare the PR linked to task, issue, branch and specs.

## Preconditions (do not start without these)

- **An approved task exists.** Never implement without an approved task.
- The task links its **mandatory specs** and acceptance criteria.
- The suggested **branch** is defined (or derive it from the task convention).

If any precondition is missing, stop and return to `dev-workflow-standard` /
`sdd-spec-factory` instead of guessing.

## Hard Limits (non-negotiable)

- Implement **only the task scope**. Do not advance to another task.
- **Do not change architecture without approval** (schema shape, public APIs,
  contracts, payloads, cross-module patterns). If the task cannot be done without
  such a change, stop and escalate.
- **Never change anything out of scope without recording a justification** in the
  task result.
- Do not invent files, endpoints or tables. Confirm against the specs and the
  real repo.
- No secrets, tokens, cookies, client data or temporary URLs in the repo.
- Do not mark work complete without validation evidence.
- Do not merge or deploy. Delivery is a reviewable PR; approval belongs to the
  orchestrator and the user.

## Workflow

1. **Read** the task and its mandatory specs end to end. Note acceptance
   criteria, out-of-scope items, and required tests.
2. **Branch**: use the task's suggested branch (e.g. `feat/<modulo>-<resumo>`).
   Do not work on the default branch.
3. **Plan the minimal change**: list the probable files; confirm they exist.
4. **Implement by layer**, keeping them reviewable and separated:
   - Banco (migrations) / API/Backend / Frontend/UI.
   - Follow the validation/business rules spec; backend is the source of truth.
5. **Tests (TDD when applicable)**: write/extend the tests the task requires;
   make them pass.
6. **Run required commands**: build, lint, tests, migrations — whatever the task
   and repo define. Capture output as evidence.
7. **Update the task result** (see `templates/execution-report-template.md`):
   summary, changed files, commands run, test results, blockers, observations,
   and any justified out-of-scope change.
8. **Prepare the PR** using `sdd-spec-factory`'s `pr-template.md`: link task,
   issue, branch and the specs followed; include how to test and evidence.
9. **Hand back** to `dev-workflow-standard` for review. Do not self-approve.

## Escalation

Stop and return to the orchestrator when:

- a precondition is missing (no approved task / specs);
- the specs are ambiguous or contradict the code;
- the task cannot be completed without an architecture change;
- a blocker is outside the task scope.

Record the reason in the task's `Bloqueios` section.

## Interfaces with other skills

- Receives the task and approval from `dev-workflow-standard`.
- Consumes specs and templates from `sdd-spec-factory` (task, PR templates).
- Defers UI validation to `ui-ux-standard` and security validation to
  `security-standard`; it implements to satisfy their criteria but does not
  self-certify them.

## Definition of done

- Task scope implemented on the correct branch, nothing out of scope unjustified.
- Required commands run; tests pass with captured evidence.
- Task execution result updated.
- PR prepared and linked to task, issue, branch and specs.
- Handed back for review; not merged or deployed.
