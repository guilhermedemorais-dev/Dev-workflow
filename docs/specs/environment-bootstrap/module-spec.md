# MODULE SPEC: Environment Bootstrap / Plugin Health

## Adendo aprovado: fontes para pesquisa no planejamento/spec

Manter biblioteca leve de fontes auxiliares na skill SDD, consumida também pelo
Harness no planejamento quando houver necessidade de API, integração ou endpoint
de validação. Fontes: inventario-apis-gratuitas e PublicAPIs.io/development.
Não promover diretórios a MCPs aprovados nem copiar listas inteiras. Registrar
problema, candidato, fonte primária, custos/limites/auth, dados/permissões,
plano/evidência de validação, data e decisão. API de validação, mock e MCP são
categorias distintas. Só pesquisar quando pertinente; sem rede, declarar lacuna.
Sem chamar APIs com dados reais, instalar ou gerar contas como efeito da pesquisa.

## Adendo de catálogo aprovado pelo usuário

Acrescentar Hostinger API MCP, AWS API MCP Server e WordPress MCP Adapter como
PROJECT_SPECIFIC / OFFICIAL. Reutilizar AUTH_REQUIRED + host_handoff; nenhuma
configuração automática, segredo ou autorização de operação em produção.
Os IDs são `hostinger`, `aws`, `wordpress`. Não incluir por padrão; resolver
seleção/capability explicitamente e retornar USER_ACTION_REQUIRED para setup.
AWS não significa instalar todos os servidores AWS Labs; WordPress representa
o adapter do site próprio, não um endpoint genérico nem WordPress.com.
Registrar lifecycle superseded do AWS API MCP e direcionar avaliação do sucessor
oficial antes de novo setup; não declarar o legado como recomendação atual.
Aceite adicional: schema público válido; fontes oficiais auditadas; testes
contra catálogo real comprovam ausência de execução mesmo com aprovação genérica.
Catálogo passa de 13 para 16 componentes, sem alterar a arquitetura/30 casos-base.

## Status e intenção pai

Implementação autorizada pelo pedido do usuário; revisão técnica do contrato pelo
Engineering Harness precede execução. Intenção pai: tornar o Engineering Harness
portátil e preparável por qualquer desenvolvedor, preservando seus especialistas
e arquitetura de skill-owned tools. Esta extensão não requer outro Product Spec
ou documentos de UI. TASK-005 é a única entrega revisável.

## Diagnóstico

- Claro: quatro operações, catálogo MCP público, estado privado, descoberta
  dinâmica, instalação seletiva e gates com evidência são obrigatórios.
- Verificado: `tool-state.py` já resolve/detecta/instala/executa tools, mas limita
  owners a três skills, detect escreve estado e execução não define cwd.
- Falta não bloqueante: escolhas locais de opcionais, MCP customizado e eventual
  autenticação pertencem ao primeiro bootstrap; não à autorização de implementar.
- Riscos iniciais: falso HEALTHY, misturar instalação/conexão/autenticação,
  invalidar cache indevidamente, instalar componentes sem seleção/autorização.
- Perguntas críticas: nenhuma para implementar este contrato.

## Objetivo e escopo incluído

Criar `dev-environment-standard`, seguindo o plugin por skill canônica existente,
com manifests raiz/Codex/Claude, agents/openai.yaml e marketplaces atuais.
Responsabilidades: discovery, bootstrap, estado, MCP Library/preparation,
preparação de tools especialistas, runtimes, package managers, browsers, health e
repair. Não implementa produto nem substitui Harness, SDD, implementação,
segurança ou UI/UX.

## Arquitetura mínima e reúso

Engineering Harness -> dev-environment-standard -> Plugin Health / MCP Library /
Tool Registries / Runtime Discovery / Environment State -> Capability Router ->
Specialist Skills.

- Um `scripts/environment.py` stdlib centraliza as quatro operações; referências
  JSON/Markdown contêm catálogo e contrato, sem framework ou daemon novo.
- Estender `plugins/dev-workflow-standard/scripts/tool-state.py`, preservando sua
  interface atual, para owners descobertos dinamicamente, probe read-only,
  resolução de executáveis do projeto/venv/node_modules, cwd do workspace e
  propagação correta de exit code. Não duplicar detector/instalador de tools.
- Cada `references/tool-registry.json` permanece com sua skill. Descobrir todas
  skills canônicas e registries; ausência de registry é permitida. Environment
  referencia ownership/capability e delega detect/install/verify ao helper.
