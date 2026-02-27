from pydantic import BaseModel
from pydantic import Field, ConfigDict

class CompCreate(BaseModel):
    name:str
    description:str | None=None
    price: int

class CompResponse(CompCreate):
    id:int

    class Config:
        from_attributes=True


class SignUpSchema(BaseModel):
    name: str = Field(max_length=24, min_length=2)
    age: int = Field(ge=1, le=120)
    username: str = Field(max_length=13, min_length=5)
    email: str = Field(min_length=8, max_length=64)
    password: str = Field(max_length=64, min_length=4)


class SignUpOut(BaseModel):
    id: int
    name: str
    age: int | None = None
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)