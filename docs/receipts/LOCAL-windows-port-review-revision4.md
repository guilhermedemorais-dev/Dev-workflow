# LOCAL-windows-port revision 4 independent review

Date: 2026-10-12 (user timezone). Contract: LOCAL-windows-port revision 4.
Scope: supplemental portable Cutter/Rizin, default-Windows text encoding and
version-token detection. Revision-3 filesystem, DACL, REA and SEO conclusions
remain recorded in LOCAL-windows-port-review.md. No new penetration experiments,
third-party targets, publication or product-code changes were performed by this
reviewer. This receipt is the only new artifact written in this review.

SKILL_RECEIPT: qa-testing-standard/security-standard and previously loaded
test-strategy/review-pipeline references remain applicable. Current task/JSON,
tool-registry, runtime README, affected helper/test diffs and executor logs read.

## Evidence interpreted independently

- outputs/windows-default-encoding-suite.txt: 626 tests, OK, no failures/errors
  or skips, 69.682 seconds. Executor reports native default encoding cp1252,
  UTF8 mode 0, without a forced UTF8 environment. An earlier 625-test default
  encoding run also passed; the new version-suffix test accounts for the increment.
- outputs/windows-default-encoding-profile.json confirms utf8_mode=0,
  default_text_encoding=cp1252 and PYTHONUTF8=null. The associated scoped helper log,
  windows-default-encoding-tool-state.txt, records 25 tests OK (5.276 seconds).
- Prior revision-3 Linux evidence: 625 tests, OK, 16 platform/runtime-specific
  skips. This reviewer does not claim a revision-4 626-test Linux execution.
- outputs/linux-revision4-tool-state-tests.txt: affected Linux helper scope,
  25 tests, OK, including the new version-suffix regression.
- outputs/cutter-windows-version.txt: exit 0, Cutter 2.5.0-HEAD-a6f6ad7.
- outputs/rizin-windows-owned-analysis.txt: exit 0, owned x64 PE entrypoint
  disassembly contains mov eax,0x2a and ret.
- outputs/rizin-windows-owned-decompile.txt: exit 0, pseudocode return 0x2a.
- outputs/cutter-rizin-state-validation.txt: detect plus two resolves for each
  tool return installed status, absolute executable, provenance and exact version;
  repeated resolves preserve last_verified, showing the cached route is reused.
- git diff --check passed during this revision review.

Cutter official portable archive provenance/checksum is recorded by the executor
in LOCAL-windows-port-reverse-cutter.md: v2.5.0 Windows x86_64, SHA256
a04154a03a392dbf5886a629938582f7d23a93636fa0611c3e1c34905b197e69,
matched release metadata before extraction. Rizin 0.9.1 is bundled there, not a
second standalone installation. Owned fixture hash remains
6d3eea26039d6f7451a1af38995e334a664996330c8d36fb34316ae594014a3d.
Archive download/extraction and runtime executions were performed by the
implementation executor; this reviewer inspected their receipts and outputs.

## Source and assertion review

Registry entries use generic cutter/rizin commands and public upstream provenance;
no generated machine-specific installation paths are embedded in distributable
registry content. Both are explicitly supplemental CLI/GUI tools, not REA provider
IDs. Runtime README distinguishes the verified executable --version command from
unvalidated GUI behavior. No interactive/offscreen GUI session is certified.

Rizin analysis/decompilation uses the owned artifact statically, with the bundled
rz-ghidra Sleigh directory explicitly selected. It does not invoke target execution
or the debugger. Pseudocode 42 matches the prior owned fixture evidence; this does
not establish reconstruction of arbitrary applications or all executable formats.

UTF8 test changes specify encoding on UTF8 repository/fixture reads and writes,
including embedded fake-gh code. Assertions, error classifications and baseline
tests are retained; no blanket skip or forced process UTF8 mode masks the defect.

The helper now accepts bounded prerelease/build version tokens such as official
2.5.0-HEAD-a6f6ad7 and rc.1+build.7. It still stores only the matched version token,
not arbitrary command output. The new test includes a synthetic secret in the
surrounding output and verifies it is not persisted. Exact required-version and
executable/PATH identity validation remain present; the supplemental flow does
not silently bypass them or mutate global PATH. Windows persistent-state DACL
handling remains protected; handle identity is checked when obtaining the ACL
write handle.

## Disposition

QA_STATUS: PASS bounded to revision-4 Windows scope and inspected runtime evidence.
SECURITY_STATUS: PASS for changed registry/version/encoding boundaries; no
unresolved blocking finding in the inspected change. This is not a new exhaustive
dependency audit or cross-platform Cutter/Rizin certification.

Database/UI: N/A. Backend CLI and local state: reviewed. Remote infrastructure:
excluded. Supply chain: official portable provenance and local install evidence
reviewed; provider binaries remain outside distributable plugin content.

Limits: Cutter GUI unvalidated; Linux/macOS supplemental runtimes unvalidated;
revision-4 Linux full-suite count not independently established here; remote
GitHub authentication/publication and human acceptance remain pending. Earlier
SEO HTTP readiness does not certify optional browser capability.

Next safe action: Harness reconciles this receipt with final revision-4 executor
receipts, installed-cache evidence and truthful support/version documentation.
