from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..models.session_models import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionDeleteRequest,
    SessionDeleteResponse,
    SessionEditRequest,
    SessionEditResponse,
    SessionChatRequest,
    SessionChatResponse,
    SessionFetchRequest,
    SessionFetchResponse
)
from ..services.session_service import SessionService

router = APIRouter(prefix="/session", tags=["sessions"])


@router.post("/create", response_model=SessionCreateResponse)
async def session_create(request: SessionCreateRequest, session_service: SessionService = Depends()):
    """Create a new session and return session ID."""
    try:
        session_id = await session_service.create_session(request.sender_id, request.receiver_id, request.subject)
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
    """Add a message to a session."""
    try:
        response = await session_service.add_message(request.session_id, request.sender_id, request.receiver_id, request.message_text, request.file_path)
        if response.startswith("Error"):
            return SessionChatResponse(
                success=False,
                response=response,
                message="Message not added!"
            )
        return SessionChatResponse(
            success=True,
            response=response,
            message="Message added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}") 
    

@router.post("/fetch", response_model=SessionFetchResponse)
async def session_fetch(request: SessionFetchRequest, session_service: SessionService = Depends()):
    """Fetch all the messages of a session."""
    try:
        response = session_service.fetch_session(request.session_id)
        if response:
            return SessionFetchResponse(
                success=True,
                response=response,
                message="Session detail fetched successfully!"
            )
        else:
            return SessionFetchResponse(
                success=False,
                response=response,
                message="Session detail fetching failed!"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch session detail: {str(e)}") 