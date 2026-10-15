# TASK-055 QA planning

Contract revision1, list_id native-qa. Phase planning, QA_STATUS NOT_VALIDATED.
SKILL_RECEIPT: qa-testing-standard loaded completely from installed
`C:/Users/teste/.codex/plugins/cache/guilherme-dev-workflow/qa-testing-standard/0.1.0/skills/qa-testing-standard/SKILL.md`;
reference test-strategy.md loaded for case selection and run interpretation.
Applied rules: independent QA, no product fixes, no relaxed oracle, evidence-bounded
claims, no active config migration or external account operation.

Inputs: docs/execution/TASK-055.json revision1 native-qa slice; required sources
loaded, Harness local normative-equivalence attestation in canonical contract.
Parent requested planning before implementation readiness; validation awaits it.

QA_GUARDRAILS: isolated synthetic config only; no live config/env/credentials writes,
PATH changes, WSL lifecycle control or publication. Runtime proof belongs to the
native-runtime list and must be reviewed separately from structural unit results.

TEST_SCENARIOS:
- QA01 Windows-native/WSL/Linux detection and explicit selection; no automatic WSL fallback.
- QA02 stable native Node/npm/browser discovery, matching runtime, spaces in paths;
  transient/Codex-internal paths rejected or flagged, missing prerequisite explicit.
- QA03 own native executable/entrypoint commands and platform-specific arguments;
  no /home or wsl.exe in Windows-native generated launch.
- QA04 global/plugin/project identities and aliases, disabled entries, selected
  integrations only, idempotent generation without redundant registration.
- QA05 env and argument preservation, no secret values printed or stored in reports.
- QA06 explicit apply authorization, source fingerprint binding, private backup,
  stale-plan rejection, rollback and refusal after unrelated edits.
- QA07 existing Linux/WSL bootstrap behavior retained; full regression suite.
- QA08 real Windows10 evidence: edition/build, versions, MCP initialize/tools/list
  plus representative operation, owned-process topology, comparable memory scope;
  missing proof NOT_VALIDATED, existing Linux consumption not falsely attributed.

REGRESSION_TARGETS: environment bootstrap/config/install callers; native adapter;
existing655-test baseline plus new meaningful behavioral cases; diff whitespace.
VALIDATION_REQUIREMENTS: parent implementation ready; changed code and tests
reviewed before run; commands, exit codes and real counts captured. Security remains
separate owner. Unit PASS does not close absent native handshake/operation proof.
