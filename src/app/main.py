from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db
from app.routers import registrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(registrations.router)
