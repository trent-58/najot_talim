from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=100)
    year: int = Field(..., ge=1, le=3000)
    pages: int = Field(..., ge=1)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
