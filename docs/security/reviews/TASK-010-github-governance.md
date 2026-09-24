# Security review: TASK-010 GitHub governance

## Executive decision

- Date: 2026-09-24; baseline `44718fe5faa49cdfde790a51ae6e63ce6c18c050`.
- Mode: Change Review; risk HIGH, privileged remote configuration and local writes.
- SECURITY_STATUS: PASS for the reviewed local change. One fixed finding, zero
  remaining confirmed security findings; remote-integration exclusions below.
- Final helper SHA-256:
  `7fa330927f7136bdfda0d34c6da98ad5bc1bf1be60c83c9b55d36850cb32c46f`.
- This reviewer did not author the helper or tests, but authored its DevOps
  reference/registry integration. Independence applies to executable-code review;
  documentation needs the Harness/QA cross-check as well.

## Authorization and scope

Approved TASK-010 local code, config/template and test review. Source of truth:
`docs/execution/TASK-010.json`, module-spec and validation-rules under
`docs/specs/github-governance/`. Allowed proof: static tracing, synthetic local
fixtures and fake GitHub calls. No real credentials, remote mutations, production
tests, scanner installation or external vulnerability publication.

## SKILL_RECEIPT

- skill: security-standard
- path: plugins/security-standard/skills/security-standard/SKILL.md
- references_loaded: review-pipeline.md, stack-profiles.md, finding-standard.md,
  false-positive-validation.md, coverage-model.md, report-template.md in that
  skill's references directory, all read completely.
- applied_rules: source-to-sink validation; false-positive checklist before
  confirmation; bounded local proof; no fabricated execution or external finding.
- status: LOADED

## System and threat summary

Python stdlib CLI delegates authenticated GitHub REST/GraphQL to existing `gh`.
Assets: authorized repository/settings/Project, local governed files, credentials
held by gh, approval intent and integrity of readiness evidence.
Actors: developer/approver; agent operating with developer's gh authority;
repository contributor controlling local project/config inputs; remote API
responses. Malicious local executable/PATH replacement is an OS trust assumption,
not automatically a defect in this helper.

Flows to review end-to-end:

1. Config/CLI → schema/target/path validation → desired plan → GitHub destinations.
2. Proposal/evidence → target/revision/hash binding → confirmation → reconstructed
   allowlisted actions → local writes or remote mutations.
3. Local stack manifests/files → generated YAML and diff → reviewed write.
4. API result/error → schema normalization → report/log sanitization.
5. Fresh local/remote state + manual evidence → required gates → readiness.

High-impact abuses: target substitution, stale approval replay, arbitrary command
or CI injection, filesystem escape, secret reflection and false READY/enforcement.
No public web service, product database or rendered UI exists in this scope.

## Coverage ledger

| Surface | Layer | Owner | Status | Evidence / next action |
| --- | --- | --- | --- | --- |
| Config, host/repo, local paths | Infra/DevOps | Security | REVIEWED | PASS within local scope: strict schema; traversal/symlink negatives; descriptor-relative writes, hardlink rejection and write-time hash |
| Proposal and confirmation | Infra/DevOps | Security | REVIEWED | PASS within local scope: reconstructed allowlist, confirmation required, target/drift/tampering negatives |
| gh subprocess, REST/GraphQL | Infra/DevOps | Security | REVIEWED | PASS within local scope: argv without shell, fixed host, read-only guards, sanitized failures, fake-gh CLI |
| CI/template generation | Supply Chain | Security | REVIEWED | PASS within local scope: existing commands only, observed runtime inputs, full SHA action pins, contents read permission |
| API/error/output handling | Privacy/Observability | Security | REVIEWED | PASS within local scope: SEC-2026-010 fixed, five independent canaries and malformed input/API tests |
| Readiness/manual evidence | Infra/DevOps | Security | REVIEWED | PASS within local scope: required governance files always hashed/tracked, including generation disabled; unknown-rule and grouping negatives; narrow plan fallback |
| Product database/API/UI | Banco/API/Frontend | N/A | NOT_APPLICABLE | Operational CLI only |
| Real GitHub enforcement/auth | Infra/DevOps | DevOps/user | DEFERRED | Future explicitly authorized disposable-repo rehearsal |

## Findings and validation backlog

### SEC-2026-010: sensitive existing content reflected into proposal

- Status: FIXED, formerly CONFIRMED MEDIUM, confidence HIGH, confidentiality / sensitive logging
  (CWE-532). Boundary: existing repository content to public proposal/log output.
- Reviewed helper SHA-256:
  `f1995e8c2132a16410ca8c6cea6d0957a66e99e3f3f0a4b8187166c5c2eed4f6`.
