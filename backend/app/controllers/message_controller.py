# Purpose: Allows the frontend to perform CRUD operations on messages in the database.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.dependencies.auth import get_current_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message_schema import (
    MessageCreate,
    MessageUpdate,
    MessageResponse,
)

router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"],
)

# CREATE
@router.post("/", response_model=MessageResponse)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_message = Message(
        content=message.content,
        user_id=current_user.id,
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

# READ ALL OWN MESSAGES
@router.get("/", response_model=list[MessageResponse])
def get_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Message)
        .filter(Message.user_id == current_user.id)
        .all()
    )

# READ ONE OWN MESSAGE
@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == current_user.id,
        )
        .first()
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    return message

# UPDATE OWN MESSAGE
@router.put("/{message_id}", response_model=MessageResponse)
def update_message(
    message_id: int,
    updated_data: MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == current_user.id,
        )
        .first()
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    message.content = updated_data.content

    db.commit()
    db.refresh(message)

    return message

# DELETE OWN MESSAGE
@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == current_user.id,
        )
        .first()
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    db.delete(message)
    db.commit()

    return {"detail": "Message deleted"}
