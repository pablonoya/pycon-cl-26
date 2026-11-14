---
title: "Sección 3: Tareas en segundo plano"
description: Cola de tareas con varios workers.
---

El envío sale del request: la cola vive en memoria y los workers la consumen en hilos aparte.

## 1. Migra el envío a una cola

Archivo nuevo, `src/app/task_queue.py`:

```py title="src/app/task_queue.py"
from queue import Queue
from threading import Thread

from app.mailer import send_confirmation

jobs = Queue()


def process_jobs():
    while True:
        name, email = jobs.get()

        try:
            send_confirmation(name, email)
        except Exception as error:
            print(f"Failed to send email: {error}")


def start_worker():
    Thread(target=process_jobs, daemon=True).start()


def enqueue_confirmation(name: str, email: str):
    jobs.put((name, email))
```

El worker arranca con la app:

```diff lang="py" title="src/app/main.py"
  from app.database import create_db
  from app.routers import registrations
+ from app.task_queue import start_worker

  load_dotenv()


  @asynccontextmanager
  async def lifespan(app: FastAPI):
      create_db()
+     start_worker()

      yield
```

El endpoint solo encola:

```diff lang="py" title="src/app/routers/registrations.py"
  from app.database import execute
- from app.mailer import send_confirmation
+ from app.task_queue import enqueue_confirmation
```

```diff lang="py" title="src/app/routers/registrations.py"
  def create_registration(data: Registration):
      registration_id = str(uuid4())

      execute(
          "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
          (registration_id, data.name, data.email),
      )

      start = time.perf_counter()
-     send_confirmation(data.name, data.email)
+     enqueue_confirmation(data.name, data.email)
      print(f"Email tardó {time.perf_counter() - start:.2f}s")
```

`enqueue_confirmation` solo agrega a la cola; el envío ocurre en el hilo del worker. La respuesta ya no espera al SMTP.

## 2. Usa varios workers

```diff lang="py" title="src/app/main.py"
  from contextlib import asynccontextmanager

  from dotenv import load_dotenv
  from fastapi import FastAPI

  from app.database import create_db
  from app.routers import registrations
- from app.task_queue import start_worker
+ from app.task_queue import start_workers

  load_dotenv()


  @asynccontextmanager
  async def lifespan(app: FastAPI):
      create_db()
-     start_worker()
+     start_workers(3)

      yield


  app = FastAPI(lifespan=lifespan)
  app.include_router(registrations.router)
```

```diff lang="py" title="src/app/task_queue.py"
          try:
              send_confirmation(name, email)
          except Exception as error:
              print(f"Failed to send email: {error}")
+         finally:
+             jobs.task_done()


- def start_worker():
-     Thread(target=process_jobs, daemon=True).start()
+ def start_workers(num: int = 1):
+     for _ in range(num):
+         Thread(target=process_jobs, daemon=True).start()
```

`start_workers(3)` levanta tres hilos sobre la misma cola; `task_done()` marca cada trabajo terminado. La respuesta llega sin esperar al SMTP y los workers envían los correos.

La cola es del proceso: si el servidor se reinicia, los trabajos pendientes se pierden.

Rama: `02-defered-execution`
