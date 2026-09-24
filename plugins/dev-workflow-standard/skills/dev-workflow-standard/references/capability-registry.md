# Engineering Capability Registry

The registry maps engineering needs to preferred capabilities and safe fallbacks.
It is a routing contract, not a list of mandatory calls. Invoke only capabilities
that are relevant to the current checkpoint.

This exact registry is a local architectural extension. Capability-based
routing is a broader agent pattern, but the names, rows, priorities, and
fallback rules below are owned by this repository.

This registry routes capability to owner skill. Each specialist owns its
versioned `references/tool-registry.json` and ignored local runtime state;
see `skill-owned-tools.md`. Do not centralize vendor installation here.

## Core Registry

| Need | Preferred capability | Fallback | Completion evidence |
| --- | --- | --- | --- |
| discovery / orchestration | `dev-workflow-standard` | none | consolidated scope and gate decision |
| environment bootstrap / plugin health | `dev-environment-standard` | explicit manual host handoff when unsupported | HEALTH_REPORT + required capability evidence |
| requirements / specs | `sdd-spec-factory` | orchestrator only for clarification, not silent replacement | specs + executable task |
| implementation | `dev-implementation-standard` with an authorized executor runtime | another authorized executor using the same task/spec contract | diff/files + commands + execution report |
| UI/UX design and review | `ui-ux-standard` | none when UI validation is mandatory | design/review findings + validation evidence |
| functional QA / test engineering | `qa-testing-standard` | none when independent QA is mandatory | test strategy + executed validation + bug disposition + QA_STATUS |
| security review | `security-standard` | none when security trigger is mandatory | findings/coverage + disposition |
| GitHub repository governance / repository bootstrap | `devops-standard` | explicit manual steps with observed evidence and approved sufficient fallback | diagnose + approved apply when required + verify + readiness report |
| CI/CD, containers and operational config | `devops-standard` | approved project-native tool under the same owner | validated config/build + relevant runtime evidence |
| IaC, Kubernetes, GitOps and cloud operations | `devops-standard` | approved project-native platform, no forced migration | scoped plan/render/dry-run + explicit human gate for mutation |
| deploy, server administration and advanced Git/releases | `devops-standard` | manual authorized handoff if target cannot be verified | target, approval, rollback and post-change health |
| observability, backup/DR and incidents | `devops-standard` | project-native runbook with same evidence requirements | checks, restore evidence or NOT VALIDATED, incident disposition |
| repository operations | GitHub connector/tooling when available | local git tooling in the active workspace | remote/local state evidence |
| deterministic repetitive operation | repository script/tool | approved equivalent tool | exit status + output |
| provider failure recovery | replacement authorized LLM/runtime | none if no compatible provider exists | `EXECUTION_HANDOFF` + resumed result |

## Routing Rules

1. Resolve the need, not merely a product name.
2. Prefer the narrowest capability that owns the work.
3. Do not invoke unrelated specialists to create ceremony.
4. Mandatory specialist triggers cannot be replaced by generic reasoning.
5. A fallback must satisfy the same task contract, permissions, scope and
   validation requirements as the preferred capability.
6. If no safe fallback exists, return `BLOCKED` with the missing capability.
7. Do not create parallel implementations when switching executors.
8. Reuse prior valid outputs and receipts instead of restarting finished stages.
9. Use `context-routing.md` for the sector/phase handoff and purpose-based
   source loading. A tool's technical owner is not necessarily the owner of
   the functional conclusion; QA may use shared tools without copying registries.

### Functional QA

Invoke `qa-testing-standard` for behavior changes, bugfixes, user flows, API
behavior, business rules, persistent state, payments, multi-tenant behavior,
imports/exports, integrations, concurrency, state machines and regressions.
Docs-only, metadata-only or administrative changes without runtime behavior
may be N/A with a reason. Pure visual changes retain UI validation even if
functional QA is N/A. Do not silently replace independent QA with the coder.
Planning scenarios may precede implementation; final QA requires executable
artifacts and current dependency receipts. QA owns behavior; Security owns
vulnerability confirmation, UI owns visual quality, DevOps owns operations.

## Runtime Availability

Use the environment skill's `status` fast path before depending on prepared
capabilities. Missing/broken prerequisites route to selective `prepare`/`repair`,
then return here to invoke the specialist. Never replace its receipt with an
environment health report. Provider knowledge lives in the portable MCP Library,
not a hardcoded developer inventory. Preserve registration/installation/
connection/authentication distinctions; host evidence has bounded freshness.

Before invoking a capability, determine whether it is available through the
current environment:

- installed skill
- connected plugin/MCP/tool
- executable script/CLI
- authorized executor LLM/runtime

If the desired capability is not actually available, do not pretend it ran. Use
the fallback policy or block explicitly.

## Specialist Trigger Summary

### DevOps and environment boundary

Repository onboarding, settings, labels, Projects and rules belong to DevOps,
using its `references/github-governance.md` and deterministic helper. Environment
only prepares Git/gh. Bootstrap before the first applicable Task; reuse compatible
evidence until drift/change/failure/request. No new owner, installer or auth flow.
Only fresh verification can justify readiness; a plan, CLI version or generated
workflow is not evidence of remote enforcement or successful CI.

Invoke `devops-standard` for operational infrastructure, not ordinary source
edits or a basic git status/diff/fetch/commit/PR. Advanced Git history rewriting,
release policy/tags and GitOps require DevOps. Application code stays with
implementation. AppSec/scanners remain with security; IAM, secrets, TLS,
firewall, public ports and elevated privilege mandate its review.

When `dev-environment-standard` exists and is available, it detects/prepares
missing tools/MCPs and returns to DevOps for operations. It never operates
production. Both plugins are included in this repository; runtime availability
and authentication require separate evidence. If unavailable, use `tool-state.py` with an
explicit owner-selected, approved official install only if necessary, not a
replacement bootstrapper/MCP catalog. Do not confuse registered/configured,
installed, connected, authenticated and successfully executed capabilities.

### UI/UX

Invoke `ui-ux-standard` when work changes screens, components, layout,
responsiveness, accessibility, interaction states or design-system behavior.

### Security

Invoke `security-standard` when work touches authentication, authorization,
sessions, tokens, secrets, sensitive data, uploads, payments, parsers, webhooks,
external integrations, tenant isolation, infrastructure or privileged
operations.

### Specs

Invoke `sdd-spec-factory` before implementation of non-trivial product work,
according to the main workflow gates.

### Implementation

Invoke `dev-implementation-standard` only after its task/spec preconditions are
satisfied. The harness remains responsible for observing execution state and
validating the returned result.
