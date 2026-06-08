---
name: dev-workflow-standard
description: "Use for any software development task where Guilherme wants a repeatable project methodology across repositories: standard docs structure, repo-local instructions/skills, discovery, architecture, implementation plan, Claude Code delegation, QA, security review, testing, documentation, commit/PR readiness, and status reporting by Banco, API/Backend, and Frontend/UI."
---

# Dev Workflow Standard

Use this skill as Guilherme's default operating process for software projects.
It standardizes quality and speed by giving every repo the same development
routine, documentation architecture, and local instruction structure while still
letting each project define its own domain rules.

## Operating Model

Codex is the technical lead:

- Understand the objective, repo, docs, environment, and constraints.
- Plan architecture and checkpoints before implementation.
- Route specialized work to the smallest adequate set of installed skills or plugins.
- Delegate implementation-heavy work to Claude Code when useful.
- Use auxiliary AI CLIs only for bounded consultation, alternative analysis, or low-risk support work.
- Review the diff, run tests, check security/QA, and report gaps.

Claude Code is the implementation worker:

- Use it for larger code edits, refactors, repetitive implementation, and bugfix execution.
- Do not use it as the final reviewer.
- Do not let Codex and Claude edit the same files concurrently.

Auxiliary CLIs are optional consultants:

- `gemini`: use for broad ideation, UX/content alternatives, documentation drafts, and second opinions on non-sensitive architecture tradeoffs.
- `blackbox`: use for small snippets, quick examples, syntax help, and low-risk implementation ideas.
- `qwen`: use for code explanation, alternative implementation sketches, and lightweight review.
- `goose` or `hermes`: use only when the project already defines a reason to use them.

Codex remains accountable for decisions. Output from auxiliary CLIs must be
reviewed before implementation and must not override repo docs, tests, PRD, or
user instructions.

Auxiliary CLIs are not assumed to work. Before using any auxiliary CLI in a
task, run the availability check in section 4a. If the CLI fails help,
authentication, network, or a minimal prompt, do not use it for that task.

## Capability Routing

The main workflow is an orchestrator, not a universal specialist. For each
meaningful task, route specialized work using
`references/capability-routing.md` before loading broad instructions or solving
the specialist problem directly.

Use an index, manifest metadata, or the platform's discovery interface first.
Load only the selected skill or plugin instructions. Do not preload the full
plugin library into context.

The orchestrator retains only:

- objective and source-of-truth constraints
- selected capability and reason
- compact specialist result with evidence
- validation status, risks, and next decision

Specialist output is advisory until checked against project docs, current code,
official documentation when relevant, tests, and acceptance criteria. A plugin
reduces cognitive/context load; it does not make unsupported claims trustworthy.

## Continuous Improvement

Only when routing finds no adequate installed capability, or an active
capability repeatedly fails, use the controlled improvement loop in
`references/continuous-improvement.md`.

The loop may discover skills, plugins, MCP servers, hooks, or CLIs from trusted
marketplaces and repositories, but it must never install or enable third-party
code automatically. Inspect, score, propose, obtain human approval, test in an
isolated scope, measure results, and preserve a rollback path before promotion.

Keep one canonical `SKILL.md` when behavior is portable. Use platform-specific
manifests or adapters for Codex, Claude Code, and Antigravity instead of copying
and independently editing the workflow instructions.

## Mandatory Project Rules

- User PRDs, mockups, architecture notes, and repo docs are source of truth.
- If documentation conflicts with code, stop and ask for a decision.
- Inspect the current environment before creating servers, Docker stacks, caches, or rebuilds.
- Reuse the project's canonical runtime and scripts.
- Keep changes scoped. Do not refactor unrelated code.
- Do not reorganize docs, folders, routes, modules, schemas, or design systems without an explicit migration plan and user approval.
- Never call delivery complete without validation evidence.
- Final approval belongs to the user.

## Standard Project Structure

Prefer this structure for new projects. For existing projects, propose a migration
plan first and preserve existing canonical docs unless the user approves changes.

```text
/
  AGENTS.md
  README.md
  docs/
    DEVELOPMENT_STANDARDS.md
    DEVELOPMENT_WORKFLOW.md
    BUG_FIX_PROTOCOL.md
    COMPONENT_STANDARDS.md
    architecture/
      overview.md
      decisions/
        ADR-YYYY-MM-DD-title.md
    product/
      PRD-YYYY-MM-DD.md
    modules/
      <module-name>/
        PRD-YYYY-MM-DD.md
        research.md
        spec.md
        implementation-plan.md
        qa-report.md
    design/
      README.md
      # Detailed UI/UX structure is governed by the ui-ux-standard plugin.
    qa/
      reports/
    security/
      threat-model.md
      review-report.md
    operations/
      environment.md
      runbook.md
  .project-ai/
    README.md
    instructions/
      project-rules.md
      architecture-rules.md
      ui-rules.md
      qa-rules.md
    skills/
      <project-specific-skill>/
        SKILL.md
    prompts/
      implementation.md
      review.md
      bugfix.md
```

