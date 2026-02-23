from fastapi import APIRouter

rout3 = APIRouter()

@rout3.get("/f1")
async def f1():
    return "rout3 f1"

@rout3.get("/f2")
async def f2():
    return "rout3 f2"

@rout3.get("/f3")
async def f3():
    return "rout3 f3"


