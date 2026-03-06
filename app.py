
from carteiracomandos.comandos import * # importar a library com as funções
from desafio113 import leiaInt #leiaInt é uma função feita por mim pra evitar erros com input
import json #manipular arquivos json
from locale import currency #formatar os valores para o sistema financeiro brasileiro
from datetime import date #salvar as datas das transações
import locale
from time import sleep

"""
O objetivo desse projeto é servir de um auxiliar de gestão de carteira de investimentos,em que o usuario
registra suas operações (Compra e vendas de ativos listados na B3, bolsa brasileira) e o programa cria
dois arquivos .JSON, um que irá registrar as posições que o usuario tem e outro que irá salvar 
a data das transações registradas pelo usuario, caso o arquivo ja exista, ele abre o que já existe, ou seja,
as operações e ativos não são perdidas após o termino da execução do programa, só em caso de exclusão
dos arquivos.
"""

print(msg("ATENÇÃO! Se vc encerrar o programa sem ser pela opção de Sair, os registros não serão salvos no extrato e na carteira", "Amarelo"))
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


arq = "carteira.json"
ext = "extrato.json" # para manipular os arquivos de carteira de ativos e extrato
carteira = {}
operacao = {}
extrato = {}
data =[]
hoje = str(date.today()) #para manipulação de data usando string

try:
    with open(arq, "rt") as arquivo: #checa se o arquivo de carteira existe, se nao existir ele cria
        carteira = json.load(arquivo)

except FileNotFoundError:
    a = open(arq, "wt")
    a.close()

"""
Detalhe importante - o extrato funciona da seguinte forma: 
    Ele é um dicionario de lista de dicionarios. 
    Cada operação é um dicionario, contendo a DATA, Ativo, horario, quantidade, tipo de operação, etc.
    
    Esse dicionario da operação é guardado dentro de uma lista, essa lista vai conter todas as operações
    de um determinado dia, ou seja, para cada dia existe uma lista contendo as operações realizadas naquele dia.
    
    Cada lista é guardada no dicionario maior, cuja chave para cada lista é exatamente a data cuja aquela lista
    vai conter as operações, em formato de aaaa-mm-dd, e tranformada em STRING.
    
    Por exemplo, a chave da lista com as operações do dia 25/02/2026, vai ser:
    "2026-02-25".
    
Já a carteira funciona de forma mais simples: 
    Ela é um dicionario de dicionarios, em que o TICKER do ativo, por exemplo, BBAS3, é a chave
    para um dicionario contendo as informações do usuario para o respectivo ativo, como o preço médio e
    quantidade. Lembrando que a quantidade pode ser negativa, pois a Bolsa de Valores permite um operador
    vender uma ação sem possuir (Venda a Descoberto)  
"""

try:
    with open(ext, "rt") as arquivo: #aqui ele tbm checa se o arquivo de extrato existe, se nao ele cria
        try:
            extrato = json.load(arquivo) # e se o arquivo existir, ele pega o dicionario contendo o extrato

        except:
            extrato = {}

        else:
            if hoje not in extrato: #Verificação se já existe uma lista com as operações de hoje, se existir ele abre, se não, ele cria uma lista vazia.
                data = []
            else:
                data= extrato[hoje]
except FileNotFoundError:
     a = open(ext, "wt")
     a.close()
     extrato = {}

sleep(1)
while True:
    menu("Registrar compra", "Registrar venda","Mostrar carteira", "Acessar extrato", "Sair")

    c = leiaInt("Sua opção: ")

    if c == 1:

        try:

            operacao1 = compraAcao(carteira, operacao) # função de registrar compra de ativo

            adicExtrato(operacao1, data) #função de adicionar operação no extrato

        except Exception as e:
            print(msg(f"Erro de {e} ao registrar compra", "Vermelho"))


    elif c == 2:
        try:
            operacao1 = vendaAcao(carteira, operacao) # recebe o dicionario da operação

            adicExtrato(operacao1, data) # adiciona a operação no extrato

        except Exception as erro:
            print(msg(f"Erro de {erro} ao registrar venda", "Vermelho"))


    elif c == 3:
        for a in carteira: # Nesse ciclo, o a vai ser cada chave do dicionario da carteira, ou seja, vai ser o TICKER de cada ativo do usuario, ex: BBAS3
            x = ""
            valores = pegarPreco(a, carteira)  # Essa função pega o preço de uma determinada ação em tempo real e calcula o lucro em função da posição, retornando tanto o preço como o lucro em uma lista
            preco_atual = valores[0]
            lucro = valores[1]
            print("-"*15)
            print(f"{a.upper()}")
            print(f"Preço médio: {currency(carteira[a]["preco"], grouping=True)}") # aqui ele acessa a posiçao de cada ativo, com o preço medio e quantidade
            print(f"Quantidade: {carteira[a]["quantidade"]}")
            print(f"Posição total: {currency(preco_atual*carteira[a]["quantidade"], grouping=True)}")
            print(f"Preço atual: {currency(preco_atual, grouping=True)}")
            if lucro < 0:
                x = "Vermelho"
            else:
                x = "Verde"
            print(msg(f"Resultado: {currency(lucro, grouping=True)}", x))
        input("Clique enter para voltar ao menu")


    elif c == 4:
        extrato[hoje] = data
        mostrarExtrato(extrato)

    elif c == 5:
        print("Encerrando... ")
        break

    else:
        print(msg("Opção não disponivel!", "Vermelho"))


with open(arq, "wt") as arquivo:
    json.dump(carteira, arquivo, indent = 4) #aqui ele salva a carteira baseado nas operações feita na execução

with open(ext, "wt") as arqui:
    json.dump(extrato, arqui, indent = 4) #aqui ele salva o extrato tbm nas operações feita na execução

""" 
PS: Eu decidi so fazer essas alterações no final do programa, pois caso eu fizesse no meio do programa,
    teria que ser feitas varias alterações, ficando mais suscetível a erros e piorando a execução do programa,
    então preferi manipular usando somente dicionarios e listas durante o programa e so manipular os arquivos
    no começo, para extrair as informações ja existentes e no final, para salvar as informações modificadas.
    
    O unico defeito de fazer assim, é caso o usuario não encerre pelo MENU, as informações não serão salvas,
    porém, isso já está avisado na inicialização do programa.
"""