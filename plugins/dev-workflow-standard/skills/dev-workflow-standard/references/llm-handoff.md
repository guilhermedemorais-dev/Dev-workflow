# LLM Handoff And Continuity

Agent roles are stable; LLM providers are replaceable execution resources. A
task must continue from repository evidence when the current LLM loses quota,
tokens, authentication, connectivity, context or availability.

## Availability States

- `AVAILABLE`
- `LLM_TOKEN_EXHAUSTED`
- `LLM_CONTEXT_EXHAUSTED`
- `LLM_AUTH_UNAVAILABLE`
- `LLM_NETWORK_UNAVAILABLE`
- `LLM_TOOL_UNAVAILABLE`

Provider failure does not automatically block the task. The orchestrator agent
may select another authorized LLM capable of the same executor role.

## Mandatory Handoff

Before switching LLMs, persist:

```text
EXECUTION_HANDOFF
- previous_llm:
- availability_state:
- task_and_specs:
- branch_and_revision:
- completed_scope:
- changed_files:
- commands_and_results:
- active_failures:
- remaining_scope:
- mandatory_skills_and_references:
- skill_receipts:
- reuse_inventory:
- minimal_code_gate:
- next_safe_action:
```

The replacement executor agent must:

1. read the task, mandatory specs and `EXECUTION_HANDOFF`
2. inspect git status, diff and changed call sites
3. read all mandatory skills and emit its own `SKILL_RECEIPT`
4. verify the previous `REUSE_INVENTORY` against the current revision
5. continue from `next_safe_action`; do not restart the task
6. never create a parallel implementation to avoid understanding existing work
7. rerun affected validation before claiming completion

If repository state and handoff evidence disagree, stop and return `BLOCKED`
with the exact conflict. Conversation memory is never the source of truth.
