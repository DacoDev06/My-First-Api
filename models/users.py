from config.database import Base
from sqlalchemy import Column, String, Integer

class Users(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key = True)
    email = Column(String)
    password = Column(String)
    token = Column(String)