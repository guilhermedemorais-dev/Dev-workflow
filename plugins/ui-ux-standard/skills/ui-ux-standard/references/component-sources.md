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

- Frappe UI: conditional foundation candidate for compatible Vue 3/Frappe UI
  projects, not React projects. Use the pinned [official instruction subset](../../frappe-ui/SKILL.md)
  only when already adopted or explicitly selected; [provenance](../../frappe-ui/ORIGIN.md)
  preserves MIT source and exact component/data/setup contracts. Existing project
  UI ownership remains authoritative, including non-Frappe backend boundaries.
  - https://ui.frappe.io/
  - https://github.com/frappe/frappe-ui
- React Bits: selected motion/visual patterns for compatible React projects,
  not a compulsory UI foundation. Read the [local adapter](../../react-bits/SKILL.md)
  and [official sources](../../react-bits/references/sources.md). License is
  MIT + Commons Clause, with restrictions on component redistribution/bundles/ports;
  inspect the exact terms before project adoption. No component code is bundled
  in this Harness. Existing project registry/tools suffice when available.
  - https://reactbits.dev/
  - https://github.com/DavidHDev/react-bits

Both libraries' instruction skills are OS-neutral and remain available on all
operating systems. Vue/React selection is framework routing. Executable tools
alone use OS-specific catalogs; adopting a library never installs every tool.

- 21st.dev: broad marketplace/catalog for modern components and blocks. Useful
  for discovery when a polished pattern is needed quickly.
  - https://21st.dev/
- Magic UI: motion-heavy and marketing-oriented React components. Prefer for
  deliberate visual emphasis, not default product chrome.
  - https://magicui.design/
- Origin UI / coss UI: application UI patterns and controls. The original
  project redirects to cosscom/ui; licensing is mixed: apps/origin and apps/ui
  are MIT, other directories AGPLv3. Inspect the exact source subtree and notices.
  - https://coss.com/ui
  - https://github.com/cosscom/ui
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

## Verified repository discovery, 2026-10-14

These are discovery candidates, not installed dependencies or runtime PASS.
Skills remain OS-neutral; select a library by project framework, purpose and
approved design. OS selection applies only to separately owned executable tools.

| Source | Original repository / official entry | Adoption boundary |
| --- | --- | --- |
| shadcn/ui | https://github.com/shadcn-ui/ui | React foundation; preserve project-selected primitives/tokens |
| Magic UI | https://github.com/magicuidesign/magicui | Selected React motion/effects; free core vs separate Pro terms |
| UI Layouts | https://github.com/ui-layouts/uilayouts | React components/blocks; exact item dependencies and Pro terms |
| Cult UI | https://github.com/nolly-studio/cult-ui | React/shadcn motion patterns; selected accents |
| Eldora UI | https://github.com/karthikmudunuri/eldoraui | React components/blocks/templates; verify selected item |
| Animata | https://github.com/codse/animata | React interactions/animation; reduced-motion and runtime cost |
| Cuicui | https://github.com/damien-schneider/cuicui | Original project; official site now points to Control UI |
| Control UI | https://github.com/damien-schneider/control-ui | Maintainer's current shadcn-compatible successor to evaluate |
| Origin UI / coss UI | https://github.com/cosscom/ui | origin-space/originui redirects here; mixed licensing: apps/origin and apps/ui MIT, other directories AGPLv3; inspect exact source subtree/notices before copying |
| Aceternity UI | https://ui.aceternity.com | Use official docs/registry and individual terms; free vs paid assets differ. Public manuarora700/ui.aceternity was found but not verified as current canonical component library or licensed distribution |
| React Native Web | https://github.com/necolas/react-native-web | React Native primitives/APIs on React DOM, not a styled UI kit; select only for an approved shared web/native architecture |

GitHub repository metadata reported MIT for React Native Web, Cuicui, shadcn,
Magic UI, UI Layouts, Cult UI, Eldora and Animata. This is a repository discovery
signal, not permission for every template, paid asset or future revision. Inspect
actual LICENSE/notices and the selected component source again on adoption.
Cuicui's official site links Control UI. Origin UI's official website and original
repository redirect to coss UI; its README/LICENSING define MIT for apps/origin and apps/ui and AGPLv3 elsewhere.
No candidate above was installed, bundled or OS-homologated by this discovery.

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
