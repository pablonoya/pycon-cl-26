---
title: "Sección 1: Base de datos"
description: SQLite, registros y validaciones.
---

## 1. Crea la tabla al arrancar

`lifespan` corre una vez al iniciar la app y crea la tabla si no existe. El endpoint `/hello` desaparece: ahora todo pasa por `/registrations`.

```diff lang="py" title="src/app/main.py"
+ from contextlib import asynccontextmanager
+
  from fastapi import FastAPI
 
- app = FastAPI()
+ from app.database import create_db
+
+
+ @asynccontextmanager
+ async def lifespan(app: FastAPI):
+     create_db()
+
+     yield
 
 
- @app.get("/hello")
- def hello(name: str | None = None):
-     return {"message": f"Hello {name or 'World'}!"}
+ app = FastAPI(lifespan=lifespan)
```

Archivo nuevo, `src/app/database.py`:

```py title="src/app/database.py"
import sqlite3
from pathlib import Path

DATABASE = Path("registrations.db")


def execute(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(query, params)


def create_db():
    execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )""")
```

`registrations.db` se crea en el directorio desde donde corrés la app, y `*.db` queda en `.gitignore`.

## 2. Guarda los registros

```diff lang="py" title="src/app/main.py"
  from contextlib import asynccontextmanager

  from fastapi import FastAPI

  from app.database import create_db
+ from app.routers import registrations


  @asynccontextmanager
  async def lifespan(app: FastAPI):
      create_db()

      yield


  app = FastAPI(lifespan=lifespan)
+ app.include_router(registrations.router)
```

Archivo nuevo, `src/app/routers/registrations.py`:

```py title="src/app/routers/registrations.py"
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
```

Pydantic valida el body y el `id` lo genera la app, no el cliente.

## 3. Valida el body

```diff lang="py" title="src/app/routers/registrations.py"
  from uuid import uuid4

  from fastapi import APIRouter
- from pydantic import BaseModel
+ from pydantic import BaseModel, EmailStr, Field

  from app.database import execute


  class Registration(BaseModel):
-     name: str
-     email: str
+     name: str = Field(min_length=2, max_length=50)
+     email: EmailStr
```

Un body inválido devuelve `422` antes de llegar al endpoint. `EmailStr` usa `email-validator`, incluido en `fastapi[standard]`.

El `POST /registrations` devuelve `201` con el `id` generado por la app, y el registro queda en `registrations.db`.

Rama: `00-database`
