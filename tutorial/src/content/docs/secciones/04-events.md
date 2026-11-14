---
title: "Sección 4: Eventos"
description: Bus de eventos con varios consumidores.
---

El bus generaliza la cola: el endpoint publica un evento y cada consumidor lo procesa en su propio hilo. La rama parte de la cola con tres workers.

## 1. Consume y suscribe eventos

Archivo nuevo, `src/app/event_bus.py`:

```py title="src/app/event_bus.py"
from collections import defaultdict
from queue import Queue
from threading import Thread

subscribers = defaultdict(list)


def consume(handler, queue: Queue):
    while True:
        event = queue.get()

        try:
            handler(event)
        finally:
            queue.task_done()


def subscribe(event_type: str, handler):
    queue = Queue()
    subscribers[event_type].append(queue)

    Thread(
        target=consume,
        args=(handler, queue),
        daemon=True,
    ).start()
```

`subscribe` crea una cola y un hilo por handler; `consume` espera eventos en un loop.

## 2. Publica `registration.created`

```diff lang="py" title="src/app/event_bus.py"
  from collections import defaultdict
+ from dataclasses import dataclass
  from queue import Queue
  from threading import Thread

+ EVENT_REGISTRATION_CREATED = "registration.created"
+
  subscribers = defaultdict(list)


- def consume(handler, queue: Queue):
+ @dataclass
+ class RegistrationEvent:
+     registration_id: str
+     name: str
+     email: str
+
+
+ def consume(handler, queue: Queue[RegistrationEvent]):
      while True:
          event = queue.get()

          try:
              handler(event)
          finally:
              queue.task_done()


  def subscribe(event_type: str, handler):
      queue = Queue()
      subscribers[event_type].append(queue)

      Thread(
          target=consume,
          args=(handler, queue),
          daemon=True,
      ).start()
+
+
+ def publish(event_type, event: RegistrationEvent):
+     for queue in subscribers[event_type]:
+         queue.put(event)
```

```diff lang="py" title="src/app/routers/registrations.py"
  from app.database import execute
- from app.task_queue import enqueue_confirmation
+ from app.event_bus import EVENT_REGISTRATION_CREATED, RegistrationEvent, publish
```

```diff lang="py" title="src/app/routers/registrations.py"
  def create_registration(data: Registration):
      registration_id = str(uuid4())

      execute(
          "INSERT INTO registrations (id, name, email) VALUES (?, ?, ?)",
          (registration_id, data.name, data.email),
      )

      start = time.perf_counter()
-     enqueue_confirmation(data.name, data.email)
+
+     event = RegistrationEvent(registration_id, data.name, data.email)
+     publish(EVENT_REGISTRATION_CREATED, event)
+
      print(f"Email tardó {time.perf_counter() - start:.2f}s")
```

`publish` reparte el evento a todas las colas suscritas. El endpoint ya no conoce al envío de correo.

## 3. Suscribe el consumidor de email

Archivo nuevo, `src/app/consumers.py`:

```py title="src/app/consumers.py"
import logging

from app.event_bus import RegistrationEvent
from app.mailer import send_confirmation

logger = logging.getLogger(__name__)


def send_confirmation_email(event: RegistrationEvent):
    print("[Event] send confirmation email")
    send_confirmation(event.name, event.email)
```

```diff lang="py" title="src/app/main.py"
  from dotenv import load_dotenv
  from fastapi import FastAPI

+ from app.consumers import send_confirmation_email
  from app.database import create_db
+ from app.event_bus import EVENT_REGISTRATION_CREATED, subscribe
  from app.routers import registrations
- from app.task_queue import start_workers

  load_dotenv()


  @asynccontextmanager
  async def lifespan(app: FastAPI):
      create_db()
-     start_workers(3)
+
+     subscribe(EVENT_REGISTRATION_CREATED, send_confirmation_email)

      yield
```

El commit `ss` solo traduce el print del consumidor al español.

## 4. Agrega un consumidor de analíticas

```diff lang="py" title="src/app/consumers.py"
  import logging
+ from time import sleep

  from app.event_bus import RegistrationEvent
  from app.mailer import send_confirmation

  logger = logging.getLogger(__name__)


  def send_confirmation_email(event: RegistrationEvent):
      print("[Event] Envía email de confirmación")
      send_confirmation(event.name, event.email)
+
+
+ def registration_analytics(event: RegistrationEvent):
+     print("[Event] Incrementando analíticas")
+     sleep(2)
+     print("Analíticas finalizó")
```

```diff lang="py" title="src/app/main.py"
- from app.consumers import send_confirmation_email
+ from app.consumers import registration_analytics, send_confirmation_email
```

```diff lang="py" title="src/app/main.py"
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      create_db()

      subscribe(EVENT_REGISTRATION_CREATED, send_confirmation_email)
+     subscribe(EVENT_REGISTRATION_CREATED, registration_analytics)

      yield
```

Cada `subscribe` tiene su propio hilo: el `sleep(2)` de analíticas no bloquea la respuesta ni el correo. El mismo commit cambia el print del endpoint a `Publicación tardó…`. En la consola aparecen los prints de ambos consumidores y el orden puede variar.

Rama: `03-event-driven`
