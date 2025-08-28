from typing import Optional
from sqlalchemy.orm import Session

from .config import get_db
from .repositories import PersonRepository


class DatabasePersonService:
    """Database-backed person service for managing persons."""

    def __init__(self):
        self.db: Optional[Session] = None

    def _get_db(self):
        """Get database session."""
        if self.db is None:
            self.db = next(get_db())
        return self.db
    
    def create_person(self, name: str, email: str, phone_number: str) -> str:
        """Create a new person in the database."""
        try:
            db = self._get_db()
            person_repo = PersonRepository(db)
            person = person_repo.create(full_name=name, email_address=email, phone_number=phone_number)
            return str(person.id)
        except Exception as e:
            raise e
        
    def seek_person(self, email: str):
        """Seek a person by email in the database."""
        try:
            db = self._get_db()
            person_repo = PersonRepository(db)
            person = person_repo.get_by_email(email)
            if person is None:
                raise ValueError("Person not found")
            return person
        except Exception as e:
            raise e