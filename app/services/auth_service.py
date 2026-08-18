import secrets
from datetime import datetime, timedelta, timezone

from app.config import BASE_URL, TOKEN_EXPIRY_MINUTES
from app.database import get_db
from app.models.token_model import (
    find_authentication_status,
    find_aluno_by_email,
    find_token,
    insert_token,
    mark_token_as_used,
    update_aluno_numero_phiz,
)
from app.services.email_service import send_auth_email


class AuthError(Exception):
    """Erro customizado para lógica de autenticação."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def create_authentication(email: str, numero_celular: str) -> dict:
    """
    Lógica de negócio do POST /authenticate.
    Valida o aluno, gera token, salva no banco e envia o e-mail.
    """
    conn = get_db()
    try:
        cur = conn.cursor()

        # 1. Verificar se o aluno existe
        aluno = find_aluno_by_email(cur, email)
        if not aluno:
            raise AuthError(404, "Aluno não encontrado ou inativo.")

        # 2. Gerar token seguro
        token = secrets.token_urlsafe(48)
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)

        # 3. Salvar token no banco
        authentication_id = insert_token(cur, token, email, numero_celular, expira_em)
        conn.commit()

        # 4. Montar link e enviar e-mail
        link = f"{BASE_URL}/finish_authentication?token={token}"
        send_auth_email(email, link)

        return {"message": "E-mail de autenticação enviado com sucesso.",
                "authentication_id": authentication_id
                }

    except AuthError:
        raise
    except Exception as e:
        conn.rollback()
        raise AuthError(500, f"Erro interno: {str(e)}")
    finally:
        conn.close()

def get_authentication_status(email: str, numero_celular: str) -> dict:
    """
    Retorna se a solicitação indicada já foi confirmada pelo link enviado por e-mail
    """
    conn = get_db()
    try:
        cur = conn.cursor()
        row = find_authentication_status(cur, email, numero_celular)
        if not row:
            raise AuthError(404, "Solicitação de autenticação não encontrada.")
        return{"verified": row[0]}
    finally:
        conn.close()


def validate_and_finish(token_value: str) -> dict:
    """
    Lógica de negócio do GET /finish_authentication.
    Valida o token e atualiza o numero_phiz do aluno.
    Retorna um dict com 'success', 'title', 'message' e 'email'.
    """
    conn = get_db()
    try:
        cur = conn.cursor()

        # 1. Buscar token
        row = find_token(cur, token_value)
        if not row:
            return {
                "success": False,
                "title": "Token inválido",
                "message": "O link que você usou é inválido ou não existe.",
            }

        token_id, email, numero_celular, expira_em, utilizado = row

        # 2. Verificar se já foi utilizado
        if utilizado:
            return {
                "success": False,
                "title": "Link já utilizado",
                "message": "Este link de vinculação já foi utilizado anteriormente.",
            }

        # 3. Verificar expiração
        now = datetime.now(timezone.utc)
        if expira_em.tzinfo is None:
            expira_em = expira_em.replace(tzinfo=timezone.utc)
        if now > expira_em:
            return {
                "success": False,
                "title": "Link expirado",
                "message": "Este link expirou. Solicite um novo link de autenticação.",
            }

        # 4. Atualizar numero_phiz na tabela Aluno
        update_aluno_numero_phiz(cur, email, numero_celular)

        # 5. Marcar token como utilizado
        mark_token_as_used(cur, token_id)

        conn.commit()

        return {
            "success": True,
            "title": "Conexão Confirmada!",
            "message": "Seu número de celular foi vinculado com sucesso.",
            "email": email,
        }

    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "title": "Erro interno",
            "message": f"Ocorreu um erro inesperado: {str(e)}",
        }
    finally:
        conn.close()
