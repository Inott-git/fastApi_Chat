from sqlalchemy import Column, Integer, String
from .database import Base, DB

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
#
# Base.metadata.create_all(DB)