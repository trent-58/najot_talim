from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..deps import ensure_owner_or_admin, get_current_user, get_db
from ..models import Book, CartItem, Order, OrderItem, User
from ..schemas import BookOut, BuyNowCreate, OrderItemOut, OrderOut
from ..services import ensure_in_stock, require_book, require_order

router = APIRouter(prefix="/orders", tags=["Orders"])


def _serialize_order(order: Order) -> OrderOut:
    items = [
        OrderItemOut(
            id=item.id,
            book_id=item.book_id,
            quantity=item.quantity,
            unit_price=float(item.unit_price),
            line_total=float(item.line_total),
            book=BookOut.model_validate(item.book),
        )
        for item in order.items
    ]
    return OrderOut(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        total_amount=float(order.total_amount),
        created_at=order.created_at,
        items=items,
    )


async def _load_order(db: AsyncSession, order_id: int) -> Order:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.book))
        .where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if order is None:
        return await require_order(db=db, order_id=order_id)
    return order


async def _load_user_orders(db: AsyncSession, user_id: int) -> list[Order]:
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.book))
        .where(Order.user_id == user_id)
        .order_by(Order.id.desc())
    )
    return list(result.scalars().all())


async def _load_user_cart(db: AsyncSession, user_id: int) -> list[CartItem]:
    result = await db.execute(
        select(CartItem)
        .options(selectinload(CartItem.book))
        .where(CartItem.user_id == user_id)
        .order_by(CartItem.id)
    )
    return list(result.scalars().all())


async def _create_order(
    db: AsyncSession,
    user_id: int,
    lines: list[tuple[Book, int]],
    cart_items_to_clear: list[CartItem] | None = None,
) -> Order:
    if not lines:
        raise HTTPException(status_code=400, detail="Nothing to order")

    for book, quantity in lines:
        ensure_in_stock(book=book, quantity=quantity)

    order = Order(user_id=user_id, status="placed", total_amount=Decimal("0.00"))
    db.add(order)
    await db.flush()

    total_amount = Decimal("0.00")
    for book, quantity in lines:
        unit_price = Decimal(str(book.price)).quantize(Decimal("0.01"))
        line_total = (unit_price * quantity).quantize(Decimal("0.01"))
        total_amount += line_total
        book.stock -= quantity

        db.add(
            OrderItem(
                order_id=order.id,
                book_id=book.id,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )

    order.total_amount = total_amount.quantize(Decimal("0.01"))

    for cart_item in cart_items_to_clear or []:
        await db.delete(cart_item)

    await db.commit()
    return await _load_order(db=db, order_id=order.id)


@router.post("/buy-now", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def buy_now(
    payload: BuyNowCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = await require_book(db=db, book_id=payload.book_id)
    order = await _create_order(
        db=db,
        user_id=current_user.id,
        lines=[(book, payload.quantity)],
    )
    return _serialize_order(order)


@router.post("/checkout", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def checkout_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cart_items = await _load_user_cart(db=db, user_id=current_user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = await _create_order(
        db=db,
        user_id=current_user.id,
        lines=[(item.book, item.quantity) for item in cart_items],
        cart_items_to_clear=cart_items,
    )
    return _serialize_order(order)


@router.get("", response_model=list[OrderOut])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = await _load_user_orders(db=db, user_id=current_user.id)
    return [_serialize_order(order) for order in orders]


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = await _load_order(db=db, order_id=order_id)
    ensure_owner_or_admin(owner_id=order.user_id, current_user=current_user)
    return _serialize_order(order)
