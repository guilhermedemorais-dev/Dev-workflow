# Controlled Continuous Improvement

Use this protocol when the workflow repeatedly fails, lacks a capability, wastes
time on a recurring manual task, or could benefit from a specialized skill,
plugin, MCP server, hook, agent, or CLI.

The objective is filling a verified routing gap with evidence. It is not the
normal task workflow, autonomous installation, or permission expansion.

Before starting this protocol, run capability routing and confirm that no
installed capability adequately covers the task, or that the selected
capability has repeatedly failed objective validation.

## Triggers

Start an evaluation when at least one condition exists:

- The same failure or correction occurred more than once.
- A recurring task is being rebuilt manually across projects.
- Current tools cannot meet an acceptance criterion.
- A platform marketplace contains a potentially relevant capability.
- A postmortem identifies a missing check, skill, integration, or guardrail.
- A plugin or skill is stale, unreliable, duplicated, or too expensive in tokens.

Do not search for new tooling during a simple task when the current workflow is
already sufficient.

## Improvement Loop

### 1. Observe

Record the gap before searching for a solution:

- task and expected result
- current tool or workflow
- failure, delay, quality issue, or token cost
- evidence and frequency
- desired measurable improvement

### 2. Search Existing Capabilities

Check in this order:

1. Skills and plugins already installed and enabled.
2. Project-local skills, rules, scripts, and documented patterns.
3. Official marketplace entries maintained by the platform vendor.
4. Maintained community marketplaces or repositories.
5. A small custom skill or script when no suitable capability exists.

Prefer reuse or a focused update over adding another overlapping capability.

### 3. Audit The Candidate

Before installation, inspect:

- source repository, maintainer, license, release history, and last update
- manifest, skills, prompts, scripts, binaries, hooks, agents, and MCP config
- requested filesystem, shell, network, browser, credential, and API access
- dependencies and install scripts
- telemetry, external endpoints, secret handling, and data retention
- compatibility with the current platform and project
- overlap or conflict with existing rules and skills
- expected context/token cost

Treat hooks, executable scripts, MCP servers, binaries, and broad permissions as
high risk. Do not approve opaque or unverifiable components for sensitive repos.

### 4. Score And Propose

Create `docs/ai-workflow/evaluations/YYYY-MM-DD-capability-name.md` when the
evaluation belongs to a project. Score each item from 0 to 5:

| Criterion | Meaning |
| --- | --- |
| Relevance | Solves the observed gap directly |
| Quality | Instructions and implementation are coherent |
| Maintenance | Active, versioned, and documented |
| Security | Minimal permissions and auditable behavior |
| Compatibility | Works with the target platform and stack |
| Efficiency | Saves time/tokens without reducing reliability |
| Testability | Can be evaluated with objective checks |
| Reversibility | Can be disabled or removed cleanly |

Document total score, blocking risks, source/version, proposed scope, test plan,
and rollback plan. A high total never overrides a critical security concern.

### 5. Human Approval Gate

Present the candidate and wait for explicit approval before:

- installing a third-party plugin or skill
- enabling hooks, MCP servers, monitors, agents, or binaries
- granting new permissions or credentials
- replacing an existing canonical workflow
- promoting a project-local experiment to global scope

Discovery and static inspection may happen without installation. Installation
and activation may not.

### 6. Sandbox And Validate

Install first at the narrowest available scope: temporary session, local repo,
or project scope before user/global scope.

Run a representative evaluation that compares baseline and candidate:

- acceptance criteria success rate
- correctness and regression count
- execution time
- token/context usage when observable
- number of manual corrections
- security and permission behavior
- deterministic/repeatable output

Do not test new third-party capabilities with production secrets or sensitive
customer data.

### 7. Promote Or Roll Back

Promote only when evidence shows a meaningful improvement and all required gates
pass. Pin a release, tag, commit SHA, or recorded version when the platform
supports it.

Roll back when the candidate introduces regressions, excessive context, unsafe
permissions, instability, hidden network calls, or maintenance risk.

### 8. Learn

Update only the durable artifact that owns the lesson:

- improve an existing skill when its instructions were incomplete
- create a focused project skill for domain-specific behavior
- update the global plugin for a reusable cross-project rule
- record rejected candidates to avoid repeating the same evaluation
- remove or archive capabilities that no longer justify their cost

Never rewrite a skill from a single anecdote. Require repeated evidence or a
clear high-impact failure.

## Capability Registry

When a project uses multiple agents or extensions, maintain
`docs/ai-workflow/capability-registry.md` with:

| Capability | Type | Source | Version/SHA | Scope | Platforms | Status | Last validation | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Allowed status values:

- `CANDIDATE`
- `APPROVED_FOR_TEST`
- `ACTIVE`
- `DISABLED`
- `REJECTED`
- `REVIEW_REQUIRED`

## Cross-Platform Strategy

Use a canonical Agent Skill folder with `SKILL.md` and optional references,
scripts, and resources. Add only the packaging required by each platform:

- Codex: `.codex-plugin/plugin.json` and a Codex marketplace entry.
- Claude Code: `.claude-plugin/plugin.json` and optionally a Claude marketplace.
- Antigravity: root `plugin.json`, or install the skill at workspace/global scope.

Platform-specific hooks, MCP definitions, permissions, or settings must remain
separate because their schemas and security models differ.

## Update Policy

- Do not enable uncontrolled auto-update for third-party capabilities used on
  production or sensitive projects.
- Review release notes and diff the installed version against the candidate.
- Re-run the representative evaluation after updates.
- Keep the prior working version or removal instructions available.
- Re-audit when ownership, repository, permissions, dependencies, or network
  behavior changes.

## Minimum Evaluation Report

```markdown
# Capability Evaluation: <name>

## Gap
## Candidate And Source
## Target Platforms And Scope
## Static Audit
## Permissions And Data Access
## Scorecard
## Baseline
## Validation Tasks
## Results
## Risks
## Rollback
## Decision
## Human Approval
```
