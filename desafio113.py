
import corestexto as cor


def leiaInt(txt):
    while True:
        try:
            a = int(input(txt))
            break
        except KeyboardInterrupt:
            print("O usuario nao informou o dado")
            break
        except Exception:
            cor.msg("ERRO! Digite um inteiro valido!", "Vermelho")
    return a





