from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
    services = Column(JSON, nullable=True)

    hotel = relationship("Hotels", back_populates="rooms")
    booking = relationship("Bookings", back_populates="room")