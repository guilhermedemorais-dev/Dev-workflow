# Workflow Pipeline

End-to-end delivery pipeline across the five skills. The LLM using
`dev-workflow-standard` is the orchestrator agent and is the only role that approves moving from one gate to
the next. It never writes product code.

## Skills and roles

| Skill | Role |
| --- | --- |
| `dev-workflow-standard` | Orchestrator agent / final reviewer |
| `sdd-spec-factory` | Requirements LLM / executable task |
| `dev-implementation-standard` | Executor agent / coder |
| `ui-ux-standard` | UI/UX specialist LLM |
| `security-standard` | Security specialist LLM |

## Pipeline

```text
Idea / demand
  -> dev-workflow-standard: diagnose (critical questions, risks)
  -> dev-workflow-standard: consolidate scope (in / out / constraints / decisions)
  -> sdd-spec-factory: generate specs (product/module/page/component/validation/API/DB)
  -> sdd-spec-factory: generate executable task (links specs, issue, branch, PR)
  -> HUMAN APPROVAL
  -> required skills read + SKILL_RECEIPT
  -> REUSE_INVENTORY + MINIMAL_CODE_GATE
  -> dev-implementation-standard: implement (only the task scope, on the branch)
  -> Pull Request (links task, issue, branch, specs followed)
  -> ui-ux-standard / security-standard / QA review (as applicable)
  -> dev-workflow-standard: approve or request rework
  -> merge / deploy (only after PR approved)
```

## Gates (must pass before advancing)

1. **Scope gate** — critical questions answered; scope consolidated. Owned by
   `dev-workflow-standard`.
2. **Spec gate** — required specs exist and follow the hierarchy
   (Product → Module → Page → Component), with Banco / API/Backend / Frontend/UI
   / Testes / Segurança / Observabilidade / Decisões / Riscos / Critérios de
   aceite separated. Owned by `sdd-spec-factory`, approved by the orchestrator.
3. **Task gate** — one small executable task links its mandatory specs, issue,
   suggested branch and expected PR. Human approval required before code.
4. **Implementation gate** — task implemented within scope; required commands run;
   tests pass; task result updated; skill receipt and reuse evidence exist. Owned
   by the executor agent using `dev-implementation-standard`.
5. **Review gate** — PR links task, issue, branch and specs; UI validated by
   `ui-ux-standard` when there is UI; security validated by `security-standard`
   when triggers apply; QA passed. Approved or sent to rework by the orchestrator.
6. **Release gate** — no deploy without an approved PR.

## Mandatory triggers

- `sdd-spec-factory`: always, before any implementation.
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
- Naming a skill never counts as applying it; every mandatory skill has a receipt.
- No new code unit is accepted without a reuse inventory and minimal-code gate.
- An unavailable LLM is replaced through `EXECUTION_HANDOFF`; the task is not restarted.
- No deploy is approved without an approved PR.

## Platforms

The same pipeline runs on Codex Desktop, Claude Code and Antigravity. Each skill
ships the platform adapters (`.codex-plugin/`, `.claude-plugin/`, root
`plugin.json`) and a single canonical `skills/<name>/SKILL.md`. See the README
for installation per platform.
