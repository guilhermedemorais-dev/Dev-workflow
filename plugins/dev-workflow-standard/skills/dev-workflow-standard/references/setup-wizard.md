# Main Plugin Setup Wizard

`dev-workflow-standard` is the principal plugin. On a new project, it must guide
configuration before running the full delivery workflow.

The setup is assisted, not silent. The plugin may inspect the project and report
what is missing. It must request explicit human permission before installing
complementary plugins, enabling hooks, adding files, creating directories or
reorganizing project documentation.

## Goals

- Keep the construction standard consistent across projects.
- Prevent developers or agents from forgetting mandatory stages.
- Reduce token cost by loading only the stage-specific skill needed now.
- Preserve project source of truth, security and human control.

## Complementary Plugins

Required for the full workflow:

- `sdd-spec-factory`
- `dev-implementation-standard`
- `minimal-implementation-gate`

Conditional but normally expected:

- `security-standard`
- `ui-ux-standard`

`security-standard` becomes required when the change touches security-sensitive
surfaces. `ui-ux-standard` becomes required when the change touches UI,
accessibility, responsiveness or design.

## Setup Flow

1. Detect installed/enabled plugins.
2. Explain missing complementary plugins and their role.
3. Ask human approval before installation or activation.
4. Inspect project organization:
   - `AGENTS.md`
   - PRD, architecture, mockups or project docs
   - `docs/specs/`
   - `docs/tasks/`
   - `docs/design/` when UI exists
   - PR/review/QA evidence location
5. Inspect workflow contract compatibility:
   - task template requires `Executor LLM`, handoff mode, claim status and
     `locked_paths`
   - task template requires Ambiguity, Spec Completeness, UI Interaction
     Contract, Backend Contract, Security Spec Contract and Traceability gates
   - UI tasks require a UI Interaction Matrix per changed screen/component
   - backend tasks require backend/API/job/webhook contract rows
   - security-triggering tasks require Security Spec Contract rows
   - execution reports require evidence by Banco, API/Backend, Frontend/UI,
     Validacao and Riscos/Lacunas
   - `AGENTS.md` or project workflow docs require spec-first, task-first,
     approval-before-code and executor/file ownership
6. Classify the project:
   - `CURRENT`: project already enforces the current workflow contracts
   - `PARTIAL`: docs exist but templates/gates are missing or old
   - `LEGACY`: no enforceable specs/tasks/gates structure
7. For `PARTIAL` or `LEGACY`, propose the smallest migration patch. Do not
   rewrite product requirements; update only workflow docs/templates after human
   approval.
8. Propose the smallest organization change that fits the existing repo.
9. Ask human approval before creating or moving anything.
10. Record the chosen project structure, active plugins, contract version and
    remaining `NAO VALIDADO` setup gaps.

## Compatibility Report

Return this before normal delivery starts:

- Plugin set: installed/missing
- Project structure: `CURRENT` / `PARTIAL` / `LEGACY`
- Missing workflow contracts
- Required migration patch, if any
- Human approvals needed
- Setup gaps marked `NAO VALIDADO`

## Token Policy

The principal plugin keeps only a lightweight map of roles, stages and required
checks in context. It does not preload all complementary plugin instructions.
Load each specialist only when its gate is active.

## Permission Policy

Never perform silently:

- third-party plugin installation
- hook enablement
- MCP/server activation
- file or directory reorganization
- creation of workflow docs in an existing project
- permission or credential changes

Return a concrete setup proposal and wait for approval.
