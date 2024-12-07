from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    PickleType,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB  # Use JSONB for PostgreSQL
from sqlalchemy.orm import relationship, validates
from sqlalchemy.types import JSON  # Fallback for other DBs

from qllm.models.base import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)

    # Relationships
    chat_histories = relationship(
        "ChatHistory", back_populates="user", cascade="all, delete-orphan"
    )
    medical_records = relationship(
        "MedicalRecord", back_populates="user", cascade="all, delete-orphan"
    )

    # Validation
    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)

    # Relationships
    user = relationship("User", back_populates="chat_histories")
    chat_conversation = relationship(
        "ChatConversation",
        uselist=False,
        back_populates="chat_history",
        cascade="all, delete-orphan",
    )


class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    chat_history_id = Column(UUID, ForeignKey("chat_histories.id"), nullable=False)

    # Messages stored as JSON
    messages = Column(JSON().with_variant(PickleType(), "sqlite"), nullable=False)

    # Relationships
    chat_history = relationship("ChatHistory", back_populates="chat_conversation")

    # Validation
    @validates("messages")
    def validate_messages(self, key, messages):
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        for message in messages:
            if (
                not isinstance(message, dict)
                or "role" not in message
                or "content" not in message
            ):
                raise ValueError(
                    "Each message must be a dict with 'role' and 'content'"
                )
        return messages


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="medical_records")

    # Validation
    @validates("file_name")
    def validate_file_name(self, key, file_name):
        if len(file_name) > 255:
            raise ValueError("File name is too long")
        return file_name

    @validates("file_path")
    def validate_file_path(self, key, file_path):
        if not file_path:
            raise ValueError("File path cannot be empty")
        return file_path
