import uvicorn
from fastapi import FastAPI
from app1 import rout1
from app2 import rout2
from app3 import rout3


app =  FastAPI()
app.include_router(rout1, prefix="/rout1")
app.include_router(rout2, prefix="/rout2")
app.include_router(rout3, prefix="/rout3")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)