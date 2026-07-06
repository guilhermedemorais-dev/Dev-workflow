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
  -> dev-workflow-standard: consolidate scope (in / out / constraints / decisions)
  -> minimal-implementation-gate: Minimal Planning Review
  -> sdd-spec-factory: generate specs (product/module/page/component/validation/API/DB)
  -> sdd-spec-factory: generate executable task (links specs, issue, branch, PR)
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

1. **Scope gate** — critical questions answered; scope consolidated. Owned by
   `dev-workflow-standard`.
2. **Minimal planning gate** — scope is reviewed for avoidable complexity,
   premature architecture, unnecessary dependencies, future scope and oversized
   tasks. Owned by `minimal-implementation-gate`, approved by the orchestrator.
3. **Spec gate** — required specs exist and follow the hierarchy
   (Product → Module → Page → Component), with Banco / API/Backend / Frontend/UI
   / Testes / Segurança / Observabilidade / Decisões / Riscos / Critérios de
   aceite separated. Owned by `sdd-spec-factory`, approved by the orchestrator.
4. **Task gate** — one small executable task links its mandatory specs, issue,
   suggested branch and expected PR. Human approval required before code.
5. **Minimal implementation gate** — the approved task is checked for existing
   repo reuse, native/platform solutions, unnecessary files/layers and avoidable
   dependencies before code starts.
6. **Implementation gate** — task implemented within scope; required commands run;
   tests pass; task result updated. Owned by `dev-implementation-standard`.
7. **Minimal code review gate** — PR diff is reviewed for avoidable complexity
   before final specialist review.
8. **Review gate** — PR links task, issue, branch and specs; UI validated by
   `ui-ux-standard` when there is UI; security validated by `security-standard`
   when triggers apply; QA passed. Approved or sent to rework by the orchestrator.
9. **Release gate** — no deploy without an approved PR.

## Mandatory triggers

- `sdd-spec-factory`: always, before any implementation.
- `minimal-implementation-gate`: always at planning review, implementation gate
  and code review stages.
- `ui-ux-standard`: whenever there is UI (screens, components, visual states,
  responsiveness, accessibility, design-system adherence).
- `security-standard`: whenever the change touches authentication, authorization,
  tokens, session, sensitive data, uploads, payments, or external integrations
  (also parsers, webhooks, infrastructure, privileged operations, tenant
  boundaries, secrets).

## Invariants

- `dev-workflow-standard` never writes product code, never skips specs, never
  creates a task without sufficient specs.
- `dev-implementation-standard` never implements without an approved task, and
  never changes anything out of scope without a recorded justification.
- Every task points to its mandatory specs.
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
