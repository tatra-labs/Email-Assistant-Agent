from fastapi import APIRouter, HTTPException, Depends

from ..models.esession_models import (
    ESessionCreateRequest,
    ESessionCreateResponse,
    ESessionDeleteRequest,
    ESessionDeleteResponse,
    ESessionEditRequest,
    ESessionEditResponse,
    ESessionChatRequest,
    ESessionChatResponse,
    ESessionFetchRequest,
    ESessionFetchResponse
)
from ..services.esession_service import SessionService

router = APIRouter(prefix="/esession", tags=["esessions"])


@router.post("/create", response_model=ESessionCreateResponse)
async def session_create(request: ESessionCreateRequest, session_service: SessionService = Depends()):
    """Create a new session and return session ID."""
    try:
        session_id = await session_service.create_session(request.sender_id, request.receiver_id, request.subject)
        return ESessionCreateResponse(
            success=True,
            session_id=session_id,
            message="Session created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.post("/delete", response_model=ESessionDeleteResponse)
async def session_delete(request: ESessionDeleteRequest, session_service: SessionService = Depends()):
    """Delete a session by ID."""
    try:
        success = await session_service.delete_session(request.session_id)
        if success:
            return ESessionDeleteResponse(
                success=True,
                message=f"Session {request.session_id} deleted successfully"
            )
        else:
            raise HTTPException(status_code=404, detail=f"Session {request.session_id} not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")


@router.post("/edit", response_model=ESessionEditResponse)
async def session_edit(request: ESessionEditRequest, session_service: SessionService = Depends()):
    """Edit a message in a session."""
    try:
        success = await session_service.edit_message(
            request.session_id,
            request.element_id,
            request.content
        )
        if success:
            return ESessionEditResponse(
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


@router.post("/chat", response_model=ESessionChatResponse)
async def session_chat(request: ESessionChatRequest, session_service: SessionService = Depends()):
    """Add a message to a session."""
    try:
        response = await session_service.add_message(request.session_id, request.sender_id, request.receiver_id, request.message_text, request.file_path)
        if response.startswith("Error"):
            return ESessionChatResponse(
                success=False,
                response=response,
                message="Message not added!"
            )
        return ESessionChatResponse(
            success=True,
            response=response,
            message="Message added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}") 
    

@router.post("/fetch", response_model=ESessionFetchResponse)
async def session_fetch(request: ESessionFetchRequest, session_service: SessionService = Depends()):
    """Fetch all the messages of a session."""
    try:
        response = session_service.fetch_session(request.session_id)
        if response:
            return ESessionFetchResponse(
                success=True,
                response=response,
                message="Session detail fetched successfully!"
            )
        else:
            return ESessionFetchResponse(
                success=False,
                response=response,
                message="Session detail fetching failed!"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch session detail: {str(e)}") 