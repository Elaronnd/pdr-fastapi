from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends
)
from app.config.config import FORBIDDEN_TAGS
from app.schemas.pydantic_users import UserData
from app.utils.jwt_user import get_current_user_ws
from html import escape

websocket_router = APIRouter(prefix="/ws")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict[str, str], websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: dict[str, str]):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@websocket_router.websocket("/chat")
async def chat_websocket(
        websocket: WebSocket,
        token: UserData = Depends(get_current_user_ws)
):
    await manager.connect(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            message = escape(message)

            if len(message) > 1000:
                await manager.send_personal_message(
                    message={
                        "name": "Chat",
                        "tag": "System",
                        "message": "Too big text"
                    },
                    websocket=websocket
                )
                continue

            elif any(tag.lower() in message.lower() for tag in FORBIDDEN_TAGS):
                await manager.send_personal_message(
                    message={
                        "name": "Chat",
                        "tag": "System",
                        "message": "Please, don't try to scam"
                    },
                    websocket=websocket
                )
                continue

            await manager.broadcast(
                message={
                    "name": token.username,
                    "tag": "(Admin)" if token.is_admin is True else "(User)",
                    "message": message
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            message={
                "name": "Chat",
                "tag": "System",
                "message": f"User '{token.username}' left the chat"
            }
        )
