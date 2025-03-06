from app.tasks.celery import celery_app
from pathlib import Path
from PIL import Image
from app.config import settings
from app.tasks.email_templates import create_booking_confrimation_email
import smtplib


@celery_app.task
def resize_image(path: str):
    im_path = Path(path)
    im = Image.open(im_path)

    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))

    im_resized_1000_500.save(f"app/static/images/1000_500_{im_path.name}.webp")
    im_resized_200_100.save(f"app/static/images/200_100_{im_path.name}.webp")


@celery_app.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: str
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confrimation_email(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg_content)