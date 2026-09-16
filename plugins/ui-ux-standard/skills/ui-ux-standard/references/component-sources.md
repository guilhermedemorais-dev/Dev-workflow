# Component Sources

Use this file only when external components, blocks, templates, or registry
search can materially improve the UI. Project-native components and approved
design references always come first.

## Source tiers

### Tier 1: project-native and official

1. Existing project components, tokens, layouts, and patterns.
2. Approved Figma/mockups/brand documentation.
3. shadcn/ui official registry when the project already uses shadcn-compatible
   primitives or can adopt them without architectural churn.

For shadcn-compatible projects, prefer registry-aware discovery. The official
shadcn MCP can browse, search, and install items from configured registries, and
supports multiple public, private, and namespaced registries.

Official references:

- https://ui.shadcn.com/docs/mcp
- https://ui.shadcn.com/docs/registry
- https://ui.shadcn.com/docs/directory
- https://ui.shadcn.com/docs/registry/github

Do not automatically add MCP configuration to a developer's global environment.
If the MCP is not available, use project-local CLI/docs/source discovery.

### Tier 2: curated component libraries

Use these as candidate sources, not as a mandate to mix them all in one project.
Always verify current license, component source, dependency footprint, and stack
compatibility before adoption.

- 21st.dev: broad marketplace/catalog for modern components and blocks. Useful
  for discovery when a polished pattern is needed quickly.
  - https://21st.dev/
- Magic UI: motion-heavy and marketing-oriented React components. Prefer for
  deliberate visual emphasis, not default product chrome.
  - https://magicui.design/
- Origin UI: practical application UI patterns and controls suitable for SaaS,
  settings, forms, dashboards, and operational interfaces.
  - https://originui.com/
- Animate UI: animated shadcn-compatible components and interaction patterns.
  Use only when motion serves state, hierarchy, or feedback.
  - https://animate-ui.com/
- Kokonut UI: modern React/Tailwind component collection with expressive visual
  patterns. Treat as a candidate source and normalize to the project design
  system.
  - https://kokonutui.com/
  - https://github.com/kokonut-labs/kokonutui
- Cult UI: components, blocks, and starter patterns useful for product and
  marketing surfaces.
  - https://cult-ui.com/
  - https://github.com/nolly-studio/cult-ui
- Aceternity UI: strong source of animated marketing sections and presentation
  patterns. Verify the license and terms of each relevant item/template before
  using it in a deliverable.
  - https://ui.aceternity.com/

### Tier 3: community registry discovery

Use the official shadcn Registry Directory and maintained public repositories to
find alternatives when Tier 1 and Tier 2 do not satisfy the requirement.
Community registries are third-party code. Inspect them before adoption.

## Search strategy

Search by the actual interface requirement, not by vague style words.

Good queries:

- `command palette with grouped search and keyboard navigation`
- `responsive inventory data table with row actions`
- `pricing comparison section with monthly annual toggle`
- `empty state for disconnected integration`
- `checkout address form multi-step`

Weak queries:

- `beautiful dashboard`
- `modern UI`
- `cool card`
- `futuristic website`

The goal is to find a pattern that solves the product problem, then adapt its
visual treatment. Do not let a catalog component redefine the product merely
because its demo looks expensive.

## Adoption checks

Before selecting an external candidate, verify:

- license or usage terms are compatible with the project
- framework and runtime compatibility
- React/Next.js/Tailwind/shadcn versions where relevant
- required dependencies and bundle/runtime cost
- server/client boundary implications
- accessibility and keyboard behavior
- responsive behavior
- reduced-motion behavior for animated components
- theming and token adaptability
- maintenance quality and source transparency
- whether an equivalent component already exists locally

Record unknowns as `NAO VALIDADO` instead of assuming compatibility.

## Selection rule

Prefer the candidate that gives the best combination of:

1. product fit
2. design-system fit
3. accessibility
4. maintainability
5. implementation cost
6. performance
7. visual distinctiveness appropriate to the product

A spectacular demo with poor product fit is a rejected candidate.
