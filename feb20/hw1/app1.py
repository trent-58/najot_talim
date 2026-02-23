from fastapi import APIRouter

r1 = APIRouter()

@r1.get("/func1")
async def func1():
    return "r1 func1"

@r1.get("/func2")
async def func2():
    return "r1 func2"

@r1.get("/func3")
async def func3():
    return "r1 func3"


