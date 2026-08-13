---
name: sdd-spec-factory
description: "Use to turn a client request, feature, idea or problem into spec-driven development artifacts: product, module, page/feature, component, validation, database, API/backend and frontend/UI specs, plus an executable task linked to issue, branch and PR, with code review and QA checklists. Specialist companion to dev-workflow-standard."
---

# SDD Spec Factory

Specialist workflow for **Spec-Driven Development (SDD)**. It converts an idea,
client request, feature or problem into detailed specs and a small executable
task, then hands execution back to `dev-workflow-standard` and the review
specialists. Keep this file lightweight: create only the specs and the task the
current request actually needs, and load the templates on demand.

## Mission

Transform a request into, when applicable:

- product spec (only when the request defines or changes the product itself)
- module spec
- page/feature spec
- component specs
- validation/business rules spec
- database spec (only when there is database impact)
- api/backend spec (only when there is a backend)
- frontend/ui spec (only when there is UI)
- one executable task
- a PR checklist
- a QA/review checklist

This plugin **does not implement product code**. It produces the contract and the
order of execution. `dev-workflow-standard` orchestrates; implementation is
carried out by `dev-implementation-standard`, reviewed with `security-standard`,
visually validated with `ui-ux-standard`, and checked for avoidable complexity
with `minimal-implementation-gate`.

## Vocabulary (non-negotiable)

- **Spec is not a PR.** A spec is the contract of what must be built.
- **Task is the order of execution.** It is small, reviewable and executable.
- **PR is the reviewable delivery.**
- **Issue is the tracking record.**
- **Review is approval or rejection.**
- **Deploy only happens after the PR is approved.**

A spec describes intent and acceptance. A task points to specs and tells a
dev/AI exactly what to do. They are never merged into the same document.

## Mandatory hierarchy

Always respect this top-down order. Never create a lower artifact without a
parent that justifies it (or an explicit, marked assumption).

```text
Product Spec
  -> Module Spec
    -> Page/Feature Spec
      -> Component Specs
        -> Task
          -> Branch
            -> Pull Request
              -> Review / QA
                -> Merge / Deploy
```

## Mandatory separation of concerns

Every spec and every task must keep these dimensions visibly separated. Do not
collapse them into one prose blob; if a dimension does not apply, write
"N/A" with a one-line reason.

1. **Banco** (database / data model / migrations)
2. **API/Backend** (endpoints, contracts, services, jobs)
3. **Frontend/UI** (screens, components, states)
4. **Testes** (unit, integration, e2e, what must be covered)
5. **Segurança** (authz/authn, tenant boundaries, secrets, sensitive data)
6. **Observabilidade/logs** (events, metrics, audit trail)
7. **Decisões pendentes** (open decisions waiting for a human)
8. **Riscos** (what can break, regressions, unknowns)
9. **Critérios de aceite** (objective, testable acceptance)

## Operating principles

- The repo, PRD, existing architecture, approved mockups and `AGENTS.md` are the
  source of truth. Inspect the real repo before writing specs.
- **Do not invent existing architecture.** If you do not know whether a table,
  endpoint, service or component exists, do not assert it. Mark it as a
  hypothesis (`HIPÓTESE:`) or as a pending decision.
- Mark every assumption explicitly. Unverified facts are hypotheses, not specs.
- Keep tasks small enough to be reviewed in one PR. Split large work into
  multiple tasks, each with its own specs and acceptance criteria.
- Stop and ask when critical scope is missing. Do not guess core scope.
- A generated spec must be execution-grade. If it only describes "what the
  screen does" but not each interaction, backend effect, data rule, permission,
  negative path and test, it is not ready.
- A task must be a vertical behavior slice whenever product code is involved:
  UI/API/Banco/Testes/Evidência together, or an explicit `N/A` with a verified
  reason. Do not create horizontal tasks like "make frontend" or "make backend"
  unless the orchestrator approved an infrastructure/refactor exception.
- Final acceptance belongs to the user.

## Blocking Gates Before Specs And Tasks

Run these gates in order. A blocking failure sets the artifact/task to
`blocked`/`needs-info` and returns numbered questions to the orchestrator. Do
not generate downstream specs or executable tasks that depend on unanswered
critical decisions.

### Gate 1 - Ambiguity Gate

Classify every missing item as:

- `BLOCKING`: prevents correct product behavior, data integrity, authorization,
  security, main UX, or acceptance testing.
- `NON_BLOCKING`: can safely proceed as an explicit `HIPÓTESE:` without
  changing external behavior or security posture.
- `RESEARCHABLE`: should be resolved by reading repo/docs/tools instead of
  asking the user.

For `RESEARCHABLE`, inspect the source before asking. For `BLOCKING`, ask one
to three concrete questions, ordered by dependency. Do not answer human product
decisions yourself.

