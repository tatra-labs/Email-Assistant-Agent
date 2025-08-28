from typing import Optional, Dict, Any


from ..database.aisession_service_db import AISessionService

class SessionService:
    """Service layer for session management and AI coordination using the database."""

    def __init__(self):
        self.db_service = AISessionService()

    async def create_session(self, user_id: str) -> str:
        """Create a new session using the database service."""
        return self.db_service.create_session(user_id)
