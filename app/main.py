from fastapi import FastAPI
from app.routers.items import router as items_router
from app.routers.auth import router as auth_router
from app.db.database import Base, engine
from app import models


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(items_router, prefix="/items")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return {"message": "Personal Inbox API"}