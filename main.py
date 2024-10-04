from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
from db.database import get_db
from schemas import Author, AuthorCreate, Book, BookCreate

app = FastAPI()


@app.get("/authors/", response_model=List[Author])
def read_authors(db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 10):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return db_author


@app.post("/authors/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.get("/books/", response_model=List[Book])
def read_books(db: Session = Depends(get_db),
               skip: int = 0,
               limit: int = 10):
    return crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/authors/{author_id}/books", response_model=List[Book])
def read_books_by_author(author_id: int,
                         db: Session = Depends(get_db),
                         skip: int = 0,
                         limit: int = 10):
    return crud.get_books_by_author_id(
        db=db,
        author_id=author_id,
        skip=skip,
        limit=limit
    )


@app.post("/authors/{author_id}/books", response_model=Book)
def create_book_for_author(author_id: int,
                           book: BookCreate,
                           db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)
