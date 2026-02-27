from fastapi import FastAPI
from database import engine
from models import Base
from computer_router import router
app.include_router(router)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Computer API")


app.include_router(computers.router)

@app.get("/")
def root():
    return {"message": "Computer API is running"}