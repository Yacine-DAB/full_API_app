from typing import Any, List
from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import User
from src.db.redis import token_in_blocklist

from .service import UserService
from .utils import decode_token
from src.errors import (
     InvalidToken,
     RefreshTokenRequired,
     AccessTokenRequired,
     InsufficientPermission,
     AccountNotVerified,
)

user_service = UserService()


