from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..deps import ensure_owner_or_admin, get_current_user, get_db
from ..models import CartItem, User
from ..schemas import BookOut, CartItemCreate, CartItemOut, CartItemUpdate, CartOut
from ..services import ensure_in_stock, require_book, require_cart_item

router = APIRouter(prefix="/cart", tags=["Cart"])


def _serialize_cart_item(cart_item: CartItem) -> CartItemOut:
    unit_price = float(cart_item.book.price)
    return CartItemOut(
        id=cart_item.id,
        user_id=cart_item.user_id,
        book_id=cart_item.book_id,
        quantity=cart_item.quantity,
        created_at=cart_item.created_at,
        updated_at=cart_item.updated_at,
        book=BookOut.model_validate(cart_item.book),
        line_total=round(unit_price * cart_item.quantity, 2),
    )


def _build_cart_response(items: list[CartItem]) -> CartOut:
    serialized_items = [_serialize_cart_item(item) for item in items]
    total_items = sum(item.quantity for item in items)
    total_amount = round(sum(item.line_total for item in serialized_items), 2)
    return CartOut(
        items=serialized_items,
        total_items=total_items,
        total_amount=total_amount,
    )


async def _load_user_cart_items(db: AsyncSession, user_id: int) -> list[CartItem]:
    result = await db.execute(
        select(CartItem)
        .options(selectinload(CartItem.book))
        .where(CartItem.user_id == user_id)
        .order_by(CartItem.id)
    )
    return list(result.scalars().all())


async def _load_cart_item(db: AsyncSession, cart_item_id: int) -> CartItem:
    result = await db.execute(
        select(CartItem)
        .options(selectinload(CartItem.book))
        .where(CartItem.id == cart_item_id)
    )
    cart_item = result.scalar_one_or_none()
    if cart_item is None:
        return await require_cart_item(db=db, cart_item_id=cart_item_id)
    return cart_item


@router.get("", response_model=CartOut)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = await _load_user_cart_items(db=db, user_id=current_user.id)
    return _build_cart_response(items)


@router.post("", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    payload: CartItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await require_book(db=db, book_id=payload.book_id)

    result = await db.execute(
        select(CartItem).where(
            CartItem.user_id == current_user.id,
            CartItem.book_id == payload.book_id,
        )
    )
    cart_item = result.scalar_one_or_none()

    if cart_item is None:
        ensure_in_stock(book=book, quantity=payload.quantity)
        cart_item = CartItem(
            user_id=current_user.id,
            book_id=payload.book_id,
            quantity=payload.quantity,
        )
        db.add(cart_item)
    else:
        ensure_in_stock(book=book, quantity=cart_item.quantity + payload.quantity)
        cart_item.quantity += payload.quantity

    await db.commit()
    cart_item = await _load_cart_item(db=db, cart_item_id=cart_item.id)
    return _serialize_cart_item(cart_item)


@router.put("/{cart_item_id}", response_model=CartItemOut)
async def update_cart_item(
    cart_item_id: int,
    payload: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = await _load_cart_item(db=db, cart_item_id=cart_item_id)
    ensure_owner_or_admin(owner_id=cart_item.user_id, current_user=current_user)

    ensure_in_stock(book=cart_item.book, quantity=payload.quantity)
    cart_item.quantity = payload.quantity

    await db.commit()
    cart_item = await _load_cart_item(db=db, cart_item_id=cart_item.id)
    return _serialize_cart_item(cart_item)


@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    cart_item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_item = await require_cart_item(db=db, cart_item_id=cart_item_id)
    ensure_owner_or_admin(owner_id=cart_item.user_id, current_user=current_user)

    await db.delete(cart_item)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = await _load_user_cart_items(db=db, user_id=current_user.id)
    for item in items:
        await db.delete(item)

    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
