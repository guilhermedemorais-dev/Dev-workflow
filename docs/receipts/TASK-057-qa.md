# TASK-057 independent QA receipt

EXECUTION_RECEIPT: TASK-057, contract revision1, list platform-install-qa,
sector QA, phase validation, mode change-validation. QA_STATUS: PASS for the
approved platform-aware preparation changes and exact publication snapshot tested.
State COMPLETED for this checkpoint; Security/publication remain separate owners.

## Sources, invocation and scope

Harness delegated independent QA and attested Task/JSON normative equivalence.
Read docs/execution/TASK-057.json, its human mirror, docs/platform-tools.md,
Environment source and developer receipt; QA SKILL and test-strategy were read
fully in this execution context. Canonical Minimal Code Gate and Environment
ownership rules remain applicable. SKILL_RECEIPT: qa-testing-standard LOADED;
applied independent behavior execution, environment-failure classification,
mock-versus-real platform distinctions and exact-artifact regression validation.
No unrelated conditional source loaded and no product implementation by QA.

Publication includes TASK-055/056/057 source/tests/docs. Unpublished TASK-054
autonomous-acceptance changes were explicitly excluded. Therefore previous
709-test workspace runs are not a count for this publication artifact.

## Exact artifact and independently executed checks

Harness materialized Git tree f072018bc84c9456a295a508259785cdea4fc5da into:
`C:/Users/teste/Documents/Codex/2026-10-12/ch-2/outputs/release-candidate-20261014-213047`.
All final regression tests below ran THERE, not against the mutable worktree.
Stable external interpreter independently reported Python3.12.10:
`C:/Users/teste/AppData/Local/Programs/Python/Python312/python.exe`.

| Arguments / command | Result |
| --- | --- |
| -m unittest discover -s tests -p test_platform_tool_routing.py | 16 PASS, exit0, 2.400s |
| -m unittest discover -s tests | 693 PASS, exit0, 75.011s |
| git diff --check, canonical worktree | PASS, exit0 |

Final source SHA256 independently read in the tested snapshot:

- environment.py: C205506B276F67704C252139E935F213DB87306DB0B0F5902C9CB91E13E56151
- test_environment_bootstrap.py: 825C7061449C484DD9536D527E4D41ACD8282A1BA765CB85C30FF00D61F41F3B
- test_platform_tool_routing.py: E551C866FB6AEF425E9ACC09124FF4C470123CEF5553728A54E11A8CADFD8400

Initial artifact execution recorded 693 tests with two failures in 57.007s:
Git ignore checks returned128 because a Git archive has no .git directory.
Focused Environment execution likewise recorded one corresponding failure among
69 tests in19.793s. Classification ENVIRONMENT_FAILURE, not product failure.
With Harness authorization QA ran git init only inside the isolated snapshot,
without add/commit or product-file edits, and reran the entire suite. The final
693-test green run includes both original failing checks. No test oracle was
changed and the earlier failures were not omitted from this receipt.

## Behavior reviewed and validated

Positive/negative platform fixtures cover native Windows, Linux, WSL selecting
Linux and native macOS remaining unvalidated. They assert compatible authored
tools preserve the existing install path; missing, invalid, unvalidated or
unsupported authored entries receive USER_ACTION_REQUIRED without install/probe
effects, including explicit selection and approval. Unsupported Bash never becomes
an automatic WSL command. Registry command/argument alignment and interpreter
runtime must match the canonical catalog, preventing a Bash/Python mismatch.

Doctor, planning and execution recheck authored eligibility. Execution checks
fresh canonical/effective registry definitions and catalog drift rather than
trusting a previously approved stale report. Redirected verification commands,
effective owner-tool overrides and changed approval-bearing metadata are rejected.
Subprocess/probe/install sentinels verify blocked actions do not reach their
effectful owners. Project-declared external locked dependencies preserve their
existing owner policy instead of receiving invented platform certification.
State reuse and runtime/catalog/source drift regressions remain covered.

## Minimal-code and boundaries

One shared Environment helper extends existing catalog routing and install/probe
consent paths. It does not introduce duplicate installers/catalogs, new runtime
dependencies or speculative architecture. Existing tool-state and dependency-plan
owners are reused; no required protection or public behavior was deleted.
Tests validate concrete wrong-command/stale-state/no-side-effect cases.
No blocking functional finding remains in the tested publication scope.

Actual Windows-native lifecycle evidence from TASK-056 remains a dated baseline;
this routing change does not claim a fresh four-provider runtime proof. OS mocks
prove control flow, not real Linux/macOS integrations or all external packages.
Active notebook config, installed caches/runtimes, credentials and existing
processes were not modified by QA. No remote push/merge was performed by QA.
Next safe action: Harness reconcile Security and exact staged source equivalence,
then perform only the user-authorized commit/push. Merge remains unauthorized.
