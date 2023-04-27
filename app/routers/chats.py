from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app import db, auth, chats
from app import config as cfg

router = APIRouter()


@router.get('/chats', response_class=HTMLResponse, tags=['Chats'])
async def get_chats(request: Request, current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]):
    """
    Get all chats for user
    """
    if not current_user:
        return RedirectResponse('/')
    chats_by_user = await request.app.manager.get_chats(current_user.id)
    return cfg.template.TemplateResponse('chat.html',
                                         {'request': request,
                                          'user': current_user,
                                          'chats': chats_by_user})


@router.post('/chats/{chat_id}/hist', response_model=list[chats.schems.Msg], tags=['Chats'])
async def get_hist_by_chat(chat_id: str, request: Request):
    """
    Get history of chat by id
    """
    msgs = await request.app.manager.get_hist_chat(chat_id)
    return msgs


@router.post('/chats/add', response_model=chats.schems.Msg, tags=['Chats'])
async def add_msg_in_hist(chat_id: Annotated[str, Form()],
                          user_id: Annotated[int, Form()],
                          text: Annotated[str, Form()],
                          request: Request):
    """
    Add new messages in chat
    """
    return await request.app.manager.add_msg(chat_id, user_id, text)


@router.post('/chats/add_chat',
             response_model=chats.schems.Chat,
             tags=['Chats'])
async def add_chat(request: Request, user_id_1: Annotated[int, Form()], user_id_2: Annotated[int, Form()]):
    """
    Add new chat
    """
    user1 = db.crud.get_user_id(request.app.db_session, user_id_1)
    user2 = db.crud.get_user_id(request.app.db_session, user_id_2)
    return await request.app.manager.create_chat({'id': user1.id, 'username': user1.username},
                                                 {'id': user2.id, 'username': user2.username})
