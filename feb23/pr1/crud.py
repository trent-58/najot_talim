from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models


async def create_computer(
    db: AsyncSession,
    brand: str,
    model: str,
    cpu: str,
    ram_gb: int,
) -> models.Computer:
    computer = models.Computer(brand=brand, model=model, cpu=cpu, ram_gb=ram_gb)
    db.add(computer)
    await db.commit()
    await db.refresh(computer)
    return computer


async def get_computers(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Computer]:
    stmt = select(models.Computer).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_computer(db: AsyncSession, computer_id: int) -> models.Computer | None:
    stmt = select(models.Computer).where(models.Computer.id == computer_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_computer(
    db: AsyncSession,
    computer: models.Computer,
    brand: str,
    model: str,
    cpu: str,
    ram_gb: int,
) -> models.Computer:
    computer.brand = brand
    computer.model = model
    computer.cpu = cpu
    computer.ram_gb = ram_gb
    await db.commit()
    await db.refresh(computer)
    return computer


async def delete_computer(db: AsyncSession, computer: models.Computer) -> None:
    await db.delete(computer)
    await db.commit()
