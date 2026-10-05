# 🛒  Análise de Dados com Python - Projeto Avaliativo - Módulo 1 - Semana 13 - Turma T3 - ETL Supermercado

Pipeline de **ETL (Extract, Transform, Load)** desenvolvido em Python para extração, armazenamento, tratamento, transformação e análise de dados de vendas de um supermercado.

O projeto utiliza dados públicos do Kaggle, **Pandas** para manipulação dos dados, **PostgreSQL** para armazenamento e **SQLAlchemy** para integração entre Python e banco de dados.

O pipeline foi estruturado para executar as principais etapas de um processo de Engenharia de Dados, desde a obtenção dos dados brutos até a geração de análises sobre os dados tratados.

---

## 📌 Visão geral

O projeto realiza o seguinte fluxo:

```text
Kaggle
  │
  ▼
Extração do dataset
  │
  ▼
PostgreSQL
  │
  └── vendas.raw_vendas
          │
          ▼
     Leitura / validação
          │
          ▼
     CSV raw_vendas.csv
          │
          ▼
      Transformação
          │
          ├── Renomeação das colunas
          ├── Conversão de tipos
          ├── Tratamento de datas
          ├── Tratamento de horários
          ├── Conversão de dados numéricos
          ├── Verificação de nulos
          └── Verificação de duplicidades
          │
          ▼
     CSV vendas_tratadas.csv
          │
          ▼
PostgreSQL
  │
  └── vendas.vendas_tratadas
          │
          ▼
     Análises estatísticas
```

---

## 🎯 Objetivos

O projeto foi desenvolvido com os seguintes objetivos:

- Praticar a construção de um pipeline ETL;
- Trabalhar com dados reais de vendas;
- Automatizar as etapas de extração, transformação e carga;
- Utilizar Python e Pandas para tratamento de dados;
- Integrar Python com PostgreSQL;
- Utilizar SQLAlchemy para conexão e carga dos dados;
- Separar dados brutos de dados tratados;
- Aplicar validações durante o processo de transformação;
- Executar consultas SQL sobre os dados;
- Gerar indicadores e estatísticas para análise das vendas;
- Praticar organização de projetos de dados utilizando Git e GitHub.

---

# 🧰 Tecnologias utilizadas

| Tecnologia              | Utilização                                  |
| ----------------------- | --------------------------------------------- |
| **Python**        | Desenvolvimento do pipeline                   |
| **Pandas**        | Leitura, transformação e análise dos dados |
| **PostgreSQL**    | Banco de dados relacional                     |
| **SQLAlchemy**    | Conexão e integração com PostgreSQL        |
| **Psycopg2**      | Driver PostgreSQL utilizado pelo SQLAlchemy   |
| **KaggleHub**     | Download do dataset do Kaggle                 |
| **python-dotenv** | Carregamento das variáveis de ambiente       |
| **SQL**           | Criação de banco, tabelas e consultas       |
| **Git**           | Controle de versão                           |
| **GitHub**        | Hospedagem do projeto                         |

---

# 📊 Fonte dos dados

O dataset utilizado é o **Supermarket Sales**, disponível no Kaggle:

**Autor:** `faresashraf1001`

**Dataset:**

```text
faresashraf1001/supermarket-sales
```

O download é realizado automaticamente pelo `kagglehub`.

O arquivo utilizado pelo pipeline é:

```text
SuperMarket Analysis.csv
```

A base possui **1.000 registros e 17 colunas**.

---

# 📋 Dados originais

As colunas disponíveis no dataset original são:

```text
Invoice ID
Branch
City
Customer type
Gender
Product line
Unit price
Quantity
Tax 5%
Sales
Date
Time
Payment
cogs
gross margin percentage
gross income
Rating
```

Esses campos representam informações como identificação da venda, filial, cidade, cliente, gênero, linha de produto, preço, quantidade, impostos, valor da venda, data, horário, pagamento, custo da mercadoria, margem, receita e avaliação.

---

# 🔄 Processo ETL

## 1. Extract — Extração

A extração é realizada em `src/extracao_dados.py`.

O projeto utiliza o `kagglehub` para localizar e baixar o dataset:

```python
kagglehub.dataset_download(
    "faresashraf1001/supermarket-sales"
)
```

Depois do download, o arquivo CSV é lido pelo Pandas e carregado na tabela:

```text
vendas.raw_vendas
```

A quantidade de registros carregados é validada por meio de uma consulta SQL:

```sql
SELECT COUNT(*)
FROM vendas.raw_vendas;
```

---

## 2. Leitura e validação dos dados brutos

