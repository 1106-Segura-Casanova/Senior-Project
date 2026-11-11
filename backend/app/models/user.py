# Purpose: Define the table for users in the database

from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    # Internal PostgreSQL primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Firebase's unique identifier for this account
    firebase_uid: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True
    )

    # Email associated with the Firebase account
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Optional name displayed in the application
    display_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    # Account creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Last profile update timestamp
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    messages = relationship("Message", back_populates="user")
