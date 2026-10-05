# Pipeline ETL - Fluxo de Execução

from normalizacao import print_response
from criar_banco_dados import (testar_conexao,
                                limpar_banco_dados,
                                criar_banco_dados, 
                                criar_schema, criar_tabela_raw,
                                criar_tabela_vendas_tratadas)
from extracao_dados import (extrair_dados_csv_kaggle,
                           carregar_dados_tabela_raw_vendas)
from consultas_sql import executar_consultas_sql
from _01_leitura_dados import (ler_dados_tabela_raw_vendas, 
                               carregar_dados_csv_raw_vendas)
from _02_etl_vendas import (extrair_dados_csv_raw_vendas,
                            carregar_dados_csv_vendas_tratadas)
from _03_estatistica import ler_csv_vendas_tratadas

def main():

    # Limpa o banco de dados, caso exista, para uma nova execução do ETL
    limpar_banco_dados()

    # Testa a uma nova conexão com o banco de dados após a limpeza da antiga instância
    testar_conexao()

    # Cria o banco de dados
    criar_banco_dados()

    # Cria o schema vendas
    criar_schema()

    # Cria a tabela raw_vendas
    criar_tabela_raw()

    # Cria a tabela vendas_tratadas
    criar_tabela_vendas_tratadas()

    # Extrai dados do Kaggle
    caminho = extrair_dados_csv_kaggle()

    # Carrega dados na tabela raw_vendas
    carregar_dados_tabela_raw_vendas(caminho)

    # Exibe consultas SQL na tabela raw_vendas
    executar_consultas_sql()

    # Lê dados da tabela raw_vendas e exibe informações
    df = ler_dados_tabela_raw_vendas()

    # Carrega dados para o CSV raw_vendas 
    carregar_dados_csv_raw_vendas(df)

    # Extrai os dados do CSV raw_vendas, realiza a limpeza e transformação dos dados
    df = extrair_dados_csv_raw_vendas()

    # Carrega os dados tratados no CSV vendas_tratadas e na tabela vendas_tratadas
    carregar_dados_csv_vendas_tratadas(df)

    # Lê os dados do CSV vendas_tratadas e exibe estatísticas
    ler_csv_vendas_tratadas()

    print_response("Pipeline ETL concluído!")

if __name__ == "__main__":
     main()

# Comando para executar o pipeline ETL no terminal: .../ETL_Supermercado/src/python executar_etl.py