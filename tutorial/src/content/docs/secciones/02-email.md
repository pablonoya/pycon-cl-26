---
title: "Sección 2: Correo de confirmación"
description: Credenciales, envío con smtplib y medición del envío.
---

## 1. Credenciales en `.env`

Copia el ejemplo y completa con tu cuenta de Gmail:

```bash
cp .env.example .env
```

```bash title=".env"
SMTP_USER=tu_correo@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

`SMTP_PASSWORD` es una [contraseña de aplicación](https://myaccount.google.com/apppasswords) de Gmail, no la de tu cuenta.

```diff lang="diff" title=".gitignore"
  # Database
  *.db
+
+ # .env
+ .env
```

Archivo nuevo, `.env.example`:

```bash title=".env.example"
SMTP_USER=user@gmail.com
SMTP_PASSWORD=acdc wasd abcd hjkl
```

`load_dotenv()` lee `.env` al importar el módulo:

```diff lang="py" title="src/app/main.py"
  from app.routers import registrations
 
+ load_dotenv()
```

`python-dotenv` ya viene con `fastapi[standard]`; no hace falta agregarlo a `pyproject.toml`.

## 2. Envía el correo

Archivo nuevo, `src/app/mailer.py`:

```py title="src/app/mailer.py"
import os
import smtplib
from email.message import EmailMessage


def send_confirmation(name: str, email: str):
    message = EmailMessage()
    message["Subject"] = "Registration confirmed"
    message["From"] = os.environ["SMTP_USER"]
    message["To"] = email
    message.set_content(f"¡Hola, {name}! Tu registro fue exitoso.")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(
                os.environ["SMTP_USER"],
                os.environ["SMTP_PASSWORD"],
            )
            smtp.send_message(message)

    except Exception as e:
        print(f"Error sending email: {e}")
```

El envío se conecta al endpoint:

```diff lang="py" title="src/app/routers/registrations.py"
  from app.database import execute
+ from app.mailer import send_confirmation
 
 
  class Registration(BaseModel):
```

```diff lang="py" title="src/app/routers/registrations.py"
  @router.post("", status_code=201)
  def create_registration(data: Registration):
      registration_id = str(uuid4())

      execute(
          "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
          (registration_id, data.name, data.email),
      )
- 
+     send_confirmation(data.name, data.email)
 
      return {"id": registration_id, **data.model_dump()}
```

El `try/except` evita que un fallo de SMTP rompa el request: el error solo se imprime. Pero el request espera al servidor de correo antes de responder; eso se arregla en la sección 3.

## 3. Mide el envío

```diff lang="py" title="src/app/routers/registrations.py"
+ import time
  from uuid import uuid4
```

```diff lang="py" title="src/app/routers/registrations.py"
  def create_registration(data: Registration):
      registration_id = str(uuid4())

      execute(
          "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
          (registration_id, data.name, data.email),
      )
 
+     start = time.perf_counter()
      send_confirmation(data.name, data.email)
-     
+     print(f"Email tardó {time.perf_counter() - start:.2f}s")
+
      return {"id": registration_id, **data.model_dump()}
```

`perf_counter` mide lo que tarda el SMTP; el print aparece en la consola. Ese tiempo es lo que se busca eliminar en la sección 3. La respuesta llega con `201` y el correo a la bandeja.

Rama: `01-email`
