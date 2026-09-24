# TASK-010: GitHub Repository Governance delivery

## Audit Summary

Baseline `main` sincronizada em `44718fe5faa49cdfde790a51ae6e63ce6c18c050`,
working tree limpa; branch de trabalho `feat/github-governance-bootstrap`.
Baseline executado: 490 testes unittest, exit 0. Issue
[#30](https://github.com/guilhermedemorais-dev/Dev-workflow/issues/30).

DevOps já possuía `gh` e referências operacionais; Environment já resolvia tools
por owner; Harness já possuía capability registry, setores e receipts. Não havia
helper de governança no checkout canônico. O `github-bootstrap.sh` do worktree
V2 histórico não foi importado: force labels, limite de busca, IDs no YAML e
ausência de diagnose/verify contrariavam o contrato atual.

## Consolidated Practice Check

| Classificação | Aplicação |
| --- | --- |
| OFFICIAL PRACTICE | CLI/API GitHub, OAuth/scopes, settings, Projects e regras, fontes na referência |
| ECOSYSTEM CONVENTION | Idempotência, diff revisável, mínimo privilégio e readback |
| PROJECT CHOICE | Oito etapas Kanban, merge humano, DevOps como owner, JSON stdlib |
| LOCAL EXTENSION | Desired/proposal schema, fingerprints e resultado de readiness |

## Architecture

Extensão de `devops-standard`, sem nova skill, daemon, OAuth ou instalador.
Um helper determinístico e seu template; `gh` reutilizado no registry existente.
Environment prepara ferramentas, DevOps opera governança, Security revê fronteiras,
QA verifica comportamento e Harness reconcilia evidências. Registry de tools e
runtime state não foram duplicados.

## Developer Roadmap

README fornece fases 0–10: instalar Harness, preparar ambiente, conectar GitHub,
validar permissões, diagnosticar, revisar, confirmar/aplicar, preparar Project/CI,
verificar e reconciliar PROJECT READY. Onboarding não se repete a cada Task;
drift, mudança relevante, falha ou pedido explícito invalidam evidência anterior.

## Authentication Flow

Sem gh, handoff Environment; sem auth, USER_ACTION_REQUIRED e login pelo terminal
do desenvolvedor. CLI usa autenticação existente. Consultas Project podem exigir
read:project, escrita project; obter apenas o necessário. Nunca solicitar token
no chat. Login não concede admin, org membership ou edição do Project.

## Desired State

`.github/governance.json` no projeto-alvo, schema v1; template dentro de DevOps.
JSON evita dependência YAML adicional e é equivalente ao exemplo permitido no
pedido. Desired state é política versionada, sem tokens, IDs ou estado efêmero.
Nenhuma configuração de governança foi criada na raiz deste próprio plugin.

## Operations

`diagnose`, `propose`, `verify` somente leitura; `apply --confirm` requer proposta
revisada vinculada ao alvo e estado relevante. Recalcular operações permitidas
evita executar comandos arbitrários inseridos na proposta. Drift exige nova
proposta/confirmação; falha parcial não recebe sucesso nem rollback destrutivo.

## Repository Governance

Arquivos locais revisáveis, templates Issue/PR, CODEOWNERS, CONTRIBUTING e docs.
Settings/labels são reconciliados sem merge; equivalência e ambiguidade tratadas
antes de criação. Arquivo CODEOWNERS presente não equivale a enforcement.

## GitHub Project

Reuso por owner/título, paginação, IDs descobertos e opções preservadas. Oito
etapas alinhadas no Harness e templates, `blocked` como label, Done reservado ao
merge humano. View board disponível na API atual; agrupamento Status e auto-add
exigem evidência/manual quando não configuráveis pela API pública. Workflows
default closed→Done precisam revisão para não contornar o gate humano.

## CI/CD

Detecção de stack e comandos existentes, sem executar scripts na fase de leitura.
Novo YAML não certifica execução. Checks obrigatórios vêm de evidência observada;
CI verde não substitui Security nem autorização de produção.

## Plan Capability Detection

Tipo de owner, visibilidade, plano disponível e resposta específica são evidência
separada. 403/404 genérico não prova limitação do plano. Regras efetivas da branch
são distintas de ruleset criado/evaluate; fallback precisa aprovação explícita e
não deve se passar por enforcement.

## Idempotency

Read/reconcile/readback, preservar recursos alheios e identidades, adicionar apenas
faltantes e bloquear duplicatas ambíguas. Nova proposta após mudança; repetir uma
proposta antiga não é caminho de idempotência. Ensaio remoto de segunda execução
permanece NOT VALIDATED até autorização futura.

## Safety

Sem credenciais versionadas, instalação, login automático, push, PR, merge ou
deploy. Aplicação em repo real fora do escopo desta entrega. Proposta/relatório
podem conter metadados privados, devem ser protegidos. Evidência manual é
separada de aprovação de fallback; configuração desconhecida não vira PASS.
Security independente [PASS local](security/reviews/TASK-010-github-governance.md),
com exposição de conteúdo antigo corrigida e retestada. O diff omite linhas
antigas, mantém hash dos bytes e exige inspeção local pelo aprovador; guardas de
segredos reconhecíveis não equivalem a um scanner universal. QA independente
[PASS local](qa/TASK-010-review.md), 539 testes totais, 47 focados e seis probes
suplementares. Harness reconciliou ambos os receipts no mesmo hash do helper.

## README

Adicionado roadmap humano, diagrama, auth assistida, quatro operações, desired
state, Project/CI/readiness, limites e prompt utilizável. Mantido manual de API
na referência DevOps. Templates e testes atualizados para oito etapas, sem
migração artificial de Tasks históricas para Done.

## Tests

- Baseline: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`,
  exit 0, 490 testes.
- README RED: teste de roadmap/referência antes da edição, exit 1, duas falhas
  esperadas por ausência das seções; GREEN mesmo arquivo, exit 0, 34 testes.
- Harness: `python3 -m unittest discover -s tests -p test_dev_workflow_skill.py -q`,
  exit 0, 103 testes após migração explícita dos oráculos de seis para oito etapas.
- Implementation: mesmo discover com `test_dev_implementation_skill.py`, exit 0,
  70 testes; execution-report com `test_execution_report_template.py`, exit 0,
  64 testes.
- Validador skill-creator, Harness: exit 0, `Skill is valid!`.
- Helper: `python3 -m unittest discover -s tests -p test_github_governance.py -q`,
  exit 0, 47 testes no reteste independente Security. SHA-256 final do helper:
  `7fa330927f7136bdfda0d34c6da98ad5bc1bf1be60c83c9b55d36850cb32c46f`.
- Suíte final pelo Harness:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`, exit 0,
  **539 testes em 43.010s**. Inclui validators estruturais do repositório,
  contratos, registries, plugins, links e regressões existentes.
- Reteste documental final: discover `test_readme.py -q`, exit 0, 34 testes;
  `test_devops_standard.py -q`, exit 0, 18 testes.
- Validador `skill-creator/scripts/quick_validate.py` para Harness e DevOps,
  exit 0 ambos. `python3 -m json.tool` para TASK-010.json e template governance,
  exit 0 ambos. `git diff --check`, exit 0.
- Duas rodadas consolidadas de rework preservadas nos relatórios. Probes de QA
  encontraram lacunas mesmo com suíte verde; os testes de regressão foram
  adicionados, não enfraquecidos para produzir PASS.

## Manual Integration Test

Procedimento na referência DevOps: repo privado descartável autorizado, estado
inicial registrado, diagnose/propose/revisão/apply/verify, ajustes manuais e CI
autorizados separadamente, segunda proposta/aplicação sem duplicatas. Sem
exclusão automática de cleanup. Não executado nesta task.

## Git

Branch `feat/github-governance-bootstrap`; gate local PASS de todos os setores
REQUIRED libera o commit autorizado, cujo HEAD será informado no handoff final.
Nenhum push/merge/instalação acompanha esta entrega. O pacote local aguarda
aprovação humana, não equivale a card Done ou repositório remoto pronto.

## Remaining Risks

API/plano/permissões e Projects reais não foram exercitados. Fixtures não provam
interoperabilidade remota. Mudanças concorrentes e falhas parciais exigem novo
diagnóstico. Limitações de API e ações manuais permanecem explícitas, sem falsa
alegação de prontidão de produção ou de instalação atualizada no host.
GitHub.com é o único host homologado pelo schema atual. Escrita local testada em
Linux/POSIX; falta de primitivas seguras bloqueia antes de mutação, sem prometer
suporte Windows. Evidência manual é observação humana confiada, não atestação
criptográfica nem prova buscada automaticamente no GitHub. Outros gerenciadores
ou stacks ambíguas exigem decisão manual; pins de Actions foram verificados nos
upstreams oficiais, mas não são uma alegação de que sejam as releases mais novas.
