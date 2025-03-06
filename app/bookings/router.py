from fastapi import APIRouter, Depends, HTTPException
from app.database import async_session_maker
from app.bookings.models import Bookings
from sqlalchemy import select
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from datetime import date
from app.tasks.tasks import send_booking_confirmation_email
from app.config import settings


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)

@router.get("/", response_model=list[SBooking])
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.get_all(user_id=user.id)


@router.post("/add")
async def add_booking(
    room_id: int, 
    date_from: date,
    date_to: date, 
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(room_id=room_id, date_from=date_from, date_to=date_to, user_id=user.id)
    if not booking:
        raise HTTPException(status_code=409, detail="Room is already booked")
    else:

        booking_dict = {column.name: getattr(booking, column.name) for column in booking.__table__.columns}
        send_booking_confirmation_email.delay(booking_dict, settings.SMTP_USER)
        return booking


@router.delete("/delete")
async def delete_booking(
    room_id: int, 
    user: Users = Depends(get_current_user),
    count: int = 1
):
    booking = await BookingDAO.delete(room_id=room_id, user_id=user.id)
    if not booking:
        return {"error": "Booking not found"}