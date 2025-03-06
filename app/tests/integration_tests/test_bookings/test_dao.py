from app.bookings.dao import BookingDAO
from datetime import datetime


async def test_and_get_booking():
    new_booking = await BookingDAO.add(
        room_id = 2, 
        date_from=datetime.strptime("2023-06-04", "%Y-%m-%d"), 
        date_to=datetime.strptime("2023-06-24", "%Y-%m-%d"), 
        user_id = 2
    )

    assert new_booking.room_id == 2
    assert new_booking.user_id == 2


    booking = await BookingDAO.find_by_id(new_booking.id)

    assert booking is not None