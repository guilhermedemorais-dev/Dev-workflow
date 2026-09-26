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

Transform NORMAL work with unspecified behavior and COMPLEX work into, when
applicable:

- product spec (only when the request defines or changes the product itself)
- module spec
- page/feature spec
- component specs
- validation/business rules spec
- database spec (only when there is database impact)
- api/backend spec (only when there is a backend)
- frontend/ui spec (only when there is UI)
- one executable task
- one v2 machine-readable execution contract with normative equivalence to the
  complete GitHub Issue/card for each new executable task
- a PR checklist
- a QA/review checklist

This plugin **does not implement product code**. It produces the contract and the
order of execution. `dev-workflow-standard` orchestrates; implementation is
carried out by `dev-implementation-standard`, reviewed with `security-standard`,
functionally validated with `qa-testing-standard` when required, and visually
validated with `ui-ux-standard`.

## Vocabulary (non-negotiable)

- **Spec is not a PR.** A spec is the contract of what must be built.
- **Task is the order of execution.** It is small, reviewable and executable.
- **PR is the reviewable delivery.**
- **Issue is the complete human task/card.** A local Markdown may mirror it but
  does not replace it when GitHub Issues is available.
- **Review is approval or rejection.**
- **Deploy only happens after the PR is approved.**

A spec describes intent and acceptance. The Human Task tells people everything
needed to understand and govern the work. The v2 Execution Contract expresses
the same normative content as structured JSON for the LLM. This **normative
equivalence** is deliberate, while runtime status, evidence and discussion stay
in Issue comments and receipts.

## Mandatory hierarchy

For work routed to this skill, respect this top-down order. Do not create every
artifact mechanically: reuse an existing parent or record an explicit,
traceable parent intent when a new product/module/page document would add no
information.

