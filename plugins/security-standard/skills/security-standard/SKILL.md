---
name: security-standard
description: "Use for authorized defensive application security work: security review of code changes, scoped or repository audits, threat modeling, vulnerability validation, remediation, security testing, and evidence-based release gates."
---

# Security Standard

The LLM using this skill acts as the security specialist. Read this `SKILL.md`
completely before analysis and return a `SKILL_RECEIPT`; a mention of the skill
is not proof that its methodology was applied.

Use this skill as the security specialist companion to `dev-workflow-standard`.
It provides an original, risk-based application security process focused on
credible attack paths, measurable coverage, reproducible evidence, durable
fixes, regression prevention, privacy, supply chain, and release governance.

Load only the reference required by the active phase:

- `references/review-pipeline.md`: phase gates and parallel review strategy
- `references/coverage-model.md`: surfaces, layers, coverage ledger, and blind spots
- `references/finding-standard.md`: evidence contract, severity, confidence, and deduplication
- `references/false-positive-validation.md`: mandatory rejection checklist and publication gate
- `references/stack-profiles.md`: multistack discovery and version-aware review rules
- `references/report-template.md`: durable report and release-gate format

## Scope And Safety

Use only for systems the user owns, is authorized to test, or controls as a
local lab. Prefer defensive analysis, secure implementation, hardening, and
safe proof of impact.

Never:

- target third-party systems without explicit authorization
- collect real credentials, tokens, customer records, or private data
- persist access, evade detection, deploy malware, or automate abuse
- run destructive tests against production
- turn a theoretical concern into an exploit against a real external target

When active exploitation is unnecessary, prove the issue with code evidence,
tests, mocks, local fixtures, or an isolated environment.

## Relationship To The Main Workflow

`dev-workflow-standard` owns the project lifecycle and final delivery status.
This plugin owns security analysis and returns evidence, findings, fixes, tests,
and a `SECURITY_STATUS`.

Do not replace project rules, PRDs, architecture, or business invariants. If a
security fix changes a product policy, public API, authorization rule, schema,
or user flow, stop for a product decision before implementing it.

## Review Modes

Choose the smallest mode that provides credible coverage.

### Change Review

Use for a working-tree diff, commit, branch, or pull request.

Focus on:

- newly introduced or weakened trust boundaries
- authentication and authorization changes
- input parsing, validation, encoding, and dangerous sinks
- secret handling, logging, error disclosure, and data exposure
- database queries, file paths, uploads, redirects, templates, and command execution
- dependency, infrastructure, CI/CD, and configuration changes
- sibling call sites affected by a modified shared helper

Do not expand into an unrelated repository audit.

### Scoped Audit

Use for a module, route group, service, package, integration, or other explicit
boundary. Include directly supporting code only when needed to prove data flow,
authorization, reachability, or impact.

### Repository Audit

Use when broad assurance is required. Start with architecture and attack
surface mapping, then prioritize internet-facing, privileged, multi-tenant,
secret-bearing, payment, upload, parser, admin, and data-export surfaces.

Repository coverage must be explicit. Record what was reviewed, excluded,
deferred, and why. Never imply exhaustive coverage from a sample of files.

Use the coverage model in `references/coverage-model.md`. For large scopes,
partition work by independent attack surface, not arbitrary file count. Keep
one owner per surface and reconcile shared controls centrally.

### Finding Validation And Fix

Use when a candidate issue already exists. Confirm that the vulnerable path is
reachable, identify the violated invariant, implement the smallest safe fix,
and add a regression test that fails before the fix and passes after it when
practical.

## Risk-Adaptive Depth

Classify the task before analysis:

- `LOW`: docs, styling, isolated non-sensitive logic, or tests with no runtime trust impact
- `MEDIUM`: ordinary API/UI behavior, data writes, dependencies, or internal integrations
- `HIGH`: auth, authorization, tenants, secrets, payments, uploads, admin, infrastructure, parsers, webhooks, or sensitive data
- `CRITICAL`: production identity boundary, cryptography, privileged execution, public deserialization, or a known active vulnerability

Minimum depth:

- `LOW`: focused diff review and secret/config check
- `MEDIUM`: focused review plus relevant automated tests
- `HIGH`: threat model update, end-to-end data-flow review, negative tests, and runtime validation where safe
- `CRITICAL`: independent validation, rollback plan, explicit human gate, and no production change without approval

## Security Workflow

