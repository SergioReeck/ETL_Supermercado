import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Teste de conexão e criação do banco de dados
engine_cdb = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/postgres",
    isolation_level="AUTOCOMMIT"
)

# Schema e tabelas
engine_etl = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)