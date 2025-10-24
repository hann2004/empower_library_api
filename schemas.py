from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional as optional
from sqlalchemy.sql.sqltypes import DateTime

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

# Add these to your existing schemas

class UserLogin(BaseModel):
    """Schema for user login (email + password)"""
    email: str
    password: str

class Token(BaseModel):
    """Schema for token response (both access and refresh tokens)"""
    access_token: str
    refresh_token: str
    token_type: str

class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str

class BorrowingBase(BaseModel):
    user_id: int
    book_id: int

class BorrowingCreate(BorrowingBase):
    due_date: DateTime

class Borrowing(BorrowingBase):
    id: int
    borrow_date: DateTime
    due_date: DateTime
    return_date: optional[DateTime] = None
    book: optional[Book] = None
    user: optional[User] = None
    
    model_config = ConfigDict(from_attributes=True)

class BorrowingReturn(BaseModel):
    borrowing_id: int