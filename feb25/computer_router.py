from typing import List
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Computer
from schemas import CompCreate,CompResponse
import crud

router=APIRouter(prefix='/computers',tags=['Computers'])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/',response_model=CompResponse)
def create(computer:CompCreate,db:Session=Depends(get_db)):
    return crud.create_comp(db,computer)


@router.get('/', response_model=List[CompResponse])
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_comps(db)

@router.get("/{computer_id}",response_model=CompResponse)
def get_one(computer_id:int,db:Session=Depends(get_db)):
    computer=crud.get_comp(db,computer_id)
    if not computer:
        raise HTTPException(status_code=404,detail="Computer topilmadi")
    return computer

@router.delete("/{computer_id}")
def delete(computer_id:int,db:Session = Depends(get_db)):
    deleted = crud.delete_computer(db,computer_id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Computer topilmadi")
    return {"message":"Computer ochirildi"}