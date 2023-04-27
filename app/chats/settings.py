import json
import pymongo.database
from bson import ObjectId
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

    async def broadcast(self, message: str, chat_id: str, client_id: int):
        chat_users = self.chats({'_id':ObjectId(chat_id)})[0]['users']
        if client_id == chat_users[0]['id'] or client_id == chat_users[1]['id']:
            connections = chat_users
            for connection in connections:
                try:
                    data = json.dumps({'uid': client_id, 'msg': message})
                    await self.active_connections[connection['id']].send_text(data)
                except Exception as ex:
                    print(ex)

    async def create_chat(self, user1: schems.ChatUser, user2: schems.ChatUser):
        chat = schems.Chat(users=[user1, user2])
        new_id = self.db['chats'].insert_one(jsonable_encoder(chat)).inserted_id
        return self.db['chats'].find_one({'_id': ObjectId(new_id)})

    async def get_chats(self, client_id):
        chats = self.chats({"users.id": client_id})
        return list(chats)

    async def get_hist_chat(self, chat_id: str):
        msgs = list(self.chats({'_id':ObjectId(chat_id)}))
        return msgs[0]['msgs']

    async def add_msg(self, chat_id: str, user_id: int, text: str):
        self.db['chats'].update_one({'_id':ObjectId(chat_id)}, {'$push': {'msgs': {'user_id': user_id, 'text': text}}})
        return self.db['chats'].find_one({'_id':ObjectId(chat_id)})['msgs'][-1]
