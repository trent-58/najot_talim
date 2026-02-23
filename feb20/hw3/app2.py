from fastapi import APIRouter

rout2 = APIRouter()

@rout2.get("/f1")
async def f1():
    return "rout f1"

@rout2.get("/f2")
async def f2():
    return "rout f2"

@rout2.get("/f3")
async def f3():
    return "rout f3"


