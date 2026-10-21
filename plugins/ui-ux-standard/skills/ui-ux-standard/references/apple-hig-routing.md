# Apple HIG Designer, conditional integration

User-selected source: https://github.com/axiaoge2/Apple-Hig-Designer
Pinned commit: `ff17b91ff2903ecd52940afabf97de5a73c9cd1b`. License: MIT.
This is the exact repository identified by the owner, not another HIG skill.
The upstream skill, REFERENCE and three resources are preserved byte-for-byte in
`apple-hig-designer/`; SKILL.md is named GUIDE.md to prevent standalone discovery.
License and hashes are included. Readmes and screenshots are not shipped.
No installer, hook, React/CSS example or external code has been executed.
This is community-authored guidance, not an Apple-maintained or endorsed skill.

## Select only what applies

For Apple-style UI, an explicitly approved Apple-inspired visual direction or
Apple platform design review, read [Decision guide](apple-hig-designer/GUIDE.md)
completely. Then select only applicable headings/resources using local search.
Do not read all references or copy every example. On an unrelated web task,
preserve the project design system and skip this package.

| Need | Conditional reference |
| --- | --- |
| Detailed design rules or review | [Reference](apple-hig-designer/REFERENCE.md), selected heading |
| A token system compatible with the approved project | [CSS examples](apple-hig-designer/resources/design-tokens.css) |
| React examples | [Components](apple-hig-designer/resources/components.jsx), selected component |
| Layout/interaction examples | [UI patterns](apple-hig-designer/resources/ui-patterns.md), selected pattern |

## Applicability and precedence

The approved PRD, design system, stack and applicable platform/accessibility rules
remain authoritative. Upstream generation/output instructions are subordinate
to UI/UX's role and the Task: a review does not authorize implementation or
rewriting a complete application. Default to solid backgrounds; glass/blur needs
an explicit request, as this selected skill itself requires.

Treat example tokens, CSS pixel values, component shapes and durations as
community implementation choices until the claimed official rule is verified.
Do not impose them on all platforms, replace approved tokens or convert native
points blindly to CSS pixels. For web, preserve WCAG, semantic controls, keyboard
navigation and reduced motion. Confirm precise values and current platform rules
against the live official documentation before calling them mandatory:
https://developer.apple.com/design/human-interface-guidelines

Record selected topic/resource, pinned source, official URL/section where
verified and applicability in the existing design/source inventory. Missing live
evidence is NOT VERIFIED, not proof of official compliance or visual quality.
The package does not establish complete coverage of every Apple product or the
current HIG release. No source inspection is runtime visual QA.

Do not bundle Apple fonts, branding, SF Symbols or proprietary artwork without
checking their separate terms. MIT on this repository does not license unrelated
Apple assets. Prefer project-approved icon/font fallbacks on unsupported systems.
Inspect selected JSX/CSS before adapting it; source presence does not mean its
React runtime/dependencies are installed or the example is accessible in situ.
