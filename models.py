from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime as dateTime
from database import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_year = Column(Integer)
    is_available = Column(Boolean, default=True)
    borrowings = relationship("Borrowing", back_populates="book")

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    hash_password = Column(String)
    borrowings = relationship("Borrowing", back_populates="user")


class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(DateTime, default=dateTime.utcnow)
    return_date = Column(DateTime, nullable=True)

    
    user = relationship("Users", back_populates="borrowings")
    book = relationship("Book", back_populates="borrowings")