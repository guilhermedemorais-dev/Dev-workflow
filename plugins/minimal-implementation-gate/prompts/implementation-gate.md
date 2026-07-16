# Prompt: Minimal Implementation Gate

Use the approved task, mandatory specs and real repo context. Find the minimum
correct implementation path before any code is written. Do not recommend a cut
unless you prove that every applicable UI Interaction Matrix row, Backend
Contract row, Security Spec Contract row, Traceability Matrix row, required
test, acceptance criterion and `locked_path` remains satisfied.

If the task lacks those contracts for an applicable surface, return
`REVISAR TASK` instead of guessing.

Return:

1. Caminho minimo recomendado
2. Arquivos que podem ser reutilizados
3. Arquivos novos realmente necessarios
4. Dependencias proibidas ou desnecessarias
5. Contratos preservados, com IDs/linhas
6. Evidencias exigidas para liberar o corte
7. Criterios minimos para implementacao
8. Recomendacao: `LIBERAR IMPLEMENTACAO` or `REVISAR TASK`
