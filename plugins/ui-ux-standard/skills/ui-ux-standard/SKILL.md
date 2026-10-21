---
name: ui-ux-standard
description: "Use for UI/UX, screens, mockups, visual design, design systems, component selection, UI libraries and registries, templates, generated assets, accessibility, responsiveness, and visual QA. Specialist companion to dev-workflow-standard."
---

# UI/UX Standard

Receive one prompt per execution list, linking the Task's single JSON file
and selecting its `execution_lists` entry by `list_id`, never per item/subitem.
All lists live in that file; do not expect JSON inside the Human Task/prompt.
Read the list JSON and relevant canonical JSON fields, not Human Task sections
as execution input. Require current Harness evidence of full card/JSON normative
equivalence, tied to the contract revision and observed Issue update time.
Missing/stale evidence or divergence returns to Harness before execution.

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

`qa-testing-standard` owns functional flows, form submission, navigation and
duplicate/retry behavior. This skill retains design fidelity, visual hierarchy,
accessibility design, responsiveness and visual runtime QA. Share relevant
evidence without claiming the other owner's PASS. A misaligned button routes
here; a button submitting twice routes to QA; unauthorized action routes to
security-standard. Playwright tool ownership remains here, even when QA uses it.

For sector-routed handoffs, read the list JSON and canonical Execution Contract,
relevant global criteria, REQUIRED sources with purpose and triggered CONDITIONAL
sources. Do not load the Human Task as execution input or OPTIONAL sources by default. Read this
SKILL.md fully and required active-mode references. Resolve context-routing from
the active Harness or explicit canonical checkout; missing required context goes
back to Harness. Planning/design may precede frontend completion; final visual
validation requires the relevant rendered artifact and current revision evidence.
For v2, verify **normative equivalence** and `contract_revision` for the routed
UI/UX slice using the current Harness comparison receipt. Load the exact
Design Guide, tokens, component library, visual references, mockup and sections
named by the contract; divergence blocks a design or validation claim.

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

For new/substantial UI or a component/source choice, read
[Component procedure](references/ui-component-procedure.md). Preserve project-native
reuse, COMPONENT_SOURCE_INVENTORY and source/license evidence; do not load every catalog.

## Registry and MCP Policy

When selecting, preparing or verifying UI tools, read
[Tooling procedure](references/ui-tooling-procedure.md). Reuse compatible local state;
do not install or rediscover unrelated tools.

## Apple HIG Designer reference selection

For Apple-platform UI, an explicitly requested Apple design direction, or evaluation
of that direction for a new interface, read [Apple HIG routing](references/apple-hig-routing.md).
This is conditional, not the default identity of every product. Never load the
whole HIG package or let it override the approved PRD, web accessibility or stack.

## Minimal Workflow

1. Discover current UI, routes, design system, frontend stack, reusable
   components, and approved visual references.
2. Classify the task: preserve, extend, redesign, or create a new surface.
3. Identify the smallest set of UI patterns and components required.
4. For new/substantial UI or component selection, build `COMPONENT_SOURCE_INVENTORY`
   using project-native sources first; otherwise reuse the current applicable inventory.
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

For module discovery/specification with frontend, read
[Live design guide](references/live-design-guide.md). Maintain both a Markdown
guide and a cumulative, navigable HTML component/widget catalogue in the client
project, or explicitly map its existing equivalent. This is not an optional
Markdown-only deliverable. Backend-only work records UI N/A without scaffolding.

Create only the applicable parts:

```text
docs/design/
  design-guide.md
  index.html
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
