# Workflow Governance

Read only when selected by the owning SKILL.md route. Backtick paths beginning
with `references/` are relative to that skill directory, not this file.

## Task And Execution Context

Keep five execution artifacts distinct:

- **Human Task:** the complete GitHub Issue/card for human reading, including a
  glanceable summary, collaborative Discovery/SDD, normative requirements,
  microtasks, sector matrix, links, progress and evidence. A local Markdown is
  a mirror/fallback, never a replacement for an available Issue.
- **Execution Contract:** v2 structured LLM representation at
  `docs/execution/TASK-XXX.json`, with **normative equivalence** to the Human
  Task under the same `contract_revision`. Mutable evidence remains outside it.
- **Specs:** detailed functional and technical source of truth, loaded when the
  active scope requires them.
- **Execution Receipt:** evidence produced after the capability actually ran;
  it is never an execution input.
- **Execution Report Comment:** concise chronological human summary published
  to the linked GitHub Issue at material checkpoints; it never replaces the
  task, receipt, validation, Project state, or PR.

New NORMAL/COMPLEX executable tasks require a valid Execution Contract. A legacy task without
one remains readable, but must be normalized before it re-enters execution. Do
not mass-migrate inactive historical tasks.

Before sector delegation load `references/context-routing.md`. New contracts
use v2 with references, design context, microtasks and all ten sectors. Legacy
v1 remains readable. Every sector has REQUIRED/N/A, owner and dependencies,
and every N/A has a verified reason.
Each source has a purpose; CONDITIONAL adds a condition and OPTIONAL never
loads automatically. Separate planning prerequisites from final validation.
CODE_COMPLETE != TASK_COMPLETE; NO_EVIDENCE != PASS;
SECTOR_REQUIRED != OPTIONAL; OUTSIDE_OWNER != AUTHORIZED_TO_PASS;
CONTEXT_AVAILABLE != CONTEXT_REQUIRED. Only each owner attests its own PASS.
Harness reconciles all REQUIRED sectors, current receipts and criteria before
closing the Task. Missing sources, unresolved IDs/cycles or source conflicts
stop the affected checkpoint. This routing is a local extension, not an engine.

## Mandatory Task Governance

### Complete module as the default Task unit

Use one complete Task per functional module within the approved demand. A
module is a coherent business capability with an end-to-end outcome, not a
technical layer, workflow phase, specialist assignment or arbitrary folder.
For changes to an existing module, cover the requested outcome completely;
do not expand scope to rebuild unrelated parts of that module.

Keep spec, database, backend, frontend, TDD, independent QA, security and
documentation as microtasks and gates inside the same Task. Preserve sector
owners, dependencies, evidence and justified N/A. Size, token budget, context
limits, specialist handoffs and review convenience do not justify separate
Tasks; use internal microtasks and resumable checkpoints instead.

Require Markdown checkboxes (`- [ ]`) for each actionable checklist item in
every stage, microtask and REQUIRED sector. Complex items may have nested
checkbox subitems within the same Task; this internal decomposition is allowed
and does not create separate Tasks or Issues. Check `- [x]` only after the
responsible owner records completion evidence. A parent stays unchecked until
all applicable children are evidenced; blocked or unvalidated items stay
unchecked with their reason. Checked items do not approve a sector, Issue,
merge or deploy automatically. Keep progress in the Human Task and evidence
ledger, not as mutable checkbox state in the normative JSON.

Each execution checklist/list has one prompt containing a clickable link to
the Task's single JSON file and its `list_id`, not a prompt per item/subitem.
Keep all list objects in `execution_lists` inside that same canonical file,
with the Task's shared context. Never embed JSON in the Human Task or create
one JSON file per list. This applies to microtask, stage and sector lists.
Give each list a stable ID, owner and phase; task identity/revision come from
the shared file. Use a real local-file link or versioned GitHub file link,
not a link to an Issue or an invented URL.
Validate list completeness, owner, dependencies and inherited scope/constraints
before handoff. See `references/context-routing.md` for the transport contract.
Harness compares the complete Human Task and canonical JSON. Specialists read
the list JSON and necessary canonical JSON fields, their skill, mandatory
sources and relevant code, not the Human Task as an execution input. Missing
context returns to Harness for a corrected JSON handoff; do not send the human
card as a substitute. Human approval gates are recorded only when observed.

