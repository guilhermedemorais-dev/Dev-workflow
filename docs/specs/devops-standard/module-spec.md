# MODULE SPEC: DevOps Standard

## Status e parent intent

Escopo autorizado pelo pedido de implementação de `devops-standard` e pela
continuação explícita do usuário. Tier: **COMPLEX**. Parent intent: ampliar o
Engineering Harness existente com especialização operacional, sem criar outro
orquestrador. [TASK-006](../../tasks/TASK-006-devops-standard.md), Issue #24.

## Diagnóstico

- Claro: domínio, fronteiras, ferramentas, validações e gates estão definidos.
- Lacuna resolvida: `devops-review` tem metadados restricted/NOASSERTION; não
  copiar seu texto, scripts ou templates. Implementar revisão original pelos
  requisitos do usuário, com proveniência honesta.
- Riscos iniciais: atribuição incorreta, operações destrutivas tratadas como
  validação, duplicação de owners e falso PASS sem runtime.
- Perguntas críticas: nenhuma para o escopo aprovado. Não depende de acesso a
  produção, credenciais, instalação global ou fusão do PR #23.

## Objetivo e escopo incluído

Criar um bundle nativo `plugins/devops-standard`, com três manifestos, skill
canônica compacta, `agents/openai.yaml`, referências por domínio, templates
selecionados, tool registry próprio e integração condicional ao Harness/SDD.
Usar COPY → AUDIT → ADAPT → INTEGRATE para material reutilizável de
`ops-devops-platform`, com revisão exata e avisos aplicáveis preservados.
Documentar conteúdo copiado/adaptado/descartado e extensões locais em ORIGIN.
A referência estrutural Anthropic orienta organização, não substitui o padrão
do repositório. Não inventar templates upstream ausentes.

Domínios: Git avançado/releases, CI/CD, containers, deploy, servidores, IaC,
Kubernetes, GitOps, cloud, observabilidade, backup/DR e incidentes. Conhecimento
grande fica em references/templates; carregar apenas o domínio necessário.
Páginas e componentes visuais: N/A, não há interface de aplicação.

## REUSE_INVENTORY e arquitetura

| Existente confirmado | Decisão |
| --- | --- |
| Harness + capability-registry + harness-execution | Reutilizar router, estados, gates e receipts |
| skill-owned-tools + scripts/tool-state.py | Estender suporte ao novo owner sem outro instalador |
| security-standard tool registry | Manter scanners com owner único |
| SDD templates e required_validations | Adicionar roteamento condicional, manter contrato enxuto |
| Marketplaces Codex/Claude e três manifestos | Reutilizar formato e categoria válida |
| Environment Bootstrap, somente PR #23 fora da main base | Integração pendente, NOT VALIDATED, não recriar |

Base inspecionada: `83e1c7296497c34267d85105f352b460136a09a7`.
Fluxo: Harness → capability owner DevOps → tool/CLI/API/MCP disponível →
execução → validação → EXECUTION_RECEIPT → gate Harness.

## Fronteiras e regras de negócio

- Harness coordena, aprova gates e mantém Git básico: status/diff/fetch/commit/PR.
- DevOps opera e valida infraestrutura/release; implementation mantém código
  da aplicação. UI não recebe responsabilidades DevOps.
- Security mantém AppSec, SAST/DAST, scanners e revisão especializada. IAM,
  secrets, TLS, firewall, portas públicas, privilégios, auth, storage sensível
  e permissões cloud exigem handoff obrigatório.
- Environment, quando existir na base, prepara/detecta tools e MCPs, nunca
  opera produção. Ausente nesta base: usar somente helper existente compatível;
  não criar segunda MCP Library nem declarar integração funcional.
- Projeto nativo primeiro, incluindo Coolify/Portainer/VPS quando já usados.
  Nenhuma cloud, Kubernetes ou migração de plataforma é obrigatória.
- Registry versionado possui 20 ferramentas avaliadas: git, gh, docker, docker
  compose, terraform, tofu, ansible, ansible-lint, kubectl, helm, kustomize,
  argocd, flux, actionlint, act, hadolint, tflint, kubeconform, shellcheck,
  promtool. Terraform/Tofu são alternativas; act é opcional.
- Runtime state é local, ignorado pelo Git. Sem instalação automática em massa,
  sudo silencioso, root ou credenciais em documentos/receipts.
- Estados existentes: PENDING → READY → RUNNING → VALIDATING, FAIL → REWORK,
  PASS → COMPLETED. Não criar DEVOPS_RECEIPT.

## Banco

N/A: nenhuma tabela, migração ou restauração de banco será executada.

## API/Backend

N/A para APIs de produto. Única extensão de runtime permitida é compatibilidade
mínima do helper tool-state existente com o novo owner, se necessária.
Isso inclui executar `run` no `--workspace` solicitado e propagar exit code real
da ferramenta, corrigindo resultados falsamente bem-sucedidos com regressões
comportamentais. Não portar todo o helper da feature Environment.

## Frontend/UI

N/A: nenhuma tela, mockup, componente visual ou QA visual de aplicação.

