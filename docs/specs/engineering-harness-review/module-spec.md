# Engineering Harness practice alignment

## Objective

Align the existing Engineering Harness with current, externally verifiable
agent-engineering practices without discarding the repository's governance or
presenting local conventions as industry standards.

## Scope

- Correct the execution lifecycle so a completed `EXECUTION_RECEIPT` records
  execution output before validation begins.
- Classify rules as consolidated practices, local architectural decisions, or
  local extensions.
- Scale planning and spec artifacts to change complexity while preserving an
  inspectable intent contract and validation evidence.
- Keep specialist skills independent and keep product-code execution outside
  the orchestrator agent.
- Add a short root `AGENTS.md` that maps agents to canonical repository sources.
- Mechanically test the critical lifecycle and classification invariants.

## Out of scope

- Renaming the repository, packages, or skills.
- Replacing the five-skill architecture.
- Installing dependencies or external capabilities.
- Changing UI, runtime product code, deployment, or security behavior.
- Treating local names such as `EXECUTION_RECEIPT` as OpenAI standards.

## Layers

- Banco: N/A, no data model exists in this documentation/plugin repository.
- API/Backend: N/A, no runtime API contract changes.
- Frontend/UI: N/A, no user interface changes.
- Tests: structural Python tests for docs, lifecycle ordering, links, and labels.
- Security: LOW risk; preserve secret-handling and approval rules.
- Observability: command exit codes and test results recorded in the task.

## Requirements

1. The repository must explain which practices have external support and which
   policies are local.
2. Invocation precedes execution; execution output precedes the completed
   receipt; validation follows the receipt; completion follows validation.
3. Trivial work may use an inline intent contract; normal work uses a concise
   issue/task contract; complex work uses durable specs and execution plans.
4. Every tier retains explicit scope, acceptance criteria, validation, and
   evidence proportional to risk.
5. `AGENTS.md` remains a short map and links to deeper canonical documentation.
6. Tests must assert semantic invariants, not obsolete presentation wording.

## Evidence basis

- OpenAI, "Harness engineering: leveraging Codex in an agent-first world",
  especially repository knowledge, progressive disclosure, lightweight versus
  complex plans, feedback loops, and mechanical enforcement.
- OpenAI Codex harness/App Server documentation for tool execution, persistent
  state, event output, approvals, and agent-loop boundaries.
- GitHub documentation confirming repository-level `AGENTS.md` support.
- Current repository documents, skills, references, manifests, and tests.

## Acceptance criteria

- Lifecycle order is consistent in README, workflow pipeline, skill, and
  execution reference.
- Local conventions are explicitly labeled and not attributed externally.
- Planning depth is adaptive without removing validation or specialist gates.
- Root `AGENTS.md` exists as a concise index.
- Baseline stale tests are corrected and the full suite passes.
- Audit matrix records findings, actions, evidence, and remaining risks.