Before requesting Task generation and before accepting its output, inspect
proposed and relevant existing Tasks by module, scope and acceptance outcome,
not titles alone. If Tasks for the same module are separated only into
"spec", "backend", "frontend", "QA" or "implementation" (including synonyms
or renamed fragments), stop generation/handoff and require consolidation into
one complete module Task. Report the affected IDs/titles, missing end-to-end
coverage and required consolidation. Do not mark the plan ready or silently
approve, close or rewrite existing Issues.

The only separation exceptions are production migration, cutover, destructive
operation, or a genuinely independent delivery requiring its own authorization
and rollback. Require a documented boundary, independent acceptance criteria,
dependencies, explicit authorization gate and rollback plan for each exception;
a different owner, phase or layer is not an independent delivery. An ordinary
development schema migration remains a microtask of its module.

This is a pre-generation and output-validation criterion. Keep the existing
Task template structure and existing contract fields; add execution_lists in
the single canonical JSON file for list routing, preserving legacy reads. Render its
action checklists with checkboxes and nested items when needed. Apply it to the active
demand; do not mass-migrate historical Tasks.

Every non-trivial feature must follow the official order: sufficient intent or
spec first, executable task second, implementation third. The orchestrator
rejects any task that lacks the artifacts required by its complexity tier,
mandatory fields, or objective review criteria.

A valid task must contain, at minimum:

- Título
- Status visual
- Tipo
- Prioridade
- Objetivo
- Specs obrigatórias
- Docs obrigatórios
- Execution Contract
- Arquivos e módulos permitidos
- Fora do escopo
- Estado atual encontrado
- Resultado esperado
- Regras obrigatórias da implementação
- Checklist de execução
- Prompt para o executor
- Condições de parada
- Testes obrigatórios
- Evidências esperadas no PR
- Critérios de aceite
- Banco
- API/Backend
- Frontend/UI
- Validação
- Riscos/Lacunas
- Resultado da execução
- Matriz de Validação por Setor, Fontes globais da verdade, Ordem de Execução
- Registro de Evidências, Gate do PR, Gate Final, Aceite Humano

Legacy layer names remain recognizable; for new tasks the ten-sector matrix
replaces redundant N/A detail sections. Required sectors use the canonical SDD
block with purpose-based sources, expected evidence and owner results.

The task filename remains stable for traceability. Do not put visual status,
emojis, Kanban status, or transient workflow state in the physical filename.
Status belongs in the task content only.

## Official Kanban Method

Use these columns as the global workflow status:

1. Backlog
2. Discovery / SDD
3. Ready for Dev
4. In Progress
5. Validation
6. In Review
7. Awaiting Final Approval
8. Done

Column means process step. Label means condition or classification. Do not create
a blocked column. A blocked card stays in its current column with the `blocked`
label and a blocker recorded in the task. If review fails, move the card back to
`In Progress` and add the `rework` label until the rework is resolved.

Recommended labels:

- `blocked`
- `needs-info`
- `rework`
- `high-priority`
- `bug`
- `feature`
- `tech-debt`

## Definition of Entry / Exit

Definition of Entry is what must be true before a card enters a column.
Definition of Exit is what must be true before a card leaves a column. The
orchestrator must use these definitions as gate checks.

