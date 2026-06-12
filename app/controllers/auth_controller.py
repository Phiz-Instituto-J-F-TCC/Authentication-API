from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.schemas.auth_schema import AuthRequest
from app.services.auth_service import AuthError, create_authentication, validate_and_finish
from app.views.templates import error_page, success_page

router = APIRouter()


@router.post("/authenticate")
def authenticate(payload: AuthRequest):
    """
    Recebe email + número de celular.
    Verifica se o email existe na tabela Aluno,
    gera um token seguro, salva no banco e envia o link por e-mail.
    """
    try:
        result = create_authentication(payload.email, payload.numero_celular)
        return result
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
