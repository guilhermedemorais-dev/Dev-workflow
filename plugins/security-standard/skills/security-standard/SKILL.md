---
name: security-standard
description: "Use for authorized defensive application security work: security review of code changes, scoped or repository audits, threat modeling, vulnerability validation, remediation, security testing, and evidence-based release gates."
---

# Security Standard

Use this skill as the security specialist companion to `dev-workflow-standard`.
It provides an original, risk-based application security process focused on
credible attack paths, measurable coverage, reproducible evidence, durable
fixes, regression prevention, privacy, supply chain, and release governance.

Load only the reference required by the active phase:

- `references/review-pipeline.md`: phase gates and parallel review strategy
- `references/coverage-model.md`: surfaces, layers, coverage ledger, and blind spots
- `references/finding-standard.md`: evidence contract, severity, confidence, and deduplication
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

When `minimal-implementation-gate` recommends simplification, security has
precedence. Never remove or weaken authentication, authorization, input
validation, tenant boundaries, secret handling, audit logs, privacy controls,
security tests or defensive error handling to reduce code, files or token cost.

## Security Spec Contract Mode

Use this mode during Discovery / SDD before product code is implemented. The
goal is not to run a pentest. The goal is to make the feature spec precise
enough that implementation cannot accidentally omit a control.

Trigger this mode when a spec/task touches:

- authentication, authorization, sessions, recovery, MFA, impersonation
- tenant boundaries, object ownership, admin/support or privileged operations
- sensitive data, privacy, retention, export/import, backups, observability
- uploads, downloads, archives, generated files, parsing or serialization
- payments, billing, credits, irreversible actions or fraud-sensitive flows
- webhooks, queues, external integrations, callbacks, redirects, SSRF surfaces
- browser storage, DOM rendering, third-party scripts, CORS, CSP, CSRF
- secrets, tokens, API keys, cryptography, signing, replay or key lifecycle
- dependencies, package managers, install scripts, CI/CD, containers, IaC,
  cloud/IAM, networks, databases, caches or release artifacts
- AI/LLM tools, agent actions, prompt/data injection, RAG, model/provider keys
- UI-visible security behavior: permission states, masked sensitive data,
  forbidden/unauthorized screens, tenant/user boundary cues, safe error copy,
  browser-visible storage and client-side exposure of secrets or tokens

For each affected surface, return a `Security Spec Contract` table:

| Surface | Asset | Attacker-controlled input | Actor/role rule | Trust boundary | Required control | Negative test/evidence | Release blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |

Block the task when any reachable security-sensitive effect lacks an explicit
control or negative test. Mark non-applicable areas as `N/A` only with a
verified reason.

Security spec output must distinguish:

- `BLOCKER`: missing required control or unverifiable security invariant.
- `REQUIRED`: control/test must be implemented in the task.
- `INFO`: defense-in-depth improvement, not required for current release.
- `N/A`: not applicable with reason.

Do not turn this mode into generic OWASP prose. Every row must point to a
specific feature surface, actor, data asset, entry point or user interaction.

When the security-sensitive behavior is visible in UI, also return the UI/UX
handoff rows that `ui-ux-standard` must validate:

| UI surface | Security/privacy expectation | Required visual state | Negative test/evidence | Release blocker |
| --- | --- | --- | --- | --- |
|  |  |  |  | sim/não |

Examples: unauthorized user cannot see or trigger an action, sensitive data is
masked, tenant/user data does not bleed across accounts, forbidden state uses
safe copy, and secrets/tokens are not visible in DOM, logs, URL, localStorage or
browser bundles.

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

During SDD, keep this compact and feature-scoped. If the threat model reveals a
missing product/security decision, return `BLOCKED` with the exact question
instead of inventing a policy.

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

During SDD, unvalidated candidate risks are not reported as confirmed
vulnerabilities. They become required controls, tests, or blocking questions in
the Security Spec Contract.

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

For `Frontend/UI`, include privacy and permission-state evidence when the task
has UI: masked sensitive fields, unauthorized/forbidden states, disabled actions,
tenant/user separation, safe errors, and no browser-visible secrets/tokens. If
that evidence belongs to `ui-ux-standard`, mark the dependency explicitly and do
not claim full `PASS` until the UI evidence is present or a scoped exception is
approved.

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
- UI-facing auth, tenant, sensitive-data, or privileged flows lack permission,
  masking, forbidden-state or browser-exposure evidence
- runtime-dependent claims were not tested or explicitly marked unvalidated
- tool failures or excluded areas were hidden
- a fix was applied without regression validation
- a security-triggering task lacks a Security Spec Contract or negative tests
  before implementation

## Handoff To Dev Workflow

Return:

- selected review mode and risk level
- Security Spec Contract result when operating during Discovery / SDD
- scope reviewed and scope excluded
- confirmed findings and unresolved candidates
- fixes applied and tests executed
- `SECURITY_STATUS`
- release blockers and residual risks
- exact next decision requiring human approval
