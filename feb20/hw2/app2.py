from fastapi import APIRouter

router2 = APIRouter()

@router2.get("/function1")
async def function1():
    return "router2 function1"

@router2.get("/function2")
async def function2():
    return "router2 function"

@router2.get("/function3")
async def function3():
    return "router2 function"

