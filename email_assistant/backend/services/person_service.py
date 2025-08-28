from ...backend.database.person_service_db import DatabasePersonService 

class PersonService:
    """Service layer for person management using the database."""

    def __init__(self):
        self.db_service = DatabasePersonService()

    async def create_person(self, name: str, email: str, phone_number: str) -> str:
        """Create a new person using the database service."""
        return self.db_service.create_person(name, email, phone_number)
    
    async def seek_person_by_id(self, id: str):
        """Seek a person by email using the database service."""
        return self.db_service.seek_person_by_id(id)
    
    async def seek_person_by_email(self, email: str):
        """Seek a person by email using the database service."""
        return self.db_service.seek_person_by_email(email)