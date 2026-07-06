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
5. Propose the smallest organization change that fits the existing repo.
6. Ask human approval before creating or moving anything.
7. Record the chosen project structure and active plugins.

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
