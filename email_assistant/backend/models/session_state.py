from typing import List, Dict, Any
from datetime import datetime


class SessionState:
    """State class for session management."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def add_message(self, role: str, content: str):
        """Add a message to the session."""
        message = {
            "id": len(self.messages) + 1,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.messages.append(message)
        self.metadata["last_updated"] = datetime.utcnow().isoformat()
    
    def edit_message(self, message_id: str, content: str) -> bool:
        """Edit a message by ID."""
        try:
            msg_id = int(message_id)
            if 1 <= msg_id <= len(self.messages):
                self.messages[msg_id - 1]["content"] = content
                self.messages[msg_id - 1]["timestamp"] = datetime.utcnow().isoformat()
                self.metadata["last_updated"] = datetime.utcnow().isoformat()
                return True
        except (ValueError, IndexError):
            pass
        return False 