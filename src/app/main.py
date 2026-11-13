from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.consumers import send_confirmation_email
from app.database import create_db
from app.event_bus import EVENT_REGISTRATION_CREATED, subscribe
from app.routers import registrations

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()

    subscribe(EVENT_REGISTRATION_CREATED, send_confirmation_email)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(registrations.router)
