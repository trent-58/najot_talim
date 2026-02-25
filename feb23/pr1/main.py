import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import Base, SessionLocal, engine

app = FastAPI(title="Computers CRUD API")


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.post("/computers", response_model=schemas.ComputerResponse, status_code=status.HTTP_201_CREATED)
async def create_computer(computer: schemas.ComputerCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_computer(
        db=db,
        brand=computer.brand,
        model=computer.model,
        cpu=computer.cpu,
        ram_gb=computer.ram_gb,
    )


@app.get("/computers", response_model=list[schemas.ComputerResponse])
async def list_computers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_computers(db=db, skip=skip, limit=limit)


@app.get("/computers/{computer_id}", response_model=schemas.ComputerResponse)
async def get_computer(computer_id: int, db: AsyncSession = Depends(get_db)):
    db_computer = await crud.get_computer(db=db, computer_id=computer_id)
    if not db_computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    return db_computer


@app.put("/computers/{computer_id}", response_model=schemas.ComputerResponse)
async def update_computer(computer_id: int, payload: schemas.ComputerUpdate, db: AsyncSession = Depends(get_db)):
    db_computer = await crud.get_computer(db=db, computer_id=computer_id)
    if not db_computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    return await crud.update_computer(
        db=db,
        computer=db_computer,
        brand=payload.brand,
        model=payload.model,
        cpu=payload.cpu,
        ram_gb=payload.ram_gb,
    )


@app.delete("/computers/{computer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_computer(computer_id: int, db: AsyncSession = Depends(get_db)):
    db_computer = await crud.get_computer(db=db, computer_id=computer_id)
    if not db_computer:
        raise HTTPException(status_code=404, detail="Computer not found")
    await crud.delete_computer(db=db, computer=db_computer)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
