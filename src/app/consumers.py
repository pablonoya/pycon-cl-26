import logging
from time import sleep

from app.event_bus import RegistrationEvent
from app.mailer import send_confirmation

logger = logging.getLogger(__name__)


def send_confirmation_email(event: RegistrationEvent):
    print("[Event] Envía email de confirmación")
    send_confirmation(event.name, event.email)


def registration_analytics(event: RegistrationEvent):
    print("[Event] Incrementando analíticas")
    sleep(2)
    print("Analíticas finalizó")
