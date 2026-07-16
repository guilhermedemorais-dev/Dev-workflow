# Workflow Pipeline

End-to-end delivery pipeline across the workflow skills. `dev-workflow-standard` is
the CTO/orchestrator and is the only skill that approves moving from one gate to
the next. It never writes product code.

## Skills and roles

| Skill | Role |
| --- | --- |
| `dev-workflow-standard` | CTO / orchestrator / final reviewer |
| `sdd-spec-factory` | Requirements & specs / executable task |
| `minimal-implementation-gate` | Anti-overengineering planning, implementation and PR review |
| `dev-implementation-standard` | Executor / coder |
| `ui-ux-standard` | UI/UX validation |
| `security-standard` | Security validation |

## Pipeline

```text
Idea / demand
  -> dev-workflow-standard: diagnose (critical questions, risks)
  -> dev-workflow-standard: Ambiguity Gate (blocking vs researchable vs hypothesis)
  -> dev-workflow-standard: consolidate scope (in / out / constraints / decisions)
  -> minimal-implementation-gate: Minimal Planning Review
  -> sdd-spec-factory: generate specs with completeness, interaction, backend,
     security and traceability gates
  -> sdd-spec-factory: generate executable vertical-slice task
     (links specs, issue, branch, PR, Executor LLM, locked_paths)
  -> dev-workflow-standard: verify executor assignment and file ownership
  -> HUMAN APPROVAL
  -> minimal-implementation-gate: Minimal Implementation Gate
  -> dev-implementation-standard: implement (only the task scope, on the branch)
  -> Pull Request (links task, issue, branch, specs followed)
  -> minimal-implementation-gate: Minimal Code Review
  -> ui-ux-standard / security-standard / QA review (as applicable)
  -> dev-workflow-standard: approve or request rework
  -> merge / deploy (only after PR approved)
```

## Gates (must pass before advancing)

1. **Ambiguity gate** — missing information classified as `BLOCKING`,
   `RESEARCHABLE` or `NON_BLOCKING`; blocking product/security/data/UX/test
   decisions are answered before specs/tasks advance. Owned by
   `dev-workflow-standard`.
2. **Scope gate** — critical questions answered; scope consolidated. Owned by
   `dev-workflow-standard`.
3. **Minimal planning gate** — scope is reviewed for avoidable complexity,
   premature architecture, unnecessary dependencies, future scope and oversized
   tasks. Owned by `minimal-implementation-gate`, approved by the orchestrator.
4. **Spec gate** — required specs exist and follow the hierarchy
   (Product → Module → Page → Component), with Banco / API/Backend / Frontend/UI
   / Testes / Segurança / Observabilidade / Decisões / Riscos / Critérios de
   aceite separated. UI specs include interaction matrices; backend specs include
   entry point contracts; security-triggering specs include a Security Spec
   Contract; all specs include traceability to tests and acceptance where
   applicable. Owned by `sdd-spec-factory`, approved by the orchestrator.
5. **Task gate** — one small executable vertical-slice task links its mandatory
   specs, issue, suggested branch, expected PR, `Executor LLM`, handoff mode,
   claim status and `locked_paths`. It includes gate results,
   allowed/prohibited files, interaction/backend/security contracts, conflict
   notes and a traceability matrix. Human approval required before code.
6. **Minimal implementation gate** — the approved task is checked for existing
   repo reuse, native/platform solutions, unnecessary files/layers and avoidable
   dependencies before code starts.
7. **Implementation gate** — task implemented within scope; required commands run;
   tests pass; task result updated with evidence for every traceability,
   interaction, backend and security row; executor matches assignment and does
   not edit outside `locked_paths`. Owned by `dev-implementation-standard`.
8. **Minimal code review gate** — PR diff is reviewed for avoidable complexity
   before final specialist review.
9. **Review gate** — PR links task, issue, branch and specs; UI validated by
   `ui-ux-standard` when there is UI; security validated by `security-standard`
   when triggers apply; QA passed; traceability evidence reviewed. Approved or
   sent to rework by the orchestrator.
10. **Release gate** — no deploy without an approved PR.

## Mandatory triggers

- `sdd-spec-factory`: always, before any implementation.
- `minimal-implementation-gate`: always at planning review, implementation gate
  and code review stages.
- `ui-ux-standard`: whenever there is UI (screens, components, visual states,
  responsiveness, accessibility, design-system adherence).
- `security-standard`: whenever the change touches authentication, authorization,
  tokens, session, sensitive data, uploads, payments, or external integrations
  (also parsers, webhooks, infrastructure, privileged operations, tenant
  boundaries, secrets, browser storage, data export/import, AI/LLM tools,
  dependencies, CI/CD, logs or admin/support workflows).

## Invariants

- `dev-workflow-standard` never writes product code, never skips specs, never
  creates a task without sufficient specs, and never advances blocking ambiguity.
- `dev-implementation-standard` never implements without an approved task, and
  never changes anything out of scope, outside `locked_paths`, or assigned to
  another executor without a recorded reallocation.
- A feature task is vertical by default: behavior, UI/API/Banco where applicable,
  tests and evidence travel together.
- UI work without interaction matrix, backend work without entry point contract,
  or security-triggering work without Security Spec Contract is not Ready for Dev.
- Every task points to its mandatory specs.
- Every executable task declares `Executor LLM`, handoff mode, claim status,
  `locked_paths`, and known conflicts before Ready for Dev.
- Every PR points to task, issue, branch and the specs it followed.
- Minimal simplification never overrides security, accessibility, required tests,
  essential logs, business rules or approved source of truth.
- No deploy is approved without an approved PR.

## Main Plugin Setup

When installed in a new project, `dev-workflow-standard` acts as the principal
plugin and guides setup. It detects missing complementary plugins, explains their
role, asks human permission before installing or enabling them, checks the
project documentation structure, and asks permission before creating or
reorganizing workflow files. Specialist skills are loaded on demand to reduce
token cost.

## Platforms

The same pipeline runs on Codex Desktop, Claude Code and Antigravity. Each skill
ships the platform adapters (`.codex-plugin/`, `.claude-plugin/`, root
`plugin.json`) and a single canonical `skills/<name>/SKILL.md`. See the README
for installation per platform.
