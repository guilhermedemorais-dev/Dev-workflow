# TASK-057 implementation, revision1

Approved execution list: platform-install-implementation in
docs/execution/TASK-057.json. Harness attested current equivalence and issue link.
Read implementation SKILL, Environment SKILL/operations/state-and-consent,
Minimal Code Gate, AGENTS, canonical script and docs/platform-tools.md.

Investigation confirmed the defect: platform_tools returned eligible per
entrypoint, but doctor probed registry tools and plan/install restored declared
dependencies without consulting that eligibility. A selected/approved component
could therefore reach an incompatible authored probe or installer.

Reused Environment platform catalog, dependency plan, specialist registry,
consent, private state and tool-state probe/install owners. Added one shared
authored eligibility helper, invoked before probe, when planning and immediately
before installation. It checks canonical command/interpreter script arguments,
not ID alone. Missing/corrupt/unvalidated/incompatible authored routes fail closed
with USER_ACTION_REQUIRED and platform/reason, even after user selection/approval.
Canonical script/reference inspection prevents a missing catalog from silently
reclassifying a packaged tool as an external dependency. Native Windows, Linux,
WSL and native macOS are reported distinctly; WSL uses the Linux catalog.

Developer commands with QA-only bundled Python:

- unittest discover -s tests -p test_platform_tool_routing.py -v:16tests OK,
  exit0,1.956s.
- unittest discover -s tests -p test_environment_bootstrap.py -q:69tests OK,
  exit0,17.119s.

Eight new behavioral cases cover the native/WSL platform matrix, unsupported Bash,
missing/invalid/unvalidated catalogs, redirected interpreter arguments, external
locked dependency preservation, no incompatible approved probe/install, and
catalog/registry drift immediately before installation and effective registry
overrides. Interpreter identity must match the catalog runtime, not merely point
to its script. Canonical and effective registry definitions are compared before
probe/install; changed verification command/arguments/distribution/policy requires
new review. Final environment.py SHA256:
C205506B276F67704C252139E935F213DB87306DB0B0F5902C9CB91E13E56151.
OS mocks test routing decisions;
they do not certify macOS, Linux integrations or arbitrary external dependencies.
Harness/independent QA own final full-suite acceptance.

Minimal Code Gate: EXTEND existing source owner and reuse compatible install
flow. No duplicate OS catalogs, installer, speculative dependency or source
deletion. External declared locked dependency semantics and owner approvals
remain unchanged; this explicitly does not certify every external package.
No automatic WSL activation, active notebook/cache mutation, secret acquisition,
merge or deployment. Developer code complete, independent approval pending.

Changed: environment.py, Environment SKILL, docs/platform-tools.md,
tests/test_platform_tool_routing.py, tests/test_environment_bootstrap.py and this
receipt. Parent owns CHANGELOG/README/task/Issue/publication. Runtime/API tokens:
NOT_AVAILABLE. Remote mutations by this executor:none.
