import uvicorn
from fastapi import FastAPI
from app1 import router1
from app2 import router2
from app3 import router3


app =  FastAPI()
app.include_router(router1, prefix="/r1")
app.include_router(router2, prefix="/r2")
app.include_router(router3, prefix="/r3")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)