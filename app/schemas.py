
from lib2to3.pytree import Base
from os import access
from typing import Optional
from venv import create
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    #rating: Optional[int] = None
    owner: UserOut

    class Config:
        orm_mode = True

class DPost(BaseModel):
    content: str
    title: str
    created_at: datetime
    published: bool = True
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class PostOut(PostBase):
    Post: Post
    votes: int


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


