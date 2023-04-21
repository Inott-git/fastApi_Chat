from sqlalchemy import Column, Integer, String
from app.db.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
