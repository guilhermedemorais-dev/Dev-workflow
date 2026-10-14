# EXECUTION_RECEIPT: native Windows tools

Task LOCAL-windows-port, contract revision 4, list windows-tools. Date 2026-10-12.
Local authorization: direct user request to fix native Windows defects, prior
explicit GitHub-disconnected exception preserved. Branch feat/platform-tool-routing.
Status VALIDATING. Remote Issue/PR/publication pending; no install/push/merge.

## SKILL_RECEIPT and context

dev-implementation-standard read completely earlier in this uninterrupted task;
Task and revision1/revision3/revision4 local contracts read for authorized scope.
AGENTS, README, existing baseline/final logs, prior platform contract, tool helper,
governance helper, Environment helper and their related tests inspected.
Microsoft primary references for CreateFile, NtCreateFile and file security were
checked; Windows native API requirements remain Windows10+ for this local test.
Only implementation/developer evidence is attested; independent QA/security and
Harness final reconciliation remain pending.

## REUSE_INVENTORY / MINIMAL_CODE_GATE

EXTEND existing helpers and APIs. Most failures came from fixtures executing
POSIX shell scripts or asserting Unix modes on Windows. Replace fixtures with
real Python executable commands via Python's installed pip/distlib console
launcher on Windows and direct interpreter shebang on Linux, preserving actual
execution, literal argument, cwd, exit-code, cache and security assertions.
No shell evaluation or blanket skips of failing tests introduced.
Windows tests require pip's already-installed distlib launcher; no test installer.

The existing POSIX no-follow directory-descriptor path remains unchanged.
Windows governance uses an OS adapter with checked directory HANDLE-relative
NtCreateFile children, OBJ_DONT_REPARSE, OPEN_REPARSE_POINT, atomic creation,
reparse/hardlink rejection and exclusive final file plus approved hash.
Initial absolute child-path traversal was rejected during review and replaced,
because pinned directories alone do not prevent junction attribute changes.

State privacy keeps POSIX0600 and adds protected Windows OwnerRights/SYSTEM DACL.
The original and reopened WRITE_DAC handles must have identical FileIdInfo;
reparse objects are rejected before setting security on the exact handle.
Two current consumers: tool-state atomic writes and Environment atomic writes.
Privacy tests inspect actual DACL rather than weakening to file existence.

Other portability changes: canonical executable case resolution, current Python
interpreter detection, platform-supported secure-write capability test, and
generated dependency exclusions from normative fingerprint/fixtures. Authored
scripts, locks and catalogs remain watched; real runtime failures remain separately
checked by owner caches. Helper modules without executable shebang are excluded
from authored entrypoint inventory, not added as runnable tools.

## Executed evidence so far

Native Windows10/Python3.12 UTF-8 explicit:
- skill-owned tools: 24 tests PASS.
- DevOps tools: 20 tests PASS.
- GitHub governance: 47 tests PASS, including real isolated fake-gh CLI apply.
- New native Windows file guards: 6 tests PASS, temporary owned files only.
- Environment integration: 4 tests PASS; Environment bootstrap: 65 tests PASS.
- Platform routing: 12 tests PASS, including matching Windows evidence status
  and generated-dependency fingerprint boundaries.
- SEO bootstrap guards: 4 tests PASS, no network/install in fixture tests,
  including native existing/dangling-junction rejection before setup.
- Full Linux/native Windows regression: pending final Harness command results.

Native Windows guards verify creation, approved existing replacement, collision,
concurrent hash, hardlinks, junction containment/no external creation, exclusive
file and pinned root against concurrent write/rename. Platform-specific guard
class is skipped on Linux because the Windows adapter is not executable there;
existing cross-platform behavior tests remain active.

## Authored SEO runtime, revision3

SEO SKILL and beyondseo-integration reference read for the runtime boundary.
The bundled setup supports --http-only, but our wrapper did not expose/forward
it and unconditionally deleted existing runtime. Wrapper now forwards explicit
--http-only and preserves an existing runtime for normal setup validation.
Three tests verify option forwarding/preservation, checksum failure and unknown
option refusal without installs or network.

Actual scoped Windows bootstrap --http-only succeeded using verified vendored
BeyondSEO2.9.1, SHA256 e9ab0e9e3a2ef46a9e3b3b3e4699b988fa256dcac91ef5e3539b49b850ac5010.
Runtime created only at plugins/seo-standard/runtime/.runtime. Real gateway probe
exit1: Python3.12.14, http_ready true (dependency availability), browser_ready false,
pdf_ready true (dependency availability), status WARN for untested optional checks.
No browser dependency/binary installed, no crawl or target network validation.
Evidence: chat outputs/seo-windows-bootstrap.txt and seo-windows-probe.json.
Correction: the initial source probe report incorrectly treated the surrounding
PowerShell pipeline's successful exit as the native gateway exit. Explicit
LASTEXITCODE capture on the source and installed-cache execution confirms exit1
with WARN, not a fully healthy runtime. Missing optional Playwright/browser
checks have blocks_crawling false in HTTP mode. No target reachability or
render/export execution was established; optional browser installation remains
outside approved scope. Bootstrap --http-only itself returned exit0 because
the upstream setup gate requires HTTP dependencies, not the optional browser.

## Revision4 native default encoding and Cutter version detection

Native Windows defaults to cp1252 in this Python runtime with UTF8 mode 0.
The earlier successful full suite used UTF8 mode and therefore did not establish
default-encoding portability. A targeted run exposed a UnicodeDecodeError in
the UTF8 task template read. Sixteen test files now explicitly read/write UTF8
repository text and fixtures; no assertions or baseline tests were removed or
skipped. The initial full 625-test rerun passed natively with PYTHONUTF8 removed,
no -X utf8 flag and scoped Node PATH. Log: outputs/windows-default-encoding-suite.txt.

The official Cutter version 2.5.0-HEAD-a6f6ad7 was also rejected by the old
numeric-only token regex. Extraction now accepts bounded prerelease/build
identifiers, maximum total token80 characters, while preserving the expected
executable/cache checks. A real executable fixture tests official-style HEAD
and rc/build versions and excludes accompanying synthetic secret/log text from
state. The 25-test tool-state subset passed under native default cp1252.
Final full626 native Windows run PASS, 69.682s, native unittest exit0. No -X utf8
flag, PYTHONUTF8 absent, actual UTF8 mode0/default cp1252 confirmed in
outputs/windows-default-encoding-profile.json. Full suite evidence:
outputs/windows-default-encoding-suite.txt. Scoped25 test-state evidence:
outputs/windows-default-encoding-tool-state.txt, PASS5.276s/nativeexit0.
Linux regression for the new encoding/semver revision remains owned by Harness.

## Changed surface / limits

tool-state.py, github_governance.py, environment.py; tests portable_executable.py,
test_skill_owned_tools.py, test_devops_tools.py, test_environment_bootstrap.py,
test_environment_devops_integration.py, test_github_governance.py,
test_platform_tool_routing.py, test_windows_file_guards.py; this receipt.
Also bootstrap.py under SEO runtime and tests/test_seo_runtime_bootstrap.py.
Reverse runtime and support/release docs handled by separate owners. External
third-party .cmd validators are not universally certified by these fixtures.
No real infrastructure or remote GitHub mutation. Issue report NOT PUBLISHED,
connector disconnected under explicit local exception. code_changed yes.
input_tokens/output_tokens/total_tokens/measurement_source: NOT_AVAILABLE.
