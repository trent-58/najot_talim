from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import auth
from schemas import schema
from deps import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=schema.SignUpOut, status_code=201)
async def signup(data: schema.SignUpSchema, db: AsyncSession = Depends(get_db)):
    return await auth.signup(db=db, data=data)