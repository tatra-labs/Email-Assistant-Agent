from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ESessionCreateRequest(BaseModel):
    """Request model for session deletion."""
    sender_id: str = Field(..., description="User ID of the sender")
    receiver_id: str = Field(..., description="User ID of the receiver")
    subject: str = Field("", description="Optional session subject")


class ESessionCreateResponse(BaseModel):
    """Response model for session creation."""
    success: bool = Field(..., description="Whether the operation was successful")
    session_id: str = Field(..., description="The created session ID")
    message: str = Field(..., description="Status message")


class ESessionDeleteRequest(BaseModel):
    """Request model for session deletion."""
    session_id: str = Field(..., description="The session ID to delete")


class ESessionDeleteResponse(BaseModel):
    """Response model for session deletion."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")


class ESessionEditRequest(BaseModel):
    """Request model for session message editing."""
    session_id: str = Field(..., description="The session ID")
    element_id: str = Field(..., description="The message ID to edit")
    content: str = Field(..., description="The new message content")


class ESessionEditResponse(BaseModel):
    """Response model for session message editing."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Status message")


class ESessionChatRequest(BaseModel):
    """Request model for session chat."""
    session_id: str = Field(..., description="The session ID")
    sender_id: str = Field(..., description="The sender's user ID")
    receiver_id: str = Field(..., description="The receiver's user ID")
    message_text: str = Field(..., description="The message text to send")
    file_path: Optional[str] = Field(None, description="Optional list of file paths to attach")


class ESessionChatResponse(BaseModel):
    """Response model for session chat."""
    success: bool = Field(..., description="Whether the operation was successful")
    response: str = Field(..., description="Added message ID")
    message: str = Field(..., description="Status message") 


class ESessionFetchRequest(BaseModel):
    """Request model for session fetch."""
    session_id: str = Field(..., description="The session ID")
    
    
class ESessionFetchResponse(BaseModel):
    """Response model for session fetch."""
    success: bool = Field(..., description="Whether the operation was successful")
    response: Optional[Dict[str, Any]] = Field(..., description="Result message")
    message: str = Field(..., description="Status message") 
