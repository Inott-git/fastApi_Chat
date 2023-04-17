from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

template = Jinja2Templates(directory='app/templates')

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ATLAS_URI = 'mongodb://localhost:27017'
DB_NAME = 'Chats_data'
