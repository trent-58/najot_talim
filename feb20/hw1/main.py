import uvicorn
from fastapi import FastAPI
from app1 import r1
from app2 import r2
from app3 import r3


app =  FastAPI()
app.include_router(r1, prefix="/r1")
app.include_router(r2, prefix="/r2")
app.include_router(r3, prefix="/r3")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)