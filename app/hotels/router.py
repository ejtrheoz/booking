from fastapi import APIRouter, Query
import datetime
from datetime import date
from app.hotels.dao import HotelsDAO
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)

@router.get("/{location}")
@cache(expire=60)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description="Date from"),
    date_to: date = Query(..., description="Date to")
):
    hotels = await HotelsDAO.search_for_hotels(location=location, date_from=date_from, date_to=date_to)
    return hotels
    
@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int):
    rooms = await HotelsDAO.rooms_list(hotel_id=hotel_id)
    return rooms