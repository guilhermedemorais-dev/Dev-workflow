# Minimal Code Review Checklist

Use after PR creation and before final review gates.

## Check

- Did the code add unnecessary complexity?
- Is logic duplicated?
- Were helpers, services, adapters, interfaces or files created prematurely?
- Was a dependency added without a current need?
- Is there dead or "future" code?
- Was a native, framework, runtime or stdlib solution ignored?
- Would simplification weaken security, tests, logs, accessibility or business
  rules?
- Does the PR respect the approved spec and task?
- Can review/token cost be reduced by deleting or consolidating code?

## Output

- Complexidade adicionada
- O que pode ser removido
- O que deve permanecer por seguranca/qualidade
- Riscos de simplificacao excessiva
- Recomendacao: `APROVAR`, `REWORK` or `ESCALAR DECISAO`
