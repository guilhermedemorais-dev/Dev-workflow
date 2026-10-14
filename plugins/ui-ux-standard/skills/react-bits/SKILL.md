---
name: react-bits
description: Discover and adapt React Bits components for compatible React projects when a selected interaction or visual pattern needs them. Use for React Bits requests, not Vue implementations or automatic design-system migration.
---

# React Bits component adapter

This is a local Harness adapter, not an official upstream skill. Use it after
ui-ux-standard identifies a compatible React project and a concrete pattern for
which project-native components are insufficient. Reuse approved components and
tokens first; selected React Bits components remain candidates until license,
dependencies, accessibility and performance fit the actual project.

Read [official sources and adoption](references/sources.md) for the requested
component/variant and [provenance](ORIGIN.md) for the pinned source boundary.
Do not infer APIs from a similarly named demo. Inspect the exact JS/TS and
CSS/Tailwind variant, required packages, client boundary and documented props.

When the project already has a shadcn-compatible registry configuration, consider
the official `@react-bits` registry through existing host tools or the project's
CLI. A registry entry does not require a new global MCP. Install only the selected
component and necessary dependencies within the approved project scope; preserve
the existing package manager, lockfile and components.json.

Normalize tokens, typography and motion to the approved design guide. Verify
keyboard/focus behavior, responsive layout, reduced motion and resource cleanup.
An animated accent does not replace product UI primitives. Return the selected
source URL/revision, variant, dependency/license findings and actual validation
in COMPONENT_SOURCE_INVENTORY. Implementation remains owned by the executor.

React Bits uses MIT + Commons Clause, not unrestricted MIT. Review the exact
[upstream terms](LICENSE.upstream.md). They permit components as part of an
application/site/product but prohibit selling, sublicensing or redistributing the
components themselves, including a bundle or port. This Harness ships references
and original routing instructions only; do not bundle React Bits component code
or assets into the plugin. Project-specific adoption requires compatible terms.

These instructions are available on Windows, Linux and macOS. Selection is by
framework and approved task, not operating system. Executable tools retain their
own OS/runtime checks; skill discovery does not install or certify those tools.
