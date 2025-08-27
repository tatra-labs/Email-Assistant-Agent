from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import uuid
import os 

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
            db = self._get_db()
            session_repo = SessionRepository(db)
            return session_repo.delete(session_id)
        except ValueError:
            return False
    
    def edit_message(self, session_id: str, message_id: str, content: str) -> bool:
        """Edit a message in the database."""
        try:
            db = self._get_db()
            message_repo = MessageRepository(db)
            return message_repo.update_text(message_id, content) is not None
        except ValueError:
            return False
    
    async def add_message(self, session_id: str, sender_id: str, receiver_id: str, message_text: str, file_path: Optional[str]) -> str:
        """Add a chat message to the database and return AI response."""
        try:
            db = self._get_db()

            if ( file_path ) and ( not os.path.exists(file_path) ):
                raise Exception("File not found!")

            message_repo = MessageRepository(db)
            message = message_repo.create(
                session_id=str(session_id),
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_text=message_text,
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
            db = self._get_db()

            session_repo = SessionRepository(db)
            session = session_repo.get_by_id(session_id)
            
            if not session:
                return None
            
            session_info = session.to_dict()

            # Get messages for this session
            message_repo = MessageRepository(db)
            messages = message_repo.get_by_session(session_id)
            
            # Add message details
            session_messages = [msg.to_dict() for msg in messages] 
            session_info["messages"] = session_messages

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