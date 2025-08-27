from __future__ import annotations

import httpx
from typing import List, Dict, Any, Optional
import json

from .base import BaseEmailAssistantBackend


class FastAPIBackend(BaseEmailAssistantBackend):
    """FastAPI backend that connects to the LangGraph engine via HTTP."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request to FastAPI server."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = await self.client.get(url)
            elif method.upper() == "POST":
                response = await self.client.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except:
                error_detail = str(e)
            raise Exception(f"HTTP {e.response.status_code}: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Request failed: {e}")
    
    def session_create(self, sender_id, receiver_id) -> str:
        """Create a new session via FastAPI."""
        import asyncio
        try:
            result = asyncio.run(self._make_request("POST", "/session/create", {
                "sender_id": sender_id,
                "receiver_id": receiver_id
            }))
            return result["session_id"]
        except Exception as e:
            raise Exception(f"Failed to create session: {e}")
    
    def session_delete(self, session_id: str) -> bool:
        """Delete a session via FastAPI."""
        import asyncio
        try:
            result = asyncio.run(self._make_request("POST", "/session/delete", {
                "session_id": session_id
            }))
            return result["success"]
        except Exception as e:
            raise Exception(f"Failed to delete session: {e}")
    
    def session_edit(self, session_id: str, message_id: str, message_content: str) -> bool:
        """Edit a message in session via FastAPI."""
        import asyncio
        try:
            result = asyncio.run(self._make_request("POST", "/session/edit", {
                "session_id": session_id,
                "element_id": message_id,
                "content": message_content
            }))
            return result["success"]
        except Exception as e:
            raise Exception(f"Failed to edit message: {e}")
    
    def session_chat(self, session_id: str, sender_id: str, receiver_id: str, message_text: str, file_path: Optional[str]) -> str:
        """Add message to session and get response via FastAPI."""
        import asyncio
        try:
            result = asyncio.run(self._make_request("POST", "/session/chat", {
                "session_id": session_id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "message_text": message_text,
                "file_path": file_path
            }))
            return result["response"]
        except Exception as e:
            raise Exception(f"Failed to process message: {e}")
        
    def session_fetch(self, session_id: str) -> str:
        """Add message to session and get response via FastAPI."""
        import asyncio
        try:
            result = asyncio.run(self._make_request("POST", "/session/fetch", {
                "session_id": session_id
            }))
            return result["response"]
        except Exception as e:
            raise Exception(f"Failed to process message: {e}")
    
    def __del__(self):
        """Cleanup HTTP client."""
        if hasattr(self, 'client'):
            try:
                import asyncio
                asyncio.run(self.client.aclose())
            except:
                pass 