O arquivo `src/_01_leitura_dados.py` é responsável por ler os dados da tabela `raw_vendas` e apresentar informações para inspeção.

São verificados:

- Informações das colunas;
- Primeiras linhas;
- Últimas linhas;
- Valores nulos;
- Estatísticas descritivas;
- Campos de data e hora;
- Quantidade de registros.

Depois dessa etapa, os dados são exportados para:

```text
data/raw/raw_vendas.csv
```

---

## 3. Transform — Tratamento dos dados

A transformação é realizada em:

```text
src/_02_etl_vendas.py
```

### Renomeação das colunas

Os nomes originais são convertidos para um padrão em português e com nomenclatura adequada para utilização no banco:

| Origem                      | Tratada               |
| --------------------------- | --------------------- |
| `Invoice ID`              | `id_venda`          |
| `Branch`                  | `filial`            |
| `City`                    | `cidade`            |
| `Customer type`           | `tipo_cliente`      |
| `Gender`                  | `genero`            |
| `Product line`            | `linha_produto`     |
| `Unit price`              | `preco_unitario`    |
| `Quantity`                | `quantidade`        |
| `Tax 5%`                  | `imposto`           |
| `Sales`                   | `valor_total`       |
| `Date`                    | `data_venda`        |
| `Time`                    | `hora_venda`        |
| `Payment`                 | `forma_pagamento`   |
| `cogs`                    | `custo_mercadoria`  |
| `gross margin percentage` | `margem_percentual` |
| `gross income`            | `receita_bruta`     |
| `Rating`                  | `avaliacao`         |

### Conversão de datas

A coluna `data_venda` é convertida para o formato de data:

```python
pd.to_datetime(
    df["data_venda"],
    format="%m/%d/%Y",
    errors="coerce"
).dt.date
```

### Conversão de horários

A coluna `hora_venda` é convertida para horário:

```python
pd.to_datetime(
    df["hora_venda"],
    format="%I:%M:%S %p",
    errors="coerce"
).dt.time
```

### Conversão das colunas numéricas

As seguintes colunas são convertidas para valores numéricos:

```text
preco_unitario
quantidade
imposto
valor_total
custo_mercadoria
margem_percentual
receita_bruta
avaliacao
```

Valores inválidos são convertidos para `NaN` utilizando `errors="coerce"`.

### Validações

O processo também verifica:

- Datas inválidas;
- Horários inválidos;
- Valores nulos por coluna;
- Registros duplicados.

---

# 4. Load — Carga dos dados tratados

Depois da transformação, os dados são armazenados em dois destinos.

### Arquivo CSV

```text
data/processed/vendas_tratadas.csv
```

### PostgreSQL

```text
vendas.vendas_tratadas
```

A carga para o PostgreSQL é realizada utilizando:

```python
df.to_sql(
    "vendas_tratadas",
    engine_etl,
    schema="vendas",
    if_exists="append",
    index=False
)
```

Ao final da carga, a quantidade de registros inseridos na tabela é validada.

---

# 🐘 Banco de dados

O projeto utiliza PostgreSQL.

O nome do banco configurado no projeto é:

```text
etl_vendas_supermercado
```

O schema utilizado é:

```text
vendas
```

As principais tabelas são:

```text
vendas.raw_vendas
vendas.vendas_tratadas
```

---

## 🗃️ Tabela `raw_vendas`

A tabela `raw_vendas` mantém os dados com a estrutura original do dataset.

```text
vendas.raw_vendas
```

Ela funciona como camada de dados brutos antes da transformação.

---

## 🧹 Tabela `vendas_tratadas`

A tabela `vendas_tratadas` armazena os dados depois do processo de transformação.

Sua estrutura contém:

```text
id_venda
filial
cidade
tipo_cliente
genero
linha_produto
preco_unitario
quantidade
imposto
valor_total
data_venda
hora_venda
forma_pagamento
custo_mercadoria
margem_percentual
receita_bruta
avaliacao
```

O campo:

```text
id_venda
```

é utilizado como **chave primária**.

A tabela também possui restrições `CHECK` para garantir que valores como quantidade, preço, impostos, receita e avaliação estejam dentro de condições válidas.

---

# 🧱 Estrutura do projeto

