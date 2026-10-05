import os

from sqlalchemy import text
from config import (engine_etl,
                    engine_cdb)
from normalizacao import (print_load,
                          print_response)

# Encerra conexões e exclui banco de dados antigo, caso exista, para evitar conflitos com a nova instância.
def limpar_banco_dados():

    print_load("Iniciando limpeza do banco de dados antigo...")

    sql_encerrar_conexoes = f"""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = '{os.getenv("DB_NAME")}'
                  AND pid <> pg_backend_pid();
                """  

    sql_excluir_banco = f"""
                DROP DATABASE IF EXISTS "{os.getenv('DB_NAME')}";
                """
    
    try:
        with engine_cdb.connect() as conn:
            conn.execute(text(sql_encerrar_conexoes))

            # Encerra conexões existentes
            print_load(f"Encerrando conexões com o banco '{os.getenv('DB_NAME')}'...")

            conn.execute(text(sql_encerrar_conexoes),
                 {"db_name": os.getenv('DB_NAME')}
            )

            print_response("Conexões encerradas com sucesso!")

            # Exclui o banco de dados antigo
            print_load(f"Excluindo banco de dados '{os.getenv('DB_NAME')}'...")

            conn.execute(text(sql_excluir_banco))

            print_response(f"Banco de dados '{os.getenv('DB_NAME')}' excluído com sucesso!")

    except Exception as erro:

        print_response("Erro ao excluir banco de dados:")
        print_response(erro)

    finally:

        engine_cdb.dispose()

        print_response("Conexão encerrada.")


def testar_conexao():

    print_load("Iniciando teste de conexão para uma nova instância...")

    try:
        with engine_cdb.connect() as conn:
            conn.execute

            print_response("Conexão realizada com sucesso!")
            print_response(f"Conectado ao PostgreSQL no host '{os.getenv('DB_HOST')}' na porta '{os.getenv('DB_PORT')}'.")

    except Exception as erro:
        print_response("Erro ao conectar ao PostgreSQL:")
        print_response(erro)


def criar_banco_dados():

    print_load("Iniciando criação do banco de dados...")

    sql_criar_banco_de_dados = f"""
                 CREATE DATABASE "{os.getenv('DB_NAME')}";
                """

    try:
        with engine_cdb.connect() as conn:
            conn.execute(text(sql_criar_banco_de_dados))

        print_response(f"Banco de dados '{os.getenv('DB_NAME')}' criado com sucesso!")

    except Exception as erro:
        print_response("Erro ao criar banco de dados:")
        print_response(erro)

def criar_schema():

    print_load("Iniciando criação do schema(s)...")

    sql_criar_schema = """
                CREATE SCHEMA IF NOT EXISTS vendas;
                """

    try:
        with engine_etl.begin() as conn:
            conn.execute(text(sql_criar_schema))

        print_response("Schema 'vendas' criado com sucesso!")

    except Exception as erro:
        print_response("Erro ao criar schema:")
        print_response(erro)

def criar_tabela_raw():

    print_load("Iniciando criação da(s) tabela(s)...")

    sql_criar_tabela_raw = """
                CREATE TABLE vendas.raw_vendas (
                    "Invoice ID" VARCHAR(50),
                    "Branch" VARCHAR(10),
                    "City" VARCHAR(100),
                    "Customer type" VARCHAR(50),
                    "Gender" VARCHAR(20),
                    "Product line" VARCHAR(150),
                    "Unit price" NUMERIC(10,2),
                    "Quantity" INTEGER,
                    "Tax 5%" NUMERIC(10,2),
                    "Sales" NUMERIC(12,2),
                    "Date" VARCHAR(50),
                    "Time" VARCHAR(50),
                    "Payment" VARCHAR(50),
                    "cogs" NUMERIC(12,2),
                    "gross margin percentage" NUMERIC(10,2),
                    "gross income" NUMERIC(12,2),
                    "Rating" NUMERIC(4,2)
                );
                """

    try:
        with engine_etl.begin() as conn:
            conn.execute(text(sql_criar_tabela_raw))

        print_response("Tabela 'raw_vendas' criada com sucesso!")
        
    except Exception as erro:
        print_response("Erro ao criar tabela:")
        print_response(erro)

def criar_tabela_vendas_tratadas():

    sql_criar_tabela_vendas_tratadas = """
                CREATE TABLE vendas.vendas_tratadas (
                    id_venda VARCHAR(50) PRIMARY KEY NOT NULL,
                    filial VARCHAR(10) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    tipo_cliente VARCHAR(50),
                    genero VARCHAR(20),
                    linha_produto VARCHAR(150) NOT NULL,
                    preco_unitario NUMERIC(10,2)
                        CHECK (preco_unitario >= 0),
                    quantidade INTEGER
                        CHECK (quantidade > 0),
                    imposto NUMERIC(10,2)
                        CHECK (imposto >= 0),
                    valor_total NUMERIC(12,2)
                        CHECK (valor_total >= 0),
                    data_venda DATE,
                    hora_venda TIME,
                    forma_pagamento VARCHAR(50) NOT NULL,
                    custo_mercadoria NUMERIC(12,2)
                        CHECK (custo_mercadoria >= 0),
                    margem_percentual NUMERIC(10,2),
                    receita_bruta NUMERIC(12,2)
                        CHECK (receita_bruta >= 0),
                    avaliacao NUMERIC(4,2)
                        CHECK (avaliacao >= 0 AND avaliacao <= 10)
                );
                """

    try:
        with engine_etl.begin() as conn:
            conn.execute(text(sql_criar_tabela_vendas_tratadas))

        print_response("Tabela 'vendas_tratadas' criada com sucesso!")

    except Exception as erro:
        print_response("Erro ao criar tabela:")
        print_response(erro)