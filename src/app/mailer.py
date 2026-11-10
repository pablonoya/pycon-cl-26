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
