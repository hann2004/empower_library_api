from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional as optional

class BookBase(BaseModel):
    title: str
    author: str
    published_year: optional[int] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    is_available: bool
    
    model_config = ConfigDict(from_attributes=True)  

class UserBase(BaseModel):
    username: str
    email: EmailStr

class Usercreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
