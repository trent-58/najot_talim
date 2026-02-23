from fastapi import APIRouter

r3 = APIRouter()

@r3.get("/func1")
async def func1():
    return "r3 func1"

@r3.get("/func2")
async def func2():
    return "r3 func2"

@r3.get("/func3")
async def func3():
    return "r3 func3"


