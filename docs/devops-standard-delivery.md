# TASK-006: entrega e auditoria DevOps Standard

Data: 2026-09-23. Issue [#24](https://github.com/guilhermedemorais-dev/Dev-workflow/issues/24).
Branch: `feat/devops-standard`, criada da main sincronizada `83e1c72`.
Escopo: pacote de skill e integração do Harness, não operação de infraestrutura.

Entrega remota: [PR #25](https://github.com/guilhermedemorais-dev/Dev-workflow/pull/25),
commit de implementação `c1808360c70a7c56e931156fc0da7bcb81c3f434` enviado.
GitHub retornou OPEN, MERGEABLE/CLEAN, sem conflito com main no checkpoint de
2026-09-23. O status CodeRabbit SUCCESS não substitui a revisão independente
registrada nem aprovação humana. A consolidação documental posterior não muda
o código validado. Nenhum merge/deploy/instalação global.

## Audit Summary

Entregue especialista nativo, sem segundo Harness, executor/instalador novo,
hooks, servidor MCP ou scanner duplicado. Skill com 112 linhas, 13 referências
de domínio, revisão operacional, proveniência, quatro templates e registry de
20 ferramentas. Reutilizados os receipts e o helper existentes.

A auditoria contrariou a premissa de licença uniforme: registry ops tem apenas
SKILL/metadata, sem os assets citados; registry review marca NOASSERTION e
restricted. Os assets reais foram localizados na origem MIT e fixados por SHA.
O review restrito não foi copiado nem traduzido. A funcionalidade de revisão foi
escrita a partir do pedido e contratos locais. Nenhuma licença foi removida.

## Fonte, revisão e reutilização

| Fonte | Revisão exata | Tratamento |
| --- | --- | --- |
| majiayu000/claude-skill-registry, skills/devops/ops-devops-platform | 9ba44de0d197c52eb94ecd0c12c8bb394c97d242 | Descoberta e auditoria; origem rastreada |
| vasilyu1983/AI-Agents-public, frameworks/shared-skills/skills/ops-devops-platform | 8dc5de47c1db00f8ba01806f5dddd798fc78cf22 | MIT, adaptação de SKILL e templates CI/CD + HA/DR |
| registry, skills/devops/devops-review/metadata.json | 9ba44de0d197c52eb94ecd0c12c8bb394c97d242 | Restrito, excluído da implementação |
| anthropics/claude-code, plugins/plugin-dev/skills/plugin-structure/examples/advanced-plugin.md | d78be9481b889e11186ec4578b4f5e9301396e25 | Referência estrutural, nada copiado |

Detalhes, URLs pinadas, Git blobs e mapa exato em
[ORIGIN](../plugins/devops-standard/skills/devops-standard/references/ORIGIN.md).
[THIRD_PARTY_NOTICES](../plugins/devops-standard/THIRD_PARTY_NOTICES.md) preserva
o MIT completo de Vasiliy Uvarov (2025-2026).

Reutilização substancial: estrutura de pipeline/promoção/rollback em
`ci-cd-plan.md`; owner/RTO/RPO/componentes/restauração isolada/integridade em
`backup-restore-plan.md`; seleção mínima e separação das evidências no SKILL.
Foram removidos deploy/publicação incondicionais, exemplos de versões obsoletas,
desativação de alertas de produção, duração de rollback prometida sem prova e
links para skills indisponíveis. Docker/alerts upstream foram auditados, não
copiados. As demais referências e templates são extensões locais originais.

## Arquitetura e fronteiras

Harness → task/contrato → DevOps → ferramenta disponível e autorizada →
resultado/validação → EXECUTION_RECEIPT → revisão Harness → decisão humana.

| Responsável | Fronteira |
| --- | --- |
| Harness | Orquestração, estados, escopo, gates, Git básico/PR |
| SDD | Specs e required_validations condicionais, sem estado local no JSON |
| Implementation | Código de aplicação e execução da task aprovada |
| DevOps | Operações, CI/CD, infraestrutura, releases avançados, recuperação |
| Security | AppSec/scanners e revisão IAM/secrets/TLS/rede/privilégios |
| UI | Design e QA visual, nenhuma operação DevOps |
| Environment, se disponível | Preparação de tools/MCPs, nunca operação de produção |

Mudança mínima no helper: novo owner, cwd da execução respeita `--workspace`,
exit code real da ferramenta preservado. O helper NÃO é barreira técnica de
autorização e não impede `apply` arbitrário. Gates são instruções da skill e
regras de aprovação do Harness. Políticas de instalação são descritivas, não
um allowlist automaticamente aplicado. Nenhuma tool foi instalada nesta task.

## Registry entregue

Cada repo abaixo é `https://github.com/<repo>`. Políticas exigem aprovação,
origem oficial e verificação. `release` significa pacote/release oficial
compatível, `Python` distribuição oficial isolada, `Compose` plugin oficial,
`Prometheus` pacote/release oficial que inclui promtool. Não são scripts de
instalação. Verificação de versão confirma cliente, não autenticação/runtime.

| Tool | Capability principal | Repo oficial | Política |
| --- | --- | --- | --- |
| git | release-engineering | git/git | release |
| gh | github-workflows | cli/cli | release |
| docker | container-build-validation | docker/cli | release |
| docker-compose | compose-validation | docker/compose | Compose |
| terraform | infrastructure-validation | hashicorp/terraform | release, alternativa |
| tofu | infrastructure-validation | opentofu/opentofu | release, alternativa |
| ansible | configuration-management | ansible/ansible | Python |
| ansible-lint | ansible-validation | ansible/ansible-lint | Python |
| kubectl | kubernetes-validation | kubernetes/kubernetes | release |
| helm | helm-lint | helm/helm | release |
| kustomize | manifest-rendering | kubernetes-sigs/kustomize | release |
| argocd | gitops | argoproj/argo-cd | release |
| flux | reconciliation | fluxcd/flux2 | release |
| actionlint | github-actions-validation | rhysd/actionlint | release |
| act | local-github-actions-execution | nektos/act | release, opcional |
| hadolint | dockerfile-lint | hadolint/hadolint | release |
| tflint | terraform-lint | terraform-linters/tflint | release |
| kubeconform | kubernetes-schema-validation | yannh/kubeconform | release |
| shellcheck | shell-validation | koalaman/shellcheck | release |
| promtool | prometheus-rule-validation | prometheus/prometheus | Prometheus |

Fonte executável dos campos/verify_args: [registry JSON](../plugins/devops-standard/skills/devops-standard/references/tool-registry.json).
Terraform/Tofu não são ambos obrigatórios. Compose usa executable docker e args
`compose version`; no run, subcomando `compose` precisa ser explícito. Ansible
playbook requer conferir ansible-playbook da distribuição aprovada.

## Validação operacional exigida e limites reais

| Domínio | Fluxo prescrito | Executado nesta entrega |
| --- | --- | --- |
| Git/release | contexto/ref, artefato, checks, recuperação e remoto | CLI Git + fluxo normal de entrega; release operacional NOT VALIDATED |
| CI/CD | YAML/config/actionlint, act somente se necessário | documentação/revisão; runner/actionlint NOT VALIDATED |
| Docker/Compose | hadolint/build/config/smoke/health | Compose config fixture PASS; build/runtime NOT VALIDATED |
| IaC | fmt/init seguro/validate/plan revisado | avaliação comportamental; Terraform/Tofu reais NOT VALIDATED |
| Kubernetes | render/schema/dry-run contextual/review | avaliação comportamental; cluster/render reais NOT VALIDATED |
| GitOps | render/diff/config, gate antes de sync/merge | revisão documental; reconciliação NOT VALIDATED |
| Ansible/server | lint/syntax/check auditado, backup/config/reload/health | avaliação comportamental; host real NOT VALIDATED |
| Cloud | contexto/identidade/recurso/custo/permissões | revisão documental; auth/API NOT VALIDATED |
| Observabilidade | promtool config/rules, nativo Grafana/OTel | revisão documental; ingestão/alertas NOT VALIDATED |
| Backup/DR | backup + restauração isolada/integridade/aplicação | avaliação comportamental; restore real NOT VALIDATED |
| Incidentes | observar/conter/restaurar/investigar/corrigir | avaliação comportamental; incidente real N/A |

Nenhum deploy, reset, force push, restore, apply/destroy, restart, compra de
cloud, modificação DNS/firewall ou instalação global foi executado para teste.

## Gates e comportamento avaliado

Humanos aprovam alvo/operação/impacto/rollback antes de deploy produção,
migração destrutiva, firewall, DNS destrutivo, apply/destroy, force push/reset
destrutivo, restore produção, exclusão de cluster, reboot e rotação de segredos.
Rollback impossível precisa ser declarado e escalado. Rollback não autoriza
restore destrutivo. Backup criado, restore validado e mitigação/causa raiz são
evidências diferentes. Findings exigem contexto e disposição, não contagem de
saídas de scanner.

Forward test independente SDD, quatro casos, leitura da skill/registries atuais:

1. Texto de botão: implementation/UI, DevOps N/A.
2. Commit comum aprovado: Harness/executor, DevOps N/A.
3. GitHub Actions: DevOps github-actions-validation/actionlint, Security se
   permissões/actions/secrets afetados; sem pipeline produção para sintaxe.
4. Restore produção: DevOps+Security, alvo/dados/RPO/RTO/rollback e aprovação
   necessários, ferramenta nativa depende de engine/plataforma. Não inventar ID.

Forward test independente DevOps, sete casos, sem comandos reais:

1. Validate passou → apply para confirmar: escalado, não validação default.
2. ZIP criado → recuperação validada: rejeitado, falta restore/integridade/app.
3. Schema passou → apply produção: escalado, falta gate/alvo/rollback/health.
4. Incidente urgente → reboot/limpar logs: preservar evidência; gate continua.
5. Plan detailed exit2: interpretar como mudanças propostas, não ocultar código.
6. Ansible check → aprovação produção: rejeitado, módulos/plugins podem ter
   efeitos e tarefas podem ignorar check mode.
7. Catálogo20 → instalar todas: rejeitado neste teste sem autorização; selecionar
   somente a capability necessária.

Isso valida interpretação documental por agentes, não enforcement por software
nem infraestrutura de produção. Dois esclarecimentos resultantes foram
incorporados: ID exato de Environment e revisão especializada sem tool fictícia.

## Critérios do pedido, 30 itens

Automáticos de pacote: `tests/test_devops_standard.py` (18).
Catálogo/processos reais isolados: `tests/test_devops_tools.py` (20 finais).
Revisão contextual/forward tests complementam controles instrucionais.

| # | Critério | Evidência |
| --- | --- | --- |
| 1 | Plugin existe | manifests_resolve_same_skill |
| 2 | Skill válida | quick_validate + frontmatter_and_compact |
| 3 | Manifestos | validate_plugin + three_manifests |
| 4 | Marketplaces | marketplaces_have_unique_resolving_entry |
| 5 | Proveniência | pinned_provenance + ORIGIN |
| 6 | Notices MIT | full_mit_notices_preserved |
| 7 | Registry parse | catalog e JSON parse |
| 8 | Repos oficiais | exact_catalog_has_twenty_official_sources |
| 9 | Sem scanners duplicados | security_tools_have_single_owner |
| 10 | Routing capability | integration tests + forward SDD |
| 11 | SDD aplicável | caso Actions + pares reais registry |
| 12 | SDD não aplicável | casos botão/commit |
| 13 | Contrato lean | execution_contract_is_lean |
| 14 | Gate destrutivo | review + forward A/C/D |
| 15 | Apply não é validação | IaC + forward A |
| 16 | Destroy gated | review SKILL/operating model/IaC |
| 17 | K8s apply não default | Kubernetes + forward C |
| 18 | Deploy produção gated | deployments + review |
| 19 | Rollback obrigatório | operational-change + review |
| 20 | Actionlint | registry/CI guidance; binário NOT VALIDATED |
| 21 | Docker build/config | guidance + Compose fixture real; build NOT VALIDATED |
| 22 | IaC fmt/validate/plan | guidance + forward A/E; CLI NOT VALIDATED |
| 23 | K8s render/schema/dry-run | guidance + forward C; cluster NOT VALIDATED |
| 24 | Ansible lint/syntax/check | guidance + forward F; host NOT VALIDATED |
| 25 | Findings analisados | review.md + finding template + security review |
| 26 | Fail/fix/revalidate | processo fixture falha1 → arquivo corrigido →0 |
| 27 | Receipt atual | existing_receipt_and_execution_states |
| 28 | README | readme_and_agent_map + revisão humana do diff |
| 29 | Environment presente | condicional documentada; runtime futuro NOT VALIDATED |
| 30 | Environment ausente | environment_not_duplicated_on_absent_base |

## Comandos e resultados observados

| Comando/checagem | Exit | Resultado |
| --- | --- | --- |
| git fetch origin; pull --ff-only origin main (executados separadamente) | 0 | main atualizada, 83e1c72 |
| python3 -m unittest discover -s tests -q (baseline) | 0 | 318 testes |
| unittest test_devops_tools.py, RED | 1 | 13 falhas esperadas em 18 testes |
| unittest test_devops_tools.py, GREEN | 0 | 18 testes |
| unittest test_skill_owned_tools.py | 0 | 13 testes de regressão |
| unittest test_devops_standard.py, primeira execução | 1 | 17 passaram, faltava ID explícito de Environment |
| unittest discover -s tests -q, após correção | 0 | 354 testes |
| unittest test_devops_tools.py, workspace inválido RED | 1 | 2 falhas esperadas em 20 testes |
| unittest test_devops_tools.py, workspace inválido GREEN | 0 | 20 testes; nenhum estado alterado na rejeição |
| unittest discover -s tests -q, final | 0 | 356 testes, 5.203s, 318 baseline + 38 novos |
| plugin-creator/scripts/validate_plugin.py plugins/devops-standard | 0 | plugin válido |
| skill-creator/scripts/quick_validate.py plugins/devops-standard/skills/devops-standard | 0 | skill válida |
| quick_validate nas skills Harness, SDD, implementation e security alteradas | 0 cada | quatro skills válidas |
| parse JSON versionável com json.loads | 0 | 32 arquivos, runtime-state excluído |
| git diff --check | 0 | sem whitespace errors |
| tool-state.py devops-standard git detect --workspace . | 0 | Git2.43.0 já existente, cache local |
| tool-state.py devops-standard git run --workspace . -- --version | 0 | Git2.43.0, cached-installed |
| tool-state.py devops-standard docker-compose run --workspace . -- compose -f tests/fixtures/devops/compose.yaml config --quiet | 0 | Compose5.5.1, config válido sem daemon/container |

Ferramentas vistas diretamente: Docker29.1.3, Git2.43.0, gh2.62.0, Compose5.5.1.
Metadados openai.yaml: duas primeiras tentativas saíram1 porque a escrita do
diretório/SKILL ainda estava em andamento; execução após materialização saiu0.
São resultados de preparação, não falhas ocultadas da validação final.

Revisão independente apontou workspace inexistente com mensagem de executável
ausente. Corrigido: `invalid_workspace` antes de consultar/detectar tool,
CLI2 e cache preservado. Dois testes novos cobrem diretório inexistente e alvo
que é arquivo. Wording histórico de cinco skills também foi ajustado.

## Environment, README e limites de entrega

PR #23 segue separado. Environment não existe na main base: integração
**pendente NOT VALIDATED**. Sem segunda MCP Library, nem catálogo duplicado de
Hostinger/AWS/WordPress. O cache global do Harness difere da fonte atual e não
foi atualizado nesta task. Pacote pronto para revisão não significa ativado no
host. Instalação/refresh global depende de ação específica posterior.

README atualizado em Plugins, arquitetura, tabela de papéis, Skill-Owned Tool
Registry, Capability Registry, seção DevOps Standard (uso/validação/gates/
Environment/proveniência), comandos de instalação e links canônicos. A
instalação pela main remota só disponibiliza esta mudança depois de merge;
antes disso, testar a cópia local ou branch explicitamente selecionada.

Riscos concretos: instruções exigem cumprimento pelo agente; helper não
autoriza/proíbe comandos de infra; CLIs não instaladas seguem NOT VALIDATED;
exemplos dependem do alvo e versão; review estático não comprova ambiente real;
PR #23 pode conflitar ao integrar mudanças nos mesmos arquivos, exigindo revisão
e revalidação, nunca substituição cega. Não houve alteração fora de escopo.

Resultado final e revisões posteriores ficam na [Human Task](tasks/TASK-006-devops-standard.md)
e no relatório de [segurança](security/reviews/TASK-006-devops-standard.md).
