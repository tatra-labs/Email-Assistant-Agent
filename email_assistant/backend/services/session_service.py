from typing import Optional
from ...core.session_manager import SessionManager


import os
from dotenv import load_dotenv
from ...backend.database.session_service_db import DatabaseSessionService

class SessionService:
    """Service layer for session management and AI coordination using the database."""

    def __init__(self):
        self.db_service = DatabaseSessionService()

    async def create_session(self, sender_id: str, receiver_id: str, summary: str) -> str:
        """Create a new session using the database service."""
        return self.db_service.create_session(sender_id, receiver_id, summary)

    async def delete_session(self, session_id: str) -> bool:
        return self.db_service.delete_session(session_id)

    async def edit_message(self, session_id: str, element_id: str, content: str) -> bool:
        return self.db_service.edit_message(session_id, element_id, content)

    async def add_message(self, session_id: str, sender_id: str, receiver_id, content: str, file_path: Optional[str]) -> str:
        return await self.db_service.add_message(session_id, sender_id, receiver_id, content, file_path)