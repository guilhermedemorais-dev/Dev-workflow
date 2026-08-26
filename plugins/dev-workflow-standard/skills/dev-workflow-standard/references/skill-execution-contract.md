# Skill Execution Contract

Installing, listing or naming a skill does not apply its methodology. Every
orchestrator agent, executor agent or specialist LLM must prove activation.

## Mandatory Sequence

1. Detect applicable skills from the task, changed surfaces and repository rules.
2. Resolve the canonical path for every required `SKILL.md`.
3. Read each selected `SKILL.md` completely before acting.
4. Read every reference marked mandatory for the active phase.
5. Emit `SKILL_RECEIPT` before planning, coding, review or approval.
6. Stop when a required skill cannot be resolved or read. Do not imitate it from
   memory or silently replace it with general reasoning.

## SKILL_RECEIPT

```text
SKILL_RECEIPT
- skill: <name>
  path: <canonical SKILL.md path>
  references_loaded: <exact paths or N/A>
  applied_rules: <short concrete rules>
  status: LOADED | BLOCKED
```

The receipt is execution evidence, not a summary of the entire skill. A final
handoff without receipts for all mandatory skills is `NOT VALIDATED`.

## Role Vocabulary

Use only role-neutral terms in methodology and handoffs:

- `orchestrator agent`
- `executor agent`
- `specialist LLM`

Codex, Claude Code, Antigravity, a CLI or another product may transport or host
an agent. Product names never define responsibility and never substitute for a
skill receipt.
