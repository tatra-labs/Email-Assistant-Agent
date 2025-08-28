from fastapi import APIRouter, HTTPException, Depends

from ..models.aisession_models import (
    AISessionCreateRequest,
    AISessionCreateResponse,
)
from ..services.aisession_service import SessionService 

router = APIRouter(prefix="/aisession", tags=["aisessions"])

@router.post("/create", response_model=AISessionCreateResponse) 
async def session_create(request: AISessionCreateRequest, session_service: SessionService = Depends()):
    """Create a new AI session and return session ID."""
    try:
        session_id = await session_service.create_session(request.user_id)
        return AISessionCreateResponse(
            success=True,
            session_id=session_id,
            message="AI Session created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create AI session: {str(e)}")
