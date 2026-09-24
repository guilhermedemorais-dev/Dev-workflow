# Context Routing and Sector Validation Matrix

This is a [LOCAL EXTENSION] of the existing Harness contract, not a new runtime
engine or provider standard. The [PROJECT CHOICE] is an additive
`schema_version: 1`: existing contracts remain readable without `sectors`.

## Sources of truth and ownership

The Harness reads the complete Human Task and Execution Contract, reconciles
scope, global acceptance criteria and all sectors, then delegates a slice.
The specialist does not read the complete Human Task by default. It reads its
entire canonical SKILL.md, routed sections and the smallest complete context
needed for its claim. Progressive disclosure never removes a mandatory rule.

Keep these invariants explicit:

- `CODE_COMPLETE != TASK_COMPLETE`
- `NO_EVIDENCE != PASS`
- `SECTOR_REQUIRED != OPTIONAL`
- `OUTSIDE_OWNER != AUTHORIZED_TO_PASS`
- `CONTEXT_AVAILABLE != CONTEXT_REQUIRED`

Only the sector owner attests its result. Another specialist can request
`REWORK_REQUESTED`, provide evidence or block its own dependent checkpoint; it
cannot mark another sector PASS or fabricate another skill's receipt. The
Harness records the owner's returned evidence and reconciles the final gate.

## Additive v1 fields

`global_acceptance_refs` contains anchored references to relevant global
criteria. `sectors` maps stable IDs to compact routing objects:

| ID | Human sector | Default owner |
| --- | --- | --- |
| database | Banco | dev-implementation-standard |
| backend | API / Backend | dev-implementation-standard |
| frontend | Frontend | dev-implementation-standard |
| ui_ux | UI / UX | ui-ux-standard |
| qa | QA / Testes | qa-testing-standard |
| security | Segurança | security-standard |
| devops | DevOps / Infraestrutura | devops-standard |
| observability | Observabilidade | Explicit owner for application instrumentation or operations |
| documentation | Documentação | Explicit scoped executor, normally dev-implementation-standard |
| harness | Gate Final do Harness | dev-workflow-standard |

All ten IDs appear in new routed contracts and in the human matrix. Resolve a
single concrete owner, including N/A rows. Additional material domains require
an explicit ID, owner and rationale in the Task, not a guessed specialist.

Every sector has `owner`, `applicability`, `depends_on`, `task_sections`,
`required_sources`, `conditional_sources` and `required_validations`.
`applicability` is `REQUIRED` or `N/A`; N/A also requires a nonempty `reason`.
N/A needs no detailed Task section, sources, validations or dependencies.
REQUIRED needs an objective, checklist and expected evidence in its routed Task
section, not copied into JSON. Validation entries are compact capability IDs.

- `task_sections`: explicit `task:#anchor` references, resolved against
  `task_path`; use unique headings or explicit HTML anchors in the Human Task.
- `required_sources`: objects with `path` and nonempty `purpose`.
- `conditional_sources`: objects with `path`, `purpose` and an explicit
  `condition`; evaluate that condition before loading the source.
- `optional_sources`: optional list of `path`/`purpose`; do not load OPTIONAL
  automatically. Record the reason if consulting one becomes useful.
- `depends_on`: sector IDs whose final validation receipts are prerequisites.
- `planning_depends_on`: optional separate IDs required only for planning;
  absent means no sector completion prerequisites for planning, not no scope
  or mandatory-source prerequisites.

Paths are repository-root relative; a `#anchor` narrows the requested section.
Global goal, allowed paths, exclusions, stop conditions and relevant acceptance
criteria always constrain the slice. Routed contracts do not automatically load
all legacy `specs`/`docs`/`required_skills` arrays: they remain compatible indexes,
while the Harness routes the necessary entries to each owner. A globally
mandatory rule cannot be omitted by omitting it from a sector source list.

Do not store status, result, logs, receipts, evidence, source bodies, checklists,
tool paths or runtime installation state in sector JSON. Mutable status and
receipt references live in the Human Task evidence ledger.

## Resolve and load a slice

Handoff contains `task_id`, `execution_contract_path`, `sector`, `phase`
(`planning` or `validation`), revision and relevant `dependency_receipts` paths.
No Task/spec bodies are pasted into it.

