from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional

from app.schemas.auth_schema import AuthRequest, AuthenticationEmailStatusRequest
from app.services.auth_service import (
    AuthError,
    create_authentication,
    get_authentication_status,
    resend_authentication,
    validate_authentication_email,
    validate_and_finish,
)
from app.views.templates import error_page, success_page

router = APIRouter()


@router.post("/authenticate")
def authenticate(payload: AuthRequest):
    """
    Inicia a confirmação do número informado pelo usuário.
    O telefone não é devolvido na resposta; o MiniApp recebe somente um token
    opaco para acompanhar a confirmação.
    """
    try:
        result = create_authentication(payload.email, payload.phone_number)
        return result
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/authentication_email_status")
def authentication_email_status(payload: AuthenticationEmailStatusRequest):
    """Valida o e-mail antes de o MiniApp receber o telefone informado."""
    try:
        return validate_authentication_email(payload.email)
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/finish_authentication", response_class=HTMLResponse)
def finish_authentication(token: str):
    """
    Recebe o token via query parameter,
    valida e — se válido — atualiza o numero_phiz do Aluno.
    Retorna uma página HTML de confirmação ou erro.
    """
    result = validate_and_finish(token)

    if result["success"]:
        return success_page(result["email"])
    else:
        return error_page(result["title"], result["message"])

@router.get("/authentication_status")
def authentication_status(
    x_authentication_polling_token: Optional[str] = Header(
        default=None,
        alias="X-Authentication-Polling-Token",
    ),
):
    """ Informa ao MiniApp se a solicitação já foi confirmada pelo link enviado por e-mail"""
    try:
        return get_authentication_status(x_authentication_polling_token)
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/authentication_resend")
def authentication_resend(
    x_authentication_polling_token: Optional[str] = Header(
        default=None,
        alias="X-Authentication-Polling-Token",
    ),
):
    """Reenvia o link sem reenviar ou expor o telefone ao MiniApp."""
    try:
        return resend_authentication(x_authentication_polling_token)
    except AuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