### Structure Rules

- `AGENTS.md`: short mandatory rules for all agents working in the repo.
- `docs/DEVELOPMENT_STANDARDS.md`: the single index for project development rules.
- `docs/DEVELOPMENT_WORKFLOW.md`: feature delivery protocol and checkpoints.
- `docs/BUG_FIX_PROTOCOL.md`: inherited bug and regression protocol.
- `docs/COMPONENT_STANDARDS.md`: component reuse rules. Detailed UI/UX standards are handled by `ui-ux-standard`.
- `docs/modules/<module>/`: source-of-truth PRDs, research, implementation specs, and QA per module.
- `docs/design/`: design system, mockups, assets, and visual QA managed by `ui-ux-standard`.
- `.project-ai/instructions/`: local AI instructions that should not be mixed with product docs.
- `.project-ai/skills/`: project-specific skills only; global skills stay in Codex/Claude config.
- `.project-ai/prompts/`: reusable prompts for this repo only.

For projects that use the improvement loop, create only when needed:

```text
docs/ai-workflow/
  capability-registry.md
  improvement-log.md
  evaluations/
    YYYY-MM-DD-capability-name.md
```

Do not create all files blindly. Create or update only what the current task needs,
unless the user explicitly asks to initialize the full structure.

## Methodology

### Feature Protocol

Every meaningful feature follows this order:

1. Source-of-truth PRD or issue exists.
2. Acceptance criteria are extracted into a checklist.
3. Architecture impact is checked.
4. Context Engineering Protocol is completed when implementation is non-trivial.
5. Technical research is completed for unfamiliar libraries, APIs, patterns, or integrations.
6. UI work invokes `ui-ux-standard` and has an approved mockup or design reference when visual fidelity matters.
7. Backend/API/data changes are implemented with tests.
8. Frontend/UI follows the approved design reference and covers loading, empty, error, permission, and responsive states.
9. Integration/e2e validation runs where practical.
10. QA and security gates are reported before merge/commit readiness.

Each step can be lightweight for small changes, but the order stays the same.

### Context Engineering Protocol

For non-trivial features, refactors, integrations, and bugfixes, separate work
into four phases. Do not let one long conversation become research, planning,
implementation, and review at once.

#### Phase 1: Research

Goal: gather only the context needed for correct implementation.

Research must inspect:

- relevant project docs and PRD
- relevant files and nearby implementation patterns
- existing components, services, APIs, schemas, and tests
- official/current docs for unfamiliar libraries or APIs
- public code examples only when local/official sources are insufficient

Write or update:

```text
docs/modules/<module>/research.md
```

Research output should include:

- objective
- source-of-truth docs
- relevant files only
- existing local patterns
- external docs/examples consulted
- decisions accepted/rejected
- risks and unknowns
- test implications

Do not include large dumps of file contents. Summarize and link paths.

#### Phase 2: Spec

Goal: turn research into an implementation contract.

Write or update:

```text
docs/modules/<module>/spec.md
```

Spec must include:

- files to create
- files to modify
- exact responsibility of each file
- expected API/schema/payload changes
- frontend/component changes
- tests to add/run
- migration/backfill needs
- acceptance criteria
- explicit out-of-scope items

Use path-based instructions. If a file is listed, say what changes there and why.

#### Phase 3: Code

Goal: implement from the spec with minimal extra context.

When delegating to Claude Code, provide:

- PRD or issue path
- `research.md`
- `spec.md`
- approved mockup/design path if UI exists
- constraints and acceptance criteria

Avoid feeding the whole research conversation into the implementation prompt.
Use the spec as the compressed context.

#### Phase 4: Review

Goal: validate the implementation independently.

Codex must review:

- diff vs spec
- tests and runtime checks
- regressions
- architecture drift
- security and data exposure
- docs/checklist updates

If implementation diverges from the spec, either fix it or update the spec with
a clear reason before continuing.

#### Context Reset Rule

When context becomes large or unfocused, stop and compress into `research.md` or
`spec.md`, then continue from the file. Prefer durable project docs over relying
on chat memory.

### Technical Research Protocol

Before coding with an unfamiliar library, framework, SDK, API, integration, or
external service:

1. Check project-local docs and existing implementation first.
2. Use Context7 or official docs for current API syntax, configuration, and migration details.
3. Use public code search such as `grep.app` only to find real-world patterns and examples.
4. Prefer official examples, maintained repos, and high-signal code over random snippets.
5. Record what was accepted, rejected, and why when the decision affects architecture or shared code.

Rules:

