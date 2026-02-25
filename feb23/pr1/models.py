from sqlalchemy import Column, Integer, String

from database import Base


class Computer(Base):
    __tablename__ = "computers"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    cpu = Column(String(100), nullable=False)
    ram_gb = Column(Integer, nullable=False)
