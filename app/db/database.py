from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQL_DATABASE = 'app/db/db.db'

DB = create_engine(f'sqlite:///{SQL_DATABASE}')

SessionLocal = sessionmaker(DB)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
