from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.session_models import (
    SessionCreateResponse,
    SessionDeleteRequest,
    SessionDeleteResponse,
    SessionEditRequest,
    SessionEditResponse,
    SessionChatRequest,
    SessionChatResponse
)
from ..services.session_service import SessionService

router = APIRouter(prefix="/session", tags=["sessions"])


@router.post("/create", response_model=SessionCreateResponse)
async def session_create(session_service: SessionService = Depends()):
    """Create a new session and return session ID."""
    try:
        session_id = await session_service.create_session()
        return SessionCreateResponse(
            success=True,
            session_id=session_id,
            message="Session created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.post("/delete", response_model=SessionDeleteResponse)
async def session_delete(request: SessionDeleteRequest, session_service: SessionService = Depends()):
    """Delete a session by ID."""
    try:
        success = await session_service.delete_session(request.session_id)
        if success:
            return SessionDeleteResponse(
                success=True,
                message=f"Session {request.session_id} deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail=f"Session {request.session_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")


@router.post("/edit", response_model=SessionEditResponse)
async def session_edit(request: SessionEditRequest, session_service: SessionService = Depends()):
    """Edit a message in a session."""
    try:
        success = await session_service.edit_message(
            request.session_id,
            request.element_id,
            request.content
        )
        if success:
            return SessionEditResponse(
                success=True,
                message=f"Message {request.element_id} in session {request.session_id} edited successfully"
            )
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Failed to edit message {request.element_id} in session {request.session_id}"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to edit message: {str(e)}")


@router.post("/chat", response_model=SessionChatResponse)
async def session_chat(request: SessionChatRequest, session_service: SessionService = Depends()):
    """Add a message to a session and get AI response."""
    try:
        response = await session_service.chat_message(request.session_id, request.content)
        return SessionChatResponse(
            success=True,
            response=response,
            message="Message processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}") 