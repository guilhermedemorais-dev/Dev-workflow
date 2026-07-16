# Prompt: Minimal Code Review

Use the PR diff, approved task, mandatory specs and evidence. Review only for
unnecessary complexity and overengineering. Do not replace security, UI/UX, QA
or correctness review. A simplification is invalid if it removes or weakens any
UI Interaction Matrix row, Backend Contract row, Security Spec Contract row,
Traceability Matrix row, required test, permission state, log/audit requirement,
acceptance criterion or `locked_path` boundary.

Return:

1. Complexidade adicionada
2. O que pode ser removido
3. O que deve permanecer por seguranca/qualidade
4. Riscos de simplificacao excessiva
5. Linhas de contrato preservadas ou violadas
6. Recomendacao: `APROVAR`, `REWORK` or `ESCALAR DECISAO`