- Library pública versionada contém metadados MCP; configuração de transporte e
  autenticação é específica do host e mediada pelas capacidades reais do host.
  Ausência de adaptador suportado produz MANUAL_ONLY/USER_ACTION_REQUIRED, nunca
  conexão simulada. Evidência importada do host deve ser validada e datada.

## Operações e regras de negócio

### doctor

Diagnóstico sem writes, instalação, invalidação persistida ou criação de cache.
Inspecionar OS, Git/Python/Node, runtimes opcionais necessários (Docker/Java/Go/PHP),
package managers relevantes, browsers, skills, manifests, marketplaces, scripts,
references, registries, estado local, MCPs/autenticação e evidências de validators.
Verificar gravabilidade sem criar arquivos; testes potencialmente mutantes só
podem rodar isolados ou fornecer evidência externa identificada. Relatar testes
nunca executados como NOT VALIDATED. Relatório humano e JSON HEALTH_REPORT.

### prepare

Executar doctor, resolver CORE + requisitos da task + escolhas explícitas,
inspecionar registries/library/estado, preparar apenas faltantes permitidos,
verificar presença/conexão/autenticação separadamente, persistir estado e health.
Seleção e aprovação são explícitas; CORE não autoriza instalar cegamente.
Dry-run não executa instaladores nem escreve. Plano contém componente, origem,
política, método, escopo e ação exigida. Sem install-all.

No primeiro bootstrap, após CORE, apresentar RECOMMENDED/OPTIONAL e perguntar
quais configurar; perguntar também se há MCP específico fora da biblioteca.
Registrar escolhas sem assumir consentimento pelo silêncio. Persistir enabled,
disabled, not_requested, auth_required e connected sem confundir preferência
com disponibilidade observada. Não repetir perguntas sem solicitação, reset,
nova necessidade/capability/projeto, quebra, mudança relevante ou incompatibilidade.

### repair

Falha real de componente anteriormente disponível invalida somente seu estado;
preparar novamente somente esse componente, sob política e aprovação aplicáveis,
verificar e persistir. Falha anterior não gera retry ilimitado. Nunca reinstalar
tudo. Componentes saudáveis permanecem intactos.

### status

Operação read-only: nunca escrever estado. Usar snapshot local e fingerprint compatível; checks baratos de executáveis,
estado tool-state, catálogo/configuração e evidência atual de conexão MCP.
Fingerprint inclui fronteiras de host/runtime/workspace e configurações relevantes.
MCP conectado em cache não prova conexão atual. Evidência vencida ou ausente
produz estado conservador e encaminha doctor/prepare, sem rede/discovery completo
em toda task. Harness pede somente capabilities requeridas antes de executar.

## MCP Library

Separar tier `CORE|RECOMMENDED|OPTIONAL|PROJECT_SPECIFIC|COMMUNITY|RUNTIME_PROVIDED`,
origem `OFFICIAL|VERIFIED_THIRD_PARTY|COMMUNITY|UNKNOWN` e estado runtime
`AVAILABLE|INSTALLED|CONNECTED|AUTH_REQUIRED|MISSING|BROKEN|UNSUPPORTED`.
Representar autenticação separadamente: installed != connected,
connected != authenticated, registered != available, planned tool != executed tool.

| MCP | Tier inicial | Fonte a verificar | Capability |
| --- | --- | --- | --- |
| GitHub | CORE | github/github-mcp-server | repositórios, arquivos, issues, PRs, colaboração, reviews |
| Context7 | CORE | upstash/context7 | documentação atual de bibliotecas/SDKs e exemplos |
| Playwright | CORE | microsoft/playwright-mcp | browser, QA runtime, E2E, interações |
| Chrome DevTools | RECOMMENDED | ChromeDevTools/chrome-devtools-mcp | console, rede, debugging, renderização, performance |
| Docker MCP Gateway | RECOMMENDED | docker/mcp-gateway | lifecycle, isolamento, discovery, execução, secrets/auth |
| Docker MCP Registry | RECOMMENDED | docker/mcp-registry | catálogo/discovery, sem confundir catálogo com servidor |
| Figma | OPTIONAL | figma/mcp-server-guide | design, frames, tokens, componentes |
| Firecrawl | OPTIONAL | firecrawl/firecrawl-mcp-server | extração/pesquisa/web pública |
| Hugging Face | OPTIONAL | huggingface/hf-mcp-server | modelos, datasets, Spaces, Hub |
| Sentry | OPTIONAL | getsentry/sentry-mcp | erros/incidentes/contexto de aplicação |
| Supabase | PROJECT_SPECIFIC | supabase/mcp | contexto de projetos Supabase |
| grep-mcp | COMMUNITY | PyPI declara galperetz/grep-mcp; origem UNKNOWN | busca de código conforme evidência |
| node_repl | RUNTIME_PROVIDED | host real | execução fornecida pelo runtime |

