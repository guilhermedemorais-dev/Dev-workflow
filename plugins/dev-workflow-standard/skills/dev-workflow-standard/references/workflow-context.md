# Workflow Context

Read only when selected by the owning SKILL.md route. Backtick paths beginning
with `references/` are relative to that skill directory, not this file.

## Context Budget Rules

### Project-local capability evolution

At task discovery/resumption, inspect the project's existing
`docs/ai-workflow/capability-registry.md` if present. Resolve only ACTIVE entries
relevant to the routed capability, with their approved scope, source revision
and current validation evidence. Read the selected SKILL.md completely and its
required references, recording the actual path/revision in SKILL_RECEIPT.
An index entry or file on disk is not proof of host discovery or execution.
Missing/stale/conflicting entries require review, never silent global fallback
or permission expansion. Do not load the entire local library.

When a verified gap triggers improvement, read
[Controlled continuous improvement](continuous-improvement.md).
Reuse, adapt, then create only if needed. Domain-specific lessons belong in
the client project, not the installed plugin cache. Specs, source references,
scripts and reusable skills have different owners; not every challenge needs
a skill. Keep global governance and acceptance gates intact. This is an
agent-executed protocol, not an autonomous self-modifying runtime.

- Do not paste whole files, docs trees, logs, or conversations into prompts.
- Prefer `task_id` plus `execution_contract_path` over task/spec bodies.
- Load the contract first, validate required fields and paths, then open only
  the active skill, routed JSON list, relevant global acceptance/constraints,
  required_sources, activated conditional_sources, code and dependency receipts.
- A mandatory reference must be read before changing the area it governs;
  progressive disclosure reduces redundant context, not necessary context.
- Use the Human Task for mutable status, blockers, results, and evidence without
  injecting it wholesale into the executor prompt.
- The Harness reads the full Task; specialists request justified context
  expansion if their slice is insufficient, not all docs preemptively.
- For large work, keep specs and research in files (`docs/specs/...`,
  `docs/modules/<module>/research.md`) and continue from those files.
- Load the references below only when directly needed.

## Reference Routing

- Consultative technical decisions in NORMAL/COMPLEX SDD: resolve the active
  SDD bundle's `references/technical-knowledge-router.md`; this checkout's
  canonical source is
  `plugins/sdd-spec-factory/skills/sdd-spec-factory/references/technical-knowledge-router.md`.
  Select only triggered topics. Require project source/version/purpose in existing
  Task/JSON reference fields and reconcile the PR Engineering Explanation with
  current owner receipts. Preserve specialist ownership and human gates;
  do not load the whole library or treat proposed tests as validation PASS.
  Missing/stale knowledge triggers the router's bounded official research and
  durable reference update; reuse compatible learned evidence and route generic
  plugin-source improvements through existing continuous-improvement review.
- Sector matrix, source purposes, phase dependencies and compatibility:
  `references/context-routing.md`
- Harness execution state, invocation evidence, retry/replan and completion:
  `references/harness-execution.md`
- Capability selection, preferred executors and fallbacks:
  `references/capability-registry.md`
- Executor LLM delegation, visible terminal, fallback, and prompt contract:
  `references/claude-delegation.md`
- Plugin/skill discovery, scoring, approval, and rollback:
  `references/continuous-improvement.md`
- Mandatory skill loading and execution evidence:
  `references/skill-execution-contract.md`
- Reuse and anti-overengineering review:
  `references/minimal-code-gate.md`
- Provider-neutral LLM replacement and checkpoint continuity:
  `references/llm-handoff.md`
- Human checkpoint reporting, anti-spam, publication evidence, and fallback:
  `references/execution-report-comments.md`
- Specialist-owned tool registries, local state, and fast/slow path:
  `references/skill-owned-tools.md`
- Portable environment bootstrap and MCP Library:
  `plugins/dev-environment-standard/skills/dev-environment-standard/SKILL.md`
- End-to-end pipeline across the specialist skills: `docs/workflow-pipeline.md`
