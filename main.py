from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
import app.db as db
import app.auth as auth
import app.config as cfg
from app.routers import users, chats
from app.chats import chat

router = FastAPI()

router.include_router(users.router)
router.include_router(chats.router)
router.include_router(chat.router)



@router.get("/users/me/", response_model=db.schems.User)
async def read_users_me(
    current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]
):
    return current_user

@router.get('/')
async def index(request: Request):
    return cfg.template.TemplateResponse('home.html', context={'request': request})