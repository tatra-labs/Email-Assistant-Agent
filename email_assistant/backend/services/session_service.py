from typing import Optional
from ...core.session_manager import SessionManager


class SessionService:
    """Service layer for session management and AI coordination."""
    
    def __init__(self):
        self.session_manager = SessionManager()
    
    async def create_session(self) -> str:
        """Create a new session."""
        return self.session_manager.create_session()
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        return self.session_manager.delete_session(session_id)
    
    async def edit_message(self, session_id: str, element_id: str, content: str) -> bool:
        """Edit a message in a session."""
        return self.session_manager.edit_message(session_id, element_id, content)
    
    async def chat_message(self, session_id: str, content: str) -> str:
        """Process a chat message and get AI response."""
        return await self.session_manager.chat_message(session_id, content)
    
    # def get_session_info(self, session_id: str) -> Optional[dict]:
    #     """Get session information."""
    #     return self.session_manager.get_session_info(session_id) 