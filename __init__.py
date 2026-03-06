
from corestexto import msg #msg é so uma funçao que retorna uma mensagem com cor, sem ter que escrever a formatação toda vez

from desafio113 import * #tem o leiaInt, explicado no programa principal
from yfinance import * # serve para acessar o preço das ações, se um ativo existe, etc
from datetime import datetime # pegar o dia
from locale import currency #formatar os valores no sistema financeiro brasileiro
import locale


def validaTicker(acao): # essa função checa de um Ticker existe
    try:
        ticker = Ticker(f"{acao.upper()}.SA")
        preco_atual = ticker.history(period="10d")["Close"].iloc[-1]
        """aqui ele tenta acessar o preço de uma ação cujo o ticker é string ticker, 
        se conseguir, retorna True (ação existe), se não, retorna false (ação nao existe)"""
    except:
        return False
    else:
        return True

def pregaoAberto(): #aqui ele ve se a bolsa está aberta, pois
                    #se estiver aberta pega o preço das ações em tempo real, se não, pega o preço do ultimo fechamento
    try:
        ticker = Ticker("VALE3.SA")
        preco_atual = ticker.history(period="1d")["Close"][-1]
    except:
        return False
    else:
        return True


def positivoInt(texto):

    while True:

        valor = leiaInt(texto)
        if valor > 0:
            return valor
        else:
            print(msg("Valor invalido! Digite um valor válido", "Vermelho"))

def positivoFloat(texto):
    while True:

        valor = leiaFloat(texto)
        if valor > 0:
            return valor
        else:
            print(msg("Valor invalido! Digite um valor válido", "Vermelho"))

# essas funções servem para aceitar somente valores positivos, para evitar que o usuario digite preços negativos de ações.

def menu(txt1, txt2, txt3, txt4,txt5): #função para organizar o MENU

    txt = [txt1, txt2, txt3, txt4,txt5]

    print("-"*14, end ='')
    print(msg("MENU", "Azul").center(14), end = '')
    print("-"*14)

    for c, d in enumerate(txt, start = 1):
        print(f"{c} - {d}")
    return

def verify(carteira, acao): # função para verificar se tem uma ação na carteira ou não, pois dependendo se tiver ou não, a forma de manipulação muda

    if any(a == acao for a in carteira):
        return True
    else:
        return False


def leiaFloat(txt): #função semelhante ao positivoFloat, mas aceita numeros negativos
    while True:
        try:
            a = float(input(txt))
        except ValueError:
            print(msg("Isso não é um numero! Digite um numero valido", "Vermelho"))
        else:
            return a


def compraAcao(carteira, operacao): #registra uma operação de compra

    while True:
        acao = input("Qual a ação vc quer registrar compra? Se quiser sair clique 0 ").upper()

        if acao != "0":

            if not validaTicker(acao): # checa se o ticker escrito é valido
                print("Código irregular!")

            else:

                quantidade = positivoInt("Qual a quantidade vc comprou? ")
                preco = positivoFloat("Qual preço da compra? (R$) ")
                gastoatual = preco * quantidade
                hora = datetime.now().strftime("%H:%M:%S")

                if verify(carteira, acao):

                    """aqui embaixo ele checa a posição do usuario, por exemplo, se a quantidade for negativa, ex -100 
                     e ele compra 100, signica q ele zerou a posição, já se a posição nao existir, ele tem que criar 
                     a nova posição, se a posição já existir, ele tem que acessar a posição antiga para calcular a nova
                     posiçao e novo preço médio, então cada if tem um caso diferente de situação, por exemplo, se ele 
                     reverteu a posição (tava vendido e comprou mais do que tinha, ex: tinha -100 e comprou 150, a posição
                     agora é 50), e a partir da situação ele calcula a nova posição e novo preço medio, ocorre da mesma forma
                     no registrar Venda.
                     """
                    if carteira[acao]["quantidade"] > 0:   # já tinha a ação na carteira em posição comprada e comprou mais ainda
                        gastoinic = carteira[acao]["quantidade"] * carteira[acao]["preco"]
                        gasto_total = gastoinic + gastoatual
                        carteira[acao]["quantidade"] += quantidade
                        carteira[acao]["preco"] = (gasto_total / carteira[acao]["quantidade"])
                        print(msg("Compra registrada com sucesso!", "Verde"))

                    elif carteira[acao]["quantidade"] < 0 and carteira[acao]["quantidade"]*-1 < quantidade: # reversão de operação, ex: tinha -50 comprou 100
                        carteira[acao]["quantidade"] += quantidade
                        carteira[acao]["preco"] = preco
                        print(msg("Compra registrada com sucesso!", "Verde"))

                    elif carteira[acao]["quantidade"] < 0 and carteira[acao]["quantidade"]*-1 > quantidade: # Caso tenha posição vendida e  comprou uma quantidade menor do que posição,
                                                                                                            # ex: -100, comprou 50, o PM nao muda, mas a posição atual fica de -50
                        carteira[acao]["quantidade"] += quantidade
                        print(msg("Compra registrada com sucesso!", "Verde"))

                    else:   # se a posição é negativa, e comprou exatamente a posição que tinha, o unico caso que restou, ex: tinha -100 comprou 100
                        del carteira[acao]
                        print(msg("Posição zerada com sucesso!", "Verde"))

                    operacao = {"Ticker" : acao, "Quantidade" : quantidade, "Preco" : preco, "Valor" : gastoatual, "Tipo" : "Compra", "Hora" : hora}
                    return operacao


                else: # caso a ação nao exista na carteira do usuario, cria uma posição nova

                    carteira[acao] = {"preco": preco, "quantidade": quantidade}
                    print(msg("Compra realizada com sucesso!", "Verde"))
                    operacao = {"Ticker" : acao, "Quantidade" : quantidade, "Preco" : preco, "Valor" : gastoatual, "Tipo" : "Compra", "Hora" : hora}
                    return operacao

        else:
            break


