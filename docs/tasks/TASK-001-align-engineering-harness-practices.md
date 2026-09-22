# Align Engineering Harness with consolidated agent practices

## Status visual
- Status visual: 🟢 Concluída
- Status Kanban: In Review
- Responsável: Codex
- Issue criada / vinculada: https://github.com/guilhermedemorais-dev/Dev-workflow/issues/12
- Branch sugerida: `refactor/harness-practice-alignment`
- Executor LLM primário: Codex
- Executor secundário/revisor: human reviewer
- Modo de handoff: Codex local
- Status da claim: done
- Claim por: Codex
- `locked_paths`: `AGENTS.md`, `README.md`, `docs/`, `plugins/dev-workflow-standard/`, `plugins/sdd-spec-factory/skills/sdd-spec-factory/SKILL.md`, `tests/`
- Conflitos conhecidos: none at task start; working tree was clean
- Labels sugeridas: enhancement
- Pronto para GitHub Projects: sim

## Tipo
Refactor / Docs / QA

## Prioridade
P1

## Objetivo
Apply the approved practice-alignment spec with the smallest coherent change.

## Specs obrigatórias
- `docs/specs/engineering-harness-review/module-spec.md`

## Docs obrigatórios
- `README.md`
- `docs/workflow-pipeline.md`
- `plugins/dev-workflow-standard/skills/dev-workflow-standard/SKILL.md`
- every reference linked by the central skill
- all specialist `SKILL.md` files

## Arquivos e módulos permitidos
Only the paths in `locked_paths`.

## Fora do escopo
Repository/package renames, new dependencies, runtime product code, deployment,
and redesign of specialist skills unrelated to the audited contradictions.

## Estado atual encontrado
- `EXECUTION_RECEIPT` appears before implementation in central diagrams.
- Full SDD language is mandatory even when OpenAI explicitly distinguishes
  lightweight small-change plans from complex execution plans.
- Local convention names are presented without a clear classification boundary.
- No root `AGENTS.md` exists.
- Baseline: 285 tests run, 4 failures caused by stale wording assertions.

## Resultado esperado
Consistent lifecycle semantics, proportional planning, explicit provenance,
short agent map, durable audit matrix, and a green structural test suite.

## Gates
- Ambiguity: PASS, the user supplied explicit constraints and desired output.
- Spec completeness: PASS for a documentation/test refactor.
- UI interaction: N/A, no UI.
- Backend contract: N/A, no backend.
- Security contract: N/A, LOW-risk documentation/test changes only.
- Traceability: requirements map directly to changed docs and structural tests.

## Minimal Planning Review
- Reuse current README, workflow docs, references, and Python unittest suite.
- Create only three durable artifacts with distinct owners: agent map, audit,
  and this spec/task contract.
- Do not add dependencies, scripts, services, or new plugin boundaries.
- Recommendation: APROVAR PLANEJAMENTO.

## Minimal Implementation Gate
- Reuse existing documents and tests.
- New files justified: `AGENTS.md` for progressive-disclosure entry; audit matrix
  for requested durable findings; spec/task required by repository governance.
- Preserve all security, UI, PR, human approval, and evidence gates.
- Recommendation: LIBERAR IMPLEMENTACAO.

## Testes obrigatórios
- `python3 -m unittest discover -s tests -v`
- link/path checks implemented in the structural suite
- `git diff --check`

## Critérios de aceite
- All criteria in the linked module spec pass.
- No unrelated files change.
- Validation commands and exit codes are recorded below.

## Banco
N/A.

## API/Backend
N/A.

## Frontend/UI
N/A.

## Validação
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
  - exit code: 0
  - result: 289 tests passed
- `git diff --check`
  - exit code: 0
  - result: no whitespace errors
- JSON manifest validation with `python3 -m json.tool`
  - exit code: 0
  - result: every marketplace/plugin manifest parsed successfully
- Cross-file stale-rule scan
  - result: only historical audit/task descriptions matched; one remaining
    `CTO/orchestrator` role label was corrected to `Engineering Harness`

## Riscos/Lacunas
- External practices guide principles, not this repository's exact vocabulary.
- Provider-specific behavior can drift and must remain linked to primary docs.

## Resultado da execução

### SKILL_RECEIPT
- `dev-workflow-standard`: loaded with all routed execution references.
- `sdd-spec-factory`: loaded; produced this focused spec/task contract.
- `minimal-implementation-gate`: loaded; approved reuse-only change.
- `dev-implementation-standard`: loaded; execution stayed inside `locked_paths`.
- `ui-ux-standard`: loaded for repository audit; runtime UI gate N/A.
- `security-standard`: loaded for repository audit; LOW-risk focused review.

### REUSE_INVENTORY
- searched paths: README, workflow docs, five canonical skills, all central
  references, manifests, and the complete test suite
- decision: EXTEND existing owners; create only agent map, audit, spec, and task
- dependencies added: none

### MINIMAL_CODE_GATE
- result: PASS
- reused: existing docs, references, manifests, and unittest structure
- new units: durable artifacts requested by the workflow and audit
- speculative abstractions: none

### EXECUTION_RECEIPT
- task_id: TASK-001 / Issue #12
- capability: documentation and structural-test implementation
- provider_or_runtime: Codex local workspace
- executor: Codex
- state: COMPLETED, ready for human review
- invocation_evidence: repository edits on `refactor/harness-practice-alignment`
- outputs_produced: corrected lifecycle, provenance labels, complexity tiers,
  root agent map, audit matrix, aligned manifests, structural tests
- commands_and_results: unittest exit 0; JSON validation exit 0; diff-check exit 0
- validation_evidence: 289 passing tests and clean whitespace check
- blockers: none
- next_safe_action: human diff review, then commit/PR if approved