```text
Product Spec
  -> Module Spec
    -> Page/Feature Spec
      -> Component Specs
        -> Human Task
          -> Execution Contract
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
- Planning depth is selected by `dev-workflow-standard`: TRIVIAL changes remain
  outside full SDD and use an inline intent contract; NORMAL changes use the
  smallest focused spec needed; COMPLEX changes use durable layered specs and
  traceability. This skill must not inflate a bounded change into a full
  document tree.

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

When planning/spec discovery requires an API, external integration or validation
endpoint, read [API Research Library](references/api-research-library.md).
Prioritize free APIs or a suitable free tier to validate application features
and test the application when relevant, with verified limits and synthetic data.
Use its two discovery sources only when relevant, verify candidates against
official documentation and record the decision plus validation plan/evidence.
An API listing is neither an approved dependency nor an available MCP. Do not
install or send real customer data during research; untested claims remain
NOT VALIDATED. Skip directory research when the task does not need it.

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

When the requested surface includes CI/CD, containers, IaC, servers, deployment,
cloud, GitOps, observability, backup/DR, incidents or advanced release strategy,
load [DevOps planning](references/devops-planning.md) and add
`devops-standard` to the required skills. Identify target_environment,
validation, rollback_strategy and human gates in the spec/task. Do not add
DevOps to unrelated application changes, UI-only work or routine Git commits.
Keep tool availability, logs and installation state out of the normative contract.

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

Load the active Harness `references/context-routing.md` before designing the
sector matrix. In this monorepo its source is
`plugins/dev-workflow-standard/skills/dev-workflow-standard/references/context-routing.md`;
installed hosts resolve the active skill, never assume sibling cache paths.
If unavailable, use an explicitly available canonical checkout or return the
missing reference to the Harness before producing a conflicting contract.

Produce one small, reviewable, complete GitHub Issue/card using
`templates/task-template.md` and one equivalent v2 JSON contract using
`templates/execution-contract-template.json`:

- Link the mandatory specs.
- Link the GitHub issue (or state that one must be created).
- Suggest the branch name (e.g. `feat/<modulo>-<resumo>`,
  `fix/<modulo>-<resumo>`).
- State the expected PR.
- Include acceptance criteria.
- Include mandatory tests (TDD when applicable).
- Include what is out of scope.
- Link the contract as `docs/execution/TASK-XXX.json`.
- Run Discovery/SDD collaboratively: ask the user critical questions, research
  authoritative references, consolidate decisions, then publish a
  `DISCOVERY_SDD_COMPLETED` Issue comment before requesting human approval.
- Keep validated sources in `docs/biblioteca-referencias/` and route the exact
  file/section and purpose. When UI applies, route the Design Guide, tokens,
  component library, visual references and approved mockup under `docs/design/`.
- Decompose execution into microtasks with owner skill/plugin, capability,
  preferred tool, dependencies, exact references, allowed paths, checklist,
  deliverables, completion condition and independent validator.
- Make `Prompt para o executor` a copy-ready ignition prompt that verifies task
  identity and contract revision, checks card/JSON equivalence, loads routed
  skills/references, stops on divergence, collects receipts, publishes material
  comments, and forbids merge/deploy without explicit authorization.
- Record planned validations in the Human Task with owner skill, capability,
  and preferred tool when known. Put only those compact identifiers in the
  Execution Contract `required_validations`; never store installation state,
  official URLs, executable paths, or logs there.
- Include all ten standard sectors with REQUIRED/N/A, concrete owner,
  dependencies and a short verified N/A reason. Detail only REQUIRED sectors;
  each has objective, sources with purpose, checklist, expected evidence and
  result placeholder. No generic full OWASP/QA checklist on unrelated tasks.
- Use v2 `sectors`, normative references and microtasks in new contracts. Human
  card and JSON share `contract_revision`; any normative change updates both.
  Mutable status, receipts, logs and execution evidence do not belong in JSON.
- Separate final `depends_on` from optional `planning_depends_on`. QA, Security
  and UI planning may start early; only executed validation closes their gates.
  Check unknown IDs, owners, missing required references and cycles before handoff.
- Give the Harness the complete Human Task; give each specialist only its
  sector, relevant global constraints/acceptance, necessary code and dependency
  receipts. Missing context requests expansion, not loading all sources by default.
- For behavioral changes, bugfixes, APIs, user flows, business rules, persistent
  state, payments, tenancy, imports/exports, integrations or concurrency, route
  independent QA planning to `qa-testing-standard`. It returns QA_GUARDRAILS,
  TEST_SCENARIOS, REGRESSION_TARGETS and VALIDATION_REQUIREMENTS proportionally.
  Docs/metadata-only work may record QA N/A; pure visual changes still require UI.

The Execution Contract must be valid JSON and include the v2 identity/revision,
human task link and equivalence declaration, summary/goal/discovery, current and
expected state, scope, protected and allowed paths, requirements, business
rules, references, design, microtasks, ten sectors, tests, acceptance criteria,
stop conditions, ignition prompt and reporting contract. Keep structure concise;
do not copy source bodies, conversation history, secrets or execution evidence.

Tasks live under `docs/tasks/TASK-XXX-<slug>.md` (or the repo's existing task
location, if one exists — reuse it, do not duplicate).

Execution Contracts live under `docs/execution/TASK-XXX.json` unless the
repository already has an equivalent canonical location.

For a legacy task without a contract, keep it readable. When it re-enters
execution, generate and validate its contract before implementation. Do not
mass-migrate historical tasks.

### Fase 4 - Checklist de PR/QA

Provide the delivery gates using `templates/pr-template.md`,
`templates/qa-review-template.md` and `templates/review-template.md`:

- Code review
- QA funcional (delegated to `qa-testing-standard` when behavioral triggers apply)
- QA visual (delegated to `ui-ux-standard`)
- Segurança (delegated to `security-standard`)
- Testes
- Evidências
- Aprovação / reprovação

## Integration with the other plugins

- `dev-workflow-standard` is the Engineering Harness. It owns discovery, scope,
  delegation, gates and approval. SDD Spec Factory feeds it the specs and the
  executable task; it does not replace it.
- `dev-implementation-standard` is the executor. It implements the approved task
  strictly within the scope these specs define; it consumes the task and PR
  templates produced here.
- `ui-ux-standard` owns design systems, mockups and visual QA. Page/component/UI
  specs should reference approved mockups and design tokens instead of inventing
  visuals.
- `qa-testing-standard` owns independent test strategy, functional validation,
  reproduction, regression and fix verification. It receives the QA Task slice
  and relevant sources; it neither writes product fixes nor attests UI/Security/
  DevOps PASS. Those owners return their own evidence.
- `security-standard` owns the security review and release gate. The security
  dimension of each spec and the security checklist of each PR are validated by
  it.

## Definition of done for this skill

- The needed specs exist and follow the hierarchy.
- Banco, API/Backend, Frontend/UI, Testes, Segurança, Observabilidade,
  Decisões pendentes, Riscos and Critérios de aceite are separated.
- There is one small executable task linking specs, issue, branch and PR.
- Every new executable task has a valid v2 Execution Contract with normative
  equivalence to the complete Issue/card and a copy-ready ignition prompt;
  legacy tasks have the compatibility fallback above.
- PR and QA/review checklists are provided.
- Sector matrix, microtasks, purpose-based routing, phase dependencies and
  explicit N/A reasons are consistent; legacy v1 contracts remain readable.
- No product code was implemented and no existing architecture was invented.
