# app/routes/communication_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.clients.auth_client import get_current_user, get_user_from_token
from app.db.database import SessionLocal
from app.services.communication_service import send_message

router = APIRouter(prefix="/ws/communication", tags=["Communication WS"])

# ---- DB dependency ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Connection Manager ----
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: UUID, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    async def send_personal_message(self, user_id: UUID, message: dict):
        for conn in self.active_connections.get(user_id, []):
            await conn.send_json(message)

    async def broadcast(self, message: dict):
        for conns in self.active_connections.values():
            for conn in conns:
                await conn.send_json(message)

manager = ConnectionManager()

@router.websocket("/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):

    db: Session = SessionLocal()
    try:
        # Use the helper for WS
        user_data = get_user_from_token(token)
        role = user_data["role"]
        if role not in ["buyer", "farmer"]:
            await websocket.close(code=1008)
            return

        user_id = UUID(user_data["id"])
        await manager.connect(user_id, websocket)

        while True:
            data = await websocket.receive_json()
            receiver_id_str = data.get("receiver_id")
            content = data.get("content")

            if not receiver_id_str or not content:
                await websocket.send_json({"error": "receiver_id and content required"})
                continue

            receiver_id = UUID(receiver_id_str)

            # Save message
            message = send_message(db, sender_id=user_id, receiver_id=receiver_id, content=content)

            # Send to receiver
            await manager.send_personal_message(receiver_id, {
                "id": str(message.id),
                "sender_id": str(user_id),
                "receiver_id": str(receiver_id),
                "content": content,
                "created_at": str(message.created_at)
            })

            # Confirm to sender
            await websocket.send_json({
                "status": "sent",
                "message": {
                    "id": str(message.id),
                    "receiver_id": str(receiver_id),
                    "content": content,
                    "created_at": str(message.created_at)
                }
            })

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        print("WebSocket auth/processing failed:", str(e))
        await websocket.close(code=1008)
    finally:
        db.close()
