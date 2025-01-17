import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.books.schema import Book
from src.reviews.schema import ReviewModel

class UserCreateModel(BaseModel):
     
     first_name: str = Field(max_length=25)
     last_name: str = Field(max_length=25)
     username: str = Field(max_length=8)
     email: str = Field(max_length=40)
     password: str = Field(max_length=6)
     
     model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }

class UserModel(BaseModel):
     uid: uuid.UUID
     username: str
     email: str
     first_namr: str
     last_name: str
     is_verified: bool
     password_hash: str = Field(exclude=True)
     created_at: datetime
     updated_at: datetime
     
class UserBookModel(UserModel):
     book: List[Book]
     reviews: List[ReviewModel]
     

class UserLoginModel(BaseModel):
     email: str = Field(max_length=40)
     password: str = Field(max_length=6)
     
class EmailModel(BaseModel):
     address: List[str]
     
     
class PasswordResetRequestModel(BaseModel):
     email: str
     
class PasswordResetConfirmModel(BaseModel):
     new_password: str
     confirm_new_password: str
     