```text
ETL_Supermercado/
│
├── data/
│   ├── raw/
│   │   └── raw_vendas.csv
│   │
│   └── processed/
│       └── vendas_tratadas.csv
│
├── src/
│   ├── config.py
│   ├── criar_banco_dados.py
│   ├── extracao_dados.py
│   ├── normalizacao.py
│   ├── consultas_sql.py
│   ├── executar_etl.py
│   ├── _01_leitura_dados.py
│   ├── _02_etl_vendas.py
│   └── _03_estatistica.py
│
├── sql/
│   ├── 00_deletar_banco.sql
│   ├── 01_criar_banco.sql
│   ├── 02_criar_tabelas.sql
│   └── 03_consultas.sql
│
├── requirements.txt
└── README.md
```

---

# 📁 Responsabilidade dos arquivos

## `src/executar_etl.py`

É o ponto principal de execução do projeto.

O arquivo organiza as etapas do pipeline na seguinte ordem:

```text
1. Limpeza do banco
2. Teste de conexão
3. Criação do banco
4. Criação do schema
5. Criação das tabelas
6. Extração do Kaggle
7. Carga dos dados brutos
8. Consultas SQL
9. Leitura da tabela raw
10. Exportação para CSV raw
11. Transformação dos dados
12. Exportação do CSV tratado
13. Carga da tabela tratada
14. Análises estatísticas
```

O pipeline é iniciado pela função:

```python
if __name__ == "__main__":
    main()
```

---

## `src/criar_banco_dados.py`

Responsável pela administração inicial do banco de dados:

- Encerramento de conexões;
- Exclusão do banco anterior;
- Teste de conexão;
- Criação do banco;
- Criação do schema `vendas`;
- Criação da tabela `raw_vendas`;
- Criação da tabela `vendas_tratadas`.

---

## `src/config.py`

Centraliza a configuração das conexões SQLAlchemy.

São utilizados dois engines:

```text
engine_cdb
```

Utilizado para conexão com o banco `postgres` e operações de criação/exclusão do banco de dados.

```text
engine_etl
```

Utilizado para conexão com o banco definido em `DB_NAME` e execução do processo ETL.

---

## `src/extracao_dados.py`

Responsável pela extração dos dados do Kaggle e carga inicial na tabela:

```text
vendas.raw_vendas
```

---

## `src/_01_leitura_dados.py`

Responsável pela leitura e inspeção dos dados brutos.

Também gera:

```text
data/raw/raw_vendas.csv
```

---

## `src/_02_etl_vendas.py`

Responsável pela transformação e carga dos dados tratados.

Executa:

- Renomeação;
- Conversão de datas;
- Conversão de horários;
- Conversão de tipos numéricos;
- Validação de dados;
- Exportação do CSV tratado;
- Carga no PostgreSQL.

---

## `src/_03_estatistica.py`

Responsável pelas análises realizadas sobre o CSV tratado.

Entre os indicadores calculados estão:

- Receita por filial;
- Quantidade de vendas por filial;
- Receita por linha de produto;
- Avaliação média por linha de produto;
- Forma de pagamento mais utilizada;
- Valor médio das vendas;
- Maior venda;
- Dia da semana com maior quantidade de vendas.

---

## `src/consultas_sql.py`

Lê o arquivo:

```text
sql/03_consultas.sql
```

e executa automaticamente as consultas SQL utilizando Pandas e SQLAlchemy.

Os títulos das consultas são extraídos dos comentários SQL e exibidos durante a execução.

---

## `src/normalizacao.py`

Contém funções auxiliares utilizadas para:

- Exibição padronizada dos títulos;
- Exibição de mensagens;
- Exibição das etapas de carga;
- Extração dos títulos dos comentários SQL;
- Remoção dos comentários antes da execução das consultas.

---

# 🗄️ Scripts SQL

A pasta `sql/` contém scripts para operações diretamente no PostgreSQL.

### `00_deletar_banco.sql`

Script destinado à exclusão do banco de dados após encerramento das conexões.

### `01_criar_banco.sql`

Cria o banco:

```text
etl_vendas_supermercado
```

### `02_criar_tabelas.sql`

Cria:

```text
schema vendas
tabela vendas.raw_vendas
tabela vendas.vendas_tratadas
```

### `03_consultas.sql`

Contém consultas para análise dos dados brutos, incluindo:

- Receita por filial;
- Quantidade de vendas por filial;
- Receita por linha de produto;
- Avaliação média por linha de produto;
- Forma de pagamento mais utilizada;
- Valor médio das vendas;
- Maior venda;
- Dia da semana com maior quantidade de vendas.

---

# 🔐 Configuração das variáveis de ambiente

As conexões com PostgreSQL são configuradas por meio de variáveis de ambiente.

Crie um arquivo:

```text
.env
```

na raiz do projeto.

Exemplo:

```env
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_supermercado
```

O arquivo `.env` deve permanecer fora do controle de versão para evitar a exposição de credenciais.

