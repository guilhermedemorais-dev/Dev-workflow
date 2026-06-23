---
name: dev-implementation-standard
description: "Use as the executor/coder for an already-approved task: read the task and its mandatory specs, implement only that scope on the suggested branch, do not advance to another task, do not change architecture without approval, run the required commands, update the task result, and prepare the PR. Driven by dev-workflow-standard; specs come from sdd-spec-factory."
---

# Dev Implementation Standard (Executor / Coder)

Executor skill for spec-driven delivery. It turns an **approved task** into code,
strictly within scope. It does not do SDD, does not plan product scope, does not
write specs, and does not own acceptance — `dev-workflow-standard` orchestrates and `sdd-spec-factory` produces
the contract.

Keep this file lightweight and act only on the current task.

## Mission

- Read the approved task and every mandatory spec it links before coding.
- Execute the task's prompt-base as the operational contract.
- Implement only the task scope.
- Use TDD when applicable.
- Run required tests and validation, with evidence.
- Update the task's execution result and final report.
- Return the work for review with task, issue, branch and specs linked.

## Preconditions (do not start without these)

- **An approved task exists.** Never implement without an approved task.
- SDD/spec work is already complete. The executor does not do SDD.
- The task links its **mandatory specs** and acceptance criteria.
- The suggested **branch** is defined (or derive it from the task convention).
- The task has GitHub-ready fields: status, responsável, bloqueios, specs
  obrigatórias, branch sugerida, evidências, and issue criada/vinculada.

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

1. **Leitura da task e specs**: read the whole approved task and every mandatory
   spec end to end before coding. Confirm scope, allowed files/modules,
   acceptance criteria, out-of-scope items, required tests, and blockers.
2. **Set status** to `🟡 Em andamento` in the task content when starting.
3. **Execute the prompt-base** from `Prompt para o executor` as the operational
   contract.
4. **Implementação**: implement only the approved scope, by layer when relevant:
   Banco, API/Backend, Frontend/UI. Do not invent files, endpoints, tables,
   payloads, or architecture.
5. **TDD/Testes**: use TDD when applicable. If full TDD is not viable, record why
   and perform manual validation with objective evidence.
6. **Validação**: run the task-required commands, build, lint, tests,
   migrations, UI checks, or manual checks defined by the repo/task. Capture
   evidence.
7. **Atualização do relatório**: fill the mandatory final report in
   `templates/execution-report-template.md`, including prompt used, checklist
   executed, evidence, layer results, risks, gaps, blockers, and GitHub-ready
   fields.
8. **Set final status**: `🔴 Bloqueada` if blocked, or `🟢 Concluída` only when
   implementation and validation evidence support completion.
9. **Handoff para review**: prepare the PR or review package linked to task,
   issue, branch and specs, then return to `dev-workflow-standard`. Do not
   self-approve, merge, or deploy.

## GitHub Projects Readiness

Do not assume GitHub Projects is available. Keep the task ready for future
mapping by preserving these fields in the task content:

- status visual
- status Kanban
- responsável
- bloqueios
- specs obrigatórias
- branch sugerida
- issue criada / vinculada
- evidências
- Pronto para GitHub Projects: sim/não

If the fields are missing, stop before implementation and ask the orchestrator
to normalize the task.

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
Use esta task como contrato operacional. O SDD já foi feito. Leia a task inteira
e todas as specs obrigatórias antes de codar. Siga o checklist na ordem,
limite-se aos arquivos e módulos permitidos, pare se precisar sair do escopo ou
alterar arquitetura, execute TDD quando aplicável, registre validação manual com
evidência quando TDD completo não for viável, preencha o Resultado da execução e
devolva para review.

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

Record the reason in the task's `Bloqueios` section, keep the card in its current
Kanban column, add the `blocked` label when a project board exists, and update
visual status to `🔴 Bloqueada`.

## Interfaces with other skills

- Receives the task and approval from `dev-workflow-standard`.
- Consumes specs and templates from `sdd-spec-factory` (task, PR templates).
- Defers UI validation to `ui-ux-standard` and security validation to
  `security-standard`; it implements to satisfy their criteria but does not
  self-certify them.

## Definition of done

- Task scope implemented on the correct branch, nothing out of scope.
- TDD used when applicable; otherwise manual validation is evidenced.
- Required commands run; tests/validation pass or blockers are recorded.
- Task execution result fully filled with the mandatory final report.
- PR/review package prepared and linked to task, issue, branch and specs.
- Handed back for review; not merged, deployed, or self-approved.