### Gate 2 - Spec Completeness Gate

Before marking a spec as approved or creating a task, verify that every
applicable behavior has:

- actor and permission
- trigger/interaction or backend entry point
- input/payload and validation rules
- state transition or data effect
- success result
- loading/processing state when user-facing
- error/empty/forbidden path
- observability/audit event when relevant
- security and privacy controls
- test/evidence requirement

If any required column is missing, the spec is incomplete. Record the gap in
`Decisoes pendentes` and block the task.

### Gate 3 - UI Interaction Contract Gate

Required for any UI change. Every clickable, editable or state-changing element
must be listed in an interaction matrix:

- buttons, menus, tabs, filters, inputs, forms, modals, uploads, cards, table
  actions, keyboard shortcuts, drag/drop, pagination, bulk actions, empty-state
  CTAs, retry actions and destructive confirmations
- for each interaction: who can see it, when it is enabled/disabled, what it
  calls, what data it sends, what changes on success, what errors look like,
  and how it is tested

If a mockup shows an element but the spec lacks its behavior, the spec is
blocked. If the spec describes behavior but the mockup lacks a place for it,
block for UI decision.

### Gate 4 - Backend Contract Gate

Required for API/backend, jobs, webhooks, queues, imports, exports, payments,
uploads or integrations. Each entry point must declare:

- route/topic/job name and owner
- authn/authz rule
- request schema and response schema
- idempotency, transaction and concurrency behavior when applicable
- validation and canonicalization
- database reads/writes
- status codes and error contract
- rate limits, retries and timeouts
- observability/audit logging
- negative tests and contract tests

No frontend task may call an unspecified backend contract.

### Gate 5 - Security Spec Contract Gate

Required when a change touches auth, authorization, tenants, admin/support,
sensitive data, uploads/downloads, payments, webhooks, external integrations,
parsers, generated files, browser storage, dependencies, infrastructure,
CI/CD, secrets, logs, data export/import, AI/LLM tools, or public endpoints.

For each affected surface, specify:

- protected asset and attacker-controlled input
- actor/role matrix and object ownership rule
- trust boundary and tenant/environment boundary
- abuse case with realistic impact
- required control: authn, authz, validation, encoding, CSRF, rate limit,
  idempotency, secret handling, encryption, audit log, retention, or rollback
- negative security test or review evidence
- release blocker if the control cannot be verified

Defense-in-depth notes may be `INFO`, but missing controls on reachable
security-sensitive effects are blockers.

### Gate 6 - Traceability Gate

Every task must include a traceability matrix linking:

```text
Requirement / RN / Mockup element
  -> UI interaction or backend entry point
  -> Banco/API/Frontend files or modules allowed
  -> Test/evidence
  -> Acceptance criterion
```

If an acceptance criterion cannot be traced to implementation and validation,
the task is not ready for development.

## Phases

### Fase 0 - Diagnóstico

Before writing any spec, produce a short diagnosis:

- **O que está claro** — what is unambiguous in the request.
- **O que falta** — missing information needed to spec safely.
- **Riscos iniciais** — early risks (technical, scope, security, data).
- **Perguntas críticas numeradas** — numbered, specific blocking questions.
- **Aguardar resposta humana** when critical scope is missing. Do not proceed to
  specs that depend on unanswered critical questions. Non-blocking gaps may
  continue as marked hypotheses.
- **Resultado do Ambiguity Gate** — `PASS` or `BLOCKED`, with each gap classified
  as `BLOCKING`, `NON_BLOCKING`, or `RESEARCHABLE`.

### Fase 1 - Consolidação

Consolidate the closed scope (becomes the basis of the product/module spec):

- Objetivo
- Escopo incluído
- Fora de escopo
- Restrições
- Usuários impactados
- Dependências
- Riscos
- Decisões pendentes

### Fase 2 - Geração de Specs

Before generating specs, consume the approved `Minimal Planning Review` from
`minimal-implementation-gate` when provided. Specs must incorporate its
simplifications or explicitly record why a recommendation was rejected.

Generate the specs the request needs, following the hierarchy:

- Create specs per module, page/screen, component and rule.
- Always separate **Banco**, **API/Backend** and **Frontend/UI** (plus the other
  mandatory dimensions).
- For UI, include the full interaction matrix before task creation.
- For backend, include entry point contracts before frontend work can depend on
  them.
- For security-triggering work, include the Security Spec Contract before the
  task can leave Discovery / SDD.
- Include traceability from requirements/mockups/rules to tests and acceptance
  criteria.
- Mark hypotheses explicitly (`HIPÓTESE:`).
- Do not invent existing architecture; reference real files/paths only when
  verified.
