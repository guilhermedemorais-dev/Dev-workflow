# Workflow Planning

Read only when selected by the owning SKILL.md route. Backtick paths beginning
with `references/` are relative to that skill directory, not this file.

## Mandatory Flow

The remaining full workflow applies to NORMAL/COMPLEX work and delegated work,
not to the confirmed inline path above.

For product briefing, a new project or reassessment of an existing/low-code
system, invoke the available `studio-prd` skill before detailed module specs.
It owns briefing, PRD and the separate internal execution plan, not a competing
task template. Resolve the active bundle; do not guess sibling cache paths.
If absent, report the missing capability and use an explicitly available
canonical checkout, without claiming it installed.

Require the approved module count/IDs, actors/journeys and boundaries, plus
`docs/planejamento/plano-de-execucao.md` and its equivalent JSON revision.
Urgency cannot silently override prerequisites; unknown capacity/estimates
stay explicit. Preserve the full agreed production scope, not an automatic MVP.
After PRD/order approval, announce the first module ready for SDD and await
the user's instruction. Each module spec ends with coverage/gaps and its Issue
report before approval to continue. PRD approval is not implementation approval.
Existing bounded tasks need not repeat an entire product briefing.

For UI-bearing modules, require the project-owned Markdown guide and live HTML
component catalogue from UI/UX during specification. Route exact component
IDs/revisions to SDD, implementation and QA. A mock widget is not a tested backend.
Reuse the existing task template, sector matrix and list prompts unchanged.
The short per-task prompt in the internal plan is a contextual tech-lead note,
not a second execution contract or automatic permission to spawn chats.

```text
Idea / demand
  -> dev-workflow-standard: diagnose + critical questions
  -> collaborative Discovery / SDD with user + research
  -> sdd-spec-factory: specs, reference/design libraries, complete Issue + v2 JSON
  -> publish DISCOVERY_SDD_COMPLETED with token usage and changed surface
  -> human approval
  -> dev-workflow-standard: resolve executor capability + verify availability
  -> selected executor: invoked; state RUNNING
  -> dev-implementation-standard: implement routed microtasks + executor tests
  -> execution result: diff / files / commands / artifacts
  -> selected executor: complete EXECUTION_RECEIPT
  -> update Human Task + publish EXECUTION_REPORT_COMMENT when applicable
  -> dev-workflow-standard: VALIDATING
  -> independent UI/UX / QA / Security / DevOps validation as applicable
  -> sector reconciliation
  -> Pull Request / PR gate
  -> Harness final gate
  -> dev-workflow-standard: approve or request rework
  -> human review / acceptance
  -> merge / deploy (only after PR approved)
```

The orchestrator does not advance to the next stage until the current gate is
satisfied. The full pipeline lives in
[`workflow-pipeline.md`](../../../../../docs/workflow-pipeline.md).

## Repository Readiness Bootstrap

When organizing a client project's folders, include portal preparation in the
onboarding plan and read [Client portal](client-portal.md). The
destination is `docs/portal/` in that project, not the plugin cache. An external
template repository may be supplied later: record that pending dependency and
continue unrelated work; never invent a URL, substitute a reference website,
or claim the portal installed. Route approved preparation/Pages configuration
to DevOps, preserving the separate backend and publication gates.

Before the first Task requiring remote governance, route repository onboarding
to `devops-standard` and load its `references/github-governance.md`. Environment
prepares Git/gh; DevOps owns diagnose/propose/confirmed apply/verify. Authentication
handoff is human, never a request for tokens in chat. Authentication, repository
access, administration, organization and Project permissions are separate gates.

Require an existing EXECUTION_RECEIPT with target/revision, current verification,
applicable capabilities, proposal/confirmation, actual mutations, limitations and
readiness. `READY`/`READY_WITH_LIMITATIONS` from governance are scoped results, not
new global execution states. Environment/auth/access/files/remote governance/
Project/CI/human gates must be evidenced; explicit N/A and approved sufficient
fallbacks must be justified. Missing required evidence is not a limitation waiver.
`PROJECT READY != PRODUCTION AUTHORIZED`; never equate configured with enforced.

