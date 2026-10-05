-- Liberar conexões ativas para o banco de dados 'etl_supermercado' antes de excluí-lo
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'etl_supermercado'
  AND pid <> pg_backend_pid();

--- Script para deletar o banco de dados para uma nova execução do ETL
DROP DATABASE etl_supermercado;