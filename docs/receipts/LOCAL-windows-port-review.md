# LOCAL-windows-port independent QA and bounded security review

Task: LOCAL-windows-port. Contract revision: 3. Date: 2026-10-12.
Local-only authorization applies; remote Issue/PR/publication and human acceptance remain separate.

## Skill receipt and scope

SKILL_RECEIPT: qa-testing-standard and security-standard loaded completely;
references/test-strategy.md and references/review-pipeline.md applied. Sources:
the current local task/JSON, affected canonical helpers, runtime gateways,
catalogs, portable fixtures and executed logs. Review mode: change-validation
and bounded change security review, covering filesystem mutation, sanitized
state, subprocess launch, provider configuration and SEO bootstrap.

This reviewer independently executed the portable routing tests and initial
native REA launch tests earlier in the task. Final suite/guard results below
were inspected from other executors' logs; they are not represented as runs
performed by this reviewer. Later review was read-only, except this receipt.

## Functional validation evidence

- outputs/windows-port-final-suite.txt: 625 tests, OK, zero failures/errors/skips,
  133.557 seconds, native Windows Python.
- outputs/windows-port-linux-final-suite.txt: 625 tests, OK, 16 skips,
  211.160 seconds. Seven Windows-specific guard cases and nine Node-dependent
  cases were unavailable in this Linux test environment. These do not establish
  Linux Node integration behavior or macOS support.
- outputs/seo-final-guard-tests.txt: four tests, OK, no skips, 4.058 seconds.
  Includes checksum rejection, HTTP-only forwarding with existing content
  preservation, Windows runtime-junction rejection and unknown-option rejection.
- outputs/windows-file-guards.txt: six native guard cases, OK, no skips.
  Covers approved creation/replacement, new-file conflict, hash conflict,
  hardlink/junction rejection and exclusive file/root mutation protection.
- git diff --check passed during the review.

Comparison of recorded test identities in the original native baseline and
intermediate final log found no baseline test identity missing. Source review
confirmed POSIX shell fixtures were replaced with actual portable Python CLI
fixtures, rather than blanket skips or relaxed exit/output assertions. Permission
checks now inspect protected Windows DACLs instead of assuming POSIX chmod bits.

Real owned REA JavaScript evidence was independently inspected: exports total
and loadOrder and their source ranges match the synthetic artifact. This is
static inert analysis, not target execution or proof of arbitrary recovered
behavior. Native Ghidra PE analysis/decompilation and managed artifact analysis
are executor evidence reconciled by the Harness; they are not independent
runtime tests by this reviewer.

## Security conclusions

The initial absolute-child-path Windows writer was revised during review.
The final adapter opens each child relative to its checked parent HANDLE using
NtCreateFile, no-reparse options and single path components. Directory creation
is atomic; target file access is exclusive; reparse/hardlink checks and the
approved SHA256 precondition apply to the same opened file before content write.
Handles are retained during traversal and closed through ownership transfer or
finally cleanup. The POSIX no-follow branch remains present.

Windows state files receive a protected owner-rights/SYSTEM DACL before JSON
content is written. Existing secret rejection and sanitized state/log behavior
remain in place. REA subprocess calls use direct JavaScript entrypoints through
Node with shell:false, preserving literal argument boundaries. Local provider
configuration admits only existing absolute GHIDRA_INSTALL_DIR/JAVA_HOME
directories; explicit process environment values take precedence. NODE_OPTIONS
injection through provider JSON is rejected by an executed regression case.

SEO bootstrap no longer deletes an existing runtime unconditionally, forwards
HTTP-only selection and rejects symlinks and Windows reparse targets. The
review-requested junction check now has passing native regression evidence.

No unresolved blocking finding remains in the examined change. This is bounded
assurance, not an exhaustive repository/dependency audit, production approval
or certification of every external provider.

## Sector disposition and limits

QA_STATUS: PASS for the approved local changed-tool scope and executed regression
evidence, with Linux Node and macOS limits stated above.
SECURITY_STATUS: PASS for reviewed CLI/filesystem/state/process trust boundaries.
Banco: N/A. API/Backend: reviewed CLI helpers. Frontend/UI: N/A.
Infra/DevOps: local file governance reviewed; remote infrastructure excluded.
Dependencias/Supply Chain: local bootstrap/pinning/launch boundaries reviewed;
no exhaustive dependency advisory audit claimed.

Installed plugin refresh and configuration preservation are Harness execution
evidence, not an action performed by this reviewer. SEO HTTP readiness is
distinct from optional browser readiness: installed probe exit 1/WARN with
http_ready=true must not be described as fully healthy browser capability.
Remote governance, macOS execution and human acceptance remain pending.

Next safe action: Harness reconciles revision-3 receipts, installed-runtime
evidence and exact README/CHANGELOG support claims before local delivery.
