from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app import db, auth
from app import config as cfg

router = APIRouter()

@router.get('/chats')
async def get_chats(request: Request, current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]):
    return cfg.template.TemplateResponse('chat.html', {'request': request, 'user': current_user})
