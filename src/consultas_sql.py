import pandas as pd

from pathlib import Path
from config import engine_etl
from normalizacao import (
    extrair_titulo_sql,
    remover_comentarios_sql,
    print_title
)

def executar_consultas_sql():

    # Caminho do arquivo SQL
    caminho_sql = (
        Path(__file__).resolve().parent.parent
        / "sql"
        / "03_consultas.sql"
    )

    # Leitura do arquivo SQL
    with open(caminho_sql, "r", encoding="utf-8") as arquivo:
        conteudo_sql = arquivo.read()

    # Separa as consultas pelo ponto e vírgula
    consultas = [
        consulta.strip()
        for consulta in conteudo_sql.split(";")
        if consulta.strip()
    ]

    # Executa cada consulta
    for consulta in consultas:

        # Extrai automaticamente o título do comentário
        titulo = extrair_titulo_sql(consulta)

        # Remove o comentário antes de enviar o SQL para o banco
        consulta_sql = remover_comentarios_sql(consulta)

        # Exibe o título
        print_title(titulo)

        # Executa a consulta
        resultado = pd.read_sql(
            consulta_sql,
            engine_etl
        )

        # Exibe o resultado
        print(resultado.to_string(index=False))