# MODULE SPEC: GitHub Repository Governance

## Status e intenção de produto
Aprovada pelo Harness em 2026-09-24 para implementação local. Deriva do [README](../../../README.md),
[pipeline](../../workflow-pipeline.md) e pedido explícito de evolução DevOps
(71 seções). Não criar outro plugin/skill. Page/component specs N/A, sem telas.

## Diagnóstico e objetivo
Base `44718fe`: DevOps já possui `gh`, referências/templates operacionais;
Environment prepara ferramentas; Harness tem setores/receipts. Busca em scripts
e paths canônicos por governance/rulesets/gh project não encontrou executor
equivalente. Implementar um bootstrap idempotente com diagnóstico, proposta,
aplicação confirmada, verificação e readiness observada.
Nenhuma pergunta bloqueante para implementação local. Capacidades atuais das
APIs GitHub precisam de pesquisa oficial antes de persistir comandos/mutations.

## Escopo
Helper Python 3.11+ stdlib em DevOps, referência técnica, template JSON desejado,
capabilities da entrada `gh` existente, onboarding README, gates/pipeline e
testes fake-gh. GitHub remoto real não será configurado nesta entrega.
Fora: nova skill, OAuth/instalador/cache paralelos, credenciais, produção,
push/PR/merge/deploy, autoaprovação e executar governance contra Dev-workflow.

## Arquitetura mínima
`plugins/devops-standard/skills/devops-standard/scripts/github_governance.py`
é o único executor novo, exigido explicitamente pelo usuário. Skill decide
política; helper inspeciona/calcula/aplica/verifica operações limitadas.
Reusar autenticação `gh`, subprocess sem shell, registries/Environment/receipts
existentes. Não chamar helper de bootstrap de ambiente nem mover owner da tool.

Desired state: `.github/governance.json` no projeto-alvo; template versionado
sob `devops-standard/templates`. JSON substitui exemplo YAML do pedido para
reusar stdlib, sem dependência/parser YAML novo. Schema version 1 com repository,
project, labels, human_gates, automation e configuração local/CI proporcional.
Não conter IDs GitHub, login state, tokens, segredos ou paths de runtime.
Agent branch prefix configurável; defaults nunca sobrescrevem política aprovada.
Schema rejeita campos/tipos inválidos; políticas perigosas como auto_merge ou
auto_deploy não são habilitadas por este recurso.

## Operações e autorização
- `diagnose`: consultar Git/gh/auth, alvo, permissões e configuração observável.
- `propose`: calcular NOOP/CREATE/UPDATE/BLOCKED e diff local/remoto, sem escrever.
- `apply --confirm`: requer proposal revisada fornecida explicitamente, alvo,
  desired state e fingerprints compatíveis; nunca inventa aprovação.
- `verify`: recolher estado novamente e comparar, read-only, reportando evidência.

As três operações read-only não escrevem arquivos/cache, alteram Git, publicam,
disparam workflows nem enviam mutations GraphQL. Proposal pode ser devolvida
em stdout e salva pelo usuário em arquivo privado para revisão. Vincular versão,
repo/host/workspace, hash do desired state e estado relevante local/remoto.
Apply valida schema/operadores permitidos, reconstrói diff com política confiável
e compara com proposal, não executa comandos arbitrários contidos nela.
Drift material após proposta exige nova proposta/confirmação antes de mutar.
Não tornar IDs efêmeros parte do desired state. IDs em proposal/evidência são
observações não secretas descobertas na execução.

## Local e remoto
Preparar conforme stack e decisões: CODEOWNERS, Issue templates bug/feature/task
e config, PR template, quality workflow, CONTRIBUTING e estrutura docs. Somente
arquivos aprovados, paths seguros dentro do workspace, sem seguir symlinks para
fora; conteúdo existente exige diff/revisão, nunca substituição silenciosa.
Labels preservadas/reutilizadas por equivalência normalizada sem duplicação.
Settings squash/delete-branch são baseline proposto, não imposição silenciosa.
Nunca mergear PR, aprová-la, fazer force push ou executar deployment.

## Projects e regras
Buscar Project por owner/título em páginas completas; reutilizar único equivalente,
bloquear ambiguidade, descobrir IDs de Project/campos/opções/itens/views.
Completar status faltantes preservando opções existentes e evitando duplicação.
View Kanban board agrupada por Status e Auto-add `is:issue is:open`, Backlog,
somente via API atual comprovada e autorização. Caso indisponível, instrução
MANUAL_ACTION_REQUIRED precisa e limitação, nunca afirmar configurado.
Vincular Project ao repo quando suportado/aprovado e verificar vínculo.
Rulesets exigem capacidade/enforcement observável, regras aprovadas e checks
reais observados após CI; não inventar nome de check ou reviewer impossível solo.
CODEOWNERS_FILE_PRESENT não significa CODEOWNERS_ENFORCEMENT_ACTIVE.