Auditoria de fontes: `docs/specs/environment-bootstrap/mcp-source-audit.md`.
Root verificou fontes primárias dos CORE. PyPI declara galperetz/grep-mcp 1.0.3,
mas repository declarado retorna 404; trust permanece UNKNOWN, preparação
MANUAL_ONLY, nenhuma instalação automática. Não confundir com serviço oficial
grep.app. Status runtime não pertence ao catálogo versionado.

Verificar fontes oficiais e registrar proveniência. Avaliar Docker Gateway como
opção, nunca dependência obrigatória. Não afirmar origem oficial de grep-mcp sem
evidência. UNKNOWN nunca instala automaticamente; COMMUNITY exige consentimento
específico. node_repl só detecta, não é instalado como MCP externo.

Custom MCP recebe nome, repository/provider, docs, capabilities, maintainer,
instalação, transporte, permissões, auth e riscos. Validar esses campos e origem;
salvar somente configuração segura no estado local. Não promover ao catálogo
público automaticamente. Sugestão de contribuição posterior é opcional.

## Preparação de ambiente e dependências

Classes: AUTO_SAFE, PROJECT_SCOPED, USER_SCOPED, AUTH_REQUIRED, PRIVILEGED,
MANUAL_ONLY, RUNTIME_PROVIDED. As primeiras três só executam quando aprovadas;
AUTH_REQUIRED prepara até handoff seguro; PRIVILEGED exige USER_ACTION_REQUIRED;
MANUAL_ONLY fornece instrução; RUNTIME_PROVIDED somente detecta.

Detectar pip/pipx/uv/npm/npx/pnpm/yarn sob demanda, preferindo o manager do projeto.
Respeitar package-lock (`npm ci`), pnpm-lock (`pnpm install --frozen-lockfile`),
yarn.lock (comando locked compatível com versão), uv.lock (`uv sync --locked` ou
equivalente que não reescreva o lock). Lockfiles conflitantes exigem resolução,
não escolha silenciosa. Python usa venv existente ou ambiente aprovado.
Instalações de dependências podem executar hooks do projeto e requerem aprovação.
Browsers Chromium/Chrome/Firefox/WebKit são selecionados por necessidade; não
instalar todos. Runtime de sistema, root/admin e alterações globais não são
silenciosos. Preservar versões e configurações existentes.

## Banco

N/A para banco/migrações. Dados operacionais JSON em runtime-state ignorado:
fingerprint, runtime versions, managers, MCP status/auth/preferências, custom
MCPs seguros, health, tool summaries, browsers, last doctor/prepare. Escrita
atômica, permissões privadas, validação de schema/campos e recuperação conservadora
de JSON inválido. Configuração local pode conter paths pessoais; arquivos
versionados não. Não aceitar secrets embutidos em URLs, argumentos ou campos livres.

## API/Backend

CLI local e arquivos JSON, sem endpoint/serviço remoto novo. Quatro operações com
saída máquina e humana, códigos de saída coerentes com sucesso/falha. HEALTH_REPORT
inclui plugin_health, runtimes, mcps, skills/missing_tools, blockers, evidência e
resultado de preparação. Não imprimir stdout/stderr arbitrário com credenciais.

## Frontend/UI

N/A para telas/browser UI do produto. CLI fornece resumo humano, seleção opcional,
custom intake e handoff de autenticação. O host conduz diálogo/consentimento.

## Plugin Health

HEALTHY exige evidência suficiente; DEGRADED para opcionais/requisitos não
comprovados; BLOCKED para estrutura inválida/requisito obrigatório indisponível.
Disponibilidade para task específica é distinta da completude de todo catálogo.
Inspecionar plugins esperados, skill canônica, SKILL/frontmatter/agents, manifests,
marketplaces (paths, nomes, registro), registries (JSON/owner/tools/capabilities/
repository/command/verify/install_policy), estado ignorado/gravável/sem secrets,
scripts presentes/sintaxe/smoke aplicável, docs/referências e validators/testes.
Ausência de evidência nunca transforma check desconhecido em PASS.

## Segurança

