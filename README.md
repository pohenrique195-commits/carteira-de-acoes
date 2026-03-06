# carteira-de-acoes

## GERENCIADOR DE CARTEIRA DE INVESTIMENTOS (B3)

Projeto em Python desenvolvido para auxiliar no controle de uma carteira de
investimentos na bolsa brasileira (B3).

O programa permite registrar compras e vendas de ativos, visualizar a posição
atual da carteira e acessar o histórico de operações realizadas.

O programa inicia com o seguinte menu:

MENU
1 - Registrar compra
2 - Registrar venda
3 - Mostrar carteira
4 - Acessar extrato
5 - Sair
Sua opção:

## FUNCIONALIDADES

1 - Registrar compra de ações
2 - Registrar venda de ações
3 - Mostrar carteira atual
4 - Mostrar extrato de operações
5 - Consulta de preço atual das ações

O programa calcula automaticamente o preço médio das posições e permite
operações de venda a descoberto (quantidade negativa).

## ARMAZENAMENTO DOS DADOS

Os dados são salvos automaticamente em dois arquivos JSON:

carteira.json
Guarda as posições atuais do usuário (preço médio e quantidade).

extrato.json
Guarda o histórico das operações registradas pelo usuário.

## ESTRUTURA DA CARTEIRA

A carteira é armazenada como um dicionário de dicionários, onde a chave é o
ticker da ação.

Exemplo:

{
"BBAS3": {
"preco": 28.50,
"quantidade": 100
}
}

Quando o usuario escolhe a opção de visualizar a carteira, as posições serão
mostradas no seguinte formato:

TICKER
Preço médio
Quantdade
Posiçao atual
Preço atual da ação
Lucro ou prejuízo

Exemplo:

VALE3
Preço médio: R$ 60,20
Quantidade: 100
Posição total: R$ 6.020,00
Preço atual: R$ 62,15
Resultado: +R$195,00

## ESTRUTURA DO EXTRATO

O extrato é organizado por data. Ele consiste num dicionário em que a chave é
uma data formatada em string, no modelo "aaaa-mm-dd" e possui uma lista com as
operações realizadas naquele dia.


Exemplo:

{
"2026-02-25": [
{
"Ticker": "VALE3",
"Quantidade": 100,
"Preco": 60.20,
"Valor": 6020,
"Tipo": "Compra",
"Hora": "10:35:12"
}
]
}

## TECNOLOGIAS UTILIZADAS

Python
JSON
Biblioteca yfinance (consulta de preços das ações)

## OBSERVAÇÃO

Os dados são salvos somente quando o programa é encerrado pela opção "Sair"
no menu. Caso o programa seja fechado abruptamente, as alterações realizadas
durante a execução podem não ser salvas.

## AUTOR

Pedro Henrique Mota Alves