- Use the templates:
  - `templates/product-spec-template.md`
  - `templates/module-spec-template.md`
  - `templates/page-spec-template.md`
  - `templates/component-spec-template.md`
  - `templates/validation-rules-spec-template.md`
  - `templates/database-spec-template.md` (only with DB impact)
  - `templates/api-spec-template.md` (only with backend)

Suggested location for generated specs (create only what is needed):

```text
docs/specs/<modulo>/
  module-spec.md
  pages/<pagina>.md
  components/<componente>.md
  validation-rules.md
  database.md
  api.md
```

### Fase 3 - Geração de Task Executável

Produce one small, reviewable, executable task using `templates/task-template.md`:

- Link the mandatory specs.
- Include the results of Ambiguity, Completeness, Interaction, Backend,
  Security and Traceability gates.
- Register and link the GitHub issue (mandatory — every task must have a real
  GitHub issue; if it cannot be created, mark the task `blocked`/`needs-info` and
  escalate to the orchestrator instead of proceeding).
- Suggest the branch name (e.g. `feat/<modulo>-<resumo>`,
  `fix/<modulo>-<resumo>`).
- Define `Executor LLM primário`, executor/revisor, assignment rationale,
  handoff mode, claim status and `locked_paths` before Ready for Dev.
- Define a complete model-specific execution contract before Ready for Dev:
  authorized model/environment, mandatory prompt to run/paste, allowed actions,
  forbidden actions, required commands, stop conditions and evidence format.
  A task assigned to Codex, Claude Desktop, Claude Code or another agent without
  this contract remains `blocked`/`needs-info`.
- Record known file/module conflicts with other tasks. If multiple LLMs will
  work in parallel, split tasks so `locked_paths` do not overlap.
- State the expected PR.
- Include acceptance criteria.
- Include mandatory tests (TDD when applicable).
- Include what is out of scope.
- Include explicit instructions for the dev/AI executor.
- Include anti-collision instructions: the executor must stop if the task is
  assigned to another LLM, if `locked_paths` conflict, or if implementation
  requires files outside the allowed/locked paths.
- Include anti-freestyle instructions: the executor must stop if the current
  model/runtime does not match the authorized executor, if it did not receive the
  mandatory prompt, if it is in the wrong branch/worktree, or if it cannot read
  the task/specs from the canonical repo path.
- Include the Minimal Planning Review result and state that implementation must
  pass `Minimal Implementation Gate` before coding.

Tasks live under `docs/tasks/TASK-XXX-<slug>.md` (or the repo's existing task
location, if one exists — reuse it, do not duplicate).

### Fase 4 - Checklist de PR/QA

Provide the delivery gates using `templates/pr-template.md`,
`templates/qa-review-template.md` and `templates/review-template.md`:

- Code review
- QA funcional
- QA visual (delegated to `ui-ux-standard`)
- Segurança (delegated to `security-standard`)
- Testes
- Evidências
- Aprovação / reprovação

## Integration with the other plugins

- `dev-workflow-standard` is the CTO/orchestrator. It owns discovery, scope,
  delegation, gates and approval. SDD Spec Factory feeds it the specs and the
  executable task; it does not replace it.
- `minimal-implementation-gate` reviews consolidated scope before specs/tasks.
  Its approved simplifications constrain this skill unless the orchestrator
  records a human-approved exception.
- `dev-implementation-standard` is the executor. It implements the approved task
  strictly within the scope these specs define; it consumes the task and PR
  templates produced here.
- `ui-ux-standard` owns design systems, mockups and visual QA. Page/component/UI
  specs should reference approved mockups and design tokens instead of inventing
  visuals.
- `security-standard` owns the security review and release gate. The security
  dimension of each spec and the security checklist of each PR are validated by
  it.

## Definition of done for this skill

- The needed specs exist and follow the hierarchy.
- All blocking gates passed, or the artifact is explicitly blocked with
  `needs-info`.
- Banco, API/Backend, Frontend/UI, Testes, Segurança, Observabilidade,
  Decisões pendentes, Riscos and Critérios de aceite are separated.
- UI specs include interaction matrices when UI exists.
- Backend/API specs include entry point contracts when backend exists.
- Security-triggering specs include the Security Spec Contract.
- Tasks include traceability from requirements/mockups/rules to implementation,
  tests and acceptance criteria.
- Tasks include executor LLM assignment, handoff mode, claim status,
  `locked_paths` and conflict notes so Codex/Claude/Human executors do not work
  on the same files.
- There is one small executable task linking specs, issue, branch and PR.
- Minimal Planning Review recommendations are incorporated or explicitly
  justified.
- PR and QA/review checklists are provided.
- No product code was implemented and no existing architecture was invented.
