from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.database import create_db
from app.routers import registrations
from app.task_queue import start_workers

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    start_workers(3)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(registrations.router)
