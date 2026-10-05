import pandas as pd

from sqlalchemy import text
from pathlib import Path
from normalizacao import (print_title,
                          print_load,
                          print_response)
from config import engine_etl

def extrair_dados_csv_raw_vendas():

    print_title("Início do processo de ETL...")

    # Extrai do arquivo raw_vendas.csv para o DataFrame
    print_load("Extraindo dados do arquivo raw_vendas.csv...")

    df = pd.read_csv(
        "data/raw/raw_vendas.csv"
    )

    print_response("Dados extraídos com sucesso!")
    print_response(f"Total de {len(df)} registros extraídos.")
    print_title("Colunas antes da renomeação")
    print(df.columns.tolist())

    # Renomeia as colunas
    print_load("Renomeando colunas...")

    df = df.rename(columns={
        "Invoice ID": "id_venda",
        "Branch": "filial",
        "City": "cidade",
        "Customer type": "tipo_cliente",
        "Gender": "genero",
        "Product line": "linha_produto",
        "Unit price": "preco_unitario",
        "Quantity": "quantidade",
        "Tax 5%": "imposto",
        "Sales": "valor_total",
        "Date": "data_venda",
        "Time": "hora_venda",
        "Payment": "forma_pagamento",
        "cogs": "custo_mercadoria",
        "gross margin percentage": "margem_percentual",
        "gross income": "receita_bruta",
        "Rating": "avaliacao"
    })

    print_title("Colunas após renomeação")
    print(df.columns.tolist())

    # Converte a data para o formato datetime
    df["data_venda"] = pd.to_datetime(
        df["data_venda"],
        format="%m/%d/%Y",
        errors='coerce'
    ).dt.date

    # Converte a hora para o formato datetime
    df["hora_venda"] = pd.to_datetime(
        df["hora_venda"],
        format="%I:%M:%S %p",
        errors='coerce'
    ).dt.time

    # Converte as colunas para númericas, 
    # tratando valores inválidos como NaN
    colunas_numericas = [
        "preco_unitario",
        "quantidade",
        "imposto",
        "valor_total",
        "custo_mercadoria",
        "margem_percentual",
        "receita_bruta",
        "avaliacao"
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    print_title("Tipos de dados após conversão:")
    print(df.dtypes)

    # Verifica datas inválidas
    print_title("Verificação de datas inválidas:")
    print(df["data_venda"].isnull().sum())

    # Verifica horas inválidas
    print_title("Verificação de horas inválidas:")
    print(df["hora_venda"].isnull().sum())

    # Verifica valores nulos
    print_title(f"Valores nulos por coluna:")
    print(df.isnull().sum())

    # Verifica valores duplicados
    print_title("Quantidade de registros duplicados:")
    print(df.duplicated().sum())

    return df

def carregar_dados_csv_vendas_tratadas(df):

    # Carrega dados no CSV vendas_tratadas
    print_load("Carregando dados no CSV vendas_tratadas...")

    df.to_csv(
        "data/processed/vendas_tratadas.csv",
        index=False,
        encoding="utf-8"
    )

    print_response("Dados carregados com sucesso!")
    print_response(f"Total de {len(df)} registros carregados no CSV vendas_tratadas")

    # Carrega os dados na tabela vendas_tratadas
    print_load("Carregando dados na tabela vendas_tratadas...")

    df.to_sql(
            "vendas_tratadas",
            engine_etl,
            schema="vendas",
            if_exists="append",
            index=False
        )
       
    print_response("Dados carregados com sucesso!")

    # Valida a quantidade de registros na tabela vendas_tratadas
    with engine_etl.connect() as conn:
        resultado = conn.execute(
            text("SELECT COUNT(*) FROM vendas.vendas_tratadas")
        )

        quantidade = resultado.scalar()

    print_response(f"Total de {quantidade} registros na tabela vendas_tratadas")

if __name__ == "__main__":

    df = extrair_dados_csv_raw_vendas()
    carregar_dados_csv_vendas_tratadas(df)