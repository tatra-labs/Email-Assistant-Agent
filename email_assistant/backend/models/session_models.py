from pydantic import BaseModel, Field
from typing import Optional


class SessionCreateResponse(BaseModel):
    """Response model for session creation."""
    success: bool = Field(..., description="Whether the operation was successful")
    session_id: str = Field(..., description="The created session ID")
    message: str = Field(..., description="Status message")


class SessionDeleteRequest(BaseModel):
    """Request model for session deletion."""
    session_id: str = Field(..., description="The session ID to delete")


class SessionDeleteResponse(BaseModel):
    """Response model for session deletion."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")


class SessionEditRequest(BaseModel):
    """Request model for session message editing."""
    session_id: str = Field(..., description="The session ID")
    element_id: str = Field(..., description="The message ID to edit")
    content: str = Field(..., description="The new message content")


class SessionEditResponse(BaseModel):
    """Response model for session message editing."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")


class SessionChatRequest(BaseModel):
    """Request model for session chat."""
    session_id: str = Field(..., description="The session ID")
    content: str = Field(..., description="The message content to send")


class SessionChatResponse(BaseModel):
    """Response model for session chat."""
    success: bool = Field(..., description="Whether the operation was successful")
    response: str = Field(..., description="The AI response")
    message: str = Field(..., description="Status message") 