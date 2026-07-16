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
- The task declares `Executor LLM primário`, handoff mode, claim status and
  `locked_paths`.
- The current executor matches `Executor LLM primário`, or the task contains an
  explicit reallocation approved by the orchestrator/user.
- The task includes completed or explicitly `N/A` gate results for Ambiguity,
  Spec Completeness, UI Interaction Contract, Backend Contract, Security Spec
  Contract and Traceability.
- UI work includes an interaction matrix; backend work includes entry point
  contracts; security-triggering work includes the Security Spec Contract.
- `minimal-implementation-gate` returned `LIBERAR IMPLEMENTACAO`, or the
  orchestrator recorded a human-approved exception.
- The suggested **branch** is defined (or derive it from the task convention).
- The task has GitHub-ready fields: status, responsável, bloqueios, specs
  obrigatórias, branch sugerida, evidências, and issue criada/vinculada.

If any precondition is missing, stop and return to `dev-workflow-standard` /
`sdd-spec-factory` instead of guessing.

## Hard Limits (non-negotiable)

- Implement **only the task scope**. Do not advance to another task.
- Do not implement a task assigned to another LLM/person. If `Executor LLM
  primário` is `Claude Desktop`, `Claude Code`, `Codex`, `Humano`, or another
  executor that is not the current executor, stop unless the task was explicitly
  reallocated.
- Do not edit paths claimed by another executor or outside the task's
  `locked_paths`/allowed modules.
- Do not implement from superficial tasks. If the task describes a screen,
  endpoint or rule without the corresponding interaction/backend/security/test
  contract, stop and return it to SDD as `blocked`/`needs-info`.
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
   acceptance criteria, gate results, interaction/backend/security contracts,
   traceability matrix, out-of-scope items, required tests, and blockers.
2. **Confirm assignment and claim**: verify that `Executor LLM primário` matches
   the current executor, `locked_paths` are present and non-conflicting, then set
   claim/status to the current executor. If the task is assigned to another LLM,
   stop and return it for manual handoff or reallocation.
3. **Set status** to `🟡 Em andamento` in the task content when starting.
4. **Execute the prompt-base** from `Prompt para o executor` as the operational
   contract.
5. **Minimal gate**: follow the approved `Minimal Implementation Gate`
   recommendation. Prefer existing repo code, native framework/runtime features,
   standard library and already-installed dependencies before creating files.
6. **Implementação**: implement only the approved scope, by layer when relevant:
   Banco, API/Backend, Frontend/UI. Do not invent files, endpoints, tables,
   payloads, or architecture.
   - For UI: implement every row of the interaction matrix, including disabled,
     loading, empty, success, error and forbidden states.
   - For backend: implement only the specified entry point contracts, including
     validation, status codes, idempotency/transaction behavior and errors.
   - For security: implement the stated invariant and negative path. Do not
     weaken auth, authorization, tenant isolation, secret handling, audit logs,
     input validation or privacy controls for simplicity.
7. **TDD/Testes**: use TDD when applicable. If full TDD is not viable, record why
   and perform manual validation with objective evidence.
8. **Validação**: run the task-required commands, build, lint, tests,
   migrations, UI checks, or manual checks defined by the repo/task. Capture
   evidence.
9. **Atualização do relatório**: fill the mandatory final report in
   `templates/execution-report-template.md`, including prompt used, checklist
   executed, evidence, layer results, risks, gaps, blockers, and GitHub-ready
   fields.
10. **Set final status**: `🔴 Bloqueada` if blocked, or `🟢 Concluída` only when
   implementation and validation evidence support completion.
11. **Handoff para review**: prepare the PR or review package linked to task,
   issue, branch and specs, then return to `dev-workflow-standard`. Do not
   self-approve, merge, or deploy.

## GitHub Projects Readiness

Do not assume GitHub Projects is available. Keep the task ready for future
mapping by preserving these fields in the task content:

- status visual
- status Kanban
- responsável
- Executor LLM primário
- Executor secundário/revisor
- modo de handoff
- status da claim
- `locked_paths`
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
- Executor LLM primário:
- Executor secundário/revisor:
- Motivo da atribuição:
- Modo de handoff:
- Status da claim:
- Claim por:
- Claim em:
- `locked_paths`:
- Conflitos conhecidos:
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
- the task is assigned to another executor, has no assignment, or has
  conflicting/missing `locked_paths`;
- any mandatory gate result is missing, `BLOCKED`, or unjustified `N/A`;
- UI/backend/security work lacks the required contract matrix;
- traceability does not map requirements to acceptance criteria and tests;
- Minimal Implementation Gate is missing, rejected, or contradicts the task;
- the specs are ambiguous or contradict the code;
- the task cannot be completed without an architecture change;
- leaving the approved scope is required;
- editing outside `locked_paths` is required;
- a blocker is outside the task scope.

Record the reason in the task's `Bloqueios` section, keep the card in its current
Kanban column, add the `blocked` label when a project board exists, and update
visual status to `🔴 Bloqueada`.

## Interfaces with other skills

- Receives the task and approval from `dev-workflow-standard`.
- Consumes the `Minimal Implementation Gate` recommendation from
  `minimal-implementation-gate`.
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
