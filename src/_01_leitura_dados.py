import pandas as pd

from config import engine_etl
from normalizacao import (print_title,
                          print_load, 
                          print_response)

def ler_dados_tabela_raw_vendas():

    print_load("Iniciando a leitura dos dados da tabela raw_vendas...")
    
    # Leitura da tabela raw_vendas para o DataFrame
    df = pd.read_sql(
        "SELECT * FROM vendas.raw_vendas",
        engine_etl
    )

    # Informações gerais do DataFrame
    print_title("Informações das colunas:")
    print(df.info())

    # Exibição das primeiras linhas do DataFrame
    print_title("Primeiras linhas:")
    print(df.head(10))

    # Exibição das últimas linhas do DataFrame
    print_title("Últimas linhas:")
    print(df.tail(10))

    # Verificação de valores nulos
    print_title("Valores nulos:")    
    print(df.isnull().sum())

    # Verificação de estatísticas
    print_title("Estatísticas:")
    print(df.describe(include="all"))

    # Tipos de data e hora
    print_title("Data e Hora:")
    print(df[["Date", "Time"]].head(10))

    # Quantidade de registros do DataFrame
    print_title("Quantidade de registros:")
    print(len(df))

    return df

def carregar_dados_csv_raw_vendas(df):

    # Exportação para CSV
    print_load("Carregando dados no CSV raw_vendas...")

    df.to_csv(
        "data/raw/raw_vendas.csv",
        index=False,
        encoding="utf-8"
    )

    print_response("Dados carregados com sucesso!")
    print_response(f"Total de {len(df)} registros carregados")

if __name__ == "__main__":

    df = ler_dados_tabela_raw_vendas()
    carregar_dados_csv_raw_vendas(df)
