from fastapi import APIRouter, HTTPException, Depends

from ..models.person_models import (
    PersonCreateRequest,
    PersonCreateResponse,
    PersonSeekByEmailRequest,
    PersonSeekByEmailResponse,
    PersonSeekByIDRequest,
    PersonSeekByIDResponse,
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
    

@router.post("/seekbyid", response_model=PersonSeekByIDResponse)
async def get_by_id(request: PersonSeekByIDRequest, person_service: PersonService = Depends()):
    """Return person detail by id."""
    try:
        response = await person_service.seek_person_by_id(request.id)
        return PersonSeekByIDResponse(
            success=True,
            person_id=str(response.id),
            email=str(response.email_address),
            full_name=str(response.full_name),
            phone_number=str(response.phone_number),
            message="Person sought successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create person: {str(e)}")
    

@router.post("/seekbyemail", response_model=PersonSeekByEmailResponse)
async def get_by_email(request: PersonSeekByEmailRequest, person_service: PersonService = Depends()):
    """Return person detail by email address."""
    try:
        response = await person_service.seek_person_by_email(request.email)
        return PersonSeekByEmailResponse(
            success=True,
            person_id=str(response.id),
            email=str(response.email_address),
            full_name=str(response.full_name),
            phone_number=str(response.phone_number),
            message="Person sought successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create person: {str(e)}")