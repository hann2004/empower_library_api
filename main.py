from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import engine, get_db
from typing import List
from security import create_access_token, create_refresh_token, verify_token
from dependencies import get_current_user
from schemas import Token, TokenRefresh, UserLogin
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create a new book
@app.post("/books", response_model=schemas.Book)  
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books", response_model=List[schemas.Book])  
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)  

@app.get("/books/{book_id}", response_model=schemas.Book)  
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_id(db, book_id)

@app.put("/books/{book_id}", response_model=schemas.Book)  
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)

@app.post("/register", response_model=schemas.User)  
def create_user(user: schemas.Usercreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return crud.create_user(db=db, user=user)


@app.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    
    # Authenticate user
    db_user = crud.authenticate_user(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create both tokens
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh", response_model=Token)
def refresh_token(refresh_data: TokenRefresh):
    
    # Verify the refresh token
    payload = verify_token(refresh_data.refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    # Extract user email from token
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # Create NEW tokens (extend the session)
    new_access_token = create_access_token(data={"sub": email})
    new_refresh_token = create_refresh_token(data={"sub": email})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.get("/protected-test")
def protected_test(current_user: schemas.User = Depends(get_current_user)):
   
    return {
        "message": f"Hello {current_user.username}!",
        "your_email": current_user.email,
        "is_active": current_user.is_active
    }

# Borrowing endpoints
@app.post("/borrow", response_model=schemas.Borrowing)
def borrow_book(borrowing: schemas.BorrowingCreate, db: Session = Depends(get_db)):
    return crud.borrow_book(db=db, borrowing=borrowing)

@app.post("/return", response_model=schemas.Borrowing)
def return_book(return_data: schemas.BorrowingReturn, db: Session = Depends(get_db)):
    return crud.return_book(db=db, borrowing_id=return_data.borrowing_id)

@app.get("/users/{user_id}/borrowings", response_model=List[schemas.Borrowing])
def get_user_borrowings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_borrowings(db=db, user_id=user_id)

@app.get("/borrowings/active", response_model=List[schemas.Borrowing])
def get_active_borrowings(db: Session = Depends(get_db)):
    return crud.get_active_borrowings(db=db)