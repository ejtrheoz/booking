from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


    model_config = ConfigDict(from_attributes=True)


