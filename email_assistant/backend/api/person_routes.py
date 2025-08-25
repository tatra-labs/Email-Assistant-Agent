from fastapi import APIRouter, HTTPException, Depends

from ..models.person_models import (
    PersonCreateRequest,
    PersonCreateResponse,
)
from ..services.person_service import PersonService

router = APIRouter(prefix="/person", tags=["persons"]) 


@router.post("/create", response_model=PersonCreateResponse)
async def person_create(request: PersonCreateRequest, person_service: PersonService = Depends()):
    """Create a new person and return person ID."""
    try:
        person_id = await person_service.create_person(request.name, request.email, phone_number=request.phone_number)
        return PersonCreateResponse(
            success=True,
            person_id=person_id,
            message="Person created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create person: {str(e)}")