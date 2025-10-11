from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException   

def get_book(db: Session):
    return db.query(models.book).all()

def get_book_by_id(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code =404, detail="Book not found")
    return book

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_data: schemas.BookCreate):
    book = db.query(models.Book).filter(models.Book.id == book_data.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_data.title
    book.author = book_data.author
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"} 