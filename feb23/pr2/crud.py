from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models


async def create_book(db: AsyncSession, title: str, author: str, year: int, pages: int) -> models.Book:
    book = models.Book(title=title, author=author, year=year, pages=pages)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Book]:
    stmt = select(models.Book).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_book(db: AsyncSession, book_id: int) -> models.Book | None:
    stmt = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_book(
    db: AsyncSession,
    book: models.Book,
    title: str,
    author: str,
    year: int,
    pages: int,
) -> models.Book:
    book.title = title
    book.author = author
    book.year = year
    book.pages = pages
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book: models.Book) -> None:
    await db.delete(book)
    await db.commit()
