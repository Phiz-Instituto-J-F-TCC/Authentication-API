import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config import FROM_EMAIL, FROM_PASSWORD, TOKEN_EXPIRY_MINUTES


SMTP_HOST = "smtp.office365.com"
SMTP_PORT = 587
SMTP_TIMEOUT_SECONDS = 15


def send_auth_email(to_address: str, link: str):
    """Envia o e-mail de autenticação com link de confirmação."""
    html_body = f"""\
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6fb; margin: 0; padding: 0; }}
            .container {{ max-width: 520px; margin: 40px auto; background: #fff; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 32px 24px; text-align: center; }}
            .header h1 {{ color: #fff; margin: 0; font-size: 22px; font-weight: 600; }}
            .body {{ padding: 32px 24px; text-align: center; }}
            .body p {{ color: #4b5563; font-size: 15px; line-height: 1.6; }}
            .btn {{ display: inline-block; margin: 24px 0; padding: 14px 36px; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #fff !important; text-decoration: none; border-radius: 10px; font-size: 16px; font-weight: 600; letter-spacing: 0.5px; }}
            .footer {{ padding: 16px 24px; text-align: center; font-size: 12px; color: #9ca3af; border-top: 1px solid #f3f4f6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Vincular Conta Phiz</h1>
            </div>
            <div class="body">
                <p>Você solicitou a vinculação da sua conta Phiz.</p>
                <p>Clique no botão abaixo para confirmar a conexão. Este link expira em <strong>{TOKEN_EXPIRY_MINUTES} minutos</strong>.</p>
                <a class="btn" href="{link}">Confirmar Vinculação</a>
                <p style="font-size:13px; color:#9ca3af; margin-top:16px;">Se você não solicitou isso, ignore este e-mail.</p>
            </div>
            <div class="footer">
                Phiz &mdash; Instituto Germinare
            </div>
        </div>
    </body>
    </html>
    """

    if not FROM_EMAIL or not FROM_PASSWORD:
        raise RuntimeError("SMTP configuration is missing")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirme a vinculação da sua conta Phiz"
    msg["From"] = FROM_EMAIL
    msg["To"] = to_address
    msg.attach(
        MIMEText(
            f"Confirme sua vinculação acessando: {link}\nEste link expira em {TOKEN_EXPIRY_MINUTES} minutos.",
            "plain",
        )
    )
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT_SECONDS) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.send_message(msg)
