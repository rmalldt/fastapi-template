"""Defines the shape of Request and Response"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# ----- User


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ----- Post


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


# Inherits PostBase
class PostResponse(PostBase):
    id: int
    created_at: datetime
