import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Dados da conta
EMAIL = os.getenv("FROM_ADDRESS")
PASSWORD = os.getenv("FROM_PASSWORD")

def send_email(subject:str, body_message:str, to_address:str):
    # Creating message
    mensagem = MIMEText(body_message)
    mensagem["Subject"] = subject
    mensagem["From"] = EMAIL
    mensagem["To"] = to_address

    # SMTP of Outlook Server
    with smtplib.SMTP("smtp.office365.com", 587) as servidor:
        servidor.starttls()
        servidor.login(EMAIL, PASSWORD)
        servidor.send_message(mensagem)

    print("Email enviado com sucesso!")

if __name__ == "__main__":
    for i in range(500): 
        send_email("Teste Outlook", f"Hellooo {i}", "raquel.tolomei@institutojef.org.br")