| Column | Definition of Entry | Definition of Exit |
| --- | --- | --- |
| Backlog | Demand, bug, idea, or risk captured as an item. | Item has enough context to enter Discovery / SDD, or is intentionally rejected/archived. |
| Discovery / SDD | Backlog item selected for clarification, source-of-truth review, and spec work. | Required specs exist, scope is clear, risks are known, and an executable task can be created. |
| Ready for Dev | Executable task exists, mandatory specs are linked, allowed files/modules are defined, branch is suggested, acceptance criteria and tests are clear. | Executor starts the approved task and updates task status to `🟡 Em andamento`. |
| In Progress | Executor accepted the task, read its list JSON, canonical JSON context and required sources, and is implementing only the approved scope. A material `RUNNING`, `REWORK`, or `BLOCKED` checkpoint is reported to the linked Issue when available. | Implementation and developer evidence are ready for independent validation. |
| Validation | Technical review package links task, specs, evidence and receipt; relevant implementation is available. | Required specialist validations pass and review package is prepared for PR. |
| In Review | PR exists with task, specs, evidence, receipt, and applicable Issue report linked. A `VALIDATING` report records the review handoff. | CI and required reviews pass; advance to Awaiting Final Approval, or return to In Progress with `rework` and an actionable report. |
| Awaiting Final Approval | Required technical validations pass and human decision is pending; identify whether this is a local package or published PR. | Human approval and human merge are observed; no automatic merge. |
| Done | Human merge observed, required validations evidenced, and no unresolved blocker remains. | No normal exit; archive only when historical tracking is no longer useful. |

A local `COMPLETED` execution checkpoint is not a merged Task or permission to
move its card to Done. Default maximum is three automatic rework cycles, then
stop with diagnosis and `BLOCKED`; do not retry unchanged permission failures.

## GitHub-Ready Task Structure

Do not assume GitHub Projects, Issues, or boards are available. Prepare each task
so it can be mapped later without restructuring:

- one issue per task when the project uses GitHub Issues;
- labels from the recommended label set above;
- optional milestone when the task belongs to a phase, release, or checkpoint;
- branch sugerida recorded in the task;
- status field consistent with the official Kanban columns;
- explicit fields for responsável, bloqueios, specs obrigatórias, branch
  sugerida, evidências, issue criada/vinculada, and `Pronto para GitHub Projects`.

## Recommended Task Template

Use `plugins/sdd-spec-factory/templates/task-template.md` and its matching
`execution-contract-template.json`; do not maintain a second template here.
Resolve the active SDD bundle in installed hosts, not a sibling cache path.
The template keeps identity/status, ten sectors, scoped source purposes,
acceptance, execution order, evidence and human gates. Only REQUIRED sectors
need detailed sections. See `references/context-routing.md` for compatibility.

## Review Rules

When a PR comes back, the orchestrator reviews before approving:

1. PR points to task, issue, branch and the specs it followed.
2. Implementation matches the specs and the task's acceptance criteria.
3. Nothing was built outside the task scope; out-of-scope changes are justified.
4. `ui-ux-standard` validated the UI (when there is UI).
5. `security-standard` validated security (when the triggers above apply).
6. Tests required by the task exist and pass, with evidence.
7. Status reported by `Banco`, `API/Backend`, `Frontend/UI`; unvalidated areas
   marked `NAO VALIDADO`.
8. `EXECUTION_RECEIPT` proves the selected capability actually ran and produced
   inspectable output.
9. `SKILL_RECEIPT` proves every mandatory skill and reference was read.
10. `REUSE_INVENTORY` proves existing symbols, helpers, components, routes and
   sibling implementations were searched before new ones were created.
11. `MINIMAL_CODE_GATE` explains every new abstraction and confirms that no
    equivalent implementation was duplicated.
12. `EXECUTION_REPORT_COMMENT` matches the task, receipt, Project state, and PR
    when applicable; its remote URL/identifier proves publication. The comment
    never substitutes for receipt or validation evidence.
13. QA_STATUS from the independent QA owner, when REQUIRED, includes executed
    validation and bug/retest disposition. Every REQUIRED sector is reconciled;
    stale receipts, missing evidence or PARTIAL/NOT_VALIDATED prevent completion.

Then: **approve** for human review (not automatic merge/deploy) or **request rework** with specific,
spec-anchored reasons. Rejected review moves the card back to `In Progress` with
the `rework` label until corrected.
