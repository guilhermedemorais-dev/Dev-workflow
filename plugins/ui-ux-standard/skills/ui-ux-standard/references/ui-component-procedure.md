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

For every PRD/spec, retain a compact record in its existing references section:
applicable catalog indexes/metadata consulted and revision, selected source ID or
project-native reuse, or N/A with reason. Unavailable/stale evidence is NOT_VALIDATED,
never an invented consultation. Metadata review does not load every source body;
only selected necessary sources become REQUIRED. Follow the Harness targeted-inventory policy; expand discovery only for a gap.

Select only an edition/item usable for the approved project without buying a
license; exclude paid Pro/Enterprise assets. Unknown cost/license is not eligible
until verified. Zero license cost and OSI open-source status are distinct: retain
applicable source-available/copy/redistribution restrictions and subtree terms.
No catalog proves every repository item free or all infrastructure/services free.

When the user/project declares a Next.js/NestJS preference and stack is undecided,
assess that reference pair through existing catalog IDs, then confirm the PRD.
Preserve approved stacks; do not apply this preference to undeclared projects. Next server/BFF adapters may call
Nest-owned domain APIs; do not duplicate business rules or assume Next cannot run backend code.

Use project-native UI first, then the curated catalog matching the actual stack.
If a concrete gap remains, use targeted Context7 documentation or GitHub official
source search; record unavailable capabilities and verified fallbacks. Libraries
are catalog candidates, not standalone installed skills or compulsory dependencies.
Do not migrate frameworks, replace approved design rules, install every candidate
or modify global MCP settings. Install only selected dependencies in the approved
project. Instructions remain OS-neutral; only executable tools use OS catalogs.

For selected or proposed library sources, read [Library source handoff](library-source-handoff.md).
Preserve the same project source ID from PRD to spec and Task; load only the selected
dependency's purpose-qualified references, not the whole catalog on every task.

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
- stable library ID and project source ID:
- official repository/docs URL and exact version/commit or UNKNOWN:
- component path/variant and purpose/module:
- decision state (PROPOSED/APPROVED/UNKNOWN/EXCLUDED):
- why selected:
- adaptation required:
- license/dependency status:
- rejected alternatives:
- custom-build justification, if any:
```

Do not pretend a source was searched when the relevant browser, registry, MCP,
CLI, or network capability was unavailable. Mark it `NAO VALIDADO` and proceed
with the best verified local option.
