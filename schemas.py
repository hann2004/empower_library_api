from pydantic import BaseModel, ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)  # ✅ Fixed!