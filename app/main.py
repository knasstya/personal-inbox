from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.db.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.items import router as items_router

from app.config import settings

app = FastAPI()

if settings.auto_create_tables:
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, prefix="/items")
app.include_router(auth_router, prefix="/auth")


@app.get("/")
def root():
    return {"message": "Personal Inbox API"}