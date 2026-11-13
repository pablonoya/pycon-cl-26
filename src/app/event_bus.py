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
