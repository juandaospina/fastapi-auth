from sqlalchemy import Column, Integer, String, Float

from app.config.database import Base

class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(45))
    overview = Column(String(255))
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)