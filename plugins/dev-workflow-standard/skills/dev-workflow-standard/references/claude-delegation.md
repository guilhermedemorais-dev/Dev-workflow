# Claude Code Delegation Protocol

Use this protocol to keep Codex focused on technical leadership while Claude
Code performs bounded implementation work.

## Objective

Reduce Codex context and token consumption without weakening source-of-truth,
review, QA, security, or user approval gates.

## Mandatory Trigger

Delegate the code-writing checkpoint to Claude Code when any of these apply:

- a feature, refactor, integration, migration, or non-trivial bugfix is requested
- implementation spans more than two files or more than one technical concern
- the expected patch is larger than a small localized edit
- repetitive code, tests, component work, or mechanical changes are required
- a PRD, spec, roadmap phase, or implementation checkpoint exists

Codex may edit directly only for genuinely small changes such as a typo,
single-line config correction, tiny documentation adjustment, or narrowly
localized patch that does not justify delegation overhead.

## Availability Gate

Before the first delegated checkpoint in a task, run:

```bash
command -v claude
claude --version
claude auth status
```

Set `CLAUDE_STATUS`:

- `AVAILABLE`: binary exists and authentication is valid.
- `SANDBOX_NETWORK_BLOCKED`: authentication is valid, but a delegated prompt fails with DNS, connection, API network, or timeout symptoms inside the restricted workspace.
- `INSTALLED_ONLY`: binary exists but authentication or provider setup fails.
- `UNAVAILABLE`: binary is missing or cannot start.

Use a minimal prompt test only when auth status is inconclusive. Do not spend a
model request on every checkpoint merely as a health check.

For mandatory-trigger work, do not silently fall back to Codex implementation
when `CLAUDE_STATUS != AVAILABLE`. Stop before code writing and report the
delegation blocker so Codex does not consume the implementation budget itself.

### Restricted Workspace Recovery

The Codex workspace may allow the `claude` binary and local authentication
checks while blocking outbound API traffic. When `claude -p` fails or times out
with connection, DNS, network, or API transport symptoms:

1. Keep the same bounded prompt, working directory, tool allowlist, and checkpoint scope.
2. Set `CLAUDE_STATUS=SANDBOX_NETWORK_BLOCKED`.
3. Retry the same command with the platform's approved external-network or escalated execution path.
4. Ask for user approval through the execution permission mechanism when required.
5. If the escalated retry succeeds, set `CLAUDE_STATUS=AVAILABLE_EXTERNAL` and continue normal diff review.
6. If it also fails, stop and report the exact error; do not implement the checkpoint in Codex as a silent fallback.

Do not repeatedly run ordinary sandbox retries after the network-block pattern
is established. One restricted attempt and one approved external retry are
sufficient for the same checkpoint.

## Checkpoint Sizing

Split implementation before calling Claude:

- one layer, module, or coherent responsibility per checkpoint
- one objective and one expected diff per invocation
- normally no more than five directly changed files per checkpoint
- one to three acceptance criteria per checkpoint
- database, backend/API, frontend/UI, tests, and docs stay separate when they can be reviewed independently

If a coherent change requires more files, explain the coupling in the brief.
Never send an entire multi-phase project as one Claude prompt.

## Context Budget

Send paths and a compressed contract, not the full Codex conversation.

Include only:

- exact objective
- source-of-truth PRD, issue, research, spec, and mockup paths
- allowed files or module boundary
- relevant public contracts and constraints
- acceptance criteria
- expected tests or validation commands
- output instruction: return only changed files, tests, and blockers in at most 12 lines

Do not paste whole repositories, long chat transcripts, unrelated logs, or
complete documentation trees. Claude should read the named files itself.
Codex should inspect the resulting files and diff instead of requesting a long
implementation explanation from Claude.

## Execution Command

Run from the canonical project root:

```bash
claude -p "<bounded implementation brief>" \
  --permission-mode acceptEdits \
  --tools "Read,Edit,Write,Glob,Grep" \
  --output-format text
```

This mode allows bounded file edits but keeps shell execution and final
validation with Codex. Add tools only when the checkpoint specifically needs
them and the risk is understood. Never use `--dangerously-skip-permissions`.

## Required Visibility

Before invoking Claude, tell the user:

- the checkpoint being delegated
- the allowed scope
- that Claude Code will implement and Codex will review

After Claude returns, report whether it executed successfully and summarize its
claimed changes. Do not imply delegation occurred if no `claude` command ran.

## Review Gate

After every Claude checkpoint, Codex must:

1. Inspect `git status` and the scoped diff.
2. Reject unrelated edits or architecture drift.
3. Validate the diff against the source-of-truth and acceptance criteria.
4. Run canonical tests, lint, typecheck, runtime, QA, or security checks as applicable.
5. Fix only small review findings directly; delegate substantial rework as a new bounded checkpoint.
6. Record `CLAUDE_STATUS`, whether external execution was required, delegated checkpoint, validation evidence, and remaining gaps.

Do not start the next implementation checkpoint until the current diff is
reviewed and reconciled.
