import time
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, Field

from app.database import execute
from app.mailer import send_confirmation


class Registration(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr


router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.post("", status_code=201)
def create_registration(data: Registration):
    registration_id = str(uuid4())

    execute(
        "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
        (registration_id, data.name, data.email),
    )

    start = time.perf_counter()
    send_confirmation(data.name, data.email)
    print(f"Email tardó {time.perf_counter() - start:.2f}s")

    return {"id": registration_id, **data.model_dump()}
