from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.database import create_db
from app.routers import registrations

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(registrations.router)
