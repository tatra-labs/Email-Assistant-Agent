from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import uuid

from .models import SQLitePerson as Person, SQLiteSession as DBSession, SQLiteMessage as Message


class PersonRepository:
    """Repository for Person operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, full_name: str, email_address: Optional[str] = None, phone_number: Optional[str] = None) -> Person:
        """Create a new person."""
        person = Person(
            id=str(uuid.uuid4()),
            full_name=full_name,
            email_address=email_address,
            phone_number=phone_number
        )
        self.db.add(person)
        self.db.commit()
        self.db.refresh(person)
        return person
    
    def get_by_id(self, person_id: uuid.UUID) -> Optional[Person]:
        """Get person by ID."""
        return self.db.query(Person).filter(Person.id == person_id).first()
    
    def get_by_email(self, email_address: str) -> Optional[Person]:
        """Get person by email address."""
        return self.db.query(Person).filter(Person.email_address == email_address).first()
    
    def update(self, person_id: uuid.UUID, **kwargs) -> Optional[Person]:
        """Update person information."""
        person = self.get_by_id(person_id)
        if person:
            for key, value in kwargs.items():
                if hasattr(person, key):
                    setattr(person, key, value)
            self.db.commit()
            self.db.refresh(person)
        return person
    
    def delete(self, person_id: uuid.UUID) -> bool:
        """Delete a person."""
        person = self.get_by_id(person_id)
        if person:
            self.db.delete(person)
            self.db.commit()
            return True
        return False


class SessionRepository:
    """Repository for Session operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, sender_id: str, receiver_id: str, summary: str) -> DBSession:
        """Create a new session."""
        session = DBSession(
            session_id=str(uuid.uuid4()),
            sender_id=sender_id,
            receiver_id=receiver_id,
            summary=summary
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def get_by_id(self, session_id: uuid.UUID) -> Optional[DBSession]:
        """Get session by ID with messages and files."""
        return self.db.query(DBSession).filter(DBSession.session_id == session_id).first()
    
    def get_all(self) -> List[DBSession]:
        """Get all sessions."""
        return self.db.query(DBSession).all()
    
    def update_summary(self, session_id: uuid.UUID, summary: str) -> Optional[DBSession]:
        """Update session summary."""
        session = self.get_by_id(session_id)
        if session:
            self.db.query(DBSession).filter(DBSession.session_id == session_id).update({"summary": summary})
            self.db.commit()
            return self.get_by_id(session_id)
        return None
    
    def delete(self, session_id: uuid.UUID) -> bool:
        """Delete a session and all its messages."""
        session = self.get_by_id(session_id)
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False


class MessageRepository:
    """Repository for Message operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, session_id: str, sender_id: str, receiver_id: str, message_text: str, message_file: Optional[str]) -> Message:
        """Create a new message."""
        file_text = ""
        message = Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_text=message_text,
            message_file=message_file,
            file_text=file_text
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_by_id(self, message_id: uuid.UUID) -> Optional[Message]:
        """Get message by ID with files."""
        return self.db.query(Message).filter(Message.message_id == message_id).first()
    
    def get_by_session(self, session_id: uuid.UUID) -> List[Message]:
        """Get all messages in a session."""
        return self.db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
    
    def update_text(self, message_id: uuid.UUID, message_text: str) -> Optional[Message]:
        """Update message text."""
        message = self.get_by_id(message_id)
        if message:
            self.db.query(Message).filter(Message.message_id == message_id).update({"message_text": message_text})
            self.db.commit()
            return self.get_by_id(message_id)
        return None
    
    def delete(self, message_id: uuid.UUID) -> bool:
        """Delete a message and its files."""
        message = self.get_by_id(message_id)
        if message:
            self.db.delete(message)
            self.db.commit()
            return True
        return False