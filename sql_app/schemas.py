from typing import Union

from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    role: str
    applist : Union[str, None] = None

class AdBase(BaseModel):
    role: str
    applist : Union[str, None] = None


class ItemCreate(ItemBase):
    pass

class AdCreate(AdBase):
    pass

class ItemUpdate(BaseModel):
    role : str
    applist : Optional[str] = None

class AdUpdate(BaseModel):
    role : str
    applist : Optional[str] = None


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class Ad(AdBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    disabled: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # disabled: bool
    userprofile: list[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

#
# class User(BaseModel):
#     id: int
#     username: str
#     email: str
#     full_name: str
#     disabled: bool
#
#     class Config:
#         orm_mode = True