import pymongo.database
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from starlette.websockets import WebSocket
from app import config as cfg
from app.chats import schems

class ConnectionManager:
    def __init__(self, mongodb: pymongo.database.Database ):
        self.active_connections: dict[int:WebSocket] = {}
        self.chats = mongodb['chats'].find
        self.db = mongodb

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket


    def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)

    async def broadcast(self, message: str, chat_id: int, client_id: int):
        chat_users = self.chats({'id':chat_id})[0]['users']
        if client_id in chat_users:
            connections = chat_users
            print(connections)
            for connection in connections:
                try:
                    await self.active_connections[connection].send_text(message)
                except:
                    #что делать с сообщениями которые пришли юзеру не в сети
                    pass

    async def create_chat(self, uid1, uid2):
        chat = schems.Chat(user_id_1=uid1, user_id_2=uid2)
        self.db['chats'].insert_one(jsonable_encoder(chat))

    async def get_chats(self, client_id):
        chats = self.chats({"users.id":client_id})
        return list(chats)


