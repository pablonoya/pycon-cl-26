from collections import defaultdict
from dataclasses import dataclass
from queue import Queue
from threading import Thread

EVENT_REGISTRATION_CREATED = "registration.created"

subscribers = defaultdict(list)


@dataclass
class RegistrationEvent:
    registration_id: str
    name: str
    email: str


def consume(handler, queue: Queue[RegistrationEvent]):
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


def publish(event_type, event: RegistrationEvent):
    for queue in subscribers[event_type]:
        queue.put(event)
