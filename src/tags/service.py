from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.books.service import BookService