"""Defines the shape of Request and Response"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.models import Post

# ---------- User


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ---------- Post


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostOut(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut


class PostWithVoteOut(BaseModel):
    post: PostOut
    votes: int


# ---------- Vote


class VoteIn(BaseModel):
    post_id: int


class VoteOut(BaseModel):
    post_id: int
    user_id: int