Sem passwords/tokens/API keys/OAuth/cookies persistidos ou impressos. Usar host
seguro para auth; ação humana real = USER_ACTION_REQUIRED. Sem sudo silencioso,
binários desconhecidos, forks aleatórios, shell injection, substituição destrutiva
ou mudanças globais desnecessárias. Não confiar em estado/custom MCP arbitrário
como autorização para executar comandos. Validar paths/owners contra traversal e
escopo. Security-standard revisa antes de concluir.

## Observabilidade/logs

Receipts distinguem planejado/detectado/instalado/executado/verificado. Relatórios
registram comando seguro, exit code, resultado, provenance e última verificação;
estado local não é log público. Auth_required só para pendências observadas.

## Testes e critérios de aceite

Todos os 30 cenários são obrigatórios, com casos positivos e negativos pertinentes:

1. Skill nova válida.
2. Manifests válidos.
3. Marketplaces com nomes/paths corretos.
4. Doctor não modifica ambiente nem estados.
5. Prepare instala somente selecionado/autorizado/política permitida.
6. Repair limita reinstalação ao componente quebrado.
7. Status usa fast path sem discovery/instalação repetidos.
8. Descoberta de skills aceita nova skill sem hardcode.
9. Descoberta de registry é dinâmica.
10. Environment não duplica registries especialistas.
11. Helper tool-state existente é reutilizado.
12. MCP Library parseia e valida schema/provenance.
13. CORE/RECOMMENDED/OPTIONAL/PROJECT_SPECIFIC roteiam corretamente.
14. Optional não instala automaticamente.
15. Optional recusado não é perguntado repetidamente.
16. Preferências sobrevivem entre execuções.
17. Custom MCP permanece local e não altera Library.
18. UNKNOWN não instala automaticamente.
19. COMMUNITY requer consentimento específico.
20. Installed não implica connected.
21. Connected não implica authenticated.
22. AUTH_REQUIRED e handoff são corretos.
23. RUNTIME_PROVIDED não instala.
24. Secrets são rejeitados e não persistem nem aparecem em output.
25. Environment state é ignorado pelo Git.
26. Fingerprint incompatível invalida cache conservadoramente.
27. Manifest quebrado piora health.
28. Registry inválido piora health.
29. Referência inexistente piora health.
30. README gate permanece funcionando.

Além disso, testar cwd do projeto, exit-code não zero real, resolução local/venv,
estado inválido/read-only, lockfiles, ausência de evidência e dry-run sem writes.
Usar fixtures e mocks para instalação, MCP/auth e browsers; não instalar tudo para
testar. Rodar suíte existente, JSON/manifests, diff check, smoke doctor/status e
prepare dry-run. Evidência deve listar comandos, exit codes e resultados reais.

## Documentação e saída final

README troca inventário pessoal por `Environment & Capability Bootstrap` e
documenta skill, Library/classes, seleção opcional, custom MCP, Tool Registries,
Environment State, doctor/prepare/repair/status e health. Atualizar referências
afetadas e roteamento sem copiar metodologia. README stale = NOT READY TO COMMIT.

Entrega final contém Audit Summary anterior, Architecture, tabela MCP (MCP,
Provider, Classification, Capability, Status), Optional MCPs por tier, Custom MCP
Support, tabela Specialist Tools (Skill, Registered Tools, Installed, Missing,
Broken), Environment (runtimes/managers/browsers/dependências), Plugin Health com
evidências, Installations realmente feitas, Authentication Required real, Tests
com comando/exit/result, README, Git (branch/SHA/status) e Remaining Risks concretos.

## Fora de escopo

DevOps, Git avançado/branches/protections, Actions/GitLab CI/Jenkins/pipelines,
deploy, servidores/SSH/VPS/cloud/Kubernetes/Terraform/Ansible/provisionamento,
observabilidade de infraestrutura, proxy/Nginx, Docker produção e IaC. Git básico
é detectável; GitHub colaboração e Sentry observabilidade de aplicação permanecem
no catálogo. Implementação não autoriza merge/deploy nem instalação opcional real.

## Dependências, riscos e decisões pendentes

Dependências: arquitetura e helper existentes, stdlib Python, host capabilities
quando disponíveis, fontes MCP verificadas pelo Harness. Riscos concretos: host
sem transporte/auth inspecionável, manifests antigos heterogêneos, caches expirados
e instalações sem permissões. Reportar limitação, não inventar prontidão.
Decisões pendentes: escolhas locais e autenticação só quando executar bootstrap.
HIPÓTESE operacional: o host pode não expor inspeção de todos os MCPs; nesses casos
a evidência permanece desconhecida e instrução manual é aceitável e explícita.
