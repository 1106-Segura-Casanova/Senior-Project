# Purpose: Define the table for messages in the database

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    user = relationship("User", back_populates="messages")
