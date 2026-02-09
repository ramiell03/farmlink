# app/services/communication_service.py
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session
from app.models.messages import Message
from uuid import UUID

def send_message(db: Session, sender_id: UUID, receiver_id: UUID, content: str) -> Message:
    msg = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_conversations(db: Session, user_id: UUID):
    """
    Returns one row per conversation (last message per user pair)
    """

    subquery = (
        db.query(
            func.max(Message.created_at).label("last_time"),
            Message.sender_id,
            Message.receiver_id
        )
        .filter(or_(
            Message.sender_id == user_id,
            Message.receiver_id == user_id
        ))
        .group_by(Message.sender_id, Message.receiver_id)
        .subquery()
    )

    messages = (
        db.query(Message)
        .join(
            subquery,
            and_(
                Message.created_at == subquery.c.last_time,
                Message.sender_id == subquery.c.sender_id,
                Message.receiver_id == subquery.c.receiver_id
            )
        )
        .order_by(Message.created_at.desc())
        .all()
    )

    conversations = []
    for msg in messages:
        other_user = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
        conversations.append({
            "user_id": other_user,
            "last_message": msg.content,
            "last_message_at": msg.created_at
        })

    return conversations


def get_messages_with_user(
    db: Session,
    user_id: UUID,
    other_user_id: UUID
):
    return (
        db.query(Message)
        .filter(
            or_(
                and_(
                    Message.sender_id == user_id,
                    Message.receiver_id == other_user_id
                ),
                and_(
                    Message.sender_id == other_user_id,
                    Message.receiver_id == user_id
                )
            )
        )
        .order_by(Message.created_at.asc())
        .all()
    )
