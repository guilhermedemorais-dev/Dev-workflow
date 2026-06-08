# Capability Routing

Use this protocol to keep the main Codex, Claude Code, or Antigravity workflow
small and disciplined while specialist plugins and skills perform bounded work.

## Principle

The orchestrator owns intent, constraints, decomposition, evidence review, and
final integration. Specialists own narrow tasks. Do not make every agent read
every rule or solve every domain problem.

## Routing Workflow

### 1. Classify The Task

Write a one-sentence intent and classify the work, for example:

- architecture
- backend/API
- database
- frontend/UI
- testing/QA
- security
- debugging
- documentation
- DevOps/deployment
- research
- media/design

### 2. Query A Lightweight Index

Use skill/plugin names, descriptions, manifests, tags, or a generated local
index. Do not open every `SKILL.md` to decide.

When `skill-router-orchestrator` is installed, prefer:

```bash
python3 ~/.codex/skills/skill-router-orchestrator/scripts/route.py "<task>"
```

Equivalent marketplace or platform discovery may be used in Claude Code and
Antigravity. Discovery should return metadata, not full plugin bodies.

### 3. Select The Minimum Set

Choose:

- one primary capability
- zero or one support capability by default
- no capability when confidence is low or the task is trivial

Do not activate multiple overlapping specialists for the same responsibility.
Use sequential handoffs when a task crosses domains.

### 4. Build A Bounded Task Packet

Send only:

- objective
- relevant source-of-truth paths
- exact files or module in scope
- constraints and prohibited changes
- required output format
- acceptance criteria
- evidence required

Do not send the entire conversation, repository, plugin catalog, or unrelated
documentation.

### 5. Require Structured Specialist Output

The specialist should return:

```text
Capability:
Task:
Findings or changes:
Evidence:
Files affected:
Validation performed:
Assumptions:
Uncertainty:
Risks:
Recommended next action:
```

For implementation work, require a diff and test results. For research, require
source links or local paths. For UI, require runtime/visual evidence. For
security, require reproducible evidence and defensive remediation.

### 6. Verify Before Integration

The orchestrator must verify critical claims against at least one authoritative
surface:

- project source of truth and current code
- official/current documentation
- deterministic command or test
- runtime observation or screenshot
- schema/API/database inspection

Reject output that lacks evidence, exceeds scope, contradicts project rules, or
expresses guesses as facts.

### 7. Compress And Release Context

After validation, preserve only the accepted conclusion, evidence, changed
paths, unresolved risks, and next action. Do not retain full specialist prompts
or verbose reasoning in the active context.

Write durable information to `research.md`, `spec.md`, an ADR, QA report, or
capability evaluation when it will be needed later.

## Anti-Hallucination Rules

- No claim of completion without evidence.
- No version/API behavior claim without current docs or local verification.
- No architecture or UI invention beyond the source of truth.
- No specialist may approve its own high-risk implementation as final.
- Separate facts, inferences, assumptions, and unknowns.
- If two specialists disagree, compare evidence; do not choose by confidence of tone.
- Stop and ask the user when documentation and code conflict.

## Load-Shedding Rules

- Prefer deterministic scripts and tools over model reasoning for parsing,
  formatting, validation, search, and repetitive transformations.
- Load references progressively and only for the active task.
- Run independent specialist tasks sequentially unless parallel execution is
  clearly safe and they do not edit the same files.
- Avoid keeping multiple large agents active in the same IDE session.
- Summarize completed checkpoints into files before starting the next one.

## Routing Record

For non-trivial work, record briefly:

```text
Primary: <capability>
Support: <capability or none>
Reason: <why this is the minimum adequate set>
Confidence: high | medium | low
Evidence required: <checks>
```

## Fallback

If no installed capability is adequate:

1. Continue directly only when the task is small and low risk.
2. For recurring or specialized gaps, invoke the controlled continuous
   improvement protocol to evaluate an existing marketplace capability.
3. Create a new skill only when reuse is unavailable and the workflow is
   demonstrably recurring.
