# TASK-057: Platform-aware preparation and publication

Revision1. User authorizes committing/pushing plugin changes and requires the
installer to select only compatible tools, explain unavailable/unsupported ones
and leave solutions to the user. Existing Windows native lifecycle work retained.

Issue: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/54,
observed updated_at2026-10-15T00:27:52Z. Harness attests Issue/local contract
revision1 equivalence. Publication uses authenticated GitHub connector because
the local Git HTTPS credential helper is not authenticated.

Scope: close authored-tool platform eligibility gaps in Environment doctor,
planning and execution before probing/installing. Detect Windows native, Linux,
WSL Linux and macOS; use the selected validated catalog, fail closed on missing,
unsupported or unvalidated authored tools. No automatic WSL, tool porting or
installation merely because Python exists. Preserve external project-locked
dependency preparation and existing permission policies, documenting its distinct
package-manager compatibility boundary. Missing external platform proof requires
specialist review rather than claiming broad certification.

Acceptance: incompatible/missing/unvalidated authored tool never executes or
installs, clear warning/action retained; compatible selected authored paths
continue; WSL remains Linux, macOS unknown stays not validated; no catalog side
effects; state reused only until relevant drift. Regression tests, independent QA
and Security. Publish only source/tests/docs, no machine configs, credentials or
private backups. Commit/push current branch authorized, merge not authorized.

Harness attests normative equivalence with contract revision1. GitHub link will
be recorded when authenticated remote capability is verified. Existing local
TASK054055056 historical approvals/receipts remain historical, not rewritten as
past human approval or main publication. Technical acceptance: QA693 tests in the
exact publication candidate, Security85 targeted tests and frozen-source review.
Commit/push authorized, remote SHA verification pending at receipt creation.
See docs/receipts/TASK-057-harness.md. Main merge remains unauthorized.
