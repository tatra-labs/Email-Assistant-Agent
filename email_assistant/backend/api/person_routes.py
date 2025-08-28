from fastapi import APIRouter, HTTPException, Depends

from ..models.person_models import (
    PersonCreateRequest,
    PersonCreateResponse,
    PersonSeekRequest,
    PersonSeekResponse,
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
    

@router.post("/seek", response_model=PersonSeekResponse)
async def get_by_email(request: PersonSeekRequest, person_service: PersonService = Depends()):
    """Create a new person and return person ID."""
    try:
        response = await person_service.seek_person(request.email)
        return PersonSeekResponse(
            success=True,
            person_id=str(response.id),
            full_name=str(response.full_name),
            phone_number=str(response.phone_number),
            message="Person sought successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create person: {str(e)}")