## Kanban e ciclos
Mudança explícita autorizada do baseline de seis para oito etapas:
Backlog; Discovery / SDD; Ready for Dev; In Progress; Validation; In Review;
Awaiting Final Approval; Done. `blocked` continua label, não coluna.
Validação técnica inicia Validation; PR criada In Review; CI + setores aprovados
Awaiting Final Approval; somente merge humano observado permite Done.
Não mover esta entrega local para Done só porque testes/commit passaram.
Máximo default de três ciclos automáticos de rework; ao atingir limite, diagnóstico
e BLOCKED sem repetir erro de permissão ou esconder problema.

## CI/CD adaptativo
Detectar stack/lockfiles/scripts existentes Node/Next, PHP/Laravel, Python e Go;
usar install locked/native e apenas lint/typecheck/test/build existentes/aplicáveis.
Ambiguidade ou falta de comandos exige proposta explícita/manual, não workflow
universal inventado. Não executar scripts do projeto durante diagnose/propose.
CI gerado não é CI executado; checks requeridos só após evidência real. Security
mantém interpretação de scanners; CI green não certifica Security ou produção.

## Readiness, auth e limites
Separar GH_MISSING/GH_BROKEN de autenticação. Fluxo seguro `gh auth login` ou
refresh oficial de scopes mínimos, sem token em chat/output. Login não comprova
admin, org ou Projects. Falta humana retorna USER_ACTION_REQUIRED, próximo passo
e checkpoint para retomar. Não repetir mutação sem permissão.
Owner type/visibility/plan são contexto; resolver capabilities específicas, não
`free => tudo impossível`. Erro genérico 403/404 não prova limitação de plano.
SUPPORTED, UNSUPPORTED_BY_PLAN, NOT_AUTHORIZED, NOT_CONFIGURED, NOT_VALIDATED
distintos; fallback limitado só vale se explicitamente aprovado e verificado.
READY exige verify executado + environment/auth/acesso/arquivos/config requerida/
Project/CI e gates comprovados; READY_WITH_LIMITATIONS exige fallback governado,
nunca ocultar check obrigatório desconhecido. Outros: AUTH_REQUIRED, BLOCKED,
NOT_VALIDATED. Readiness não é nova máquina de estados global.
Evidência manual deve identificar alvo/revisão, ação observada, resultado,
data e referência verificável; uma atestação vaga não certifica configuração.
Aprovar fallback registra aceitação de limitação, não prova que a etapa manual
executou. Manter essas duas entradas separadas e revalidar configuração observável.

## Banco
N/A, sem modelo/schema/persistência de aplicação.

## API/Backend
N/A endpoint de aplicação. REST/GraphQL GitHub operacional pertence ao DevOps.

## Frontend/UI
N/A, sem interface renderizada.

## Testes
[validation-rules](validation-rules.md) define vinte casos mínimos, negativos de
segurança e regressão. Fake gh sem conta/network GitHub na suíte padrão.

## Segurança
Security REQUIRED: permissões, sanitização, subprocess/input, escrita local e
respostas/erros. Nunca imprimir auth token, stderr bruto, config de credencial ou
traceback sensível; fixtures usam marcadores sintéticos. Não relaxar gates.

## Observabilidade/logs
JSON de resultado + resumo humano, erros categorizados, mutações realmente feitas,
verification/limitações e EXECUTION_RECEIPT existente; sem novo tipo de recibo.

## Target, validação e rollback_strategy
Nesta task: checkout local + diretórios temporários/fake gh. Integração remota
manual somente em repo/organização de teste e após autorização futura explícita.
Apply parcial preserva evidência e para; sem rollback remoto automático destrutivo.
Reverter requer diff/estado anterior e aprovação; algumas operações exigem forward
fix. Nunca prometer atomicidade remota ou deletar recursos para restaurar estado.

## Reuse Inventory / Minimal Code Gate
EXTEND DevOps Skill/gh registry/referências/templates e Harness routing/pipeline;
REUSE Environment, gh auth/API e receipts; CREATE apenas helper determinístico,
desired-state template, testes e artifacts pedidos. PASS de planejamento sujeito
à aprovação Harness. Sem serviço/framework/policy engine genérico.

## Proveniência, riscos e decisões pendentes
[OFFICIAL PRACTICE] comandos/API/plan limits somente após fontes primárias
verificadas e registradas na referência técnica; [ECOSYSTEM CONVENTION]
idempotência/diff/revalidação; [PROJECT CHOICE] oito etapas/human gates/JSON;
[LOCAL EXTENSION] proposal fingerprints e readiness fields.
Riscos: drift, paginação incompleta, aliases/duplicatas, dados sensíveis em erros,
limites API/plano e falsos READY. Integração remota e instalação continuam
NOT VALIDATED nesta entrega. Publicação/merge final dependem de decisão humana.

## Critérios de aceite
RN-01–RN-12/T01–T20 atendidos e testes adicionais; suíte/validators/README PASS;
Security e QA independentes; nenhum side effect remoto; commit só após PASS local.
