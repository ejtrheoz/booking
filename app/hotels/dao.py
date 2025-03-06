from app.hotels.models import Hotels
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select, and_, or_, func
from app.rooms.models import Rooms



class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def rooms_list(cls, hotel_id):
        async with async_session_maker() as session:
            query = select(Rooms).where(Rooms.hotel_id == hotel_id)
            rooms = await session.execute(query)
            rooms = rooms.scalars().all()
            return rooms


    @classmethod
    async def search_for_hotels(cls, location):
        async with async_session_maker() as session:
            query = select(Hotels).join(
                select(Rooms).where(
                    and_(
                        Rooms.hotel_id == Hotels.id,
                        Rooms.quantity > 0
                    )
                ).cte("rooms"),
            ).where(
                Hotels.location.contains(location)
            ).group_by(Hotels.id).having(
                func.count(Rooms.id) > 0
            )
            

            hotels = await session.execute(query)
            hotels = hotels.scalars().all()
            return hotels