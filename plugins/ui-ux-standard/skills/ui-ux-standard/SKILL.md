---
name: ui-ux-standard
description: "Use for UI/UX, screens, mockups, visual design, design systems, component selection, UI libraries and registries, templates, generated assets, accessibility, responsiveness, and visual QA. Specialist companion to dev-workflow-standard."
---

# UI/UX Standard

Act as the UI/UX specialist. Read this `SKILL.md` completely before review and
return a `SKILL_RECEIPT`; a mention of the skill is not proof that its
methodology was applied.

Keep this control plane compact. Create only the design docs and artifacts that
are needed for the current task.

## Ownership

Own:

- design discovery and design-system rules
- component and template discovery before custom UI invention
- mockup-first workflow when visual direction is not already approved
- `docs/design` organization when needed
- visual assets and media prompts
- accessibility, responsiveness, interaction states, and runtime visual QA

Do not own backend architecture, database design, deployment, or final user
approval.

## Non-Negotiables

- Inspect existing UI, routes, components, styling stack, dependencies, design
  docs, and approved references before proposing new UI.
- Treat approved Figma, mockups, screenshots, brand docs, project design files,
  and the project's existing design system as source of truth.
- If design docs and production code conflict materially, stop and surface the
  conflict before redesigning.
- Reuse project components and design tokens before importing or creating new
  ones.
- Before inventing a new visual component, search approved component sources or
  registries when the project stack and task make that practical.
- Do not combine several component libraries merely for visual novelty. Prefer
  one coherent foundation plus narrowly selected specialist components.
- External components are references or implementation candidates, not a new
  design system. Adapt them to the project's tokens, typography, spacing,
  states, accessibility rules, and product context.
- Do not copy a complete third-party product visual identity or proprietary
  template without an applicable license and explicit project justification.
- Review third-party code, dependencies, maintenance status, license, runtime
  cost, accessibility, and compatibility before adoption.
- Do not redesign unrelated surfaces.
- Do not use unlicensed external assets as final assets.
- Frontend/UI is not complete until runtime behavior and visual fidelity are
  checked where practical.

## Component Intelligence

For new screens, sections, or substantial UI work, produce a lightweight
`COMPONENT_SOURCE_INVENTORY` before implementation.

Use this priority:

1. Existing project components and tokens.
2. Approved project design references or internal component library.
3. Official framework or design-system primitives already used by the project.
4. shadcn-compatible registries and curated component libraries appropriate to
   the stack.
5. Custom implementation only when reuse is unsuitable or would cost more than
   a focused custom component.

Consult `references/component-sources.md` when external components, blocks, or
templates could materially improve the result.

Consult `references/component-selection.md` when choosing among several
components, libraries, templates, or interaction patterns.

Consult `references/anti-ai-design.md` when creating a new marketing page,
product surface, dashboard, SaaS UI, e-commerce interface, or any screen where
visual differentiation and perceived product quality matter.

### Required inventory

Return or record:

```text
COMPONENT_SOURCE_INVENTORY
- project-native candidates:
- external candidates searched:
- selected source/component:
- why selected:
- adaptation required:
- license/dependency status:
- rejected alternatives:
- custom-build justification, if any:
```

Do not pretend a source was searched when the relevant browser, registry, MCP,
CLI, or network capability was unavailable. Mark it `NAO VALIDADO` and proceed
with the best verified local option.

## Registry and MCP Policy

Own browser, visual, and accessibility tooling through
`references/tool-registry.json`. Follow the shared `skill-owned-tools.md`
protocol: consult ignored per-skill runtime state, use its compatible fast
path, or detect, install from an official supported source when required,
verify, and persist. Revalidate after a failed visual check or fix. A cached
Playwright CLI does not prove browser binaries or the project's runtime are
ready; validate those in the active workspace before claiming coverage.

When a shadcn-compatible project is detected, prefer registry-aware discovery
instead of generating JSX from memory.

- If shadcn MCP is already available, use it to browse and search configured
  registries before installing candidate components.
- If MCP is unavailable, use official documentation, the project's shadcn CLI,
  or public source repositories as discovery fallback.
- Do not silently modify global MCP configuration or install a new global tool.
  Propose that environment change separately when it is actually needed.
- Treat community registries as third-party code. Inspect source and license
  before adoption.
- When `components.json` defines registries, inspect those project-approved
  registries before unrelated public sources.

## Minimal Workflow

1. Discover current UI, routes, design system, frontend stack, reusable
   components, and approved visual references.
2. Classify the task: preserve, extend, redesign, or create a new surface.
3. Identify the smallest set of UI patterns and components required.
4. Build `COMPONENT_SOURCE_INVENTORY` using project-native sources first and
   approved external sources second.
5. If visual direction is missing, establish a concise direction or mockup
   before implementation.
6. Define visual acceptance criteria for hierarchy, layout, states,
   responsiveness, accessibility, assets, motion, and interaction behavior.
7. Hand implementation to the main development workflow with exact component
   choices, adaptation notes, and acceptance criteria.
8. Validate rendered output in runtime with Playwright, Browser, Chrome
   DevTools, or the repository's existing test setup when available.
9. Reject visual regressions, generic template assembly, unjustified library
   mixing, and implementation that diverges from the approved design direction.

## Default Design Structure

Use only when needed:

```text
docs/design/
  design-guide.md
  design.json
  design-tokens.json
  component-standards.md
  component-source-inventory.md
  references/
  mockups/
  media-prompts/
  assets/
  visual-qa/
```

Do not initialize the full tree blindly.

## Visual Quality Gate

Reject the UI for rework when one or more of these materially apply:

- generic assembly of cards, gradients, pills, glows, and oversized headings
  without product rationale
- hierarchy or density inconsistent with the actual workflow
- visually impressive component that damages usability, accessibility, or
  performance
- several libraries mixed without a clear design-system normalization layer
- external component copied without adaptation to project tokens and states
- desktop-only composition with mobile behavior treated as an afterthought
- missing loading, empty, error, disabled, permission, destructive, or success
  states where the product flow requires them
- visual language conflicts between adjacent screens
- decorative motion that competes with task completion

## Visual QA Checklist

- fidelity against approved mockup/reference
- consistency with design tokens and existing product language
- desktop and mobile responsiveness
- text overflow and overlap
- spacing, alignment, hierarchy, and component states
- loading, empty, error, success, destructive, and permission states when
  relevant
- keyboard accessibility, focus behavior, semantics, and contrast
- images and assets render correctly
- animation respects usability and reduced-motion expectations
- route/auth context is stated accurately
- selected external component dependencies are actually present and compatible

Report untested items as `NAO VALIDADO`.

## Handoff Output

Return concise handoff data:

- `SKILL_RECEIPT`
- mockup/design reference path
- changed design docs or tokens
- `COMPONENT_SOURCE_INVENTORY`
- selected component/library/template sources and adaptation notes
- assets/media prompt status
- visual acceptance criteria
- runtime validation evidence
- unresolved decisions
