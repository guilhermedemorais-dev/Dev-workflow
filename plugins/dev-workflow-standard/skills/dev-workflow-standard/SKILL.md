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
- Administer and develop the software end to end using this workflow as the primary capability.
- Use its own instructions, available tools, project code, and documented process by default.
- Delegate non-trivial code-writing checkpoints to Claude Code so Codex remains focused on planning, review, QA, and delivery governance.
- Use auxiliary AI CLIs only for bounded consultation, alternative analysis, or low-risk support work.
- Review the diff, run tests, check security/QA, and report gaps.

Claude Code is the implementation worker:

- Use it by default for features, refactors, integrations, repetitive implementation, and non-trivial bugfix execution.
- Split work into bounded checkpoints; never send the whole project or conversation in one prompt.
- Do not use it as the final reviewer.
- Do not let Codex and Claude edit the same files concurrently.
- Follow `references/claude-delegation.md` before every delegated implementation checkpoint.

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

## Available MCP Environment

Guilherme's current Codex environment has these MCP servers enabled:

- `chrome-devtools`: inspect rendered pages, console output, network activity, and browser performance.
- `context7`: consult current library and SDK documentation and examples.
- `figma`: read approved Figma design context when the task provides or depends on a Figma source.
- `firecrawl-mcp`: discover and extract targeted public web content when higher-priority sources are insufficient.
- `grep-mcp`: search public GitHub code through `grep.app` for real-world implementation patterns.
- `hf-mcp-server`: access relevant Hugging Face models, datasets, Spaces, or documentation when the task requires them.
- `node_repl`: support bounded JavaScript execution and tool orchestration when exposed by the active Codex runtime.
- `playwright`: validate rendered web pages, interactions, states, responsiveness, and end-to-end flows.

Treat this as an environment capability inventory, not a requirement for other
installations. At task start, select only the MCPs that materially help the
current work. When availability matters, verify the live state with
`codex mcp list`; an enabled configuration does not prove authentication,
network access, or successful startup.

MCP rules:

- Do not invoke every enabled server by default.
- Project files, PRDs, approved mockups, architecture, and official docs remain source of truth.
- Do not send secrets, private code, customer data, cookies, or production credentials to remote MCP services.
- If an MCP fails or is rate-limited, use the documented fallback and report any resulting validation gap.
- Never copy local MCP credentials or `~/.codex/config.toml` into a repository.

## Capability Gap And Continuous Improvement

This plugin remains the primary workflow and must execute the normal software
development process itself. Do not delegate ordinary responsibilities merely
because another plugin exists.

Only when the current task requires a capability that this workflow and its
available tools genuinely do not provide:

1. Define the missing capability precisely.
2. Search installed plugins and skills by metadata without loading the entire catalog.
3. If necessary, search trusted official/community marketplaces for an existing capability.
4. Audit compatibility, permissions, maintenance, security, and expected value.
5. Request human approval before installation or activation.
6. Use the approved capability only for the bounded missing task.
7. Validate its output before integrating it into the main development workflow.
8. If no adequate capability exists and the need is recurring, propose creating a focused skill or plugin.

Use the controlled process in `references/continuous-improvement.md` for this
exception path. Do not turn capability discovery into a mandatory step for every
feature, bugfix, review, or project task.

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
3. Use `grep-mcp`/`grep.app` only to find real-world patterns and examples in public code.
4. Prefer official examples, maintained repos, and high-signal code over random snippets.
5. Record what was accepted, rejected, and why when the decision affects architecture or shared code.

Use Firecrawl only when web content must be discovered or extracted and the
local project, official documentation, and Context7 do not provide enough
usable context. Suitable cases include documentation sites with fragmented
navigation, release-note discovery, multi-page vendor research, and extracting
structured content from public pages.

Firecrawl rules:

