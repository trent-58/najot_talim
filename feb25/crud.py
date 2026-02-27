from sqlalchemy import Session
from models import Computer
from schemas import CompCreate


def create_comp(db:Session,computer:CompCreate):
    new_comp=Computer(**computer.dict())
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return new_comp

def get_all_comps(db:Session):
    return db.query(Computer).all()

def get_comp(db:Session,computer_id:int):
    return db.query(Computer).filter(Computer.id == computer_id).first()

def update_comp(db:Session,computer_id:int,computer:CompCreate):
    db_computer=get_comp(db,computer_id)
    if not db_computer:
        return None

    db_computer.name=computer.name
    db_computer.description=computer.description
    db_computer.price=computer.price

    db.commit()
    db.refresh(db_computer)
    return db_computer


def delete_computer(db:Session,computer_id:int):
    db_computer=get_comp(db,computer_id)
    if not db_computer:
        return None

    db.delete(db_computer)
    db.commit()
    return db_computer



