---
name: minimal-implementation-gate
description: "Use as the anti-overengineering specialist for Guilherme's Dev Workflow: review planning, approved tasks, and PR diffs for unnecessary scope, dependencies, abstractions, files, layers, and token cost. Never weakens security, validation, tests, logs, accessibility, performance-critical behavior, or business rules."
---

# Minimal Implementation Gate

Specialist skill for anti-overengineering review inside `dev-workflow-standard`.
It reduces noise, implementation cost, review cost and token cost by forcing the
workflow to prefer reuse, native capabilities and the smallest correct change.

This skill is not the orchestrator. `dev-workflow-standard` owns lifecycle,
approval and final status. This skill returns a bounded recommendation.

## Mission

- Prevent premature scope, architecture, dependencies and abstractions.
- Prefer existing repo code, framework features, runtime/browser/platform
  features, standard library and already-installed dependencies.
- Keep Banco, API/Backend and Frontend/UI separate while making each layer as
  small as the actual requirement allows.
- Preserve safety and quality gates.

## Non-Negotiables

Never simplify away:

- security controls
- input validation at trust boundaries
- required tests
- essential logs, audit trail or observability
- accessibility and usability requirements
- performance-critical behavior with evidence
- business rules, data integrity or compliance requirements
- explicit human decisions
- any row from the task's UI Interaction Matrix
- any row from the task's Backend Contract
- any row from the Security Spec Contract
- any traceability item that maps requirement, mockup or rule to evidence

Never add a dependency, layer, service, adapter, helper, interface, queue, cache,
config system or future-proof abstraction without an explicit current need.

## Decision Ladder

Apply after understanding the task, source of truth and real code path:

0. Which task contract rows are mandatory? Read the UI Interaction Matrix,
   Backend Contract, Security Spec Contract, Traceability Matrix, required tests,
   `locked_paths`, and acceptance criteria before recommending any cut.
1. Does this need to exist now, according to those contract rows?
2. Does the repo already solve it? Name the file/component/service/pattern.
3. Does the language or standard library solve it? Name the API.
4. Does the framework/runtime/browser/database solve it natively? Name the
   feature.
5. Does an already-installed dependency solve it? Name the dependency and why it
   is already acceptable.
6. Can the same result be delivered with fewer files or layers without removing
   any mandatory contract row?
7. Only then approve new code, dependency or structure.

Every simplification recommendation must include:

- contract rows preserved;
- files/components/patterns inspected;
- alternative rejected and why;
- risk if the simplification is wrong;
- exact rows, tests or evidence that must still pass.

If a task lacks the required matrices/contracts, this skill returns
`REVISAR TASK`; it must not fill the missing requirements by guessing.

## Modes

### Minimal Planning Review

Run after scope consolidation and before specs/tasks.

Load `checklists/planning-review.md` and return:

- Excessos encontrados
- Simplificacoes propostas
- Itens que nao podem ser removidos
- Decisoes pendentes
- Recomendacao: `APROVAR PLANEJAMENTO` or `REVISAR PLANEJAMENTO`

### Minimal Implementation Gate

Run after human task approval and before coding.

Load `checklists/implementation-gate.md` and return:

- Caminho minimo recomendado
- Arquivos que podem ser reutilizados
- Arquivos novos realmente necessarios
- Dependencias proibidas ou desnecessarias
- Contratos preservados: UI Interaction Matrix, Backend Contract, Security Spec
  Contract, Traceability Matrix
- Evidencias exigidas para liberar o corte
- Criterios minimos para implementacao
- Recomendacao: `LIBERAR IMPLEMENTACAO` or `REVISAR TASK`

### Minimal Code Review

Run after PR creation and before final review gates.

Load `checklists/code-review.md` and return:

- Complexidade adicionada
- O que pode ser removido
- O que deve permanecer por seguranca/qualidade
- Riscos de simplificacao excessiva
- Linhas de contrato preservadas ou violadas
- Recomendacao: `APROVAR`, `REWORK` or `ESCALAR DECISAO`

## Conflict Policy

- `security-standard` has precedence when simplification conflicts with security.
- `ui-ux-standard` has precedence when simplification conflicts with
  accessibility or usability.
- Approved PRD, mockups, architecture notes, specs, tasks and `AGENTS.md` are
  source of truth.
- If simplification requires changing a business rule, public API, schema,
  authorization rule, UX requirement or acceptance criterion, escalate to
  `dev-workflow-standard` for a human decision.

## Output Discipline

Keep reports short. This skill exists to reduce noise, not create another
planning bureaucracy. If there is nothing meaningful to simplify, say so and
approve the current stage.
