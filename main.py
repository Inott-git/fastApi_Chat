from typing import Annotated
from fastapi import FastAPI, Depends
from pymongo import MongoClient
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from app.chats import settings
from starlette.requests import Request
import app.db as db
import app.auth as auth
import app.config as cfg
from app.routers import users, chats
from app.chats import chat

root = FastAPI()

root.mount("/static", StaticFiles(directory=r"D:\Проекты\fastApi_WebSoket\app\static"), name="static")

root.include_router(users.router)
root.include_router(chats.router)
root.include_router(chat.router)


@root.on_event("startup")
def startup_db_client():
    root.mongodb_client = MongoClient(cfg.ATLAS_URI)
    root.database = root.mongodb_client[cfg.DB_NAME]
    root.manager = settings.ConnectionManager(root.database)
    root.db_session = db.database.get_db()
    print("Connected to the databases!")


@root.on_event("shutdown")
def shutdown_db_client():
    root.mongodb_client.close()
    root.db_session.close()


@root.get('/', response_class=HTMLResponse, tags=['Home'])
async def index(request: Request):
    return cfg.template.TemplateResponse('logreg.html', context={'request': request})
