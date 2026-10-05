import pandas as pd
import kagglehub

from sqlalchemy import text
from pathlib import Path
from config import engine_etl
from normalizacao import (print_load,
                          print_response)

def extrair_dados_csv_kaggle():

    print_load("Extraindo dados do Kaggle...")

    file_path = Path(
        kagglehub.dataset_download(
            "faresashraf1001/supermarket-sales"
        )
    )

    print("Dataset encontrado em:", file_path)

    return file_path

def carregar_dados_tabela_raw_vendas(file_path):

    print_load("Carregando dados na tabela raw_vendas...")
    print_load("Lendo registros do arquivo CSV baixado...")

    # Lê o arquivo CSV baixado do Kaggle
    df = pd.read_csv(
        file_path / "SuperMarket Analysis.csv"
    )

    print_response(f"Leitura concluída. Total de {len(df)} registros lidos")

    # Exporta os dados para a tabela raw_vendas
    print_load("Carregando os dados na tabela raw_vendas...")

    df.to_sql(
        "raw_vendas",
        engine_etl,
        schema="vendas",
        if_exists="append",
        index=False,
    )

    print_response("Carga na tabela raw_vendas concluída!")

    # Valida a quantidade de registros carregados na tabela raw_vendas
    with engine_etl.connect() as conn:
        resultado = conn.execute(
            text("SELECT COUNT(*) FROM vendas.raw_vendas")
        )

        quantidade = resultado.scalar()

    print_response(f"Total de {quantidade} registros carregados na tabela raw_vendas")

if __name__ == "__main__":

    caminho = extrair_dados_csv_kaggle()
    carregar_dados_tabela_raw_vendas(caminho)