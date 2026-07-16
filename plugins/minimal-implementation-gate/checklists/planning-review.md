# Minimal Planning Review Checklist

Use after consolidated scope and before specs/tasks.

## Check

- Is the plan bigger than the problem?
- Can the MVP be smaller without removing a required UI interaction, backend
  behavior, security control, traceability row, negative test, log or acceptance
  criterion?
- Is there premature architecture? Name the layer/service/abstraction and the
  current requirement that fails to justify it.
- Are integrations proposed without a confirmed requirement, owner, auth model,
  failure mode and test evidence?
- Are dependencies proposed without justification, existing usage and fallback?
- Are layers, services, adapters, helpers or interfaces proposed without a real
  current use?
- Are tasks too large for one reviewable PR?
- Is future scope being implemented now?
- Are Banco, API/Backend and Frontend/UI separated without unnecessary ceremony?
- Can docs/specs be narrower while still preserving the interaction matrix,
  backend contract, Security Spec Contract, traceability and evidence?
- Are `Executor LLM`, handoff mode and `locked_paths` clear enough to avoid
  Codex/Claude collisions?

## Output

- Excessos encontrados
- Simplificacoes propostas
- Itens que nao podem ser removidos
- Contratos que precisam permanecer intactos
- Decisoes pendentes
- Recomendacao: `APROVAR PLANEJAMENTO` or `REVISAR PLANEJAMENTO`
