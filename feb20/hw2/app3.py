from fastapi import APIRouter

router3 = APIRouter()

@router3.get("/function1")
async def function1():
    return "router3 function1"

@router3.get("/function2")
async def function2():
    return "router3 function2"

@router3.get("/function3")
async def function3():
    return "router3 function3"
