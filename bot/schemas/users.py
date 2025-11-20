from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    chat_id: int


class UserCreate(UserBase):
    ...


class User(UserBase):
    ...


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
