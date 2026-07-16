---
name: ui-ux-standard
description: "Use for UI/UX, screens, mockups, visual design, design systems, components, generated assets, accessibility, responsiveness, and visual QA. Specialist companion to dev-workflow-standard."
---

# UI/UX Standard

Specialist workflow for design and frontend visual quality. Keep this file
compact and create only the docs/artifacts needed for the current task.

## Ownership

Owns:

- design discovery and design-system rules
- mockup-first workflow
- `docs/design` organization when needed
- visual assets and media prompts
- accessibility, responsiveness, and runtime visual QA criteria

Does not own backend architecture, database design, deployment, or final user
approval.

## Non-Negotiables

- Inspect existing UI, routes, components, styling stack, and design docs before
  proposing new UI.
- Approved mockups, Figma, screenshots, brand docs, and project design files are
  source of truth.
- If docs and code conflict, stop and ask.
- Reuse existing components and design tokens before creating new ones.
- Do not redesign unrelated surfaces.
- Do not use unlicensed external assets as final assets.
- Frontend/UI is not complete until runtime behavior and visual fidelity are
  checked with Playwright, Browser, Chrome DevTools, screenshots, existing UI
  tests, or an explicit `NAO VALIDADO` blocker with reason. Do not declare UI
  complete from static code review alone.
- UI work must include or consume a UI Interaction Matrix for each changed
  screen/component. If no matrix exists for an applicable UI surface, return the
  work to `sdd-spec-factory`/`dev-workflow-standard` as `blocked`/`needs-info`.
- Every button, link, input, menu item, tab, toggle, modal action, keyboard path,
  permission state and visible feedback state must map to a mockup/spec/task row
  or be explicitly marked out of scope.
- When `minimal-implementation-gate` recommends simplification, accessibility,
  usability, approved mockups and required visual states have precedence. Do not
  remove keyboard access, contrast, responsive behavior, error/loading/empty
  states or design-system requirements merely to reduce files or tokens.

## Minimal Workflow

1. Discover current UI/design context.
2. Identify whether the task needs a mockup, design tokens, media prompt, or
   visual QA report.
3. Create only the required artifact under `docs/design/` if the repo has or
   needs that structure.
4. Define visual acceptance criteria: layout, states, responsiveness,
   accessibility, assets, and interaction behavior.
5. Build or validate the UI Interaction Matrix for every changed screen and
   component.
6. Include security/privacy UI states when applicable: masked sensitive data,
   forbidden/unauthorized state, tenant/user boundary, role-specific disabled
   actions, safe empty state and no secret/token exposure in client-visible UI.
7. Hand implementation back to the main development workflow.
8. Validate in runtime with Playwright, Browser, Chrome DevTools, screenshots or
   the repo's existing test setup. If blocked, mark exactly what is
   `NAO VALIDADO` and why.

## Default Design Structure

Use only when needed:

```text
docs/design/
  design-guide.md
  design.json
  design-tokens.json
  component-standards.md
  references/
  mockups/
  media-prompts/
  assets/
  visual-qa/
```

Do not initialize the full tree blindly.

## Visual QA Checklist

- fidelity against approved mockup/reference
- desktop and mobile responsiveness
- text overflow and overlap
- spacing, alignment, and component states
- every button/link/input/menu/tab/toggle/modal action from the task or mockup
  exists, has the correct enabled/disabled/loading state, and triggers the
  specified effect
- loading, empty, error, success, disabled, forbidden and permission states when
  relevant
- keyboard accessibility and contrast
- images/assets render correctly
- route/auth context is stated accurately
- privacy and security UI behavior: sensitive data masking, role/tenant
  restrictions, safe error copy, no tokens/secrets in visible UI or browser
  storage unless explicitly approved
- runtime evidence exists for desktop and mobile, or the missing validation is
  marked `NAO VALIDADO`

Report untested items as `NAO VALIDADO`.

## UI Interaction Matrix Gate

For any UI task, validate or produce a table with this shape:

| ID | Screen/component | Element/action | Source mockup/spec/task | Permission/condition | Expected effect | Required states | Security/privacy rule | Runtime evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UI-01 |  |  |  |  |  |  |  |  | PASS/BLOCKED/NAO VALIDADO |

Rules:

- One row per interactive element and required state group.
- `PASS` requires evidence, not just assertion.
- `NAO VALIDADO` is allowed only with reason and prevents final UI acceptance.
- Missing buttons, missing states, unverified permissions, text overflow,
  overlapping elements or mockup drift are `BLOCKED` until corrected or
  explicitly descoped by the orchestrator/user.
- If a UI simplification proposed by `minimal-implementation-gate` removes a
  matrix row, reject that simplification unless the row is formally descoped.

## Handoff Output

Return concise handoff data:

- mockup/design reference path
- changed design docs or tokens
- assets/media prompt status
- visual acceptance criteria
- UI Interaction Matrix status
- security/privacy UI states status
- runtime validation evidence
- unresolved decisions
