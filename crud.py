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

def borrow_book(db: Session, borrowing: schemas.BorrowingCreate):
    # Check if book is available
    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
    
    # Check if user exists
    user = db.query(models.Users).filter(models.Users.id == borrowing.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create borrowing record
    db_borrowing = models.Borrowing(
        user_id=borrowing.user_id,
        book_id=borrowing.book_id,
        borrow_date=datetime.utcnow(),
        due_date=borrowing.due_date
    )
    
    # Mark book as unavailable
    book.is_available = False
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

def return_book(db: Session, borrowing_id: int):
    borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()
    if not borrowing:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    
    if borrowing.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")
    
    # Mark as returned
    borrowing.return_date = datetime.utcnow()
    
    # Mark book as available
    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    book.is_available = True
    
    db.commit()
    db.refresh(borrowing)
    return borrowing

def get_user_borrowings(db: Session, user_id: int):
    return db.query(models.Borrowing).filter(models.Borrowing.user_id == user_id).all()

def get_active_borrowings(db: Session):
    return db.query(models.Borrowing).filter(models.Borrowing.return_date == None).all()