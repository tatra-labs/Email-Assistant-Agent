from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AISessionCreateRequest(BaseModel):
    """Request model for email assistant agent session deletion."""
    esession_id: str = Field(..., description="Session ID from email service")


class AISessionCreateResponse(BaseModel):
    """Response model for email assistant agent session creation."""
    success: bool = Field(..., description="Whether the operation was successful")
    aisession_id: str = Field(..., description="The created session ID")
    message: str = Field(..., description="Status message")

class AISessionChatRequest(BaseModel):
    """Request model for chat with sox.""" 
    aisession_id: str = Field(..., description="AI session ID")
    message: str = Field(..., description="Message from user") 
    context: Optional[Dict[str, Any]] = Field(..., description="Context for AI response")

class AISessionChatResponse(BaseModel):
    """Response model for chat with sox."""
    aisession_id: str = Field(..., description="AI session ID")
    response: str = Field(..., description="AI response") 