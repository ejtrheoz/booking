from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import and_, insert, select, or_, delete, update
from app.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def rooms_left(cls, room_id, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_to,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            rooms_left_query = (
                select(Rooms.quantity)
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left_cte = rooms_left_query.cte("rooms_left")

            query = select(rooms_left_cte)
            rooms_left_result = await session.execute(query)
            rooms_left_result = rooms_left_result.scalar()

            return rooms_left_result

    @classmethod
    async def add(cls, room_id, date_from, date_to, user_id):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_to,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            rooms_left_query = (
                select(Rooms.quantity)
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left_cte = rooms_left_query.cte("rooms_left")

            query = select(rooms_left_cte)
            rooms_left_result = await session.execute(query)
            rooms_left_result = rooms_left_result.scalar()

            if rooms_left_result > 0:
                get_price_query = select(Rooms.price).where(Rooms.id == room_id)
                price = await session.execute(get_price_query)
                price = price.scalar()

                add_booking_query = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        date_from=date_from,
                        date_to=date_to,
                        user_id=user_id,
                        price=price,
                    )
                    .returning(Bookings)
                )

                new_booking = await session.execute(add_booking_query)

                rooms_decrease_query = (
                    update(Rooms)
                    .where(Rooms.id == room_id)
                    .values(quantity=Rooms.quantity - 1)
                )

                await session.execute(rooms_decrease_query)

                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    async def get_all(cls, user_id):
        async with async_session_maker() as session:
            query = select(Bookings).where(Bookings.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def delete(cls, user_id, room_id, count: int = 1):
        async with async_session_maker() as session:
            query = (
                select(Bookings.id)
                .where(and_(Bookings.user_id == user_id, Bookings.room_id == room_id))
                .limit(count)
            )
            result = await session.execute(query)
            booking_ids = result.scalars().all()

            if booking_ids:
                delete_query = delete(Bookings).where(Bookings.id.in_(booking_ids))
                await session.execute(delete_query)
                await session.commit()
                return booking_ids  # Returns the deleted booking IDs
            else:
                return None
