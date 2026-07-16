# Prompt: Minimal Planning Review

Use the consolidated scope and source-of-truth docs. Review only for excessive
scope, premature architecture, unjustified dependencies and unnecessary layers.
Any simplification must preserve required UI interactions, backend behavior,
security controls, traceability, negative tests, logs, acceptance criteria,
`Executor LLM` assignment and `locked_paths`.

Return:

1. Excessos encontrados
2. Simplificacoes propostas
3. Itens que nao podem ser removidos
4. Contratos que precisam permanecer intactos
5. Decisoes pendentes
6. Recomendacao: `APROVAR PLANEJAMENTO` or `REVISAR PLANEJAMENTO`