- Local code and project docs outrank public examples.
- Official docs outrank public examples.
- Public examples are references, not source of truth.
- Do not copy code blindly from public search results.
- Do not use public examples to justify insecure, stale, or dependency-heavy patterns.
- If external research affects the design, mention the source category in the implementation plan:
  `local pattern`, `official docs`, `Context7`, `public code search`, or `manual decision`.

### Bug Fix Protocol

For bugs and regressions:

1. Reproduce or document the symptom with evidence.
2. Identify root cause: where it fails and why.
3. Add or identify a failing test/check when practical.
4. Apply the smallest safe fix.
5. Validate against the original PRD/expected behavior.
6. Run regression checks for nearby flows.
7. Document the fix and remaining risk.

Do not patch symptoms repeatedly without root-cause analysis. If three fixes fail,
stop and question the architecture or assumptions.

### UI/UX Delegation Protocol

When a task involves screens, mockups, design system, components, visual assets,
landing pages, dashboards, responsiveness, accessibility, or visual QA:

1. Invoke `ui-ux-standard` before frontend implementation.
2. Let `ui-ux-standard` define the design docs, mockup workflow, media prompts, and visual QA criteria.
3. Do not implement frontend until the required mockup/design reference is approved when visual fidelity matters.
4. After implementation, Codex still owns final integration review and reports `Frontend/UI` status.

### Documentation Protocol

When project rules are missing or scattered:

1. List existing docs and rules.
2. Identify conflicts, gaps, and stale instructions.
3. Propose a consolidation plan.
4. Create or update docs only after the plan is accepted when changes are broad.
5. Keep `DEVELOPMENT_STANDARDS.md` as the index, not a giant duplicate of every file.

### API And Webhook Test Protocol

Before pointing a new outbound integration, webhook, callback, or third-party API
flow at production:

1. Prefer local mocks or test/staging endpoints when available.
2. For outbound webhook/callback payload inspection, use a disposable Webhook.site URL or equivalent request-capture tool.
3. Send only non-sensitive test payloads.
4. Verify method, headers, auth behavior, body shape, retry behavior, timeout behavior, and error handling.
5. Save sanitized evidence in `docs/qa/reports/` or the module QA report when relevant.
6. Switch to production only after the test endpoint behavior matches acceptance criteria.

Rules:

- Never send real secrets, customer data, tokens, PHI, PCI data, passwords, cookies, session IDs, or production payloads to Webhook.site.
- Never leave Webhook.site URLs in committed production config.
- Do not use Webhook.site as a production dependency.
- For inbound webhooks, validate signature verification locally/staging before production.
- For production readiness, prefer provider sandbox environments when the provider offers them.

## Default Workflow

### 1. Discover

Read the minimal context needed:

- `AGENTS.md`, `CLAUDE.md`, `.project-ai/`, README, PRD/docs, package/dependency files.
- Existing scripts, test commands, Docker/compose files, env examples.
- Current git status and changed files.

Output if planning is needed:

- Objective.
- Source-of-truth docs.
- Current environment.
- Risks and assumptions.

### 2. Classify

Classify the task:

- `bugfix`
- `feature`
- `refactor`
- `QA/review`
- `architecture`
- `DevOps`
- `security`
- `documentation`

Pick the smallest workflow that fits. Do not force full ceremony for a small fix.

### 3. Plan Checkpoints

For multi-step work, create checkpoints with acceptance criteria:

- Banco
- API/Backend
- Frontend/UI
- Documentation/project standards
- QA
- Security
- Docs/Runbook when relevant

If the user or docs require a gate, stop at that gate.

### 4. Delegate To Claude Code

Delegate only when implementation effort is meaningful. Prefer direct Codex edits for small patches.

Use this command shape:

```bash
claude -p "<brief>"
```

For safer implementation delegation, include:

- exact objective
- PRD/research/spec paths when available
- files/modules allowed
- acceptance criteria
- constraints from docs
- instruction to avoid unrelated refactors
- instruction to summarize changed files

Recommended prompt:

```text
You are implementing under Codex review.
Task: <objective>
Source of truth: <PRD/issue/docs>
Research: <docs/modules/<module>/research.md if available>
Spec: <docs/modules/<module>/spec.md if available>
Allowed scope: <files/modules>
Project rules: AGENTS.md, docs/DEVELOPMENT_STANDARDS.md, and .project-ai/instructions if present.
Constraints: preserve public APIs, schemas, payloads, and business rules unless explicitly requested.
Acceptance criteria:
- <criterion 1>
- <criterion 2>
Do not perform unrelated refactors.
After changes, summarize files changed and tests to run.
```

After Claude returns, Codex must inspect the diff before any claim of progress.

### 4a. Consult Auxiliary AI CLIs

Use auxiliary CLIs when they can save time without increasing risk:

