from fastapi import APIRouter

r2 = APIRouter()

@r2.get("/func1")
async def func1():
    return "r2 func1"

@r2.get("/func2")
async def func2():
    return "r2 func2"

@r2.get("/func3")
async def func3():
    return "r2 func3"


