import psycopg2
from app.config import DATABASE_URL


def get_db():
    """Retorna uma conexão com o PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn
