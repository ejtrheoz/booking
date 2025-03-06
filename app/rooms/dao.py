from app.dao.base import BaseDAO
from rooms.models import Rooms

class RoomsDAO(BaseDAO):
    model = Rooms