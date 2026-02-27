import hashlib

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schema


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


async def signup(db: AsyncSession, data: schema.SignUpSchema):
    statement = select(models.User).where(or_(models.User.username == data.username, models.User.email == data.email))
    result = await db.execute(statement)
    db_user = result.scalars().first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username yoki email avval ro'yxatdan o'tgan",
        )

    user = models.User(
        name=data.name,
        age=data.age,
        username=data.username,
        email=data.email,
        password=_hash_password(data.password),
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username yoki email avval ro'yxatdan o'tgan",
        )
    await db.refresh(user)
    return user
