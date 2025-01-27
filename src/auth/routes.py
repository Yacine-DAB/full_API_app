from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.redis import add_jti_blocklist

from .dependencies import (
     AccessTokenBeaarer,
     RefreshTokenBearer,
     RoleChecker,
     get_current_user,
)

from .schema import (
     UserBookModel,
     UserCreateModel,
     UserLoginModel,
     UserModel,
     EmailModel,
     PasswordResetRequestModel,
     PasswordResetConfirmModel,
)

from .service import UserService
from .utils import (
     create_access_token,
     verify_password,
     generate_passwrd_hash,
     create_urlsafe_token,
     decode_url_safe_token,
)
from src.errors import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from src.config import Config
from src.db.main import get_session
from src.celery_tasks import send_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRY = 2

# Bearer token

@auth_router.post('/send_mail')
async def send_mail(emails: EmailModel):
     emails = emails.addresses
     
     html = '<h1>Welcome to our app</h1>'
     subject = 'Welcome to our app'
     
     send_email.delay(emails, subject, html)
     
     return {'message': 'Eamil sent successfully! '}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(
     user_data: UserCreateModel,
     db_tasks: BackgroundTasks,
     session: AsyncSession = Depends(get_session)
):
     '''Create user account using email, username, first_name, last_name, 
     params: 
          user_data: UserCreateModel
          '''     
     email = user_data.email
     
     user_exists = await user_service.user_exists(email, session)
     
     if user_exists:
          raise UserAlreadyExists()
     
     new_user = await user_service.create_user(user_data, session)
     
     token = create_urlsafe_token({'email': email})
     
     link = f'http://{Config.DOMAIN}/api/v1/auth/verify/{token}'
     
     html = f''' 
     <h1> Verify your Email </h1>
     <p> Please click this <a href="{link}">link</a> to verify tour email'''
     
     emails = [email]
     
     subject = 'Verify your email'
     
     send_email.delay(emails, subject, html)
     
     return {
          'message': 'Account Created! Check email to verify your account',
          'user': new_user,
     }
     
     
