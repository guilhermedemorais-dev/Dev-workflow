---
name: ui-ux-standard
description: "Use when a task involves UI/UX, screens, mockups, visual design, design systems, components, generated images/videos/assets, accessibility, responsiveness, or visual QA. This skill owns docs/design organization and mockup-first workflow; implementation remains under the main development workflow."
---

# UI/UX Standard

Use this skill for all design, mockup, visual asset, and frontend visual-quality work.
It is the specialist companion to `dev-workflow-standard`.

## Responsibility

This skill owns:

- design discovery
- design-system rules
- design tokens and `design.json`
- mockup-first workflow
- component standards
- media prompt PRDs
- visual asset approval
- accessibility and responsive QA
- runtime visual validation criteria

It does not own backend architecture, database design, deployment, or final delivery approval.

## Standard Design Structure

Prefer this structure for new projects. For existing projects, inspect current
design docs first and propose migration before moving files.

```text
docs/
  design/
    README.md
    design-guide.md
    design.json
    design-tokens.json
    component-standards.md
    references/
      reference-YYYY-MM-DD.md
    mockups/
      mockup-YYYY-MM-DD-feature-name.html
    media-prompts/
      PRD-YYYY-MM-DD-media-prompts.md
      image-prompt-YYYY-MM-DD-asset-name.md
      video-prompt-YYYY-MM-DD-asset-name.md
    assets/
      README.md
    visual-qa/
      report-YYYY-MM-DD-feature-name.md
.project-ai/
  instructions/
    ui-rules.md
  prompts/
    ui-mockup.md
    media-generation.md
    visual-review.md
```

Do not create all files blindly. Create only the files needed by the current task
unless the user explicitly asks to initialize the full UI/UX structure.

## Design Workflow

### 1. Discover Existing UI

Before creating anything:

- inspect existing UI/routes/components
- inspect `docs/design/`, design guides, screenshots, mockups, Figma links, or style docs
- identify component library and styling stack
- identify reusable components before proposing new ones
- identify audience and product domain

If docs and code conflict, stop and ask for a decision.

### 2. Design Reference Protocol

When no sufficient project reference exists:

1. Gather 2-3 visual references or describe desired direction.
2. Extract reusable design qualities, not copied layouts.
3. Convert references into `design.json` and rules:
   - colors
   - typography
   - spacing
   - radius
   - shadows
   - borders
   - imagery style
   - illustration style
   - layout density
   - component behavior
   - motion style
4. Store the resulting plan in `docs/design/references/`, `docs/design/design.json`, or `docs/design/design-guide.md`.

Rules:

- Do not copy external design 1:1.
- Do not use unlicensed assets.
- Do not replace an approved design system without explicit approval.
- SaaS/CRM/operational tools should prioritize dense, calm, scannable layouts.
- Marketing/product pages may use stronger visual storytelling, but still need real assets or generated bitmap visuals when appropriate.
- Reject generic AI-looking UI by default: unexplained purple gradients, generic icon-only visuals, one-note palettes, default font choices without rationale, and flat template-like layouts.

### 3. Design.json And Tokens

When creating or updating a visual system, produce or update:

```text
docs/design/design.json
docs/design/design-tokens.json
```

Use `design.json` as the human-readable design contract extracted from references
or project style. Use `design-tokens.json` when implementation needs a stricter
token map.

Recommended `design.json` shape:

```json
{
  "design_direction": "",
  "brand_feel": [],
  "colors": {},
  "typography": {},
  "layout": {},
  "spacing": {},
  "radius": {},
  "shadows": {},
  "components": {},
  "imagery": {},
  "illustrations": {},
  "motion": {},
  "avoid": []
}
```

Recommended `design-tokens.json` shape:

```json
{
  "colors": {},
  "typography": {},
  "spacing": {},
  "radius": {},
  "shadows": {},
  "components": {},
  "motion": {}
}
```

The token file is a design contract. Frontend implementation should refer to it
or explicitly map it to the project's styling system.

Reference extraction prompt:

```text
Analyze this visual reference as a design system, not as a layout to copy.
Return a design.json with: design_direction, brand_feel, colors with hex values,
typography, layout density, spacing, radius, shadows, component patterns,
imagery style, illustration style, motion style, accessibility concerns, and
avoid rules.
Do not copy the design 1:1. Extract reusable visual principles that can be
adapted to this project.
Project/domain context: <context>
Target UI: <screen or flow>
```

### 4. Mockup-First Protocol

For new screens, major UI changes, dashboards, landing pages, or visual redesigns:

1. Create/update a mockup before frontend implementation.
2. Put mockups in `docs/design/mockups/`.
3. Name them `mockup-YYYY-MM-DD-feature-name.html`.
4. Use the existing layout/design system where present.
5. Add only the new feature or changed flow; do not redesign unrelated UI.
6. Get user approval before coding when visual fidelity matters.

Mockup must cover:

- desktop layout
- mobile/responsive behavior or notes
- empty state
- loading state
- error state
- permission/locked state when relevant
- primary interactions

### 5. Component Standards

Before creating components:

1. Search existing components.
2. Reuse when possible.
3. If creating a component, document:
   - purpose
   - props/data shape
   - variants
   - states
   - accessibility behavior
   - examples
