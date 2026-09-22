# Engineering Harness audit

Audit date: 2026-09-22

Revision inspected: `33e4da76004d0bf10c837294ffc3718434c57b26`

Issue: [#12](https://github.com/guilhermedemorais-dev/Dev-workflow/issues/12)

## Audit summary

The architecture is directionally sound: repository-first context, real tool
execution, modular specialists, inspectable evidence, validation loops, and
recovery all match recurring agent-engineering practice. The main defects were
semantic and governance-related: the published pipeline placed a completed
receipt before execution, full SDD was treated as universal, local convention
names lacked provenance labels, and tests asserted obsolete wording instead of
behavioral invariants.

## Rule and component matrix

| Rule / component | Status | Internal evidence | External evidence | Action |
| --- | --- | --- | --- | --- |
| Repository as source of truth | CONSOLIDADO | README and central skill already prioritize repository artifacts | OpenAI describes repository knowledge as the system of record | Keep and link from `AGENTS.md` |
| Short `AGENTS.md` as map | PRECISA AJUSTE | No root file existed | OpenAI recommends a short table of contents; GitHub supports repository agent instructions | Add a concise root map |
| Progressive disclosure | CONSOLIDADO | Central skill routes to focused references | OpenAI explicitly recommends a small entry point with deeper sources | Keep; avoid copying specialist bodies |
| Real tools and inspectable results | CONSOLIDADO | Capability registry and harness execution reference | OpenAI describes agents using normal tools and feedback loops | Keep |
| Mechanical validation | PRECISA AJUSTE | Structural tests exist but four asserted stale presentation strings | OpenAI recommends linters, CI, and structural tests for invariants | Replace brittle assertions; add lifecycle/provenance tests |
| Adaptive planning depth | INCONSISTENTE | `Never skip specs` and `always before any implementation` applied one level of ceremony to all work | OpenAI distinguishes ephemeral lightweight plans for small changes from durable execution plans for complex work | Introduce TRIVIAL, NORMAL, COMPLEX tiers while retaining an intent contract |
| `EXECUTION_RECEIPT` | LOCAL JUSTIFICADO | Prevents assignment from being mistaken for execution | External basis is inspectable tool output and outcome validation, not this name/schema | Keep and label as a local extension |
| Receipt order | INCONSISTENTE | Central diagrams placed `RUNNING + EXECUTION_RECEIPT` before implementation | Agent loops emit tool results before outcome validation | Move completed receipt after execution result and before validation |
| `SKILL_RECEIPT` | LOCAL JUSTIFICADO | Proves required local methodology was loaded | No evidence that this exact name/schema is an ecosystem standard | Keep and label local |
| `REUSE_INVENTORY` and `MINIMAL_CODE_GATE` | LOCAL JUSTIFICADO | Prevent duplicate implementations and speculative abstractions | Reuse and minimal changes are established engineering principles; schemas are local | Keep and label local |
| Capability Registry | LOCAL JUSTIFICADO | Resolves need before selecting a product/provider | Capability routing is established; this table and fallback contract are project-specific | Keep and label local |
| Execution state machine | LOCAL JUSTIFICADO | Provides recovery and completion semantics | Durable state, tool results, approvals, and recovery are established; exact state names are local | Keep after semantic correction |
| Orchestrator does not write product code | LOCAL JUSTIFICADO | Separates coordination, execution, and independent review | OpenAI's experiment used agents for code, but does not establish this role split as a universal rule | Keep as an explicit local architectural decision |
| Specialist skills remain independent | LOCAL JUSTIFICADO | Prevents a monolithic central skill and preserves ownership | Progressive disclosure and specialized agents support the principle; exact five-skill topology is local | Keep |
| Six-column Kanban and mandatory human gates | LOCAL JUSTIFICADO | Existing governance and user control model | Common workflow ideas, but exact columns and gates are project policy | Keep and label local |
| Static MCP inventory in README | REDUNDANTE | Environment-specific list can drift and is not a package contract | Live capability discovery is safer than static environment claims | Treat as informative only; do not use as proof of availability |
| Full README as operating manual | PRECISA AJUSTE | README duplicates significant skill content | Progressive disclosure favors indexed canonical references | Keep overview/install material; move operational authority to skills/references |

## Consolidated versus local

### Consolidated practice

- repository-local, versioned source of truth
- short instruction entry point with progressive disclosure
- agents using real tools against real project state
- explicit feedback, validation, and recovery loops
- small reviewable changes and mechanical enforcement of invariants
- risk- and complexity-proportional planning artifacts

### Local architectural decision

- the orchestrator agent does not write product code
- Global Harness, CTO Harness, and Engineering Harness remain distinct levels
- five independent specialist skills with the central skill as control plane
- the six-column Kanban model and selected human approval gates
- issue/task/PR traceability for non-trivial work

### Local extension

- `EXECUTION_RECEIPT`
- `SKILL_RECEIPT`
- `REUSE_INVENTORY`
- `MINIMAL_CODE_GATE`
- `EXECUTION_HANDOFF`
- the exact capability registry and execution-state vocabulary

These names are owned by this repository. They adapt broader principles but are
not represented as OpenAI, Codex, GitHub, or market standards.

## Problems found

1. `plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md` and
   `docs/workflow-pipeline.md` placed the completed execution receipt before the
   implementation step.
2. The central and SDD skills imposed durable specs on trivial changes, despite
   the entry gate already distinguishing non-trivial work.
3. The repository did not explicitly classify local architecture and extension
   names.
4. No root `AGENTS.md` mapped agents to canonical sources.
5. Four baseline tests failed because they asserted superseded headings and
   role wording rather than current behavior.
6. README contains environment-specific MCP claims that can drift. They remain
   informational and require live verification before use.

## External sources

- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [OpenAI: Unlocking the Codex harness](https://openai.com/index/unlocking-the-codex-harness/)
- [GitHub: custom instruction support](https://docs.github.com/en/copilot/reference/custom-instructions-support)

## Remaining risks

- Documentation tests prove structure and cross-file consistency, not actual
  executor/runtime behavior.
- Provider APIs and supported instruction-file semantics can change; live
  documentation and runtime checks still take precedence.
- The README remains larger than an ideal quick-start. Further compression is a
  separate editorial task to avoid mixing architecture correction with a broad
  rewrite.
