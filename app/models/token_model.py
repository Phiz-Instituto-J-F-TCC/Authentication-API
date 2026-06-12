from datetime import datetime


def find_aluno_by_email(cur, email: str):
    """Busca um aluno ativo pelo email."""
    cur.execute(
        'SELECT "id" FROM "Aluno" WHERE "email" = %s AND "ativo" = TRUE',
        (email,),
    )
    return cur.fetchone()


def insert_token(cur, token: str, email: str, numero_celular: str, expira_em: datetime):
    """Insere um novo token de autenticação."""
    cur.execute(
        """
        INSERT INTO "Token_Autenticacao" ("token", "email", "numero_celular", "expira_em")
        VALUES (%s, %s, %s, %s)
        """,
        (token, email, numero_celular, expira_em),
    )


def find_token(cur, token: str):
    """Busca um token de autenticação pelo valor do token."""
    cur.execute(
        """
        SELECT "id", "email", "numero_celular", "expira_em", "utilizado"
        FROM "Token_Autenticacao"
        WHERE "token" = %s
        """,
        (token,),
    )
    return cur.fetchone()


def mark_token_as_used(cur, token_id: int):
    """Marca o token como utilizado."""
    cur.execute(
        'UPDATE "Token_Autenticacao" SET "utilizado" = TRUE WHERE "id" = %s',
        (token_id,),
    )


def update_aluno_numero_phiz(cur, email: str, numero_phiz: str):
    """Atualiza o numero_phiz do aluno pelo email."""
    cur.execute(
        'UPDATE "Aluno" SET "numero_phiz" = %s WHERE "email" = %s',
        (numero_phiz, email),
    )