Reuse compatible evidence after onboarding. Repeat only for drift, relevant
change, actual failure or explicit request, not full bootstrap before every Task.
Repository governance makes DevOps REQUIRED; trigger Security for permissions,
secrets/IAM or equivalent risk. QA may be N/A for pure remote configuration with
reason, but deterministic helper behavior changes require independent QA.

## When to Trigger Each Specialist

- API discovery during planning/spec: route relevant API, integration or
  validation-endpoint needs to `sdd-spec-factory` and its
  [API Research Library](../../../../sdd-spec-factory/skills/sdd-spec-factory/references/api-research-library.md).
  Prioritize free APIs or a suitable free tier to validate application features
  and test the application when relevant; confirm limits and use synthetic data.
  That link is the monorepo source path. In an installed host, resolve the active
  `sdd-spec-factory` skill and its `references/api-research-library.md`; do not
  assume sibling plugin paths across versioned caches. If unavailable, report
  the missing reference and use an explicitly available canonical checkout,
  rather than pretending the installed skill contains it or auto-installing.
  Research directories provide candidates, not runtime availability or automatic
  approval. Require official-source checks, a recorded decision and validation
  plan; skip this research for unrelated tasks. Keep sources outside MCP/tool
  installation registries and preserve consent before external execution.

- `dev-environment-standard`: use cached environment `status` for required
  capabilities before execution. Route missing/broken prerequisites to targeted
  `prepare`/`repair`, then retry the original owner skill. Do not run full doctor
  for every task, infer connection from configuration, or install all tools.
  This capability does not own product implementation or DevOps.
  Use its persisted `platform_tools.selected_folder` and per-entry `eligible`
  routes; never infer native Windows support from WSL or repeat OS-choice
  questions on each task. Unvalidated entries require verification or an approved
  adapter. Context retrieval does not replace the ignored environment state.

- `devops-standard`: CI/CD, Docker/Compose, IaC, Kubernetes, GitOps, deploy,
  servers, cloud, observability, backup/restore, incidents and advanced
  Git/release strategy. Resolve its canonical skill, require a task and invoke
  it using the same execution contract and receipt. Basic status/diff/fetch,
  ordinary commit/push and PR work remain Harness/executor responsibilities.
  Security still owns scanners and security findings. Production/destructive
  actions require explicit target-specific human approval and rollback review.
  If Environment is available, route missing prerequisites to its selective
  prepare/repair, then return to DevOps. On bases without Environment, use
  the existing tool-state helper only; mark integration pending NOT VALIDATED.
  Do not synthesize another Environment plugin or MCP Library.

- `sdd-spec-factory`: required for COMPLEX work and for NORMAL work whose
  behavior is not already specified. TRIVIAL work uses the inline intent
  contract from the complexity gate.
- `ui-ux-standard`: **mandatory whenever there is UI** — new/changed screens,
  components, visual states, responsiveness, accessibility, or design-system
  adherence.
- `qa-testing-standard`: mandatory for changed behavior, bugfixes, user flows,
  APIs, business rules, persistent state, payments, tenancy, imports/exports,
  integrations, concurrency and regressions. QA planning may start before
  implementation; final QA depends on current executable artifacts. Docs-only
  or metadata-only work may record N/A with a reason. Never silently substitute
  the implementer's own tests for required independent QA.
- `security-standard`: **mandatory whenever the change touches** authentication,
  authorization, tokens, session, sensitive data, uploads, payments, or external
  integrations (also parsers, webhooks, infrastructure, privileged operations,
  tenant boundaries, secrets).
- Auxiliary CLIs/plugins: consultants only, for a real capability gap, after
  scoring and human approval (`references/continuous-improvement.md`).
