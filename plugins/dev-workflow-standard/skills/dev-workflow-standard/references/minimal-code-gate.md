# Minimal Code Gate

Apply before specs, before implementation, and during final review. The goal is
the smallest complete change that satisfies current approved requirements.

## Reuse Inventory

Before creating code, search by responsibility, domain term, symbol, route,
interface, schema, call site and behavior. Inspect sibling modules and shared
controls, not only the target file.

```text
REUSE_INVENTORY
- searched_paths:
- queries_and_symbols:
- existing_candidates:
- call_sites_checked:
- decision: REUSE | EXTEND | REPLACE | CREATE
- reason:
```

## Decision Order

Prefer, in order:

1. reuse an existing implementation
2. extend the existing owner of the responsibility
3. replace and migrate a defective duplicate
4. create new code only when no suitable owner exists

Do not create wrappers, services, repositories, helpers, hooks, components,
configuration layers or generic abstractions for hypothetical future use.

## New-Code Test

Every new unit must answer:

- What approved requirement needs it now?
- Which existing implementations were inspected?
- Why can none be reused or extended safely?
- Who owns this responsibility after the change?
- Which duplicate or obsolete path is removed or deliberately retained?
- What test proves the behavior without coupling to implementation detail?

New abstractions require at least two current concrete consumers or an explicit
approved architecture decision. Similar behavior with different names is still
duplication.

```text
MINIMAL_CODE_GATE
- result: PASS | REWORK | BLOCKED
- reused_or_extended:
- new_units_and_justification:
- duplicates_removed:
- retained_overlap_and_owner:
- evidence:
```

`PASS` is forbidden when the reuse inventory is missing, a new abstraction is
speculative, or equivalent behavior was duplicated without an approved reason.
