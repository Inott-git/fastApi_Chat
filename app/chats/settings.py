import json
import pymongo.database
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocket
from app.chats import schems


class ConnectionManager:
    def __init__(self, mongodb: pymongo.database.Database):
        self.active_connections: dict[int:WebSocket] = {}
        self.chats = mongodb['chats'].find
        self.db = mongodb

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)

    async def broadcast(self, message: str, chat_id: int, client_id: int):
        chat_users = self.chats({'id': chat_id})[0]['users']
        if client_id == chat_users[0]['id'] or client_id == chat_users[1]['id']:
            connections = chat_users
            for connection in connections:
                try:
                    data = json.dumps({'uid': client_id, 'msg': message})
                    await self.active_connections[connection['id']].send_text(data)
                except:
                    #TODO: что делать с сообщениями которые пришли юзеру не в сети
                    pass

    async def create_chat(self, uid1, uid2):
        chat = schems.Chat(user_id_1=uid1, user_id_2=uid2)
        return self.db['chats'].insert_one(jsonable_encoder(chat))

    async def get_chats(self, client_id):
        chats = self.chats({"users.id": client_id})
        return list(chats)

    async def get_hist_chat(self, chat_id):
        msgs = list(self.chats({'id': chat_id}))
        return msgs[0]['msgs']

    async def add_msg(self, chat_id: int, user_id: int, text: str):
        return self.db['chats'].update_one({'id': chat_id}, {'$push': {'msgs': {'user_id': user_id, 'text': text}}})
