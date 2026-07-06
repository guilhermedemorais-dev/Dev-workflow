# Prompt: Minimal Code Review

Use the PR diff, approved task, mandatory specs and evidence. Review only for
unnecessary complexity and overengineering. Do not replace security, UI/UX, QA
or correctness review.

Return:

1. Complexidade adicionada
2. O que pode ser removido
3. O que deve permanecer por seguranca/qualidade
4. Riscos de simplificacao excessiva
5. Recomendacao: `APROVAR`, `REWORK` or `ESCALAR DECISAO`
