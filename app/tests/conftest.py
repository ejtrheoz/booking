import pytest
from app.config import settings
from app.database import Base, async_session_maker, engine
import json
from sqlalchemy import insert, delete
from datetime import datetime

from app.users.models import Users
from app.hotels.models import Hotels
from app.rooms.models import Rooms
from app.bookings.models import Bookings

import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding='utf-8') as file:
            return json.load(file)
    

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        await session.execute(delete(Users))
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test"
    ) as ac:
        yield ac



@pytest.fixture(scope="session")
async def authenticated_client():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url="http://test"
    ) as ac:
        await ac.post("auth/login", json={
            "email": "vasya@example.com", 
            "password": "ejer"}
            )
        
        assert ac.cookies["booking_access_token"]
        yield ac

@pytest.fixture(scope="function")
async def session():
    async with async_session_maker as session:
        yield session