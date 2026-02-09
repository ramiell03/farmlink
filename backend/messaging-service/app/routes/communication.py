# app/routes/communication.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import SessionLocal
from app.clients.auth_client import require_roles
from app.schemas.communication import MessageRequest, MessageResponse, ConversationResponse
from app.services.communication_service import get_messages_with_user, send_message, get_conversations
from app.models.messages import Message


router = APIRouter(prefix="/communication", tags=["Communication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/conversations",
    response_model=List[ConversationResponse]
)
def list_conversations(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["buyer", "farmer"]))
):
    return get_conversations(db, user_id=user["id"])


@router.get("/messages/{other_user_id}", response_model=List[MessageResponse])
def get_messages_with_user_endpoint(
    other_user_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["buyer", "farmer"]))
):
    user_id = UUID(user["id"])
    msgs = get_messages_with_user(db, user_id, other_user_id)
    return msgs
