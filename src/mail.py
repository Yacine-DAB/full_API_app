from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR  = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
     MAIL_USERNAME=Config.MAIL_USERNAME,
     MAIL_PASSWORD=Config.MAIL_PASSWORD,
     MAIL_FROM=Config.MAIL_FROM,
     MAIL_PORT=Config.MAIL_PORT,
     MAIL_SERVER=Config.MAIL_SERVER,
     
)