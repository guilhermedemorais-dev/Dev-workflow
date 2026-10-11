# Technical Knowledge Router (consultative engineering references)

## Purpose and loading policy
Use this index only for NORMAL/COMPLEX tasks where a technical decision, affected boundary, or failure mode merits investigation. Never load every domain indiscriminately. Inspect the actual project, approved PRD, architecture, lockfile, ADRs, tests, and versioned documentation first. Reuse existing routing, security-standard, QA, DevOps and tool registry; this reference supplements, never overrides their ownership.

## Evidence precedence
1. Existing application source, deployed behavior and explicit accepted project contracts (note conflict between code and docs).
2. Official version-matched specs and vendor documentation, official standards and maintained implementations.
3. Reputable implementations and technical literature, verified against first-party references.
4. Explicitly identified local decision or hypothesis.

For each material technical decision capture: question; affected code/contract; alternatives and tradeoffs; chosen approach; source URL + version/revision/date where available; concrete negative/positive test; rollback/observability where relevant; confidence (VERIFIED / ASSUMPTION / OPEN); owner and approval gate. Missing evidence NEVER becomes a made-up guarantee. Escalate blocking domain requirements to the owner. Cite short source pointers, not giant copied excerpts. Don't ingest secrets.

## Domain routing (activate only matched rows)
| Trigger | Investigate | Primary reference |
| --- | --- | --- |
| Algorithm, refactor, APIs, abstraction | complexity, immutability, coupling/cohesion, DRY/KISS/SOLID applicability, maintainability, error semantics, version compatibility | language/framework official docs and source/tests |
| Service boundaries or changing modules | domain boundaries, modular monolith vs services, ADR, failure isolation, observability, compatibility, migrations | existing ADRs and code, https://martinfowler.com/articles/microservices.html |
| Persistence, inventory, checkout, payment | transactions, ACID, isolation level, atomic conditional updates, locks, idempotency, uniqueness, deadlocks, retries, reconciliation, data migrations | database official docs (e.g. https://www.postgresql.org/docs/current/transaction-iso.html) |
| Auth, sessions, tokens, access | authentication vs authorization, OAuth/OIDC scopes, token lifetimes/rotation, secure cookie, race on refresh, CSRF, session invalidation, threat model, negative tests | https://www.rfc-editor.org/rfc/rfc6749 ; https://openid.net/developers/specs/ ; https://owasp.org/www-project-application-security-verification-standard/ |
| Integration, API or webhook | HTTP semantics, schemas, pagination, timeouts, signatures, backoff+jitter, deduplication, idempotency, partial failures, compatibility | https://www.rfc-editor.org/rfc/rfc9110 ; integration vendor docs |
| Queues, concurrent jobs, distributed state | at-least-once delivery, retries, ordering, poison messages, outbox, compensating actions, eventual consistency | selected queue/database official docs |
| AppSec, sensitive data, dependency change | threat model, validation, access control, secrets, dependency advisories, versioned ASVS controls, OSV and security-standard gating | https://owasp.org/www-project-application-security-verification-standard/ ; https://osv.dev/ ; security-standard |
| Testing or bug fixing | reproducible failure, risk-based unit/integration/e2e, regression, property/negative test, flaky tests, evidence and independent QA | project test framework docs and qa-testing-standard |
| CI/CD, infrastructure, production release | least privilege, artifacts, rollout, rollback, backups, DR, logging, SLO, alerting, supply chain | https://csrc.nist.gov/projects/ssdf ; devops-standard |
| Fiscal/legal regulated business logic | jurisdiction, product classification, tax parameters, official schemas, signature/certificates, rejection flows, homologation, audit trail | current official regulator documents, accountant/product owner approval; never infer tax rules from examples |

## Minimum impact-oriented contract
For each affected sector of the existing Human Task and equivalent JSON: link discovered source, identify applicable controls, acceptance criteria and explicitly executable positive/negative tests. Keep N/A with reason. Map requirement -> implementation microtask -> verification evidence. For the PR, include a concise human-readable Engineering Explanation: why this approach; what alternatives were considered; what might fail; what was actually tested; known limitations and pending human decisions. This is a report section, not a new mandatory competing Task/schema.

## Stop conditions
- Unverified regulatory/business logic, critical authorization gap, destructive migration without rollback, or unresolved architecture conflict: BLOCKED until decision.
- Unavailable docs/tool or inconclusive advisory: mark NOT VERIFIED and use safest non-invented fallback or block based on impact.
- Scanner PASS or AI code review is not proof of security. Human acceptance and existing Harness gates remain intact.
- Do not prescribe an exhaustive pattern catalog as mandatory. Applying every concept by default increases cost and introduces accidental complexity.

## Verification examples
- Concurrent last-unit checkout: test two parallel purchases and assert exactly one inventory reservation; distinguish paid from reserved, verify rollback/idempotency on timeout.
- Login and token refresh: test expiry, rotation, revocation, concurrent refresh, authz cross-user denial, secret storage and audit behavior.
- Fiscal integration: test schema reject, transport retry, duplicate document, cancellation, reconciliation and jurisdiction-specific rules with approved expert input.
