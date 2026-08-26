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

The LLM using this skill acts as the requirements LLM. Before producing specs,
it must read this `SKILL.md` completely and return a `SKILL_RECEIPT`. Naming the
skill in a prompt is not evidence of activation.

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
and visually validated with `ui-ux-standard`.

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
- Before specifying a new service, helper, component, route, abstraction or
  subsystem, search the source-of-truth repository for an existing equivalent.
  Prefer reuse or extension and record the decision in `REUSE_INVENTORY`.
- Reject speculative abstractions and duplicated responsibilities. New
  abstractions require two current concrete consumers or an explicit approved
  architectural requirement.
- Stop and ask when critical scope is missing. Do not guess core scope.
- Final acceptance belongs to the user.

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

Generate the specs the request needs, following the hierarchy:

- Create specs per module, page/screen, component and rule.
- Always separate **Banco**, **API/Backend** and **Frontend/UI** (plus the other
  mandatory dimensions).
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
- Link the GitHub issue (or state that one must be created).
- Suggest the branch name (e.g. `feat/<modulo>-<resumo>`,
  `fix/<modulo>-<resumo>`).
- State the expected PR.
- Include acceptance criteria.
- Include mandatory tests (TDD when applicable).
- Include what is out of scope.
- Include explicit instructions for the dev/AI executor.

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
- Banco, API/Backend, Frontend/UI, Testes, Segurança, Observabilidade,
  Decisões pendentes, Riscos and Critérios de aceite are separated.
- There is one small executable task linking specs, issue, branch and PR.
- PR and QA/review checklists are provided.
- No product code was implemented and no existing architecture was invented.
