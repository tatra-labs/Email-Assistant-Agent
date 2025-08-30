from fastapi import APIRouter, HTTPException, Depends

from ..models.aisession_models import (
    AISessionCreateRequest,
    AISessionCreateResponse,
    AISessionChatRequest,
    AISessionChatResponse,
)
from ..services.aisession_service import SessionService 

router = APIRouter(prefix="/aisession", tags=["aisessions"])

@router.post("/create", response_model=AISessionCreateResponse) 
async def session_create(request: AISessionCreateRequest, session_service: SessionService = Depends()):
    """Create a new AI session and return session ID."""
    try:
        session_id = await session_service.create_session(request.esession_id)
        return AISessionCreateResponse(
            success=True,
            aisession_id=session_id,
            message="AI Session created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create AI session: {str(e)}")
    

@router.post("/chat_with_sox", response_model=AISessionChatResponse) 
async def session_chat(request: AISessionChatRequest, session_service: SessionService = Depends()):
    """Create a new AI session and return session ID."""
    try:
        response = session_service.chat_with_sox(request.aisession_id, request.message, request.context)
        return AISessionChatResponse(
            aisession_id=request.aisession_id,
            response=str(response)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to chat in AI session: {str(e)}")
