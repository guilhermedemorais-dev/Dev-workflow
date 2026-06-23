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

- Read the approved task and every mandatory spec it links before coding.
- Execute the task's prompt-base as the operational contract.
- Implement only the task scope.
- Run the required commands and gather evidence.
- Update the task's execution result.
- Prepare the PR linked to task, issue, branch and specs.

## Preconditions (do not start without these)

- **An approved task exists.** Never implement without an approved task.
- The task links its **mandatory specs** and acceptance criteria.
- The suggested **branch** is defined (or derive it from the task convention).
- The task has GitHub-ready fields: status, responsável, bloqueios, specs
  obrigatórias, branch sugerida and evidências.

If any precondition is missing, stop and return to `dev-workflow-standard` /
`sdd-spec-factory` instead of guessing.

## Hard Limits (non-negotiable)

- Implement **only the task scope**. Do not advance to another task.
- **Do not change architecture without approval** (schema shape, public APIs,
  contracts, payloads, cross-module patterns). If the task cannot be done without
  such a change, stop and escalate.
- **Never change anything out of scope.** If leaving scope is required, stop and
  record it in `Bloqueios`.
- Do not invent files, endpoints or tables. Confirm against the specs and the
  real repo.
- No secrets, tokens, cookies, client data or temporary URLs in the repo.
- Do not mark work complete without validation evidence.
- Do not merge or deploy. Delivery is a reviewable PR; approval belongs to the
  orchestrator and the user.

## Task Status Rules

Visual status is updated in the task content, never in the physical filename:

- `🟡 Em andamento`: set this when starting execution.
- `🔴 Bloqueada`: set this when blocked, with the reason in `Bloqueios`.
- `🟢 Concluída`: set this only after implementation and validation evidence are
  recorded.

The task filename remains stable. Do not use emojis or status prefixes in the
filename.

## Workflow

1. **Read** the whole task and every mandatory spec end to end before coding.
   Note acceptance criteria, out-of-scope items, and required tests.
2. **Set status** to `🟡 Em andamento` in the task content.
3. **Execute the prompt-base** from `Prompt para o executor` as the operational
   contract.
4. **Follow the checklist in order**. Do not reorder work unless the task or
   orchestrator explicitly allows it.
5. **Branch**: use the task's suggested branch (e.g. `feat/<modulo>-<resumo>`).
   Do not work on the default branch.
6. **Plan the minimal change**: list the probable files; confirm they exist.
7. **Implement by layer**, keeping them reviewable and separated:
   - Banco (migrations) / API/Backend / Frontend/UI.
   - Follow the validation/business rules spec; backend is the source of truth.
8. **Tests (TDD when applicable)**: write/extend the tests the task requires;
   make them pass.
9. **Run required commands**: build, lint, tests, migrations — whatever the task
   and repo define. Capture output as evidence.
10. **Update the task result** (see `templates/execution-report-template.md`):
    prompt used, checklist executed, changed files, commands run, evidence,
    blockers, layer results, risks and gaps.
11. **Set final status**: `🔴 Bloqueada` if blocked, or `🟢 Concluída` only when
    evidence supports completion.
12. **Prepare the PR** using `sdd-spec-factory`'s `pr-template.md`: link task,
    issue, branch and the specs followed; include how to test and evidence.
13. **Hand back** to `dev-workflow-standard` for review. Do not self-approve.

## GitHub Projects Readiness

Do not assume GitHub Projects is available. Keep the task ready for future
mapping by preserving these fields in the task content:

- status
- responsável
- bloqueios
- specs obrigatórias
- branch sugerida
- evidências

If the fields are missing, stop before implementation and ask the orchestrator
to normalize the task.

## Recommended Task Template

```markdown
# Título

## Status visual
- Status: [A definir | 🟡 Em andamento | 🔴 Bloqueada | 🟢 Concluída]
- Responsável:
- Issue criada / vinculada:
- Branch sugerida:
- Milestone:
- Labels sugeridas:
- Pronto para entrar no GitHub Projects: sim/não

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
1.
2.
3.

## Prompt para o executor
Use esta task como contrato operacional. Leia a task inteira e todas as specs
obrigatórias antes de codar. Siga o checklist na ordem, limite-se aos arquivos e
módulos permitidos, pare se precisar sair do escopo ou alterar arquitetura, rode
os testes obrigatórios e preencha o Resultado da execução com evidências.

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

## Escalation

Stop and return to the orchestrator when:

- a precondition is missing (no approved task / specs);
- the specs are ambiguous or contradict the code;
- the task cannot be completed without an architecture change;
- leaving the approved scope is required;
- a blocker is outside the task scope.

Record the reason in the task's `Bloqueios` section and update visual status to
`🔴 Bloqueada`.

## Interfaces with other skills

- Receives the task and approval from `dev-workflow-standard`.
- Consumes specs and templates from `sdd-spec-factory` (task, PR templates).
- Defers UI validation to `ui-ux-standard` and security validation to
  `security-standard`; it implements to satisfy their criteria but does not
  self-certify them.

## Definition of done

- Task scope implemented on the correct branch, nothing out of scope unjustified.
- Required commands run; tests pass with captured evidence.
- Task execution result fully filled with the mandatory final report.
- PR prepared and linked to task, issue, branch and specs.
- Handed back for review; not merged or deployed.
