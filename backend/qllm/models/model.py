from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import JSON, UUID, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import relationship, validates

from .base import Base


class User(Base):
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    # Relationships
    conversations = relationship(
        "Conversation", back_populates="user", cascade="all, delete-orphan"
    )
    medical_records = relationship(
        "MedicalRecord", back_populates="user", cascade="all, delete-orphan"
    )
    memories = relationship(
        "Memory", back_populates="user", cascade="all, delete-orphan"
    )
    memory_indices = relationship(
        "MemoryIndex", back_populates="user", cascade="all, delete-orphan"
    )

    # Validation
    @validates("email")
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email


class Conversation(Base):
    # Define columns
    document_id = Column(UUID(as_uuid=True), nullable=True)

    # Other columns
    title = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # Relationships
    messages = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
    user = relationship("User", back_populates="conversations")
    conversation_document = relationship(
        "ConversationDocument",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class MessageRoleEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class MessageStatusEnum(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class MessageSubProcessStatusEnum(str, Enum):
    PENDING = "PENDING"
    FINISHED = "FINISHED"


def to_pg_enum(enum_class) -> ENUM:
    return ENUM(enum_class, name=enum_class.__name__)


class Document(Base):
    """
    A document along with its metadata
    """

    # URL to the actual document (e.g. a PDF)
    url = Column(String, nullable=False, unique=True)
    metadata_map = Column(JSONB, nullable=True)
    conversation = relationship(
        "ConversationDocument", back_populates="document", cascade="all, delete-orphan"
    )


class ConversationDocument(Base):
    """
    A many-to-many relationship between a conversation and a document
    """

    conversation_id = Column(
        UUID(as_uuid=True), ForeignKey("conversation.id"), index=True
    )
    document_id = Column(UUID(as_uuid=True), ForeignKey("document.id"), index=True)
    conversation = relationship("Conversation", back_populates="conversation_document")
    document = relationship("Document", back_populates="conversation")


class Message(Base):
    """
    A message in a conversation
    """

    conversation_id = Column(
        UUID(as_uuid=True), ForeignKey("conversation.id"), index=True
    )
    content = Column(String)
    role = Column(to_pg_enum(MessageRoleEnum), nullable=False)
    status = Column(
        to_pg_enum(MessageStatusEnum), nullable=False, default=MessageStatusEnum.PENDING
    )

    conversation = relationship("Conversation", back_populates="messages")
    sub_processes = relationship(
        "MessageSubProcess", back_populates="message", cascade="all, delete-orphan"
    )


class MessageSubProcess(Base):
    """
    A record of a sub-process that occurred as part of the generation of a message from an AI assistant
    """

    message_id = Column(UUID(as_uuid=True), ForeignKey("message.id"), index=True)
    # source = Column(to_pg_enum(MessageSubProcessSourceEnum))
    message = relationship("Message", back_populates="sub_processes")
    status = Column(
        to_pg_enum(MessageSubProcessStatusEnum),
        default=MessageSubProcessStatusEnum.FINISHED,
        nullable=False,
    )
    metadata_map = Column(JSONB, nullable=True)


class MedicalRecord(Base):
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
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


class MemoryType(str, Enum):
    EPISODIC = "episodic"  # Lưu trữ các sự kiện/tương tác cụ thể
    SEMANTIC = "semantic"  # Lưu trữ kiến thức tổng quát
    PROCEDURAL = "procedural"  # Lưu trữ các quy trình/cách thức


class Memory(Base):
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    type = Column(to_pg_enum(MemoryType), nullable=False)
    content = Column(JSON, nullable=False)  # Lưu trữ nội dung memory dưới dạng JSON
    meta_data = Column(JSON)  # Lưu trữ metadata bổ sung
    embedding = Column(JSON)  # Vector embedding của memory
    importance_score = Column(Float, default=0.0)  # Điểm quan trọng của memory

    # Relationships
    user = relationship("User", back_populates="memories")


class MemoryIndex(Base):
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    memory_type = Column(to_pg_enum(MemoryType), nullable=False)
    index_data = Column(JSON)  # Lưu trữ cấu trúc index

    # Relationships
    user = relationship("User", back_populates="memory_indices")
