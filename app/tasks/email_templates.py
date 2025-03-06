from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings


def create_booking_confrimation_email(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    message = f"""<h1>confirm your booking</h1>
    <p>Booking is from {booking["date_from"]} to {booking["date_to"]} </p>
    """

    email.set_content(
        message,
        subtype="html"
    )

    return email