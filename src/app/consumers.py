import logging

from app.event_bus import RegistrationEvent
from app.mailer import send_confirmation

logger = logging.getLogger(__name__)


def send_confirmation_email(event: RegistrationEvent):
    print("[Event] Envía email de confirmación")
    send_confirmation(event.name, event.email)
