import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.config import BASE_URL, TOKEN_EXPIRY_MINUTES
from app.database import get_db
from app.models.token_model import (
    find_authentication_for_resend,
    find_authentication_status,
    find_aluno_by_email,
    find_token,
    insert_token,
    mark_token_as_used,
    renew_token,
    update_aluno_phiz_id,
)
from app.services.email_service import send_auth_email


RESEND_COOLDOWN_SECONDS = 30


class AuthError(Exception):
    """Erro customizado para lógica de autenticação."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def validate_authentication_email(email: str) -> dict:
    """Confirma se o e-mail pertence a um aluno ativo antes da vinculação."""
    conn = get_db()
    try:
        cur = conn.cursor()
        aluno = find_aluno_by_email(cur, email)
        if not aluno:
            raise AuthError(404, "E-mail não encontrado ou está inativo.")
        return {"eligible": True}
    except AuthError:
        raise
    except Exception:
        raise AuthError(500, "Não foi possível validar o e-mail.")
    finally:
        conn.close()


def create_authentication(email: str, phiz_id: str) -> dict:
    normalized_email = email.strip().lower()
    normalized_phiz_id = phiz_id.strip() if isinstance(phiz_id, str) else ""

    if not normalized_email:
        raise AuthError(422, "E-mail é obrigatório.")

    if not normalized_phiz_id:
        raise AuthError(422, "Phiz ID inválido.")

    validate_authentication_email(normalized_email)

    conn = get_db()
    try:
        cur = conn.cursor()
        aluno = find_aluno_by_email(cur, normalized_email)
        if not aluno:
            raise AuthError(404, "E-mail não encontrado ou está inativo.")

        confirmation_token = secrets.token_urlsafe(48)
        polling_token = secrets.token_urlsafe(48)
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
        insert_token(
            cur,
            confirmation_token,
            polling_token,
            normalized_email,
            normalized_phiz_id,
            expira_em,
        )

        link = f"{BASE_URL}/finish_authentication?token={confirmation_token}"
        send_auth_email(normalized_email, link)
        conn.commit()
        return {"polling_token": polling_token}
    except AuthError:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        raise AuthError(500, "Não foi possível iniciar a confirmação. Tente novamente.")
    finally:
        conn.close()


def get_authentication_status(polling_token: Optional[str]) -> dict:
    """
    Retorna se a solicitação indicada já foi confirmada pelo link enviado por e-mail
    """
    if not polling_token:
        raise AuthError(401, "Sessão de autenticação inválida.")

    conn = get_db()
    try:
        cur = conn.cursor()
        row = find_authentication_status(cur, polling_token)
        if not row:
            raise AuthError(404, "Solicitação de autenticação não encontrada.")
        utilizado, expira_em = row
        if utilizado:
            return {"verified": True}

        if expira_em.tzinfo is None:
            expira_em = expira_em.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expira_em:
            raise AuthError(410, "Solicitação de autenticação expirada.")

        return {"verified": False}
    finally:
        conn.close()


def resend_authentication(polling_token: Optional[str]) -> dict:
    """Reenvia o link usando a solicitação já autorizada pelo MiniApp."""
    if not polling_token:
        raise AuthError(401, "Sessão de autenticação inválida.")

    conn = get_db()
    try:
        cur = conn.cursor()
        row = find_authentication_for_resend(cur, polling_token)
        if not row:
            raise AuthError(404, "Solicitação de autenticação não encontrada.")

        token_id, email, utilizado, criado_em = row
        if utilizado:
            raise AuthError(409, "A autenticação já foi concluída.")

        if criado_em.tzinfo is None:
            criado_em = criado_em.replace(tzinfo=timezone.utc)
        elapsed_seconds = (datetime.now(timezone.utc) - criado_em).total_seconds()
        if elapsed_seconds < RESEND_COOLDOWN_SECONDS:
            raise AuthError(429, "Aguarde antes de solicitar outro e-mail.")

        token = secrets.token_urlsafe(48)
        expira_em = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
        renew_token(cur, token_id, token, expira_em)

        link = f"{BASE_URL}/finish_authentication?token={token}"
        send_auth_email(email, link)
        conn.commit()
        return {"message": "E-mail de autenticação reenviado com sucesso."}
    except AuthError:
        raise
    except Exception:
        conn.rollback()
        raise AuthError(500, "Não foi possível reenviar o e-mail de autenticação.")
    finally:
        conn.close()


def validate_and_finish(token_value: str) -> dict:
    """
    Lógica de negócio do GET /finish_authentication.
    Valida o token e atualiza o Phiz ID do aluno.
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

        token_id, email, phiz_id, expira_em, utilizado = row

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

        if not phiz_id:
            return {
                "success": False,
                "title": "Solicitação desatualizada",
                "message": "Este link foi gerado pelo fluxo anterior. Inicie uma nova vinculação.",
            }

        # 4. Atualizar Phiz ID na tabela Aluno
        update_aluno_phiz_id(cur, email, phiz_id)

        # 5. Marcar token como utilizado
        mark_token_as_used(cur, token_id)

        conn.commit()

        return {
            "success": True,
            "title": "Conexão Confirmada!",
            "message": "Seu Phiz ID foi vinculado com sucesso.",
            "email": email,
        }

    except Exception:
        conn.rollback()
        return {
            "success": False,
            "title": "Erro interno",
            "message": "Ocorreu um erro inesperado. Tente novamente.",
        }
    finally:
        conn.close()
