from typing import Optional, Dict, Any
from ..backend.engine.agents.email_assistant_agent import EmailAssistantAgent


class SessionManager:
    """Core session manager used by both CLI and backend."""
    
    def __init__(self):
        self.ai_agent = EmailAssistantAgent()
    
    def create_session(self) -> str:
        """Create a new session and return session ID."""
        return self.ai_agent.create_session()
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        return self.ai_agent.delete_session(session_id)
    
    def edit_message(self, session_id: str, message_id: str, content: str) -> bool:
        """Edit a message in a session."""
        return self.ai_agent.update_session_message(session_id, message_id, content)
    
    async def chat_message(self, session_id: str, content: str) -> str:
        """Process a chat message and get AI response."""
        return await self.ai_agent.process_message(session_id, content)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information."""
        return self.ai_agent.get_session_info(session_id) 