Adicione ao `.gitignore`:

```gitignore
.env
```

---

# ⚙️ Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3;
- PostgreSQL;
- Git;
- pip;
- acesso à internet para download do dataset pelo KaggleHub.

Também é necessário que o serviço do PostgreSQL esteja ativo.

---

# 📦 Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/SergioReeck/ETL_Supermercado.git
```

Entrar na pasta:

```bash
cd ETL_Supermercado
```

---

## 2. Criar ambiente virtual

### macOS / Linux

```bash
python3 -m venv .venv
```

Ativar:

```bash
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

> **Observação:** no estado atual do repositório, `requirements.txt` contém `os` e `pathlib`, que são módulos da biblioteca padrão do Python e não precisam ser instalados via `pip`. O projeto também utiliza `dotenv` via `from dotenv import load_dotenv`; para esse import, o pacote normalmente utilizado é `python-dotenv`. Se a instalação do `requirements.txt` apresentar erro, ajuste essas dependências antes de executar o pipeline.

Uma lista mínima de dependências externas utilizadas pelo código é:

```text
pandas
sqlalchemy
psycopg2-binary
dotenv
pathlib
kagglehub
matplotlib
```

---

# ▶️ Execução

Com o PostgreSQL ativo, o `.env` configurado e o ambiente virtual ativado, execute o pipeline a partir da raiz do projeto:

```bash
python src/executar_etl.py
```

No macOS/Linux, também pode ser necessário utilizar:

```bash
python3 src/executar_etl.py
```

O `executar_etl.py` coordena todas as etapas do processo.

---

# ⚠️ Atenção à execução

O pipeline foi desenvolvido para criar uma nova instância do banco durante a execução.

A primeira etapa chama:

```python
limpar_banco_dados()
```

Essa função encerra conexões e exclui o banco configurado em `DB_NAME`, caso ele exista.

Portanto:

> **Não execute o pipeline em um banco que contenha dados que você deseja preservar.**

O processo foi pensado para uma execução controlada do ETL, recriando a estrutura do banco antes de carregar os dados novamente.

---

# 📊 Resultados obtidos

A base tratada presente no projeto contém:

```text
1.000 registros
17 colunas
```

## Receita por filial

| Filial |    Receita |
| ------ | ---------: |
| Giza   | 110.568,86 |
| Alex   | 106.200,57 |
| Cairo  | 106.198,00 |

A filial **Giza** apresentou a maior receita.

---

## Quantidade de vendas por filial

| Filial | Vendas |
| ------ | -----: |
| Alex   |    340 |
| Cairo  |    332 |
| Giza   |    328 |

A filial **Alex** apresentou a maior quantidade de vendas.

---

## Receita por linha de produto

As três maiores receitas por linha de produto foram:

| Linha de produto       |   Receita |
| ---------------------- | --------: |
| Food and beverages     | 56.144,96 |
| Sports and travel      | 55.123,00 |
| Electronic accessories | 54.337,64 |

---

## Melhor avaliação média por linha de produto

A maior avaliação média foi registrada para:

```text
Food and beverages
```

com aproximadamente:

```text
7,11
```

---

## Forma de pagamento mais utilizada

| Forma de pagamento | Quantidade |
| ------------------ | ---------: |
| Ewallet            |        345 |
| Cash               |        344 |
| Credit card        |        311 |

A forma de pagamento mais utilizada foi:

```text
Ewallet
```

---

## Valor médio das vendas

O valor médio das vendas foi aproximadamente:

```text
322,97
```

---

## Maior venda

A maior venda registrada na base tratada foi:

```text
ID: 860-79-0874
Filial: Giza
Linha de produto: Fashion accessories
Valor: 1.042,65
```

---

## Dia da semana com mais vendas

O dia com maior quantidade de vendas foi:

```text
Saturday — 164 vendas
```

---

# 🧪 Validações realizadas

Durante o processo de transformação são realizadas validações para verificar a qualidade dos dados.

Entre elas:

```text
✓ Datas inválidas
✓ Horários inválidos
✓ Valores nulos
✓ Registros duplicados
✓ Tipos de dados
✓ Quantidade de registros
✓ Quantidade de registros carregados no PostgreSQL
```

Além disso, a tabela `vendas.vendas_tratadas` possui restrições no PostgreSQL para evitar valores inválidos em campos importantes.

Exemplo:

```sql
CHECK (quantidade > 0)
```

e:

```sql
CHECK (avaliacao >= 0 AND avaliacao <= 10)
```

---

# 🔗 Arquitetura simplificada

