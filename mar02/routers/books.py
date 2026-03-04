from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import ensure_owner_or_admin, get_current_user, get_db
from ..models import Book, User
from ..schemas import BookCreate, BookOut, BookUpdate
from ..services import require_book, require_category, require_genre

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_book(
    payload: BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await require_category(db=db, category_id=payload.category_id)
    await require_genre(db=db, genre_id=payload.genre_id)

    book = Book(**payload.model_dump(), author_id=current_user.id)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


@router.get("", response_model=list[BookOut])
async def list_books(
    category_id: int | None = Query(default=None, ge=1),
    genre_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Book).order_by(Book.id)
    if category_id is not None:
        stmt = stmt.where(Book.category_id == category_id)
    if genre_id is not None:
        stmt = stmt.where(Book.genre_id == genre_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    return await require_book(db=db, book_id=book_id)


@router.put("/{book_id}", response_model=BookOut)
async def update_book(
    book_id: int,
    payload: BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await require_book(db=db, book_id=book_id)
    ensure_owner_or_admin(owner_id=book.author_id, current_user=current_user)

    update_data = payload.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        await require_category(db=db, category_id=update_data["category_id"])
    if "genre_id" in update_data:
        await require_genre(db=db, genre_id=update_data["genre_id"])

    for field, value in update_data.items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await require_book(db=db, book_id=book_id)
    ensure_owner_or_admin(owner_id=book.author_id, current_user=current_user)

    await db.delete(book)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
