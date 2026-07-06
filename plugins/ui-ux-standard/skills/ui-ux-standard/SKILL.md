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
  checked where practical.
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
5. Hand implementation back to the main development workflow.
6. Validate in runtime with Playwright, Browser, Chrome DevTools, or the repo's
   existing test setup when available.

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
- loading, empty, error, permission states when relevant
- keyboard accessibility and contrast
- images/assets render correctly
- route/auth context is stated accurately

Report untested items as `NAO VALIDADO`.

## Handoff Output

Return concise handoff data:

- mockup/design reference path
- changed design docs or tokens
- assets/media prompt status
- visual acceptance criteria
- runtime validation evidence
- unresolved decisions
