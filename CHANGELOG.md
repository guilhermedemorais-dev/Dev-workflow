# Historico de atualizacoes e versoes

Este arquivo registra mudancas publicadas na main e trabalho ainda nao
publicado. Merge na main, versao do manifest, instalacao no desktop e carregamento
na sessao sao estados diferentes. O repositorio nao possui uma versao global
unica estabelecida; cada plugin/host possui seu manifest.

## Ainda nao integrado na main

- TASK-058, Issue55: pilotos opt-in de contexto derivado por trechos exatos
  (hashes e casos literais de recuperacao/mutacao, sem alegacao de equivalencia
  semantica) e renderer deterministico do template de Task com campos permitidos,
  validacao, escape e escrita atomica. TRIVIAL deixa de exigir matriz de dez
  setores; gates permanecem por superficie/risco. Suite Linux PASS com7 skips;
  Windows/WSL/macOS reais continuam NOT_VALIDATED. Medicao do exemplo usa bytes,
  sem alegacao de economia operacional ou aceite independente.

- TASK-057: preparacao por sistema com bloqueio de execucao/instalacao de tools
  proprias incompativeis ou nao validadas, aviso com motivo e escolha explicita
  de alternativa. Separa Windows nativo de Linux/WSL e preserva permissoes e
  dependencias bloqueadas do projeto. Publicacao vinculada a Issue54.

- TASK-056: ciclo MCP sob demanda, com catalogo privado verificado, inicio na
  primeira chamada, reutilizacao durante a tarefa, encerramento da arvore propria
  e fallback por inatividade. Credenciais por provedor e deteccao de registros
  redundantes. Quatro integracoes validadas no Windows10; configuracao ativa e
  cache instalado preservados, sem publicacao.

- TASK-055: ciclo MCP nativo Windows com selecao explicita, executaveis externos
  persistentes, identidade global/plugin, migracao por fingerprint, backup privado
  e rollback. Quatro transportes gerados validados no Windows10; Playwright/Edge
  permanecem provas locais condicionais. Configuracao ativa nao migrada.

- TASK-053: upgrade aditivo do Minimal Code Gate inspirado em Ponytail, com
  limpeza comprovada, biblioteca padrao/plataforma/dependencias, correcao na
  origem e consumidores completos. Preserva regras anteriores, escopo aprovado
  e protecoes; integra execucao e QA sem hooks, instalacao ou modo global.

- TASK-051 revisao9: Next.js MIT explicito e par Next/Nest preferido para novas
  propostas deste usuario, preservando stacks aprovadas;42 candidatos backend.
- TASK-051 revisao8: fontes Web3 verificadas e elegibilidade gratuita por item,
  com custos de RPC/rede separados e toolchains somente como referencias.
- TASK-051 revisao7: filtra41 candidatos backend de core/edicao gratuita OSI;
  exclui Liquibase FSL e recursos pagos, preservando obrigacoes e custos de servico.
- TASK-051 revisao6: acrescenta10 candidatos Java e5 frameworks/data tools
  JavaScript, com revisoes/licencas e limites; preserva as27 entradas anteriores
  e a matriz original de dominios tecnicos.
- TASK-051 revisao5: catalogo candidato backend, pagamentos/fiscal e commerce,
  com origem/revisao/licenca e limites; sem instalacao ou escolha de arquitetura.
- TASK-051 revisao4: explicita registro compacto de consulta e escolha de fontes
  em cada PRD/spec, com reuso nativo/N/A justificado e evidencia indisponivel
  NOT_VALIDATED; preserva consulta global, sem instalar ou carregar todo catalogo.
- TASK-051 revisao3: APIBrasil adicionado somente ao catalogo de pesquisa API do
  SDD, com fonte/pin/MIT do cliente e termos comerciais dos servicos separados;
  NOT_CONNECTED/NOT_VALIDATED, sem instalacao, chamadas ou pagamentos.

- TASK-051 revisao2: Frappe UI e React Bits passam a referencias do catalogo curado;
  removidas as skills standalone empacotadas. Reuso nativo primeiro, catalogo
  por stack depois, Context7/GitHub oficial para lacunas. ID de fonte/proveniencia
  preservado em PRD, spec e Task; fontes REQUIRED apenas para dependencias escolhidas.
  Sem componentes/dependencias distribuidos ou instalacao global; licencas e pins
  verificados mantidos como referencias. Instrucoes sem restricao por SO.


