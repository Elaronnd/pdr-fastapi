from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set

from app.schemas.pydantic_users import (
    UserData
)

from app.db.queries import (
    get_user_by_id
)

websocket_router = APIRouter(prefix="/ws")

active_users: Set[WebSocket] = set()

@websocket_router.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    id = websocket.query_params["id"]

    if not id:
        await websocket.close(code=1008, reason="User ID not provided")
        raise ValueError("User ID not provided")

    user = get_user_by_id(id)

    if not user:
        await websocket.close(code=1008, reason="User not found")
        raise ValueError("User not found")
    
    name = user["username"]
    active_users.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()

            for user in active_users.copy(): 
                if websocket != user:
                    try:
                        await user.send_text(f"{name}: {data}")
                    except:
                        active_users.discard(user)

    except WebSocketDisconnect:
        pass

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        await websocket.close()
        active_users.discard(websocket)