# CINEMATIC-UI-001: cinematic specialization inside UI/UX

Contract revision: 1. Owner authorized integration in conversation; no merge/deploy.

## schema_version

2

## contract_revision

1

## task_id

CINEMATIC-UI-001

## human_task

- **representation**: local_mirror
- **issue_url**: None
- **local_mirror**: docs/tasks/CINEMATIC-UI-001.md
- **normative_equivalence**: This mirror is generated from the same revision JSON; remote Issue publication is pending, never fabricated.

## summary

Integrate cinematic specialization within existing UI/UX

## goal

Make approved cinematic work discoverable inside the existing UI/UX owner without loose duplicate plugin or new sector.

## current_state

UI/UX is integrated, cinematic skill exists only outside this repository.

## expected_result

Nested cinematic skill, conditional routing, validated media helpers and V2 route where applicable.

## scope

Preserve cinematic resources inside existing UI/UX plugin; Conditional workflow, implementation and SDD handoffs; Office V2 opt-in ux-cinematic capability where applicable; Structural and deterministic media-helper validation; Register the three authored media helpers in existing OS catalogs without installing dependencies or claiming untested OS support

## out_of_scope

Standalone Work skill deletion (handled separately); New top-level plugin or sector; GSAP/MCP/FFmpeg installation; Product page implementation, merge or deploy

## allowed_paths

