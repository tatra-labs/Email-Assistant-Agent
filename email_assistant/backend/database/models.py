from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .config import Base


class Person(Base):
    """Person model for message sender and receiver."""
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.full_name}', email='{self.email_address}')>"


class Session(Base):
    """Session model containing multiple messages."""
    __tablename__ = "sessions"
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.session_id})>"


class Message(Base):
    """Message model within a session."""
    __tablename__ = "messages"
    
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("persons.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="messages")
    sender = relationship("Person", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("Person", foreign_keys=[receiver_id], back_populates="received_messages")
    files = relationship("MessageFile", back_populates="message", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Message(id={self.message_id}, text='{self.message_text[:50]}...')>"


class MessageFile(Base):
    """File attachments for messages."""
    __tablename__ = "message_files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.message_id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_content = Column(Text, nullable=True)  # Parsed text content
    file_type = Column(String(100), nullable=True)  # e.g., "pdf", "docx", "txt"
    file_size = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    message = relationship("Message", back_populates="files")
    
    def __repr__(self):
        return f"<MessageFile(id={self.id}, path='{self.file_path}', type='{self.file_type}')>"


# For SQLite compatibility (since SQLite doesn't support UUID natively)
class SQLiteUUID(String):
    """Custom UUID type for SQLite compatibility."""
    
    def __init__(self):
        super().__init__(36)  # UUID string length
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return str(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(value)


# SQLite-specific model definitions
class SQLitePerson(Base):
    """Person model for SQLite compatibility."""
    __tablename__ = "persons"
    
    id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email_address = Column(String(255), nullable=True)
    phone_number = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SQLiteSession(Base):
    """Session model for SQLite compatibility."""
    __tablename__ = "sessions"
    
    session_id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SQLiteMessage(Base):
    """Message model for SQLite compatibility."""
    __tablename__ = "messages"
    
    message_id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    session_id = Column(SQLiteUUID(), ForeignKey("sessions.session_id"), nullable=False)
    sender_id = Column(SQLiteUUID(), ForeignKey("persons.id"), nullable=False)
    receiver_id = Column(SQLiteUUID(), ForeignKey("persons.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SQLiteMessageFile(Base):
    """File attachments for SQLite compatibility."""
    __tablename__ = "message_files"
    
    id = Column(SQLiteUUID(), primary_key=True, default=uuid.uuid4)
    message_id = Column(SQLiteUUID(), ForeignKey("messages.message_id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_content = Column(Text, nullable=True)
    file_type = Column(String(100), nullable=True)
    file_size = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 