- brainstorming implementation options
- summarizing documentation
- generating non-final examples
- checking for overlooked edge cases
- drafting tests/checklists
- creating first-pass copy or docs

Do not use auxiliary CLIs for:

- final architecture decisions
- secret handling
- production database changes
- security-sensitive code
- legal/financial/compliance conclusions
- direct unattended edits to the repo

Availability check is mandatory before first use in a task:

```bash
timeout 8s <cli> --help
timeout 20s <cli> -p "Reply with exactly: OK"
```

CLI-specific checks:

```bash
timeout 20s gemini -p "Reply with exactly: OK" --approval-mode plan
timeout 20s blackbox -p "Reply with exactly: OK" --approval-mode plan --skip-update
timeout 20s qwen "Reply with exactly: OK" --approval-mode plan
timeout 20s goose doctor
```

Status meanings:

- `AVAILABLE`: help works and the minimal prompt/doctor succeeds.
- `INSTALLED_ONLY`: binary/help works, but auth/network/provider/prompt check fails.
- `UNAVAILABLE`: binary missing, hangs, or errors before help.

Known local status from last verification:

- `gemini`: `INSTALLED_ONLY` - help works; minimal prompt timed out in this environment.
- `blackbox`: `INSTALLED_ONLY` - help works; minimal prompt returned API connection error.
- `qwen`: `INSTALLED_ONLY` - help works; minimal prompt timed out in this environment.
- `goose`: `INSTALLED_ONLY` - binary works; `goose doctor` reported no provider configured.

Only use a CLI marked `AVAILABLE` during the current task. If the user fixes
auth/provider/network setup, rerun the availability check and update the task
status before using it.

Command shapes:

```bash
gemini -p "<bounded question>"
blackbox -p "<bounded question>"
qwen -p "<bounded question>"
```

If a CLI does not support `-p`, check its help before use and prefer interactive
terminal use only when the user explicitly wants that CLI involved.

Recommended consultation prompt:

```text
You are a secondary consultant. Do not edit files.
Context: <short project/task context>
Question: <specific question>
Return: concise bullets with risks, alternatives, and tests.
Do not assume facts not provided.
```

After consultation, Codex must summarize what was accepted, rejected, and why.

### 5. Review Diff

Always check:

- behavioral regressions
- adherence to repo-local rules in `AGENTS.md`, `docs/`, and `.project-ai/`
- type/schema/API contract changes
- auth/permission impact
- validation and error handling
- migration/backfill needs
- UI state, responsiveness, empty/loading/error states when frontend exists
- test coverage and missing cases
- documentation updates required by the change

If the diff is risky, fix or ask before proceeding.

### 6. Validate

Run the project's canonical checks when available:

- unit tests
- integration tests
- typecheck/lint
- migrations or DB checks
- e2e/browser checks for UI
- security checks for auth, secrets, injection, exposed data
- webhook/API capture tests with sanitized payloads for outbound integrations

Do not invent a new runtime if the project already defines one.

### 7. Report

Always separate status:

- `Documentacao/Regras`
- `Banco`
- `API/Backend`
- `Frontend/UI`

Also include:

- changed files
- validation commands and results
- unvalidated gaps
- risks
- next action

Use clear labels:

- `PASS`
- `PARTIAL`
- `BLOCKED`
- `NOT VALIDATED`

## Quality Gates

Block completion if:

- project rules/source-of-truth docs were not checked for a non-trivial task
- broad doc/folder reorganization was performed without approval
- non-trivial work skipped research/spec or equivalent compressed context
- implementation diverged from spec without documented reason
- unfamiliar external API/library usage was implemented without local pattern or current-docs check
- production integration/webhook behavior was not tested with safe staging/capture flow when relevant
- tests fail and are relevant
- QA is not validated for changed user flows
- security impact is unknown for auth/data changes
- frontend was changed but runtime/UI was not checked
- docs/mockup acceptance criteria were skipped
- environment was not inspected before runtime changes

## Standard Prompts

### Initialize Project Standards

```text
Use Dev Workflow Standard to inspect this repo's existing docs and rules, then propose a safe project-standard structure using docs/ and .project-ai/. Do not reorganize files until I approve the migration plan.
```

### Start Work

```text
Use Dev Workflow Standard. Inspect the repo and source-of-truth docs, classify the task, propose checkpoints, and execute the first checkpoint only.
```

### Delegate Implementation

```text
Use Dev Workflow Standard. Codex should plan and review; delegate implementation to Claude Code via `claude -p` only for the code-writing checkpoint.
```

### Review Before Commit

```text
Use Dev Workflow Standard to review the current diff, run relevant checks, identify risks, and prepare commit/PR readiness notes.
```

## Final Response Template

```text
Diagnostico:
Documentacao/Regras:
Banco:
API/Backend:
Frontend/UI:
Validacao:
Riscos:
Proxima acao:
```
