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

# Implemented from FastAPI docs https://fastapi.tiangolo.com/tutorial/security/get-current-user/#get-the-user
router = APIRouter(
    prefix="/api/messages",
    tags=["Messages"],
)

# CREATE
# Implemented from FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/main.py#L45
@router.post("/", response_model=MessageResponse)
def create_message(
    # Implemented from FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/main.py#L46-L48
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_message = Message(
        content=message.content,
        user_id=current_user.id,
    )
    #Implemented from FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/crud.py#L31-L36
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
 #Implemented from FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/crud.py#L28
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
# FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/crud.py#L7
    message = (
        db.query(Message)
        .filter(
            Message.id == message_id,
            Message.user_id == current_user.id,
        )
        .first()https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/crud.py
    )
# FastAPI docs Use HTTPException https://fastapi.tiangolo.com/tutorial/handling-errors/
    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    return message

# UPDATE OWN MESSAGE
# Decorator line implemented from FastAPI github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/body_updates/tutorial001.py#L30
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
# This we wrote
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
