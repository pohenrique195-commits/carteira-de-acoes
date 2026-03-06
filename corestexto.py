
cores = {"Vermelho" : "\033[1:31m",
        "Verde" : "\033[1:32m",
         "Azul" : "\033[1:34m",
         "Encerrar" : "\033[0m",
         "Amarelo" : "\033[1:33m",}

def msg(txt, cor):
    return f"{cores[cor]} {txt} {cores['Encerrar']}"
