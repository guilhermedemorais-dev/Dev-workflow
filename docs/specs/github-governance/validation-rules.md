# SPEC: Validação de GitHub Governance

## Status e contexto
Aprovada pelo Harness em 2026-09-24, vinculada à [module-spec](module-spec.md), TASK-010.

## Regras
- RN-01: diagnose/propose/verify sem escrita local ou mutação remota, inclusive
  GraphQL; a modalidade de transporte HTTP não define sozinha se query é read-only.
- RN-02: apply exige confirmação + proposta correspondente ao alvo e snapshots;
  drift/tampering/ação extra bloqueiam antes da primeira mutação.
- RN-03: operação aprovada reconcilia recursos semanticamente, pagina coleções,
  preserva recursos alheios e bloqueia matching ambíguo; rerun converge a NOOP.
- RN-04: auth, repository access/admin, organization/project capabilities separados.
  Sem gh solicita Environment; sem auth conduz login seguro; não vazar tokens.
- RN-05: limitação de plano exige fonte/capability observada; fallback aprovado
  explícito. Ausência de permissão não vira automaticamente plan limitation.
- RN-06: local path seguro dentro workspace; symlink/traversal/arquivo conflitante
  ou overwrite não aprovado bloqueiam. Não executar shell arbitrário da proposta.
- RN-07: Project owner/título, fields/options/views descobertos; status preservados
  e faltantes acrescentados, nenhum ID fixo. Unsupported retorna ação humana.
- RN-08: oito estados autorizados, Done somente após merge humano; blocked label;
  três ciclos default de rework, depois diagnóstico bloqueante.
- RN-09: CI adaptativo/native/locked sem inventar scripts; required checks observados;
  criado/configurado não prova execução/enforcement.
- RN-10: READY exige verificação fresca; mutation failure/partial, drift ou validação
  obrigatória ausente não produzem PASS. N/A/fallback deve ser justificado.
- RN-11: usar EXECUTION_RECEIPT existente, sem credentials/runtime IDs no desired state;
  logging allowlist/sanitizado inclusive exceções e respostas hostis.
- RN-12: capability GitHub Governance pertence DevOps; Environment só prepara;
  Security revisa risco; Harness gate; QA valida helper independentemente.

## Entrada, camada e erros
Validar JSON v1, chaves/tipos/valores, owner/repo/host/workspace, branch/prefix,
nomes/textos/diffs locais, proposal schema e hashes. Recusar valores interpretáveis
como comando, path externo, token ou autorização para merge/deploy. Subprocess
com argv explícito e operações permitidas, não shell strings.
Banco/API de aplicação/Frontend: N/A. Regras aplicadas no helper DevOps e gates.
Categorias: GH_MISSING, AUTH_REQUIRED, INSUFFICIENT_PERMISSION, PLAN_LIMITATION,
API_UNAVAILABLE, GRAPHQL_UNSUPPORTED, REMOTE_CONFLICT, LOCAL_CONFLICT,
VALIDATION_FAILED. Ação humana informa motivo, comando seguro e próxima etapa.

## Testes unitários mínimos do pedido
| ID | Cenário | Resultado obrigatório |
| --- | --- | --- |
| T01 | gh ausente | GH_MISSING, nenhum instalador próprio |
| T02 | gh sem login | AUTH_REQUIRED + login seguro, sem credencial no output |
| T03 | repo inacessível | Falha de acesso explícita; não mutar |
| T04 | repo sem admin | Bloquear alterações administrativas |
| T05 | Project scope/permissão ausente | Ação humana mínima; não presumir Project disponível |
| T06 | repo configurado | NO CHANGE REQUIRED |
| T07 | Project existente | Reutilizar, sem create duplicado |
| T08 | labels parciais | Criar só faltantes, preservar existentes equivalentes |
| T09 | ruleset suportado | Apenas regras/checks aprovados, verificar enforcement |
| T10 | ruleset sem suporte plano | Limitação fundamentada + fallback governado |
| T11 | propose | Zero writes/mutations/workflows/Git alterações |
| T12 | apply sem confirm | Bloqueio antes de mutação |
| T13 | apply repetido | Idempotente após refresh e nova proposta se necessário |
| T14 | verify com drift | Detectar e negar READY indevido |
| T15 | IDs Project variáveis | Usar IDs observados, sem literais fixos |
| T16 | status existente | Sem duplicação/perda |
| T17 | status ausente | Acrescentar preservando existentes |
| T18 | mutation falha | Sem PASS; reportar parcial e não seguir cegamente |
| T19 | respostas/erros com marcador sensível | Nenhum segredo/traceback bruto em output |
| T20 | READY | Só com evidência fresca de todos requisitos observados |

## Negativos e regressão adicionais
Alvo diferente/proposta adulterada/hash alterado/local ou remote drift; traversal,
symlink e filesystem root; status/label duplicado por cosmetic difference;
Project matching ambíguo, segunda página, mutation GraphQL em modo read-only;
403/404 ambíguo; partial failure seguida de resume; CI inexistente/unexecutado;
runtime IDs não persistidos no desired; comando injection; repo sem stack detectável.
Fixture fake-gh deve registrar chamadas e falhar qualquer mutation read-only,
não apenas confiar na descrição textual do teste.
README tests exigem fases 0–10, auth assistida, USER_ACTION_REQUIRED, quatro modos,
gates, capability/limitação, segurança credenciais e referência DevOps.

## Teste manual documentado, não executado nesta task
Repo privado descartável autorizado: diagnose -> propose -> revisão -> apply
confirmado -> verify -> propor/aplicar de novo -> NO CHANGE REQUIRED.
Registrar owner/visibility/capabilities/plano observado/IDs/commands/resultados,
sem tokens. Segunda execução real prova idempotência operacional, não o mock.
Planos/operações não suportados viram limite explícito. Não usar Dev-workflow
como alvo automático. Sem delete/reset de recursos como limpeza implícita.

## Segurança / Observabilidade
Security owner revê cadeia input/proposal/CLI/paths/API/output. Relatório sanitizado
classifica falha sem imprimir payload/headers/credenciais. QA distingue fixture/tool
failure de bug do helper. Sem callback externo ou coleta de configuração de auth.

## Riscos e decisões pendentes
Mock não prova permissões nem mutações na API real. Status de integração remota
permanece NOT VALIDATED até ensaio autorizado. Aprovador humano decide rollout.

## Critérios de aceite
Comando/exit code/resultado de testes focados, suíte completa, README, validators
e diff check; RNs verificadas por QA/Security; artefatos coerentes e nenhuma
alegação de readiness remoto real desta entrega.