plugins/ui-ux-standard/**; plugins/dev-workflow-standard/skills/dev-workflow-standard/**; plugins/dev-implementation-standard/skills/dev-implementation-standard/SKILL.md; plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md; README.md; tests/test_cinematic_integration.py; docs/tasks/CINEMATIC-UI-001.md; docs/execution/CINEMATIC-UI-001.json; docs/reports/CINEMATIC-UI-001.md; plugins/dev-environment-standard/Tools (Linux)/catalog.json; plugins/dev-environment-standard/Tools (Windows)/catalog.json; plugins/dev-environment-standard/Tools (macOS)/catalog.json; tests/test_platform_tool_routing.py

## protected_paths

main branch; credentials; runtime-state; unrelated skills

## requirements

-
  - **id**: REQ-01
  - **description**: Nested cinematic skill ships its references, scripts and assets under UI/UX
  - **source**: Owner explicit request in conversation, 2026-10-25
  - **priority**: MUST
-
  - **id**: REQ-02
  - **description**: Only cinematic scopes trigger loading; existing UI/UX, implementation, QA and Security boundaries remain
  - **source**: Owner explicit request in conversation, 2026-10-25
  - **priority**: MUST
-
  - **id**: REQ-03
  - **description**: Office V2 ux-design plan can select ux-cinematic with global/UX prerequisites
  - **source**: Derived acceptance from existing repository routing/preservation policies and cinematic integration/media-helper contract, not a verbatim owner request.
  - **priority**: MUST
-
  - **id**: REQ-04
  - **description**: Deterministic frame manifests and negative gap/budget checks run without production media
  - **source**: Derived acceptance from existing repository routing/preservation policies and cinematic integration/media-helper contract, not a verbatim owner request.
  - **priority**: MUST

## business_rules

None.

## specs

docs/tasks/CINEMATIC-UI-001.md

## docs

AGENTS.md; docs/workflow-pipeline.md

## references

-
  - **id**: REF-CINEMATIC
  - **title**: Canonical cinematic integration
  - **project_path**: plugins/ui-ux-standard/skills/cinematic-web-standard/references/dev-workflow-integration.md
  - **purpose**: Owner boundaries and nested placement
  - **applies_to**:
    MT-01

## design

- **applicability**: N/A
- **guide**: N/A
- **tokens**: N/A
- **visual_references**:
  None.
- **component_library**: N/A
- **mockup**: N/A
- **reason_if_na**: Skill packaging/routing; no product UI created or changed.

## microtasks

-
  - **id**: MT-01
  - **title**: Integrate UI cinematic capability
  - **summary**: Package and route approved specialization with regression evidence
  - **owner_skill**: dev-implementation-standard
  - **owner_plugin**: dev-implementation-standard
  - **capability**: implementation
  - **preferred_tool**: repository-native-tooling
  - **depends_on**:
    None.
  - **references**:
    REF-CINEMATIC
  - **allowed_paths**:
    Same approved allowed_paths as the global allowed_paths section above (all entries inherited).
  - **checklist**:
    Preserve source bundle; Add conditional routing; Run structural and media-helper checks
  - **deliverables**:
    Nested skill and integration; Validation evidence
  - **completion_condition**: Required checks pass or limitations explicitly recorded
  - **validator**: qa-testing-standard
-
  - **id**: MT-02
  - **title**: Independently review cinematic packaging and routing
  - **summary**: Read-only independent structural/media-helper review
  - **owner_skill**: qa-testing-standard
  - **owner_plugin**: qa-testing-standard
  - **capability**: qa
  - **preferred_tool**: repository-native-tooling
  - **depends_on**:
    MT-01
  - **references**:
    REF-CINEMATIC
  - **allowed_paths**:
    docs/reports/CINEMATIC-UI-001.md
  - **checklist**:
    Inspect actual diff and routing; Run targeted regression checks; Record defects and validation limits
  - **deliverables**:
    Independent review evidence
  - **completion_condition**: Reviewer reports executed checks and disposition without self-certifying UI or production
  - **validator**: dev-workflow-standard

## execution_lists

-
  - **list_id**: LIST-IMPLEMENT
  - **owner_skill**: dev-implementation-standard
  - **phase**: implementation
  - **microtask_ids**:
    MT-01
  - **depends_on**:
    None.
  - **references**:
    REF-CINEMATIC
  - **required_tests**:
    TEST-REGRESSION; TEST-DIFF
  - **acceptance_criteria**:
    AC-01; AC-02; AC-03; AC-04
  - **checklist**:
    -
      - **instruction**: Preserve source bundle
    -
      - **instruction**: Add conditional routing
    -
      - **instruction**: Run structural and media-helper checks
-
  - **list_id**: LIST-QA
  - **owner_skill**: qa-testing-standard
  - **phase**: validation
  - **microtask_ids**:
    MT-02
  - **depends_on**:
    MT-01
  - **references**:
    REF-CINEMATIC
  - **required_tests**:
    TEST-REGRESSION; TEST-DIFF
  - **acceptance_criteria**:
    AC-01; AC-02; AC-03; AC-04
  - **checklist**:
    -
      - **instruction**: Inspect actual diff and routing
    -
      - **instruction**: Run targeted regression checks
    -
      - **instruction**: Record defects and validation limits

## sectors

- **database**:
  - **owner**: dev-implementation-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **backend**:
  - **owner**: dev-implementation-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **frontend**:
  - **owner**: dev-implementation-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **ui_ux**:
  - **owner**: ui-ux-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **qa**:
  - **owner**: qa-testing-standard
  - **applicability**: REQUIRED
  - **reason**: Independent source-package/routing and media-helper behavior review; no product/browser QA claim.
  - **depends_on**:
    documentation
  - **microtasks**:
    MT-02
  - **required_sources**:
    REF-CINEMATIC
  - **required_validations**:
    TEST-REGRESSION; TEST-DIFF
  - **planning_depends_on**:
    None.
- **security**:
  - **owner**: security-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **devops**:
  - **owner**: devops-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **observability**:
  - **owner**: devops-standard
  - **applicability**: N/A
  - **reason**: No product/runtime/security/infrastructure surface changed; copied local helpers run only on synthetic fixtures.
  - **depends_on**:
    None.
  - **microtasks**:
    None.
  - **required_sources**:
    None.
  - **required_validations**:
    None.
  - **planning_depends_on**:
    None.
- **documentation**:
  - **owner**: dev-implementation-standard
  - **applicability**: REQUIRED
  - **reason**: Approved packaging and conditional routing change
  - **depends_on**:
    None.
  - **microtasks**:
    MT-01
  - **required_sources**:
    REF-CINEMATIC
  - **required_validations**:
    TEST-REGRESSION; TEST-DIFF
  - **planning_depends_on**:
    None.
- **harness**:
  - **owner**: dev-workflow-standard
  - **applicability**: REQUIRED
  - **reason**: Approved packaging and conditional routing change
  - **depends_on**:
    documentation; qa
  - **microtasks**:
    MT-01
  - **required_sources**:
    REF-CINEMATIC
  - **required_validations**:
    TEST-REGRESSION; TEST-DIFF
  - **planning_depends_on**:
    None.

## pipeline

owner_scope_approved; bounded_source_integration; executor_tests; independent_packaging_routing_review; reviewable_pull_request; human_acceptance_merge_separate

## gates

- **scope**: Owner explicitly authorized integration inside existing UI/UX on 2026-10-25
- **final_acceptance**: Human PR review pending
- **merge_deploy**: Not authorized

## required_tests

-
  - **id**: TEST-REGRESSION
  - **type**: regression
  - **command**: python -m unittest discover -s tests -v
  - **expected**: No introduced failures
-
  - **id**: TEST-DIFF
  - **type**: structural
  - **command**: git diff --check
  - **expected**: No whitespace errors

## acceptance_criteria

-
  - **id**: AC-01
  - **description**: Nested cinematic skill ships its references, scripts and assets under UI/UX
  - **validation**: TEST-REGRESSION
-
  - **id**: AC-02
  - **description**: Only cinematic scopes trigger loading; existing UI/UX, implementation, QA and Security boundaries remain
  - **validation**: TEST-REGRESSION
-
  - **id**: AC-03
  - **description**: Office V2 ux-design plan can select ux-cinematic with global/UX prerequisites
  - **validation**: TEST-REGRESSION
-
  - **id**: AC-04
  - **description**: Deterministic frame manifests and negative gap/budget checks run without production media
  - **validation**: TEST-REGRESSION

## stop_conditions

source_of_truth_conflict; material scope expansion; credential or protected-path mutation required

## execution_prompt

- **instruction**: Keep all execution_lists in this single JSON file, never embedded in the Human Task or split into per-list JSON files. Harness verifies normative equivalence of the Human Task and this file, then supplies one prompt per list pointing to execution_contract_path and list_id. Specialists read the file, select the identified execution_lists entry and inherit global constraints, required sources, tests and dependencies. Verify task identity, contract revision, owner and current Harness evidence without reading the Human Task. Execute only the selected approved list and its subitems, return evidence and receipts, and never merge or deploy without explicit authorization.
- **required_checkpoints**:
  DISCOVERY_SDD_COMPLETED; RUNNING; VALIDATING; REWORK; BLOCKED; COMPLETED

## reporting

- **evidence**: docs/reports/CINEMATIC-UI-001.md
- **tokens**: NOT_AVAILABLE; never infer savings

## discovery

- **questions_and_answers**:
  None.
- **research**:
  Current repo owner policies, UI plugin loader and cinematic integration reference inspected
- **decisions**:
  Cinematic remains inside existing UI/UX plugin and sector
- **open_hypotheses**:
  None.
- **approval_requirement**: Implementation within this bounded scope was explicitly authorized by the owner in conversation; do not request that approval again. Final PR acceptance and merge/deploy remain separate.

