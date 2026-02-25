from pydantic import BaseModel, Field


class ComputerBase(BaseModel):
    brand: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    cpu: str = Field(..., max_length=100)
    ram_gb: int = Field(..., ge=1, le=1024)


class ComputerCreate(ComputerBase):
    pass


class ComputerUpdate(ComputerBase):
    pass


class ComputerResponse(ComputerBase):
    id: int

    class Config:
        from_attributes = True
