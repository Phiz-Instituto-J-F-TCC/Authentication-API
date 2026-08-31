import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from app.config import RESEND_API_KEY, RESEND_FROM_EMAIL, TOKEN_EXPIRY_MINUTES

RESEND_EMAILS_URL = "https://api.resend.com/emails"
RESEND_TIMEOUT_SECONDS = 15


def send_auth_email(to_address: str, link: str):
    """Envia o e-mail de autenticação pela API HTTPS do Resend."""
    if not RESEND_API_KEY or not RESEND_FROM_EMAIL:
        raise RuntimeError("Resend configuration is missing")

    text_body = (
        f"Confirme sua vinculação acessando: {link}\n"
        f"Este link expira em {TOKEN_EXPIRY_MINUTES} minutos."
    )
    html_body = f"""\
    <html>
    <body>
        <h1>Vincular Conta Phiz</h1>
        <p>Você solicitou a vinculação da sua conta Phiz.</p>
        <p>Este link expira em <strong>{TOKEN_EXPIRY_MINUTES} minutos</strong>.</p>
        <p><a href=\"{link}\">Confirmar Vinculação</a></p>
        <p>Se você não solicitou isso, ignore este e-mail.</p>
    </body>
    </html>
    """
    payload = json.dumps(
        {
            "from": RESEND_FROM_EMAIL,
            "to": [to_address],
            "subject": "Confirme a vinculação da sua conta Phiz",
            "text": text_body,
            "html": html_body,
        }
    ).encode("utf-8")
    request = Request(
        RESEND_EMAILS_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=RESEND_TIMEOUT_SECONDS) as response:
            if response.status not in (200, 201):
                raise RuntimeError("Resend email delivery failed")
    except HTTPError as error:
        raise RuntimeError("Resend email delivery failed") from error
