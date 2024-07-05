from bd.database import Base

from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    title =Column(String(100))
    overview = Column(String(255))
    year=Column(Integer)
    rating=Column(Float)
    categoria=Column(String(100))