from typing import Annotated
from fastapi import APIRouter, Depends, Form
from starlette.requests import Request
from app import db, auth
from app import config as cfg

router = APIRouter()

@router.get('/chats')
async def get_chats(request: Request, current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]):
    chats = await request.app.manager.get_chats(current_user.id)

    return cfg.template.TemplateResponse('chat_base.html', {'request': request, 'user': current_user, 'chats': chats})


@router.get('/chat/{chat_id}')
async def get_chats(chat_id: int, request: Request, current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]):
    return cfg.template.TemplateResponse('chat.html', {'request': request, 'user': current_user, 'chat_id': chat_id})

@router.post('/chats/{chat_id}/hist')
async def get_hist_by_chat(chat_id: int, request: Request):
    msgs = await request.app.manager.get_hist_chat(chat_id)
    return msgs

@router.post('/chats/add')
async def add_msg_in_hist(chat_id: Annotated[int, Form()], user_id: Annotated[int, Form()], text: Annotated[str, Form()], request: Request):
    print(chat_id, user_id, text)
    await request.app.manager.add_msg(chat_id, user_id, text)
    return 'OK'
