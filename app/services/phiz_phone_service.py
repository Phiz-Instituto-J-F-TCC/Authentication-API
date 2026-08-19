import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from app.config import PHIZ_API_SERVER, PHIZ_APP_ID, PHIZ_PERSONAL_ACCESS_TOKEN


PHONE_ENDPOINT_PATH = "/api/v1/open/dev/mini-apps/unified-auth/phone/get"
REQUEST_TIMEOUT_SECONDS = 10


class PhoneResolutionError(Exception):
    """Erro seguro ao trocar o código temporário pelo telefone no Phiz."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def resolve_phone_number(phone_code: str) -> str:
    """Obtém o telefone no Phiz sem devolvê-lo ao MiniApp."""
    if not isinstance(phone_code, str) or not phone_code:
        raise PhoneResolutionError(400, "Código de autorização do Phiz inválido.")

    api_server = _get_api_server()
    if not PHIZ_APP_ID or not PHIZ_PERSONAL_ACCESS_TOKEN:
        raise PhoneResolutionError(503, "A integração com o Phiz ainda não está configurada.")

    body = json.dumps({"appId": PHIZ_APP_ID, "code": phone_code}).encode("utf-8")
    request = Request(
        f"{api_server}{PHONE_ENDPOINT_PATH}",
        data=body,
        headers={
            "Authorization": f"Bearer {PHIZ_PERSONAL_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError, UnicodeDecodeError):
        raise PhoneResolutionError(502, "Não foi possível obter o número pelo Phiz. Tente novamente.")

    if not isinstance(payload, dict) or payload.get("errcode") != "OK":
        raise PhoneResolutionError(502, "Não foi possível obter o número pelo Phiz. Tente novamente.")

    data = payload.get("data")
    phone = data.get("phone") if isinstance(data, dict) else None
    if not isinstance(phone, str) or not phone.strip():
        raise PhoneResolutionError(502, "Não foi possível obter o número pelo Phiz. Tente novamente.")

    return phone.strip()


def _get_api_server() -> str:
    parsed = urlparse(PHIZ_API_SERVER)
    if parsed.scheme != "https" or not parsed.netloc:
        raise PhoneResolutionError(503, "A integração com o Phiz ainda não está configurada.")
    return PHIZ_API_SERVER.rstrip("/")