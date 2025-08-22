import uuid
from typing import Dict, Any, Optional
from ..llm.base import BaseLLM
from ..llm.mock_llm import MockLLM
from ..langgraph.email_workflow import EmailWorkflow


class EmailAssistantAgent:
    """Main AI agent for email assistance."""
    
    def __init__(self, llm: Optional[BaseLLM] = None):
        self.llm = llm or MockLLM()
        self.workflow = EmailWorkflow()
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self) -> str:
        """Create a new session and return session ID."""
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        self.sessions[session_id] = {
            "messages": [],
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "last_updated": "2024-01-01T00:00:00Z"
            }
        }
        return session_id
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def update_session_message(self, session_id: str, message_id: str, content: str) -> bool:
        """Update a message in the AI agent's session state."""
        if session_id not in self.sessions:
            return False
        
        try:
            msg_id = int(message_id)
            session = self.sessions[session_id]
            if 1 <= msg_id <= len(session["messages"]):
                session["messages"][msg_id - 1]["content"] = content
                return True
        except (ValueError, IndexError):
            pass
        return False
    
    async def process_message(self, session_id: str, content: str) -> str:
        """Process a message and generate AI response."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        
        # Add user message to session
        session["messages"].append({
            "id": len(session["messages"]) + 1,
            "role": "user",
            "content": content,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        # Prepare state for LangGraph workflow
        state = {
            "session_id": session_id,
            "messages": session["messages"],
            "user_input": content
        }
        
        # Run the workflow
        try:
            result = self.workflow.run(state)
            ai_response = result.get("ai_response", "No response generated")
        except Exception as e:
            # Fallback to direct LLM call if workflow fails
            messages = [{"role": "user", "content": content}]
            ai_response = await self.llm.generate_response(messages)
        
        # Add AI response to session
        session["messages"].append({
            "id": len(session["messages"]) + 1,
            "role": "assistant",
            "content": ai_response,
            "timestamp": "2024-01-01T00:00:00Z"
        })
        
        return ai_response 