- Source and actor: a legitimate operator runs `propose` against an existing
  repository whose governed document contains sensitive text. No malicious
  GitHub response, stolen credential or `apply` approval is required.
- Reachable path: `make_proposal` reads existing governed files, passes their
  complete previous content into `difflib.unified_diff`, includes that diff in
  actions, and the CLI prints the full JSON proposal. At this revision these
  operations are around lines 467–476 and 673 of the helper.
- Missing control: desired-input validation rejects token-like strings, but old
  file content never passes that control or output redaction.
- Safe independent reproduction: temporary `CONTRIBUTING.md`, one fake marker
  formed from `ghp_` plus 40 `Z` characters, ordinary valid desired config and a
  synthetic observed snapshot. `make_proposal` produced JSON containing the
  marker verbatim in `actions[].diff` for `CONTRIBUTING.md`. Output recorded only
  the boolean result (`true`), affected path and helper hash, not real secrets.
- Security impact and preconditions: an existing secret can propagate into
  terminal logs, proposal artifacts or reviewer/agent context where the user
  expected sanitized output. The secret must already be in a governed file;
  this does not imply arbitrary file reads or access escalation.
- Counterevidence / false-positive validation: no real token or external transfer
  was used; the proposal is legitimately intended to show changes, but the
  sanitization contract explicitly excludes secret disclosure. Input-token
  rejection does not protect this old-content path. Read-only execution and
  approval hashing do not prevent disclosure before application.
- Required correction: reject sensitive content with a sanitized error or
  deterministically redact proposal display. Preserve approval integrity by
  binding the actual bytes through the existing snapshot hash, not by silently
  ignoring changed input. Add a regression asserting no synthetic secret in
  public JSON/stderr and safe application behavior.
- Retest: helper SHA-256
  `ab47f472fef917ca8324a1c3a5c0fec7648e789e0e2d5d0f310479ad45c3ac1d`
  rejects sensitive old material before constructing the diff and guards the
  complete proposal/public output, including preserved remote fields.
  Four independent synthetic probes (GitHub-token prefix, password assignment,
  private-key header and Bearer credential) all returned sanitized blocking
  errors without the fixture value. Snapshot binding remains intact.
  Pattern detection is bounded, not proof that every arbitrary secret can be
  recognized; operators must still inspect proposals before sharing them.

Readiness/manual-evidence and effective-rules candidates were consolidated
by Harness with functional QA and author. Final code blocks unknown-rule
exceptions, observed wrong grouping and unpublished state, checks stale-review
and thread-resolution requirements and flags applicable bypass actors. These
acceptance gaps were corrected and were not counted as additional confirmed
security findings without independent security-impact validation.

## Validation evidence

An independent temporary-fixture secret-reflection probe reproduced SEC-2026-010.
The corrected implementation passed four independent sensitive-material probes
and two malformed `ci`/`rules` array probes. At final RC the four recognizable
markers were repeated and a fifth arbitrary unrecognizable canary was verified
absent from proposal JSON, because all previous-file lines are omitted. Public
review uses the replacement and previous-byte hash; the operator must inspect
the original locally before approval.

Final command: `python3 -m unittest discover -s tests -p test_github_governance.py -q`
returned 47 tests PASS in 6.566 seconds on final RC. All five independent canary
probes were repeated successfully on this final hash. The suite includes real CLI subprocesses
with fake gh, not real GitHub authentication. It covers proposal tampering/staleness, missing
approval, read-only guards, traversal/symlinks, partial apply, publication drift,
unknown-rule exceptions and raw credential error suppression.
The final helper hash above was checked after execution. `git diff --check`
returned zero. No production target, real credential, real API mutation or CI
service execution was used. The first consolidated correction cycle resolved
the confirmed finding; a second corrected QA Q05's ignored-file publication
coverage. Regression 46 verifies disabled generation cannot exclude required
files from hashing and publication validation. Regression 47 checks unsupported
filesystem primitives block before any application mutation.

## Release gate

QA_STATUS belongs to the independent QA owner; not assessed here.
SECURITY_STATUS is PASS for this exact helper snapshot and local review scope.
Remote integration is NOT VALIDATED: actual scopes, ruleset enforcement, Project
automation and CI service behavior require the separately authorized rehearsal.
Manual evidence is a trusted human observation, not a cryptographic attestation
or independently fetched proof. Concurrent malicious modification by the same
OS principal is outside the helper's isolation boundary; reviewed path/hash
guards reduce accidental overwrite but do not create an OS security sandbox.
Filesystem mutation was validated on Linux/POSIX only. Required descriptor/
no-follow primitives are checked before apply; Windows is not homologated.
No production authorization or user acceptance is implied by this report.