- Cutter2.5.0 e Rizin0.9.1 portateis preparados no Windows, SHA256 oficial
  verificado. Disassembly e rz-ghidra recuperaram retorno42 de PE proprio.
  Registro suplementar e reutilizacao pelo tool-state; sem providerREA inventado.
- Tests leem/escrevem UTF8 explicitamente; tool-state aceita tokens de versao
  prerelease/build limitados sem guardar logs arbitrarios. 626 testes passaram
  com PythonUTF8mode0/cp1252. Linux:25 testes do helper passaram nesta revisao.

- Adaptacao local Windows10: 626 testes nativos passaram com codificacao padrao Windows, zero falhas/erros.
  Fixtures POSIX foram substituidas por executaveis adequados ao host; DACL
  privada, NtCreateFile relativo a handle, hardlinks/reparse e hash aprovado
  preservam protecoes de arquivos. Nenhum teste antigo foi ignorado para passar.
- REA4.1.0: bootstrap/gateway Windows chamam entrypoints Node diretamente;
  provider paths locais persistidos, Ghidra12.1.4 e JDK21 preparados com
  checksums oficiais. Analises reais de fixtures JavaScript/.NET/PE x64 e
  decompilacao `return 0x2a` passaram. Hopper/IDA sem instalacao/licenca.
- BeyondSEO2.9.1: bootstrap HTTP-only e probe executados no Windows; nenhuma
  instalacao de browser ou crawl real. Runtime pronto nao certifica sites reais.
- Fingerprint exclui dependencias geradas; catalogo WINDOWS_SUITE distingue
  execucao nativa observada de macOS ainda nao verificado.
- Catalogos `Tools (Linux)`, `Tools (Windows)` e `Tools (macOS)` para os 11
  entrypoints proprios, com caminhos canonicos e status individual.
- Selecao de plataforma persistida no Environment State existente, com
  reutilizacao e invalidacao por mudanca relevante de runtime/catalogo/fonte.
- README com suporte relatado, suite Linux executada e Windows/macOS ainda
  nao homologados no baseline. O port Windows10 foi executado na etapa seguinte.
- Inicio deste historico de versoes e atualizacoes. Nenhum novo numero de
  release ou homologacao Windows/macOS foi publicado nesta alteracao.

## 2026-10-12, commit 43685da, PR #48

[Merge publicado na main](https://github.com/guilhermedemorais-dev/Dev-workflow/pull/48).
Roteamento consultivo de conhecimento tecnico no SDD/Harness, seis referencias
tematicas de arquitetura, dados/concorrencia, autenticacao, APIs/jobs,
qualidade/operacoes e fiscal; aprendizado sustentado por fontes e testes
estruturais. Nao corresponde a homologacao nativa Windows/macOS.

Versoes observadas nos manifests dessa revisao, mantidas sem incremento por
este trabalho:

| Plugin | Codex | Claude |
| --- | --- | --- |
| dev-environment-standard | 0.1.0 | 0.1.0 |
| dev-workflow-standard | 0.3.0+codex.20260922 | 0.7.0 |
| sdd-spec-factory | 0.1.0+codex.20260622 | 0.1.0 |

O merge #48 mudou conteudo sem incrementar esses manifests. Por isso, a versao
sozinha nao identifica todas as mudancas: registre tambem o commit exato.

## 2026-10-10, commit 0e17c69, PR #44

[Merge publicado na main](https://github.com/guilhermedemorais-dev/Dev-workflow/pull/44).
Evolucao local de conhecimento/contexto dos projetos. Este registro foi
reconstruido pelo historico Git, nao por uma release numerada. O historico
anterior ainda nao foi reconstruido integralmente.

## Regra para as proximas publicacoes

1. Registrar resumo, plugins afetados, mudancas de comportamento, dependencias
   e incompatibilidades antes do merge.
2. Incrementar os manifests de distribuicao afetados e manter os catalogos do
   host coerentes. Nao atribuir versao nova a plugin sem mudanca.
3. Registrar commit exato, PR, data e comandos/resultados de validacao por
   sistema e runtime. Teste simulado de SO nao certifica execucao nativa.
4. Mover a entrada aprovada de "Nao publicado" para a versao/data correspondente
   quando a publicacao ocorrer; nao anunciar Windows10/macOS antes da evidencia.
5. Documentar migracao, atualizacao da instalacao local, necessidade de nova
   sessao/reinicio e rollback quando aplicavel.
