# Tools por sistema operacional

Status: alteracao local ainda nao publicada. A compatibilidade nativa
Windows10 nativo foi validado localmente com 626 testes, sem falhas ou erros.
Windows11 e macOS ainda nao foram executados.

## Estrutura

Os catalogos estao dentro do plugin `dev-environment-standard`, para serem
distribuidos com ele:

```text
plugins/dev-environment-standard/
  Tools (Linux)/catalog.json
  Tools (Windows)/catalog.json
  Tools (macOS)/catalog.json
```

Cada catalogo aponta para as implementacoes canonicas dos 12 entrypoints
proprios: 9 Python, 2 Node e 1 Bash. O novo `compose-scope.py` foi testado
com fixtures Linux; continua `NOT VALIDATED` nos catalogos Windows e macOS. Scripts compartilhados nao sao duplicados
nem movidos, preservando os caminhos usados pelas skills e pelos testes.
Os registros de ferramentas externas continuam pertencendo aos especialistas;
o catalogo de plataforma nao copia nem substitui `tool-registry.json`.

`eligible` e o sinal de roteamento individual do catalogo, sujeito aos limites
registrados. `WINDOWS_SUITE` descreve cobertura na suite Windows nativa;
`LINUX_SUITE` descreve cobertura na suite Linux, nao teste de todas
as integracoes externas ou de todos os casos de uso. `NOT VALIDATED` e
`UNSUPPORTED` nao podem ser tratados como PASS. O launcher Bash com
gnome-terminal nao possui versao Windows/macOS. Runtimes SEO/REA ainda requerem
validacao de suas dependencias e integracoes reais.

## Preparar uma vez, reutilizar no mesmo ambiente

A instalacao assistida invoca `environment.py prepare` com os caminhos reais do
checkout, projeto e estado local. Ela persiste `platform_tools` no mesmo
Environment State ignorado que ja guarda preferencias e evidencias. Esta
alteracao nao cria um hook automatico de instalacao no host.

Em tarefas seguintes, `environment.py status` informa a selecao compativel. Nao
instala nada, nao altera manifests do plugin e nao pede o sistema novamente.
Verificacoes locais de integridade sao diferentes de repetir descoberta em
rede, instalacao ou perguntas. Estado de saude expirado pode exigir nova
validacao sem exigir que o usuario escolha novamente seu sistema.

Troca de runtime/SO/interprete ou alteracao relevante do catalogo/fonte invalida
a selecao. WSL seleciona Linux porque a execucao ocorre no Linux, mesmo com o
desktop no Windows. Estado Linux nao autoriza executar a mesma tool no Python
nativo Windows. Windows10 e Windows11 compartilham o catalogo Windows, mas
continuam exigindo evidencias das versoes que forem declaradas suportadas.

Os comandos abaixo sao exemplos para um checkout, substituindo os caminhos
pelos reais e usando o Python do ambiente onde as tools vao executar:

```text
python plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py prepare --repo-root CAMINHO_DO_HARNESS --workspace CAMINHO_DO_PROJETO --state-dir CAMINHO_DO_ESTADO --host codex --json
python plugins/dev-environment-standard/skills/dev-environment-standard/scripts/environment.py status --repo-root CAMINHO_DO_HARNESS --workspace CAMINHO_DO_PROJETO --state-dir CAMINHO_DO_ESTADO --host codex --json
```

`prepare` continua respeitando as politicas e aprovacoes existentes. Catalogo
selecionado nao prova que MCP esta conectado ou autenticado. Capacidade ausente
ou nao homologada requer alternativa compativel ou uma pendencia explicita;
nao reescrever scripts ou instalar WSL sem autorizacao.

## Contexto nao e estado do ambiente

`context-retriever.py` oferece recuperacao complementar com Potpie quando
disponivel e busca lexical local como fallback. Ele encontra referencias de
projeto; nao guarda escolhas de sistema nem concede compatibilidade.
`Environment State` guarda a selecao/saude/preferencias. `tool-state.py` guarda
executaveis e versoes por especialista e ambiente. Reutilizar esses mecanismos,
sem criar um segundo cache ou usar RAG como fonte de autorizacao.

## Evidencia inicial e proxima adaptacao

No baseline 43685da, Windows10 build19045, Python nativo e UTF-8 explicito:
595 testes, 24 falhas e 13 erros. Ubuntu24.04.5 no WSL2, filesystem Linux:
595 testes, OK, 1 ignorado. Linux Mint e o ambiente original relatado pelo
mantenedor; nova execucao/versao especifica nao foi registrada nesta sessao.
macOS e Windows11 nao foram executados.

O port local corrigiu fixtures nativas, DACL e escrita relativa a handles,
sem remover protecoes. Windows10: 626 testes passaram com codificacao padrao Windows, zero falhas/erros.
Regressao Ubuntu/WSL: 626 testes, OK, 16 ignorados, sendo 7 Windows e
9 dependentes de Node ausente no runtime Linux. REA analisou JavaScript,
managed.NET e PE x64 proprio com Ghidra. SEO HTTP-only foi instalado; probe
retorna WARN/exit1 por renderer opcional ausente, http_ready=true. Nao houve
crawl real. Cinco plugins instalados foram atualizados como preview local;
refresh da main pode substituir esse preview enquanto a publicacao estiver pendente.

Revisao4: Cutter/Rizin suplementares preparados no Windows, decompilacao42
observada. Linux:25 testes do helper e suite completa626 passaram nesta revisao. GUI Cutter e runtimes Cutter/Rizin Linux/macOS nao foram homologados.
