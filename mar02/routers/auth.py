from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_current_user, get_db
from ..models import User
from ..schemas import RefreshTokenIn, Token, UserCreate, UserLogin, UserOut
from ..security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from ..services import create_user, get_user_by_id

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db=db, payload=payload)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import or_, select

    result = await db.execute(
        select(User).where(
            or_(User.username == payload.login, User.email == payload.login)
        )
    )
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    return Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.post("/refresh", response_model=Token)
async def refresh_tokens(payload: RefreshTokenIn, db: AsyncSession = Depends(get_db)):
    try:
        decoded = decode_token(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    subject = decoded.get("sub")
    if subject is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="Invalid token subject") from exc

    user = await get_user_by_id(db=db, user_id=user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")

    return Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