Follow the gated pipeline in `references/review-pipeline.md`. A phase may not
claim completion until its required evidence exists. Preserve intermediate
evidence so an interrupted audit can resume without repeating or overstating
coverage.

### 1. Establish Authority And Source Of Truth

Identify:

- authorized target and exact scope
- project rules and security documentation
- architecture and deployment model
- sensitive assets and regulated data
- environments allowed for testing
- acceptance criteria and prohibited actions

### 2. Build A Compact Threat Model

Document only what is useful for the current scope:

- assets worth protecting
- actors and privilege levels
- entry points and attacker-controlled inputs
- trust boundaries and tenant boundaries
- sensitive sources and dangerous sinks
- existing controls and assumptions
- abuse cases with plausible impact

Threat models must reflect the actual repository and runtime. Generic OWASP
lists are prompts for investigation, not evidence of vulnerabilities.

### 3. Trace Security-Relevant Flows

Follow data and authority from entry point to effect:

```text
input/source -> parsing -> validation -> authorization -> transformation -> sink/effect
```

Check both happy paths and negative paths. Inspect shared helpers and alternate
entry points when a control is centralized.

### 4. Discover Candidates

Evaluate, as applicable:

- broken access control, IDOR, tenant isolation, privilege escalation
- authentication, sessions, recovery, MFA, token lifecycle, CSRF
- injection into SQL, NoSQL, shell, templates, expressions, headers, or logs
- XSS, unsafe HTML, redirects, CORS, CSP, and browser trust boundaries
- SSRF, webhooks, outbound requests, DNS/IP validation, and callback handling
- file upload, archive extraction, path traversal, MIME and content handling
- unsafe deserialization, parsing limits, recursion, memory and CPU exhaustion
- cryptography, randomness, key handling, signature verification, and replay
- secrets in code, configuration, logs, build output, browser bundles, or history
- dependency and supply-chain risks, install scripts, CI permissions, and artifact provenance
- insecure defaults, debug modes, exposed services, containers, cloud/IAM, and network controls
- privacy, excessive data collection, retention, exports, backups, and observability

### 5. Validate Before Reporting

A reportable finding needs:

- precise affected location
- attacker-controlled source or violated privilege boundary
- missing, bypassed, or insufficient control
- reachable security-sensitive sink or effect
- realistic preconditions
- concrete confidentiality, integrity, availability, or privacy impact
- evidence that relevant mitigations do not already block the path

Classify uncertain candidates as `NEEDS_VALIDATION`, not as confirmed.
Ordinary correctness bugs are not security findings without security impact.

Before assigning `CONFIRMED`, load and apply
`references/false-positive-validation.md`. Validation must trace imported guards,
middleware, framework defaults, deployment controls, and other upstream or
downstream mitigations instead of judging one suspicious line in isolation.

Use `references/stack-profiles.md` to detect the repository's actual languages,
frameworks, package managers, lockfiles, runtime versions, infrastructure, and
deployment conventions. Load only the profiles that match detected evidence.
Never assume a Next.js, Node.js, PHP, WordPress, Laravel, Vue, container, or
cloud convention without proving that it applies to the target revision.

Apply the complete evidence and deduplication rules in
`references/finding-standard.md`. Independent vulnerable entry points remain
separate findings even when they share a root cause; remediation may group them.

### 6. Rate Severity

Use impact and exploitability together:

- `CRITICAL`: broad compromise with realistic low-friction exploitation
- `HIGH`: account/tenant compromise, significant sensitive-data exposure, privileged action, or credible code execution
- `MEDIUM`: meaningful but constrained security impact requiring notable conditions
- `LOW`: limited impact or defense-in-depth weakness with a plausible path
- `INFO`: hardening or hygiene recommendation without demonstrated vulnerability

State confidence separately as `HIGH`, `MEDIUM`, or `LOW`. Tool-generated
severity never overrides repository evidence.

### 7. Remediate At The Correct Boundary

Prefer fixes that enforce the security invariant centrally and preserve public
contracts when possible. Avoid scattered symptom patches.

For each fix:

- explain the violated invariant
- identify why the current control failed
- implement the smallest complete correction
- add negative and regression tests
- verify expected legitimate behavior still works
- assess migration, compatibility, observability, and rollback needs
- search for affected sibling instances

### 8. Validate The Result

Use the repository's canonical commands and environment. Depending on risk,
run unit, integration, API, browser/e2e, dependency, SAST, secret, container,
or infrastructure checks.

For runtime testing:

