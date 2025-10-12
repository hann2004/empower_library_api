from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database
import crud
import models
import schemas
from  database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/books", response_model=schemas.BookCreate)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books", response_model=List[schemas.BookCreate])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookCreate)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book_by_id(db, book_id)


@app.put("/books/{book_id}", response_model=schemas.BookCreate)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)

# ✅ Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)
