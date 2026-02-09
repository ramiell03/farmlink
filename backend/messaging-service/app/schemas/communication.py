# app/schemas/communication.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List

class MessageRequest(BaseModel):
    receiver_id: UUID
    content: str

class MessageResponse(BaseModel):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    user_id: UUID          # the other participant
    last_message: str
    last_message_at: datetime
