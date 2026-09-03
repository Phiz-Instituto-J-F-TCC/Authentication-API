import psycopg2
from app.config import DATABASE_URL


def get_db():
    """Retorna uma conexão com o PostgreSQL."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not configured")

    return psycopg2.connect(DATABASE_URL, connect_timeout=15)
