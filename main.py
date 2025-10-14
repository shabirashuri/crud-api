from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel,Field # type: ignore
from uuid import UUID

app = FastAPI()

class Books(BaseModel):
    id : int
    name :str = Field(min_length = 1)
    descripttion :str =  Field(min_length = 1,max_length = 100)
    rating : int = Field(gt = -1,lt = 11)

BOOKS = []

@app.get('/')
def index():
    return BOOKS


@app.post("/")
def add_book(book:Books):
    BOOKS.append(book)
    return book

@app.put('/')
def update_book(book_id :id,book:Books):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id ==  book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
        raise HTTPException(
            status_code = 404,
            detail = f"book id {book_id} does not found"
        )

@app.delete('/')
def delete_book(book_id : id ,book:Books):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID {book_id}: DELETED"
        raise HTTPException(
            status_code = 404,
            detail = f"book id {book_id} does not found"
        )






