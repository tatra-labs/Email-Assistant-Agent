from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AISessionCreateRequest(BaseModel):
    """Request model for email assistant agent session deletion."""
    user_id: str = Field(..., description="User ID of the current invoker of email assistant")


class AISessionCreateResponse(BaseModel):
    """Response model for email assistant agent session creation."""
    success: bool = Field(..., description="Whether the operation was successful")
    session_id: str = Field(..., description="The created session ID")
    message: str = Field(..., description="Status message")