def vendaAcao(carteira, operacao): # funciona da mesma forma da compra, só que adaptada para venda, casa if tbm funciona igual a compra, soq adaptada pra venda
    hora = datetime.now().strftime("%H:%M:%S")
    while True:
        acao = input("Qual ação vc quer vender? Clique 0 pra sair ").upper()

        if acao != "0":
            if validaTicker(acao):
                quantidadeVenda = positivoInt("Qual a quantidade vc quer vender? ")
                precoVenda = positivoFloat("Qual foi o preço da venda? (R$) ")
                valoratual = precoVenda * quantidadeVenda
                if verify(carteira, acao):
                    if carteira[acao]["quantidade"] == quantidadeVenda:
                        try:
                            del carteira[acao]
                        except Exception as e:
                            print(f"Erro de {e} ao zerar posição")
                        else:
                            print("Posição zerada com sucesso!")
                    elif carteira[acao]["quantidade"] < quantidadeVenda:
                        carteira[acao]["quantidade"] -=  quantidadeVenda
                        carteira[acao]["preco"] = precoVenda
                        print("Operação vendida feito com sucesso! ")

                    else:
                        carteira[acao]["quantidade"] -= quantidadeVenda
                        print(msg("Venda registrada com sucesso!", "Verde"))
                    operacao = {"Ticker": acao, "Quantidade": quantidadeVenda, "Preco": precoVenda, "Valor": valoratual,
                                "Tipo": "Venda", "Hora": hora}
                    return operacao
                else:
                    carteira[acao] = {"quantidade" : quantidadeVenda*-1, "preco": precoVenda}
                    print(msg("Operação vendida feita com sucesso!", "Verde"))
                    operacao = {"Ticker": acao, "Quantidade": quantidadeVenda, "Preco": precoVenda, "Valor": valoratual,
                                "Tipo": "Venda", "Hora": hora}
                    return operacao
            else:
                print(msg("Ticker inválido!", "Vermelho"))
        else:
            break


def pegarPreco(acao, carteira): # recebe o ticker de uma ação e a carteira, ai na carteira ele pega a quantidade, preço meido, pesquisa o preço da ação e retorna o preço da ação e o lucro em base no preço medio e posição

    ticker = Ticker(f"{acao.upper()}.SA")
    if not pregaoAberto():
        preco_atual = ticker.history(period="5d")["Close"].iloc[-1]
    else:
        preco_atual = ticker.history(period="5d")["Close"][-1]
    lucro = (preco_atual - carteira[acao]["preco"])*carteira[acao]["quantidade"]
    return preco_atual, lucro

def mostrarExtrato(extrato):
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
    for k, v in extrato.items():
        print("-" * 15)
        print(f"{k}: ")
        for a in v:
            print("-" * 15)
            for b, c in a.items():
                if b == "Preco" or b == "Valor":
                    print(f"{b}: {currency(c, grouping=True)}")
                else:
                    print(f"{b}: {c}")
    input("Clique enter para voltar ao menu")

def adicExtrato(operacao, lista):

    lista.append(operacao)

    return


