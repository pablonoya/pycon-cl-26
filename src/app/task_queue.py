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
        finally:
            jobs.task_done()

def start_workers(num: int = 1):
    for _ in range(num):
        Thread(target=process_jobs, daemon=True).start()


def enqueue_confirmation(name: str, email: str):
    jobs.put((name, email))
