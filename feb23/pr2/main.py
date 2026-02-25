import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import Base, SessionLocal, engine

app = FastAPI(title="Books CRUD API")


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.post("/books", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(
        db=db,
        title=book.title,
        author=book.author,
        year=book.year,
        pages=book.pages,
    )


@app.get("/books", response_model=list[schemas.BookResponse])
async def list_books(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_books(db=db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(book_id: int, payload: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud.update_book(
        db=db,
        book=db_book,
        title=payload.title,
        author=payload.author,
        year=payload.year,
        pages=payload.pages,
    )


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await crud.delete_book(db=db, book=db_book)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