4. Update `docs/design/component-standards.md` when the component becomes reusable.

Avoid creating visually similar duplicate components.

### 6. Media Prompt Protocol

For images, icons, illustrations, videos, backgrounds, product visuals, or motion:

1. Create a media prompt PRD before generating assets.
2. Store it in `docs/design/media-prompts/`.
3. Create specific image/video prompt files for each important asset.
4. Store generated files under the project asset path chosen by the repo, and record approved asset references in `docs/design/assets/`.
5. Validate generated assets inside the mockup or real UI before approval.

Media prompt PRDs should define:

- objective and target screen/flow
- asset type
- visual style and brand constraints
- dimensions/aspect ratios
- forbidden elements
- accessibility constraints
- text/no-text requirements
- variants needed
- generation prompt
- negative prompt
- review checklist
- selected asset path or link
- license/source notes

Use separate prompt files when assets will be generated in external tools:

```text
docs/design/media-prompts/image-prompt-YYYY-MM-DD-asset-name.md
docs/design/media-prompts/video-prompt-YYYY-MM-DD-asset-name.md
```

Recommended image prompt file:

```markdown
# Image Prompt: <asset name>

## Usage
- Screen/flow:
- Placement:
- Target size/aspect ratio:
- Output format:

## Design Context
- Product/domain:
- User emotion:
- design.json reference:
- Brand constraints:

## Prompt
<prompt to paste into the image model>

## Negative Prompt
<things to avoid>

## Variants
- Variant A:
- Variant B:
- Variant C:

## Review Checklist
- Matches design.json
- Works at target size
- No unreadable text
- No unlicensed brands/characters
- No sensitive/private data
- Accessible contrast when used behind text

## Approved Asset
- Path/link:
- Notes:
```

Recommended video prompt file:

```markdown
# Video Prompt: <asset name>

## Usage
- Screen/flow:
- Placement:
- Duration:
- Aspect ratio:
- Output format:

## Storyboard
1. Opening frame:
2. Main motion:
3. Ending frame/loop:

## Design Context
- Product/domain:
- Mood:
- design.json reference:
- Brand constraints:

## Prompt
<prompt to paste into the video model>

## Negative Prompt
<things to avoid>

## Motion Notes
- Camera:
- Transitions:
- Speed:
- Looping:

## Review Checklist
- Matches design.json
- Does not distract from UI task
- Compresses well
- No text artifacts
- No unlicensed brands/characters
- No sensitive/private data
- Accessible when paired with text/controls

## Approved Asset
- Path/link:
- Notes:
```

Rules:

- Do not use unlicensed external images/videos as final assets.
- Do not copy a reference image 1:1.
- Prefer generated or owned assets when licensing is unclear.
- Save reusable generated prompts in the repo so the asset can be regenerated later.
- Do not include real people, brands, private customer data, secrets, or copyrighted characters unless the user has rights and explicitly requests it.
- For videos, define storyboard, duration, aspect ratio, frame style, motion notes, and export target before generation.

### 7. Visual QA Protocol

Frontend/UI is not complete until runtime behavior is checked.

Validate:

- visual fidelity against approved mockup
- responsiveness
- text overflow
- spacing and alignment
- component states
- keyboard accessibility
- color contrast
- loading/empty/error/permission states
- no incoherent overlap
- images/assets render correctly

Use the project's existing Playwright setup when available for repeatable
browser flows, responsive viewport checks, and screenshots. Use another
approved browser tool as fallback. Do not mark visual QA complete from static
code inspection or screenshots alone; interactions, states, accessibility, and
runtime behavior must also be checked.

Record findings in:

```text
docs/design/visual-qa/report-YYYY-MM-DD-feature-name.md
```

## Handoff Back To Development

When UI/UX planning is complete, hand back:

- approved mockup path
- design docs changed
- tokens/components affected
- asset/media prompt status
- visual QA checklist
- frontend acceptance criteria
- unresolved visual decisions

The main development workflow then owns implementation, tests, integration, and final status reporting.

## Standard Prompts

### Initialize UI Docs

```text
Use UI/UX Standard. Inspect existing UI/design docs and propose a safe docs/design structure. Do not reorganize files until approved.
```

### Create Mockup

```text
Use UI/UX Standard to create a mockup-first plan for this feature. Reuse the existing design system, create only the needed mockup, and define visual acceptance criteria before implementation.
```

### Media Prompt PRD

```text
Use UI/UX Standard to create a media prompt PRD for generated assets. Do not use external unlicensed assets. Include prompt, negative prompt, variants, dimensions, and review checklist.
```

### Design.json Extraction

```text
Use UI/UX Standard to extract a design.json from this reference. Do not copy the layout 1:1. Extract reusable style variables, imagery rules, component patterns, motion guidance, and avoid rules for this project.
```

### Image/Video Generation Prompt

```text
Use UI/UX Standard to create image and video prompt files under docs/design/media-prompts for the required assets. Include prompt, negative prompt, variants, dimensions, storyboard for video, and review checklist. Do not generate or use unlicensed external media directly.
```

### Visual Review

```text
Use UI/UX Standard to compare the implemented UI against the approved mockup and produce a visual QA report.
```
