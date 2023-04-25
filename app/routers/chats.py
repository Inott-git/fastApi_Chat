from typing import Annotated
from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from starlette.requests import Request
from app import db, auth, chats
from app import config as cfg

router = APIRouter()


@router.get('/chats')
async def get_chats(request: Request, current_user: Annotated[db.schems.User, Depends(auth.funcs.get_current_user)]):
    chats = await request.app.manager.get_chats(current_user.id)
    return cfg.template.TemplateResponse('chat.html', {'request': request, 'user': current_user, 'chats': chats})


@router.post('/chats/{chat_id}/hist')
async def get_hist_by_chat(chat_id: str, request: Request):
    msgs = await request.app.manager.get_hist_chat(chat_id)
    return msgs


@router.post('/chats/add')
async def add_msg_in_hist(chat_id: Annotated[str, Form()],
                          user_id: Annotated[int, Form()],
                          text: Annotated[str, Form()],
                          request: Request):
    await request.app.manager.add_msg(chat_id, user_id, text)
    return 'OK'


@router.post('/chats/add_chat', response_model=chats.schems.Chat)
async def add_chat(request: Request, user_id_1: Annotated[int, Form()], user_id_2: Annotated[int, Form()], session: Session = Depends(db.database.get_db)):
    user1 = db.crud.get_user_id(session, user_id_1)
    user2 = db.crud.get_user_id(session, user_id_2)
    return await request.app.manager.create_chat({'id': user1.id, 'username': user1.username},
                                       {'id': user2.id, 'username': user2.username})
