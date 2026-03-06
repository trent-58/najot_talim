from fastapi import FastAPI

from .database import Base, engine
from .routers.auth import router as auth_router
from .routers.books import router as books_router
from .routers.cart import router as cart_router
from .routers.categories import router as categories_router
from .routers.comments import router as comments_router
from .routers.genres import router as genres_router
from .routers.orders import router as orders_router
from .routers.users import router as users_router

app = FastAPI(title="mar04 Bookstore API")


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(genres_router)
app.include_router(books_router)
app.include_router(comments_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {"message": "mar04 Bookstore API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mar04.main:app", host="0.0.0.0", port=8004, reload=True)