- use local, test, or staging environments
- use synthetic accounts and sanitized fixtures
- avoid destructive payloads and uncontrolled load
- capture reproducible evidence without storing secrets

## Tool Policy

Use installed security tools when they improve evidence, but do not make one
vendor or scanner mandatory. Inspect configuration and versions before use.

Examples include dependency audits, secret scanners, SAST, linters, container
scanners, IaC checks, Playwright, API clients, and repository-native tests.

Guilherme's current Codex environment also enables MCPs that may support
authorized defensive work:

- `playwright` and `chrome-devtools` for safe browser/runtime validation.
- `context7` for current security-relevant library and framework documentation.
- `grep-mcp` for public implementation patterns and sibling-instance research.
- `firecrawl-mcp` for targeted collection of public advisories or vendor documentation.
- `figma` when an approved design is needed to verify privacy, permission, or security UX.
- `hf-mcp-server` when the authorized scope includes Hugging Face models, datasets, Spaces, or supply-chain context.
- `node_repl` for bounded local analysis when exposed by the runtime, never for unapproved exploitation.

Verify live MCP availability before relying on it. Do not send private source,
secrets, customer data, tokens, cookies, or vulnerability evidence to remote MCP
services. MCP output is candidate evidence and never replaces repository or
runtime validation.

Scanner output is candidate input. Validate findings in code and runtime before
reporting them as vulnerabilities. Record tool failures and blind spots.

## External Publication Gate

Do not create or update a GitHub issue, pull request, Jira ticket, Linear issue,
security advisory, customer report, release blocker, or vulnerability count for
a `CANDIDATE`, `NEEDS_VALIDATION`, or `FALSE_POSITIVE` item.

External tracking is allowed only when all are true:

- status is `CONFIRMED`, or `FIXED` with the original confirmation retained
- confidence is `HIGH` or `MEDIUM`
- the complete evidence contract is present
- the mandatory false-positive checklist passed
- affected revision and locations are stable and reproducible
- duplicates and sibling instances were reconciled

If any condition fails, keep the item in the internal validation backlog. A
human may explicitly request publication of an unconfirmed item, but its title
and body must clearly say `NEEDS_VALIDATION`; never present it as a vulnerability
or include it in confirmed totals.

The proprietary `Codex Security` plugin may be used as an optional independent
second opinion when installed. Do not copy or redistribute its content, scripts,
templates, or internal workflow. This plugin remains independently authored and
must function without it.

## Evidence And Reporting

Write project reports under the existing canonical security/docs structure. If
none exists and durable reporting is required, prefer:

```text
docs/security/
  threat-model.md
  reviews/
    YYYY-MM-DD-<scope>.md
```

Each finding must include:

- ID and title
- status: `CONFIRMED`, `NEEDS_VALIDATION`, `FALSE_POSITIVE`, `FIXED`, or `ACCEPTED_RISK`
- severity and confidence
- affected file/route/component
- evidence and attack path
- preconditions and impact
- recommended fix
- tests or validation steps
- residual risk

Use `references/report-template.md` for durable audits. Maintain a coverage
ledger for scoped or repository audits and reconcile every row as `REVIEWED`,
`NOT_APPLICABLE`, `DEFERRED`, or `BLOCKED`, with evidence or an exact reason.

Always report status by layer:

- `Banco`
- `API/Backend`
- `Frontend/UI`
- `Infra/DevOps`
- `Dependencias/Supply Chain`

Final gate values:

- `PASS`: relevant scope validated; no unresolved release-blocking finding
- `PARTIAL`: useful review completed, but coverage or runtime evidence is incomplete
- `BLOCKED`: confirmed release-blocking risk or required validation cannot proceed
- `NOT VALIDATED`: no credible security validation was executed

Never issue final acceptance for the user. `PASS` means ready for human review,
not approved for production.

## Completion Rules

Do not claim a security review is complete when:

- authorization or scope is unclear
- high-risk changed paths were not reviewed
- candidates were reported without validation
- auth, tenant, sensitive-data, or privileged flows lack negative tests
- runtime-dependent claims were not tested or explicitly marked unvalidated
- tool failures or excluded areas were hidden
- a fix was applied without regression validation

## Handoff To Dev Workflow

Return:

- selected review mode and risk level
- scope reviewed and scope excluded
- confirmed findings and unresolved candidates
- fixes applied and tests executed
- `SECURITY_STATUS`
- release blockers and residual risks
- exact next decision requiring human approval
