from fastapi import APIRouter

rout1 = APIRouter()

@rout1.get("/f1")
async def f1():
    return "rout1 f1"

@rout1.get("/f2")
async def f2():
    return "rout1 f2"

@rout1.get("/f3")
async def f3():
    return "rout1 f3"


