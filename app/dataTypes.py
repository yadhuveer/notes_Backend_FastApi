from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    user_email: EmailStr
    password: str


class UserResponse(UserBase):
    user_id: str
    create_on: datetime
    last_update: datetime

    class Config:
        orm_mode = True




class NoteBase(BaseModel):
    note_title: str
    note_content: str



class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    note_id: str
    created_on: datetime
    last_update: datetime
    user_id: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
