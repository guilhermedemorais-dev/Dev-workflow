# Exemplo sintético: consultar pedido do tenant

Documento ilustrativo, não descreve aplicação existente neste repositório.
Nenhum endpoint, interface ou teste de produto foi implementado ou executado.
As hipóteses abaixo definem somente o cenário didático; numa Task real precisam
ser confrontadas com código/arquitetura antes de autorizar implementação.

<a id="scope"></a>
## Escopo
Adicionar tela e adaptador de API para consulta por ID. Hipótese didática:
o projeto-alvo já tem sessão autenticada e serviço de leitura que exige tenant
do contexto servidor e ID do pedido, sem alterar query ou persistência.
O adaptador reutiliza esse serviço e não aceita tenant do payload do cliente.
Sem cadastro, alteração de pedido, pagamentos, deploy ou telemetria nova.

<a id="api"></a>
## API e contrato
Reutilizar serviço existente, validar formato do ID, mapear DTO mínimo.
Pedido ausente ou de outro tenant retorna resposta indistinguível sem dados
do pedido. Entrada inválida e falha temporária têm erros seguros e distintos.
Autorização é servidor, nunca só ocultação da interface. A hipótese do serviço
existente precisa de prova no projeto real antes da implementação.

<a id="ui"></a>
## Interface
Campo ID com label, ação Consultar, loading, resultado vazio, erro recuperável
e sucesso. Bloquear envio duplicado durante loading; preservar navegação por
teclado e foco visível. Não mostrar PII não requerida no DTO.

<a id="security"></a>
## Segurança
Tenant deriva da sessão, dados de outro tenant não são retornados ou logados.
Revisar chamadas reais e mitigadores, com teste negativo de isolamento.
Knowledge/scanner/QA candidate não confirma vulnerabilidade automaticamente.

<a id="qa"></a>
## Comportamento a verificar
Consulta legítima, ID inválido/vazio, inexistente, acesso entre contas, falha
temporária, retry e duplo envio. Validar esperado versus observado, estado e
número de chamadas. QA encaminha possível acesso cross-tenant à Security.
Regressão protege consulta legítima e ausência de envio duplicado.

<a id="persistence"></a>
## Invariantes da persistência
Neste cenário nenhuma query, regra de persistência ou schema é alterado.
Se uma implementação exigir nova query ou mudança desses contratos, ativar
esta fonte condicional e voltar ao Harness para revisar database N/A e escopo.
Ausência de migração sozinha não justifica ignorar semântica de consulta.

<a id="acceptance"></a>
## Aceite
Fluxos e erros correspondem ao contrato; isolamento servidor validado pela
Security; estados/fidelidade validados por UI; QA independente verifica cenários;
documentação corresponde ao comportamento. Nenhuma execução é afirmada aqui.
