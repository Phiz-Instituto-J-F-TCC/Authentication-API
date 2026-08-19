from datetime import datetime


def find_aluno_by_email(cur, email: str):
    """Busca um aluno ativo pelo email."""
    cur.execute(
        'SELECT "id" FROM "Aluno" WHERE "email" = %s AND "ativo" = TRUE',
        (email,),
    )
    return cur.fetchone()


def insert_token(
    cur,
    token: str,
    polling_token: str,
    email: str,
    numero_celular: str,
    expira_em: datetime,
) -> int:
    """Insere um novo token de autenticação."""
    cur.execute(
        'INSERT INTO "Token_Autenticacao" ("token", "polling_token", "email", "numero_celular", "expira_em") VALUES (%s, %s, %s, %s, %s) RETURNING "id"',
        (token, polling_token, email, numero_celular, expira_em),
    )
    return cur.fetchone()[0]

def find_authentication_status(cur, polling_token: str):
    """Buscar o status de uma solicitação sem expor o token de confirmação"""
    cur.execute(
        'SELECT "utilizado", "expira_em" FROM "Token_Autenticacao" WHERE "polling_token" = %s',
        (polling_token,),
    )
    return cur.fetchone()


def find_authentication_for_resend(cur, polling_token: str):
    """Busca a solicitação pendente autorizada pelo token opaco de polling."""
    cur.execute(
        'SELECT "id", "email", "utilizado", "criado_em" FROM "Token_Autenticacao" WHERE "polling_token" = %s FOR UPDATE',
        (polling_token,),
    )
    return cur.fetchone()


def renew_token(cur, token_id: int, token: str, expira_em: datetime):
    """Substitui o link de confirmação sem expor o telefone armazenado."""
    cur.execute(
        'UPDATE "Token_Autenticacao" SET "token" = %s, "expira_em" = %s, "utilizado" = FALSE, "criado_em" = NOW() WHERE "id" = %s',
        (token, expira_em, token_id),
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