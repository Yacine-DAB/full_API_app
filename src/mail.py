from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path
from pydantic import SecretStr

BASE_DIR  = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
     MAIL_USERNAME=Config.MAIL_USERNAME,
     MAIL_PASSWORD=SecretStr(Config.MAIL_PASSWORD),
     MAIL_FROM=Config.MAIL_FROM,
     MAIL_PORT=Config.MAIL_PORT,
     MAIL_SERVER=Config.MAIL_SERVER,
     MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
     MAIL_STARTTLS=True,
     MAIL_SSL_TLS=False,
     USE_CREDENTIALS=True,
     VALIDATE_CERTS=True,
)

mail = FastMail(config=mail_config)

def create_message(recipients: list[str], subject: str, body: str):
     
     message = MessageSchema(
          recipients=recipients,
          subject=subject,
          body=body,
          subtype=MessageType.html
     )
     
     return message

