from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import uuid

from .config import get_db
from .repositories import SessionRepository, MessageRepository, PersonRepository
from .models import SQLitePerson as Person, SQLiteSession as DBSession, SQLiteMessage as Message


class DatabaseSessionService:
    """Database-backed session service that integrates with the core session manager."""
    
    def __init__(self):
        self.db: Optional[Session] = None
    
    def _get_db(self):
        """Get database session."""
        if self.db is None:
            self.db = next(get_db())
        return self.db
    
    def create_session(self, sender_id: str, receiver_id: str, summary: str) -> str:
        """Create a new session in the database."""
        try:
            db = self._get_db()
            session_repo = SessionRepository(db)
            session = session_repo.create(sender_id, receiver_id, summary)
            return str(session.session_id)
        except Exception as e:
            raise e
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session from the database."""
        try:
            session_uuid = uuid.UUID(session_id)
            db = self._get_db()
            session_repo = SessionRepository(db)
            return session_repo.delete(session_uuid)
        except ValueError:
            return False
    
    def edit_message(self, session_id: str, message_id: str, content: str) -> bool:
        """Edit a message in the database."""
        try:
            session_uuid = uuid.UUID(session_id)
            message_uuid = uuid.UUID(message_id)
            db = self._get_db()
            message_repo = MessageRepository(db)
            return message_repo.update_text(message_uuid, content) is not None
        except ValueError:
            return False
    
    async def add_message(self, session_id: str, sender_id: str, receiver_id: str, content: str, file_path: Optional[str]) -> str:
        """Add a chat message to the database and return AI response."""
        try:
            session_uuid = uuid.UUID(session_id)
            db = self._get_db()
            
            message_repo = MessageRepository(db)
            message = message_repo.create(
                session_id=str(session_uuid),
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_text=content,
                message_file=file_path
            )

            return str(message.message_id)
            
        except ValueError:
            return "Error: Invalid session ID"
        except Exception as e:
            return f"Error processing message: {str(e)}"
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information from the database."""
        try:
            session_uuid = uuid.UUID(session_id)
            db = self._get_db()
            session_repo = SessionRepository(db)
            session = session_repo.get_by_id(session_uuid)
            
            if not session:
                return None
            
            # Get messages for this session
            message_repo = MessageRepository(db)
            messages = message_repo.get_by_session(session_uuid)
            
            # Convert to dictionary format
            session_info = {
                "session_id": str(session.session_id),
                "summary": session.summary,
                "created_at": None,  # Simplified for now
                "updated_at": None,  # Simplified for now
                "message_count": len(messages),
                "messages": []
            }
            
            # Add message details
            for msg in messages:
                message_data = {
                    "message_id": str(msg.message_id),
                    "text": msg.message_text,
                    "sender": {
                        "id": str(msg.sender.id),
                        "name": msg.sender.full_name,
                        "email": msg.sender.email_address
                    },
                    "receiver": {
                        "id": str(msg.receiver.id),
                        "name": msg.receiver.full_name,
                        "email": msg.receiver.email_address
                    },
                    "created_at": msg.created_at.isoformat() if msg.created_at else None, # type: ignore
                    "files": []
                }
            
            return session_info
            
        except ValueError:
            return None
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None
    
    def close(self):
        """Close the database connection."""
        if self.db:
            self.db.close()
            self.db = None 