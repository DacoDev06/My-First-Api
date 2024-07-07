from config.database import Base
from sqlalchemy import Column,Integer,String,Float

class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    rating = Column(Float)
    category = Column(String)