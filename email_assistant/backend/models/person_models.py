from pydantic import BaseModel, Field 


class PersonCreateRequest(BaseModel):
    """Request model for creating a person."""
    name: str = Field(..., description="Name of the person")
    email: str = Field(..., description="Email address of the person")
    phone_number: str = Field(..., description="Phone number of the person")


class PersonCreateResponse(BaseModel):
    """Response model for creating a person."""
    success: bool = Field(..., description="Whether the operation was successful")
    person_id: str = Field(..., description="The created person's ID")
    message: str = Field(..., description="Status message")


class PersonSeekByEmailRequest(BaseModel):
    """Request model for seeking a person by email."""
    email: str = Field(..., description="Email address of the person to seek")


class PersonSeekByEmailResponse(BaseModel):
    """Response model for seeking a person."""
    success: bool = Field(..., description="Whether the operation was successful")
    person_id: str = Field(..., description="The sought person's ID")
    email: str = Field(..., description="Email address of the sought person")
    full_name: str = Field(..., description="Name of the sought person")
    phone_number: str = Field(..., description="Phone number of the sought person")
    message: str = Field(..., description="Status message")


class PersonSeekByIDRequest(BaseModel):
    """Request model for seeking a person by email."""
    id: str = Field(..., description="ID of the person to seek")


class PersonSeekByIDResponse(BaseModel):
    """Response model for seeking a person."""
    success: bool = Field(..., description="Whether the operation was successful")
    person_id: str = Field(..., description="The sought person's ID")
    email: str = Field(..., description="Email address of the sought person")
    full_name: str = Field(..., description="Name of the sought person")
    phone_number: str = Field(..., description="Phone number of the sought person")
    message: str = Field(..., description="Status message")