## Testes e validação por domínio

| Domínio | Caminho exigido na skill, executado somente quando aplicável |
| --- | --- |
| CI/CD | Validação YAML/config, actionlint; act opcional, nunca pipeline de produção para sintaxe |
| Docker | Hadolint, build, smoke/health isolado; Compose config |
| IaC | fmt/check, init quando seguro, validate, plan; apply/destroy não são validação padrão |
| Kubernetes | Render, schema, dry-run contextual, review; sem apply produção automático |
| Ansible | lint, syntax-check, check mode com limitações explícitas |
| GitOps | Render/configuração nativa e review; sync/reconcile mutante exige escopo/gate |
| Servidor | Identificar alvo/estado, backup config, mudança, validador, reload aprovado, health |
| Observabilidade | promtool config/rules; validador nativo Grafana/OTel quando existente |
| Backup/DR | BACKUP_CREATED distinto de RESTORE_NOT_VALIDATED e RESTORE_VALIDATED |

Testar estruturalmente e com fixtures temporárias/execução inofensiva do helper.
Comandos de referência não contam como executados. Ferramenta ausente ou serviço
não exercitado deve ser NOT VALIDATED, sem instalação apenas para forçar PASS.

## Segurança

Antes de risco material: identificar alvo/ambiente/dados protegidos, impacto e
rollback_strategy. Se rollback seguro for impossível, declarar explicitamente
e escalar antes da execução. Gate humano explícito para deploy produção,
migração destrutiva, firewall, DNS destrutivo, IaC apply/destroy, force push,
reset destrutivo, restore de banco produção, excluir cluster, reboot e rotação
de segredos. Aprovação de criar este plugin não autoriza essas operações.

## Observabilidade/logs

Reutilizar SKILL_RECEIPT e EXECUTION_RECEIPT, registrando capability, tool/version,
target_environment, comandos/exit codes, estado inicial/final, mudanças,
validação, rollback e blockers quando aplicáveis. Issue recebe resumo humano,
sem logs grandes, secrets ou dados de clientes.
Findings são candidatos a confirmar/rejeitar/N/A por contexto. Registrar severity
(CRITICAL/HIGH/MEDIUM/LOW/INFO), category (Reliability/Security/Performance/Cost/
Maintainability/Operations/Compliance), evidence, impact, recommended action e
validation. Corrigir em escopo e revalidar; não afirmar PASS manual.
Incidentes: observar, conter, restaurar serviço, investigar, corrigir causa;
preservar evidências e separar mitigação de solução definitiva.

## Fora de escopo

Segundo Harness, instalação global/cache do plugin, provisionamento real,
alterações em produção, merge automático, fechar Issues como aprovação humana,
recriação do Environment, duplicação de scanners/MCP Library, cópia do review
restricted, versões globais inventadas ou migração de stack existente.

## Dependências, decisões pendentes e riscos

Dependências: contratos e helper atuais, revisão de segurança, fontes oficiais
pinadas e validadores locais. Decisões pendentes: nenhuma bloqueante para a
entrega do plugin. Integração Environment aguarda sua presença na base e teste
posterior, NOT VALIDATED. Riscos: exemplos podem exigir adaptação ao projeto;
validação estática não comprova produção; instalação não comprova conexão/auth.

## Critérios de aceite

1. Bundle e skill canônica válidos, control plane compacto.
2. Três manifestos, agents/openai.yaml e marketplaces consistentes.
3. ORIGIN com SHA exato, notices aplicáveis e mapa de reutilização honesto.
4. Review restricted excluído; revisão original rastreável aos requisitos.
5. Registry parseável com 20 tools, fontes oficiais e políticas explícitas.
6. Não duplicar scanners de segurança nem instalação/MCP Library.
7. Helper resolve novo owner preservando owners existentes.
8. Capability router cobre domínios sem virar catálogo de vendors.
9. SDD inclui DevOps somente para superfícies aplicáveis.
10. Contract e task guardam owner/capability/preferred_tool, não estado local.
11. Gates humanos cobrem todas as operações destrutivas enumeradas.
12. Validação IaC/Kubernetes não executa apply/destroy produção por padrão.
13. Rollback, health, backup versus restore e incidente preservam evidências.
14. Findings exigem análise e FAIL exige correção/revalidação ou bloqueio.
15. Mesmo SKILL_RECEIPT/EXECUTION_RECEIPT e relatório humano existentes.
16. README/pipeline/fronteiras atualizados antes de commit.
17. Environment ausente é declarado pendente NOT VALIDATED, sem duplicação.
18. Pelo menos 30 verificações relevantes, incluindo fixtures seguras e casos
    positivos/negativos de roteamento/owner/gates; suíte existente sem regressão.
19. Cada comando efetivamente executado registra exit code e resultado real.
20. Nenhuma infraestrutura real/destrutiva executada para testar a skill.

## Hipóteses

Nenhuma hipótese sobre infraestrutura de clientes. Compatibilidade futura com
Environment é intenção contratual, não evidência de integração executada.
