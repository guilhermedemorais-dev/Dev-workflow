# Minimal Implementation Gate Checklist

Use after human task approval and before coding.

## Check

- Does the task really need new code?
- Does the repo already have a helper, component, service, pattern or utility
  that solves it?
- Does the language or standard library solve it?
- Does the framework solve it?
- Does the browser, runtime or database solve it natively?
- Does an already-installed dependency solve it?
- Can the solution use fewer files?
- Can the solution use fewer layers?
- Does the solution avoid future abstractions with no real case?
- Are security, tests, logs, validations, accessibility and business rules kept?

## Output

- Caminho minimo recomendado
- Arquivos que podem ser reutilizados
- Arquivos novos realmente necessarios
- Dependencias proibidas ou desnecessarias
- Criterios minimos para implementacao
- Recomendacao: `LIBERAR IMPLEMENTACAO` or `REVISAR TASK`
