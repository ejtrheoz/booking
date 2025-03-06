from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelsAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

middleware = [
    Middleware(SessionMiddleware, secret_key="..."),  # Replace with a strong secret key
]

app = FastAPI(lifespan=lifespan, middleware=middleware)

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(images_router)



admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelsAdmin)