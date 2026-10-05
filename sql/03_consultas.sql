
-- Filial com maior receita
SELECT
    "Branch" AS "Filial",
    SUM("Sales") AS "Receita Total"
FROM vendas.raw_vendas
GROUP BY "Branch"
ORDER BY "Receita Total" DESC;


-- Filial com maior quantidade de vendas
SELECT
    "Branch" AS "Filial",
    COUNT(*) AS "Quantidade de Vendas"
FROM vendas.raw_vendas
GROUP BY "Branch"
ORDER BY "Quantidade de Vendas" DESC;


-- Linha de produto com maior receita
SELECT
    "Product line" AS "Linha de Produto",
    SUM("Sales") AS "Receita Total"
FROM vendas.raw_vendas
GROUP BY "Product line"
ORDER BY "Receita Total" DESC;


-- Linha de produto com melhor avaliação média
SELECT
    "Product line" AS "Linha de Produto",
    ROUND(AVG("Rating"), 2) AS "Avaliação Média"
FROM vendas.raw_vendas
GROUP BY "Product line"
ORDER BY "Avaliação Média" DESC;


-- Forma de pagamento mais utilizada
SELECT
    "Payment" AS "Forma de Pagamento",
    COUNT(*) AS "Quantidade de Vendas"
FROM vendas.raw_vendas
GROUP BY "Payment"
ORDER BY "Quantidade de Vendas" DESC;


-- Valor médio das vendas
SELECT
    ROUND(AVG("Sales"), 2) AS "Valor Médio das Vendas"
FROM vendas.raw_vendas;


-- Maior venda
SELECT
    "Invoice ID" AS "ID da Venda",
    "Branch" AS "Filial",
    "Product line" AS "Linha de Produto",
    "Sales" AS "Valor da Venda"
FROM vendas.raw_vendas
ORDER BY "Sales" DESC
LIMIT 1;


-- Dia da semana com mais vendas
SELECT
    TO_CHAR(
        TO_DATE("Date", 'MM/DD/YYYY'),
        'Day'
    ) AS "Dia da Semana",
    COUNT(*) AS "Quantidade de Vendas"
FROM vendas.raw_vendas
GROUP BY "Dia da Semana"
ORDER BY "Quantidade de Vendas" DESC;