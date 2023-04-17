from typing import Annotated
from starlette.requests import Request
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app import auth, db
router = APIRouter()


@router.websocket("/ws/{client_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, chat_id: int):
    manager = websocket.app.manager
    await manager.connect(websocket, client_id)
    print(f'{client_id} пришел')
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(chat_id=chat_id, client_id=client_id, message=f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f'{client_id} ушел')
