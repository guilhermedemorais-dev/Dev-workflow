---
name: frappe-ui
description: Use Frappe UI components and semantic tokens in compatible Vue 3 projects when frappe-ui is already adopted or explicitly selected. Use for Frappe UI work, not React implementations or automatic framework/design-system migration.
---

## Harness integration boundary

Apply only to compatible Vue 3 work with existing or explicitly approved Frappe UI adoption.
ui-ux-standard owns design decisions; project-native components, tokens and approved
references remain authoritative. Resolve conflicts before adopting Frappe defaults.
SETUP.md applies to approved fresh setup or scoped dependency changes, never an
automatic Tailwind/framework replacement in an existing project. Do not add a Frappe
backend or perform data mutations merely because DATA.md contains examples.
These instructions are available on Windows, Linux and macOS; framework compatibility
selects this skill. Operating-system selection applies only to executable tools.
Read [ORIGIN.md](ORIGIN.md) for the pinned subset and local changes.

<!-- BEGIN UPSTREAM BODY -->
# frappe-ui

Build UIs that look and feel like Frappe products by composing **frappe-ui** components and styling with the library's **semantic Tailwind tokens**.

## Quick start

```vue
<script setup>
import { Button, Dialog, FormControl } from 'frappe-ui'
import { ref } from 'vue'

const open = ref(false)
const name = ref('')
</script>

<template>
  <div class="p-4 bg-surface-base text-ink-gray-8">
    <Button variant="solid" theme="gray" @click="open = true">New Task</Button>
    <Dialog v-model:open="open" title="Create Task">
      <FormControl v-model="name" label="Title" required />
    </Dialog>
  </div>
</template>
```

## Where to look

Prop names, prop value types, slot names and token names live in these files, not here. Open the one you need before you write markup.

| Writing this | Open this first |
|---|---|
| any component, any page, any Tailwind class | [CORE.md](CORE.md) |
| anything that fetches or writes data | [DATA.md](DATA.md) |
| a fresh Vite + Vue 3 project | [SETUP.md](SETUP.md) |

## Contracts

These hold across components. Everything else is per-component, and lives in
[CORE.md](CORE.md).

1. **Pick the component.** Every interactive element comes from `CORE.md`. Raw
   HTML is for layout: grids, flex, spacing wrappers.
2. **Color is two props: `variant` and `theme`.** The value sets differ per
   component — `CORE.md` lists each one. In your own markup, colors come from
   the semantic scales: `bg-surface-*`, `text-ink-*`, `border-outline-*`.
3. **Two-way state is `v-model`.** Inputs take `v-model`. Overlays take
   `v-model:open`. `Combobox` and `MultiSelect` add optional `v-model:query`.
   `List` adds `v-model:selection` and `v-model:active`.
4. **Icons are CSS classes.** `<span class="lucide-edit size-4" aria-hidden="true" />`.
   A prop named `icon` takes the string `"lucide-edit"`.
5. **Slot names are per component, never universal.** Read the component's
   entry in `CORE.md` before writing a `<template #…>`.
6. **Frappe API calls go through the `use*` composables** — `useCall`,
   `useList`, `useDoc`, `useDoctype`, `useNewDoc`, all exported from
   `frappe-ui`. Each one takes its own option set and returns its own shape;
   [DATA.md](DATA.md) lists them separately.
