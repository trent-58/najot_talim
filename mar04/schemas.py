from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenIn(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    is_active: bool | None = None


class UserLogin(BaseModel):
    login: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class GenreOut(GenreBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    published_year: int = Field(ge=1, le=3000)
    pages: int = Field(ge=1, le=100000)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(ge=1)
    genre_id: int = Field(ge=1)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    published_year: int | None = Field(default=None, ge=1, le=3000)
    pages: int | None = Field(default=None, ge=1, le=100000)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = Field(default=None, ge=1)
    genre_id: int | None = Field(default=None, ge=1)


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    published_year: int
    pages: int
    price: float
    stock: int
    category_id: int
    genre_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime


class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CommentCreate(CommentBase):
    book_id: int = Field(ge=1)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    user_id: int
    book_id: int
    created_at: datetime
    updated_at: datetime


class CartItemBase(BaseModel):
    book_id: int = Field(ge=1)
    quantity: int = Field(ge=1, le=1000)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=1000)


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
    book: BookOut
    line_total: float


class CartOut(BaseModel):
    items: list[CartItemOut]
    total_items: int
    total_amount: float


class BuyNowCreate(BaseModel):
    book_id: int = Field(ge=1)
    quantity: int = Field(ge=1, le=1000)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    quantity: int
    unit_price: float
    line_total: float
    book: BookOut


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut]
