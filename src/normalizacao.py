def extrair_titulo_sql(consulta):
    
    linhas = consulta.strip().splitlines()

    for linha in linhas:

        linha = linha.strip()

        if linha.startswith("--"):
            return linha[2:].strip()

    return "Consulta SQL"


def remover_comentarios_sql(consulta):

    linhas = []

    for linha in consulta.splitlines():

        if not linha.strip().startswith("--"):
            linhas.append(linha)

    return "\n".join(linhas).strip()


def print_title(titulo):
    print("")
    print("=" * 70)
    print(f"{titulo.center(70)}")
    print("=" * 70)
    print(" ")

def print_response(resposta):
    print(" ")
    print(f"{resposta}")
    

def print_load(carga):
    print(" ")
    print(f"{carga}")