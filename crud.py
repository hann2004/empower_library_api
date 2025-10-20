from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException   
from security import get_hash_password, verify_password
from sqlalchemy.exc import IntegrityError 

def get_books(db: Session):  
    return db.query(models.Book).all()  

def get_book_by_id(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title, 
        author=book.author, 
        published_year=book.published_year  
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):  # ✅ Added book_id parameter
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_data.title
    book.author = book_data.author
    book.published_year = book_data.published_year  # ✅ Update all fields
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

def create_user(db: Session, user: schemas.Usercreate):
    existing_user = db.query(models.Users).filter(models.Users.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hash_password = get_hash_password(user.password)

    db_user = models.Users(
        username=user.username,
        email=user.email,
        hash_password=hash_password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="user creation failed") 

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user with email and password
    Returns user object if valid, False if invalid
    """
    user = db.query(models.Users).filter(models.Users.email == email).first()
    
    if not user:
        return False
    
    if not verify_password(password, user.hash_password):
        return False
    
    return user