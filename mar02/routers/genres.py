from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_current_user, get_db
from ..models import Genre, User
from ..schemas import GenreCreate, GenreOut, GenreUpdate
from ..services import require_genre

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post("", response_model=GenreOut, status_code=status.HTTP_201_CREATED)
async def create_genre(
    payload: GenreCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    genre = Genre(**payload.model_dump())
    db.add(genre)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Genre already exists") from exc

    await db.refresh(genre)
    return genre


@router.get("", response_model=list[GenreOut])
async def list_genres(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Genre).order_by(Genre.id))
    return list(result.scalars().all())


@router.get("/{genre_id}", response_model=GenreOut)
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    return await require_genre(db=db, genre_id=genre_id)


@router.put("/{genre_id}", response_model=GenreOut)
async def update_genre(
    genre_id: int,
    payload: GenreUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    genre = await require_genre(db=db, genre_id=genre_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(genre, field, value)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Genre already exists") from exc

    await db.refresh(genre)
    return genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre(
    genre_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    genre = await require_genre(db=db, genre_id=genre_id)
    await db.delete(genre)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
