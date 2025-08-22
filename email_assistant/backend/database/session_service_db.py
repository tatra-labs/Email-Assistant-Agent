from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
import uuid

from .config import get_db
from .repositories import SessionRepository, MessageRepository, PersonRepository, MessageFileRepository
from .models import Person, Session as DBSession, Message, MessageFile


class DatabaseSessionService:
    """Database-backed session service that integrates with the core session manager."""
    
    def __init__(self):
        self.db: Optional[Session] = None
    
    def _get_db(self):
        """Get database session."""
        if self.db is None:
            self.db = next(get_db())
        return self.db
    
    def create_session(self, summary: Optional[str] = None) -> str:
        """Create a new session in the database."""
        db = self._get_db()
        session_repo = SessionRepository(db)
        session = session_repo.create(summary)
        return str(session.session_id)
    
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
    
    async def chat_message(self, session_id: str, content: str) -> str:
        """Add a chat message to the database and return AI response."""
        try:
            session_uuid = uuid.UUID(session_id)
            db = self._get_db()
            
            # Get or create default sender/receiver for now
            # In a real implementation, this would come from user context
            person_repo = PersonRepository(db)
            sender = person_repo.get_by_email("ai.assistant@example.com")
            if not sender:
                sender = person_repo.create("AI Assistant", "ai.assistant@example.com")
            
            receiver = person_repo.get_by_email("user@example.com")
            if not receiver:
                receiver = person_repo.create("User", "user@example.com")
            
            # Create the message
            message_repo = MessageRepository(db)
            message = message_repo.create(
                session_id=session_uuid,
                sender_id=sender.id,
                receiver_id=receiver.id,
                message_text=content
            )
            
            # For now, return a mock AI response
            # In the future, this would call the actual AI engine
            ai_response = f"Mock AI response to: {content}"
            
            # Create AI response message
            ai_message = message_repo.create(
                session_id=session_uuid,
                sender_id=sender.id,
                receiver_id=receiver.id,
                message_text=ai_response
            )
            
            return ai_response
            
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
                    "created_at": msg.created_at.isoformat() if msg.created_at else None,
                    "files": []
                }
                
                # Add file information
                file_repo = MessageFileRepository(db)
                files = file_repo.get_by_message(msg.message_id)
                for file in files:
                    message_data["files"].append({
                        "id": str(file.id),
                        "path": file.file_path,
                        "type": file.file_type,
                        "size": file.file_size,
                        "content": file.file_content
                    })
                
                session_info["messages"].append(message_data)
            
            return session_info
            
        except ValueError:
            return None
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None
    
    def add_file_to_message(self, message_id: str, file_path: str, file_content: Optional[str] = None,
                           file_type: Optional[str] = None, file_size: Optional[str] = None) -> bool:
        """Add a file attachment to a message."""
        try:
            message_uuid = uuid.UUID(message_id)
            db = self._get_db()
            file_repo = MessageFileRepository(db)
            file_repo.create(
                message_id=message_uuid,
                file_path=file_path,
                file_content=file_content,
                file_type=file_type,
                file_size=file_size
            )
            return True
        except ValueError:
            return False
        except Exception as e:
            print(f"Error adding file: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.db:
            self.db.close()
            self.db = None 