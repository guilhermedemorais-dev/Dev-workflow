---
name: dev-workflow-standard
description: "Use for Guilherme's repeatable software delivery workflow: repo discovery, project rules, scoped planning, implementation coordination, Claude Code delegation, QA/security checks, documentation, commit/PR readiness, and status reporting by Banco, API/Backend, and Frontend/UI."
---

# Dev Workflow Standard

Primary workflow for Guilherme's software projects. Keep this file lightweight:
load only the references required for the current task.

## Non-Negotiables

- Repo docs, PRDs, mockups, architecture notes, and `AGENTS.md` are source of truth.
- If docs conflict with code, stop and ask for a decision.
- Inspect the real repo, git status, scripts, and runtime before changing environment.
- Reuse the canonical runtime; do not create duplicate Docker stacks or alternate flows.
- Keep changes scoped and preserve public APIs, schemas, payloads, and business rules unless explicitly approved.
- Do not call work complete without validation evidence.
- Final acceptance belongs to the user.

## Operating Model

Codex is the technical lead: discover, plan, coordinate, review diffs, validate,
and report. Claude Code can implement bounded non-trivial checkpoints under Codex
review. Auxiliary CLIs or plugins are consultants only when they solve a real
capability gap.

Use `ui-ux-standard` for UI/UX, mockups, visual QA, assets, accessibility, and
responsive checks. Use `security-standard` when changes touch auth, permissions,
tenant boundaries, secrets, payments, uploads, parsers, webhooks, infrastructure,
privileged operations, or sensitive data.

## Minimal Workflow

1. Discover: read only the relevant repo rules, docs, files, scripts, env hints,
   and current git status.
2. Classify: bugfix, feature, refactor, QA/review, architecture, DevOps,
   security, documentation, or UI/UX.
3. Plan only as much as the task needs. For multi-step work, define checkpoints
   and acceptance criteria by `Banco`, `API/Backend`, `Frontend/UI`, QA,
   security, and docs when relevant.
4. Implement or delegate the smallest safe scope.
5. Review the diff against the requested behavior and source-of-truth docs.
6. Run targeted tests/runtime checks where practical.
7. Report status, validation evidence, gaps, and next action.

## Context Budget Rules

- Do not paste whole files, docs trees, logs, or conversations into prompts.
- Prefer paths plus concise constraints.
- For large work, write or update `docs/modules/<module>/research.md` and
  `spec.md`, then continue from those files.
- Load references below only when directly needed.

## Delegation

For non-trivial implementation, prefer a bounded Claude Code checkpoint:

- allowed files/modules
- source-of-truth docs
- acceptance criteria
- constraints
- requested summary: changed files, tests to run, blockers, max 12 lines

Before delegating, read `references/claude-delegation.md`.

## Capability Gaps

This workflow remains the primary owner. Search/install/use other plugins only
for a specific missing capability, after scoring value and risk and getting human
approval for installation or activation. For that path, read
`references/continuous-improvement.md`.

## Reporting

Always separate relevant delivery status into:

- `Banco`
- `API/Backend`
- `Frontend/UI`

For unvalidated areas, say `NAO VALIDADO` and explain the missing evidence.
For commits, report local status and push status when the user appears to expect
remote sync.

## Reference Routing

- Claude Code delegation, visible terminal, fallback, and prompt contract:
  `references/claude-delegation.md`
- Plugin/skill discovery, scoring, approval, and rollback:
  `references/continuous-improvement.md`
