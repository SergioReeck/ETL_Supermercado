import pandas as pd

from normalizacao import (print_title,
                          print_load,
                          print_response)

def ler_csv_vendas_tratadas():
    # Leitura da base tratada
    print_load("Iniciando a leitura dos dados do CSV vendas_tratadas para análise...")
    df = pd.read_csv(
        "data/processed/vendas_tratadas.csv"
    )

    print_response("Base carregada com sucesso!")
    print_response(f"Total de registros {len(df)} carregados")

    # Filial com maior receita
    receita_por_filial = (
        df.groupby("filial")["valor_total"]
        .sum()
        .sort_values(ascending=False)
    )

    print_title("Receita total por filial")
    print(receita_por_filial)

    maior_receita = receita_por_filial.idxmax()
    valor_maior_receita = receita_por_filial.max()

    print_title("Filial com maior receita")
    print(f"Filial: {maior_receita}")
    print(f"Receita total: {valor_maior_receita:.2f}")

    # Filial com maior quantidade de vendas
    vendas_por_filial = (
        df.groupby("filial")
        .size()
        .sort_values(ascending=False)
    )

    print_title("Quantidade de vendas por filial")
    print(vendas_por_filial)

    maior_vendas = vendas_por_filial.idxmax()
    valor_maior_vendas = vendas_por_filial.max()

    print_title("Filial com maior quantidade de vendas")
    print(f"Filial: {maior_vendas}")
    print(f"Quantidade de vendas: {valor_maior_vendas}")

    # Linha de produto com maior receita
    receita_por_produto = (
        df.groupby("linha_produto")["valor_total"]
        .sum()
        .sort_values(ascending=False)
    )

    print_title("Receita total por linha de produto")
    print(receita_por_produto)

    # Linha de produto com melhor avaliação média
    avaliacao_por_produto = (
        df.groupby("linha_produto")["avaliacao"]
        .mean()
        .sort_values(ascending=False)
    )

    print_title("Avaliação média por linha de produto")
    print(avaliacao_por_produto)

    melhor_avaliacao_produto = avaliacao_por_produto.idxmax()
    maior_avaliacao_media = avaliacao_por_produto.max()

    print_title("Linha de produto com melhor avaliação média")
    print(f"Linha de produto: {melhor_avaliacao_produto}")
    print(f"Avaliação média: {maior_avaliacao_media:.2f}")

    # Forma de pagamento mais utilizada
    vendas_por_pagamento = (
        df.groupby("forma_pagamento")
        .size()
        .sort_values(ascending=False)
    )

    print_title("Quantidade de vendas por forma de pagamento")
    print(vendas_por_pagamento)

    forma_pagamento_mais_utilizada = vendas_por_pagamento.idxmax()
    quantidade_pagamentos = vendas_por_pagamento.max()

    print_title("Forma de pagamento mais utilizada")
    print(f"Forma de pagamento mais utilizada: {forma_pagamento_mais_utilizada}")
    print(f"Quantidade de vendas: {quantidade_pagamentos}")

    # Valor médio das vendas
    valor_medio_vendas = df["valor_total"].mean()

    print_title("Valor médio das vendas")
    print(f" {valor_medio_vendas:.2f}")

    # Maior venda
    maior_venda = df.loc[df["valor_total"].idxmax()]

    print_title("Maior venda")
    print(f"ID da venda: {maior_venda['id_venda']}")
    print(f"Filial: {maior_venda['filial']}")
    print(f"Linha de produto: {maior_venda['linha_produto']}")
    print(f"Valor da venda: {maior_venda['valor_total']:.2f}")

    # Dia da semana com mais vendas
    df["dia_semana"] = pd.to_datetime(
        df["data_venda"]
    ).dt.day_name()

    vendas_por_dia = (
        df.groupby("dia_semana")
        .size()
        .sort_values(ascending=False)
    )

    print_title("Quantidade de vendas por dia da semana:")
    print(f"{vendas_por_dia}")