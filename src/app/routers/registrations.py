from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from app.database import execute


class Registration(BaseModel):
    name: str
    email: str


router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.post("", status_code=201)
def create_registration(data: Registration):
    registration_id = str(uuid4())

    execute(
        "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
        (registration_id, data.name, data.email),
    )

    return {"id": registration_id, **data.model_dump()}