- Treat Firecrawl as a collection tool, not a source of truth.
- Prefer targeted page fetches before broad crawling.
- Restrict crawl scope, page count, and depth to the minimum needed.
- Respect site access rules, licenses, rate limits, and terms of service.
- Never submit credentials, private URLs, customer data, cookies, or production secrets.
- Verify technical claims against official/current sources before implementation.
- If Firecrawl is unavailable, continue with official docs, Context7, direct browser access, or manual research instead of blocking ordinary development.

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

### Security Delegation Protocol

When a task changes authentication, authorization, tenant boundaries, secrets,
payments, uploads, parsers, webhooks, infrastructure, privileged operations, or
sensitive data, invoke `security-standard` for risk-adaptive review.

Use change review for ordinary diffs, scoped audit for a defined subsystem, and
repository audit only when broad assurance is explicitly needed. Security tool
output remains advisory until validated against code, tests, and runtime.

An installed proprietary security plugin may provide an independent second
opinion, but it must not replace the canonical project rules or the original
`security-standard` workflow.

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

Delegation is mandatory for non-trivial implementation. Codex should preserve
its context and token budget for discovery, architecture, checkpoint planning,
diff review, QA, security, and final reporting. Direct Codex edits are reserved
for genuinely small localized patches.

Follow `references/claude-delegation.md`. Before implementation:

1. Classify whether the mandatory delegation trigger applies.
2. Verify `claude --version` and `claude auth status` once for the task.
3. Set and report `CLAUDE_STATUS`.
4. Split implementation by layer/module into bounded checkpoints.
5. Open the real Claude Code CLI in a visible terminal for one checkpoint at a time.
6. Wait for Claude to exit, then review its diff before continuing.

If a delegated call fails with DNS, connection, network, API transport, or
timeout symptoms inside a restricted workspace, follow the Restricted Workspace
Recovery in `references/claude-delegation.md`: retry the same bounded command
through the approved external-network/escalated execution path. Do not classify
this as invalid Claude authentication and do not silently implement the work in
Codex.

If mandatory delegation applies and Claude is unavailable, stop before code
writing and report the blocker. Do not silently consume the implementation
budget in Codex.

Guilherme's default is visible interactive delegation. Use the bundled
`scripts/claude-visible-delegate.sh` helper through the approved GUI/external
execution path. It opens `gnome-terminal`, submits the checkpoint to the real
Claude Code CLI, and writes a status file after the user ends Claude with
`/exit`. Codex must not edit the delegated scope while that terminal is active.

Use headless mode only when a graphical terminal is unavailable and the user
approves the fallback:

```bash
claude -p "<bounded implementation brief>" \
  --permission-mode acceptEdits \
  --tools "Read,Edit,Write,Glob,Grep" \
  --output-format text
```

For safer implementation delegation, include:

- exact objective
- PRD/research/spec paths when available
- files/modules allowed
- acceptance criteria
- constraints from docs
- instruction to avoid unrelated refactors
- instruction to summarize changed files

Pass paths and concise constraints instead of pasting the full conversation,
repository, logs, or documentation tree. Prefer at most one coherent module,
five directly changed files, and one to three acceptance criteria per call.

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
After changes, return only files changed, tests to run, and blockers in at most 12 lines.
```

Before running the command, tell the user which checkpoint and scope are being
delegated. After Claude returns, Codex must inspect the scoped diff and run the
relevant validation before any claim of progress or next delegation.

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

Use Playwright for browser validation when the changed behavior depends on a
real rendered page or user flow. Prefer the project's existing Playwright
configuration and tests. Appropriate checks include navigation, forms,
authentication and permissions, loading/empty/error states, responsive
breakpoints, screenshots, and critical end-to-end flows.

Playwright rules:

- Reuse the canonical running environment; do not start a duplicate stack.
- Use test accounts and sanitized fixtures, never production credentials or data.
- Add or update automated tests when the flow is stable and regression-prone.
- Use focused interactive checks for exploratory QA, then record reproducible evidence.
- A screenshot alone does not validate behavior, accessibility, or business rules.
- If Playwright is unavailable, use another approved browser tool or report the UI/runtime check as `NOT VALIDATED`.

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
