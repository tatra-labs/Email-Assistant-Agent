from typing import Optional
from sqlalchemy.orm import Session

from .config import get_db
from .repositories import AISessionRepository


class AISessionService:
    """Database-backed session service that integrates with the core session manager."""
    
    def __init__(self):
        self.db: Optional[Session] = None
    
    def _get_db(self):
        """Get database session."""
        if self.db is None:
            self.db = next(get_db())
        return self.db
    
    def create_session(self, user_id: str) -> str:
        """Create a new session in the database."""
        try:
            db = self._get_db()
            aisession_repo = AISessionRepository(db)
            session = aisession_repo.create(user_id)
            return str(session.session_id)
        except Exception as e:
            raise e
    
    def close(self):
        """Close the database connection."""
        if self.db:
            self.db.close()
            self.db = None 