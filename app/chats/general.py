from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/{client_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, chat_id: str):
    manager = websocket.app.manager
    await manager.connect(websocket, client_id)
    print(f'{client_id} пришел')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(chat_id=chat_id, client_id=client_id, message=data)
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        print(f'{client_id} ушел')
