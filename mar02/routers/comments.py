from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import ensure_owner_or_admin, get_current_user, get_db
from ..models import Comment, User
from ..schemas import CommentCreate, CommentOut, CommentUpdate
from ..services import require_book, require_comment

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment(
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await require_book(db=db, book_id=payload.book_id)

    comment = Comment(
        content=payload.content,
        user_id=current_user.id,
        book_id=payload.book_id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("", response_model=list[CommentOut])
async def list_comments(
    book_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Comment).order_by(Comment.id)
    if book_id is not None:
        stmt = stmt.where(Comment.book_id == book_id)

    result = await db.execute(stmt)
    return list(result.scalars().all())


@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    return await require_comment(db=db, comment_id=comment_id)


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = await require_comment(db=db, comment_id=comment_id)
    ensure_owner_or_admin(owner_id=comment.user_id, current_user=current_user)

    comment.content = payload.content
    await db.commit()
    await db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = await require_comment(db=db, comment_id=comment_id)
    ensure_owner_or_admin(owner_id=comment.user_id, current_user=current_user)

    await db.delete(comment)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