```text
                  ┌─────────────────────┐
                  │       Kaggle        │
                  │  Supermarket Sales  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ extracao_dados.py   │
                  │      EXTRACT        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    PostgreSQL       │
                  │ vendas.raw_vendas   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ _01_leitura_dados   │
                  │    Validação        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ _02_etl_vendas.py   │
                  │     TRANSFORM       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ vendas_tratadas.csv │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    PostgreSQL       │
                  │ vendas.vendas_      │
                  │      tratadas       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ _03_estatistica.py  │
                  │      ANÁLISE        │
                  └─────────────────────┘
```

---

# 📓 Notebook de Análise e Visualização

Como etapa complementar ao processo de ETL, o projeto possui um notebook destinado à **análise exploratória e visualização dos dados tratados**.

O notebook utiliza o arquivo:

```text
data/processed/vendas_tratadas.csv
```

e apresenta os principais indicadores obtidos após o processo de transformação dos dados.

### 📊 Análises realizadas

O notebook apresenta análises e visualizações sobre:

- 💰 Faturamento por filial;
- 🧾 Quantidade de vendas por filial;
- 🛒 Faturamento por linha de produto;
- ⭐ Avaliação média por linha de produto;
- 💳 Distribuição das formas de pagamento;
- 📈 Distribuição dos valores das vendas;
- 📅 Quantidade de vendas por dia da semana;
- 🏆 Identificação da maior venda realizada;
- 📌 Indicadores gerais do conjunto de dados.

Os resultados são apresentados por meio de tabelas e gráficos, facilitando a interpretação dos dados e permitindo identificar padrões e características relevantes das vendas.

### ▶️ Execução

O notebook pode ser executado utilizando **Jupyter Notebook**, **JupyterLab** ou diretamente pelo **Visual Studio Code** com a extensão Jupyter.

A partir da raiz do projeto:

```bash
jupyter notebook
```

Em seguida, abra:

```text
notebooks/ETL_Supermercado_Estatisticas.ipynb
```

> **Observação:** o notebook utiliza os dados gerados pelo processo de ETL. Portanto, recomenda-se executar o pipeline antes da análise para garantir que o arquivo `data/processed/vendas_tratadas.csv` esteja atualizado.

### 🔄 Fluxo do projeto

O notebook representa a etapa de **Análise e Visualização** após o processo de ETL:

```text
Extract → Transform → Load → Analyze & Visualize
```

Dessa forma, o projeto não apenas realiza a extração, tratamento e armazenamento dos dados, mas também demonstra como os dados tratados podem ser utilizados para gerar **indicadores e insights sobre as vendas do supermercado**.

# 🧠 Conceitos aplicados

Este projeto coloca em prática conceitos de:

- ETL;
- Engenharia de Dados;
- Data Cleaning;
- Data Transformation;
- Data Validation;
- SQL;
- PostgreSQL;
- Modelagem de tabelas;
- Python;
- Pandas;
- SQLAlchemy;
- Integração Python + banco de dados;
- Variáveis de ambiente;
- Controle de versão;
- Organização de pipelines;
- Análise exploratória e estatística.

---

# 🚀 Possíveis melhorias

Algumas evoluções que podem ser implementadas futuramente:

- [ ] Adicionar testes automatizados;
- [ ] Melhorar o tratamento de exceções;
- [ ] Implementar logging estruturado;
- [ ] Implementar validações de qualidade de dados mais robustas;
- [ ] Utilizar Docker para PostgreSQL e aplicação;
- [ ] Criar dashboard com Power BI ou afins;
- [ ] Implementar uma camada de dados analítica.

---

# 👨‍💻 Autor

**Sérgio Roberto Reeck Filho**

Projeto avaliativo desenvolvido para o curso da SCTEC/SENAI - Análise de Dados com Python -  Módulo 1 - Semana 13 - Turma T3.

---

# 🔗 Repositório

GitHub:

https://github.com/SergioReeck/ETL_Supermercado

---

# ⭐ Considerações finais

Este projeto demonstra, na prática, a construção de um pipeline ETL completo:

```text
EXTRACT
   ↓
Dados do Kaggle
   ↓
LOAD
   ↓
PostgreSQL — raw_vendas
   ↓
TRANSFORM
   ↓
Limpeza + padronização + conversão + validação
   ↓
LOAD
   ↓
PostgreSQL — vendas_tratadas
   ↓
ANALYZE
   ↓
Indicadores e estatísticas
```

O resultado é uma base de vendas estruturada, validada e pronta para utilização em análises e futuras soluções de Business Intelligence.
