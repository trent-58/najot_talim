from fastapi import APIRouter

router1 = APIRouter()

@router1.get("/function1")
async def function1():
    return "router1 function1"

@router1.get("/function2")
async def function2():
    return "router1 function"

@router1.get("/function3")
async def function3():
    return "router1 function"


