from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Book, CartItem, Category, Comment, Genre, Order, User
from .schemas import UserCreate
from .security import get_password_hash


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    existing = await db.execute(
        select(User).where(
            or_(User.username == payload.username, User.email == payload.email)
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists") from exc

    await db.refresh(user)
    return user


async def require_category(db: AsyncSession, category_id: int) -> Category:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def require_genre(db: AsyncSession, genre_id: int) -> Genre:
    result = await db.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


async def require_book(db: AsyncSession, book_id: int) -> Book:
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def require_comment(db: AsyncSession, comment_id: int) -> Comment:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


async def require_cart_item(db: AsyncSession, cart_item_id: int) -> CartItem:
    result = await db.execute(select(CartItem).where(CartItem.id == cart_item_id))
    cart_item = result.scalar_one_or_none()
    if cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


async def require_order(db: AsyncSession, order_id: int) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


def ensure_in_stock(book: Book, quantity: int) -> None:
    if book.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock for book '{book.title}'",
        )
