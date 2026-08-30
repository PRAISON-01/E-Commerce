from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.database import create_db_and_tables
from app.routers.auth_router import router as auth_router
# import app.models

@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)