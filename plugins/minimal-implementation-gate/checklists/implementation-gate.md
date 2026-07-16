# Minimal Implementation Gate Checklist

Use after human task approval and before coding.

## Check

- Does the task include the required UI Interaction Matrix, Backend Contract,
  Security Spec Contract, Traceability Matrix, required tests, `locked_paths`,
  and acceptance criteria for its scope? If not, return `REVISAR TASK`.
- Does the task really need new code? Evidence required: current file/component/
  service/pattern inspected and why reuse is insufficient.
- Does the repo already have a helper, component, service, pattern or utility
  that solves it? Name the path or mark `NAO ENCONTRADO` with search evidence.
- Does the language or standard library solve it? Name the API or mark `N/A`.
- Does the framework solve it? Name the framework feature or mark `N/A`.
- Does the browser, runtime or database solve it natively? Name the feature or
  mark `N/A`.
- Does an already-installed dependency solve it? Name the dependency and where it
  is already used, or mark `N/A`.
- Can the solution use fewer files without dropping any UI/backend/security/
  traceability row? List the rows preserved.
- Can the solution use fewer layers without changing behavior, authz, data
  integrity, observability or acceptance evidence? List the affected rows.
- Does the solution avoid future abstractions with no real case? Name the
  abstraction avoided.
- Are security, tests, logs, validations, accessibility and business rules kept?
  Link each one to a task/spec row or mark `N/A` with reason.

## Output

- Caminho minimo recomendado
- Arquivos que podem ser reutilizados
- Arquivos novos realmente necessarios
- Dependencias proibidas ou desnecessarias
- Contratos preservados
- Evidencias exigidas para liberar o corte
- Criterios minimos para implementacao
- Recomendacao: `LIBERAR IMPLEMENTACAO` or `REVISAR TASK`