1. Validate the base v1 fields and resolve the named sector and owner.
2. Check all ten applicability decisions, N/A reasons, known dependency IDs,
   no self-dependencies or cycles in either phase graph, and that final Harness
   dependencies include every other REQUIRED sector.
3. Resolve the sector's canonical SKILL.md and read it completely. Read its
   mandatory active-phase references and emit SKILL_RECEIPT.
4. Read the minimal global summary/constraints and relevant
   `global_acceptance_refs`, then all listed `task_sections`.
5. Read REQUIRED sources for their stated purpose. Evaluate each CONDITIONAL
   source against observed scope and record activated/not activated with reason.
   OPTIONAL sources are not loaded by default. Inspect only relevant code.
6. Check the phase's dependency receipts for owner, validation scope, artifact
   and revision. Unavailable, incomplete or stale evidence is not a passed
   prerequisite. Revalidate after material artifact changes; a new revision
   needs an explicit applicability check before prior evidence can be reused.
7. Execute the bounded checkpoint and return the existing EXECUTION_RECEIPT
   with sector, phase, revision, sources_loaded, conditional_sources_loaded and
   validation_scope. Keep results in the Task, not in the router JSON.

Missing REQUIRED source/anchor/skill uses `mandatory_reference_missing` and
stops that checkpoint. Unknown sectors, owners, dependencies, cycles or
contradictory applicability stop contract resolution. Conflicts between
Task/spec/code use `source_of_truth_conflict`; do not silently pick one.
An active conditional source becomes mandatory. If its condition cannot be
determined and affects a required claim, request context before proceeding.

For insufficient context, send `CONTEXT_EXPANSION` using the existing handoff:
`reason`, `required_source`, `blocking_claim`. The Harness resolves the request.
Full Task reading is allowed for an actual conflict, a governing source rule,
necessary global context or explicit Harness instruction, with the reason
recorded; it is not the default fallback.

## Phases, states and final gate

Planning QA/Security/UI may proceed before implementation when their own
prerequisites are met. Planning completion never satisfies final validation
`depends_on` and never closes the sector's final result. Do not union the two
graphs: phase ordering can differ without requiring a second state engine.

Reuse PENDING, READY, RUNNING, VALIDATING, REWORK, BLOCKED, COMPLETED.
PASS is a validation outcome mapped to COMPLETED only with owner evidence.
PARTIAL and NOT_VALIDATED cannot complete REQUIRED work; FAILED maps to REWORK
or BLOCKED with cause. N/A is applicability, not a successful test, and a
justified N/A does not block or become a required dependency.

The final Harness gate requires every other REQUIRED sector to have current,
scope-matching owner SKILL_RECEIPT and EXECUTION_RECEIPT, executed mandatory
validation, satisfied acceptance criteria, and no unresolved blocker. Only
then may the Harness close its own gate with reconciliation evidence. PENDING,
REWORK, BLOCKED, PARTIAL or NOT_VALIDATED in any REQUIRED sector prevents Task
COMPLETED. PR consistency, required documentation and human acceptance gates
remain mandatory. Code completion alone cannot bypass QA or another owner.

## Compatibility and installed hosts

Without `sectors`, v1 is valid legacy input: Harness derives a bounded handoff
from existing scope/specs, records the routing decision in the Task when work
resumes and does not bulk-migrate inactive contracts. Never assume unknown
sector fields were consumed by an older installed plugin; verify support.

Resolve this reference from the active `dev-workflow-standard` skill's
`references/context-routing.md`. Monorepo paths in documentation are source
locations, not assumptions about sibling versioned plugin caches. If the active
bundle lacks it, use an explicitly available canonical checkout or return the
missing capability to the Harness. Do not silently install or imitate it.

| Previous responsibility | Location after extension |
| --- | --- |
| Flat required skills/specs/docs | Preserved v1 indexes; sector-specific source routing for new contracts |
| Banco/API/Frontend task sections | Ten-row matrix plus details only for REQUIRED sectors |
| Generic QA checklist | QA sector and qa-testing-standard; UI/Security retain their own evidence |
| Large task handoffs | Identifiers, phase, sector, revision and dependency receipt paths |
| Mutable progress | Human Task ledger and existing receipts, never contract JSON |

Structural tests and scenario reviews validate these documents and fixtures;
they are not an automated runtime enforcement engine or proof of future LLM
behavior. Context economy is qualitative unless measured: Harness reads the
whole Task; a specialist omits unrelated sectors, sources and receipts.
