from __future__ import annotations

import uuid
from typing import List, Dict, Any

from .base import BaseLLMBackend


class DummyBackend(BaseLLMBackend):
	"""A placeholder backend that provides mock implementations for all functions."""

	# In-memory storage for sessions (in real implementation this would be persistent)
	_sessions: Dict[str, List[Dict[str, str]]] = {}

	def chat_completion(self, messages: List[Dict[str, str]]) -> str:
		# Find the latest user message
		last_user = next((m for m in reversed(messages) if m.get("role") == "user"), None)
		user_text: str = (last_user.get("content") if last_user else None) or "(no input)"
		return (
			"Thank you for your message. Here is a brief acknowledgement while the full AI backend "
			"is being configured: " + user_text
		)

	def get_structured_output(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
		# Return schema keys with placeholder values
		result: Dict[str, Any] = {}
		for key, value in schema.items():
			if isinstance(value, dict):
				result[key] = self.get_structured_output(prompt, value)
			elif isinstance(value, list):
				result[key] = []
			else:
				result[key] = "TBD"
		return result

	def session_create(self) -> str:
		"""Create a new session and return session ID."""
		session_id = f"session_{uuid.uuid4().hex[:8]}"
		self._sessions[session_id] = []
		return session_id

	def session_delete(self, session_id: str) -> bool:
		"""Delete a session by ID. Returns success status."""
		if session_id in self._sessions:
			del self._sessions[session_id]
			return True
		return False

	def session_edit(self, session_id: str, message_id: str, message_content: str) -> bool:
		"""Edit a message in a session. Returns success status."""
		if session_id not in self._sessions:
			return False
		
		try:
			msg_index = int(message_id) - 1  # Convert to 0-based index
			if 0 <= msg_index < len(self._sessions[session_id]):
				self._sessions[session_id][msg_index]["content"] = message_content
				return True
		except (ValueError, IndexError):
			pass
		return False

	def session_chat(self, session_id: str, message_content: str) -> str:
		"""Add a message to a session and get response."""
		if session_id not in self._sessions:
			return f"Error: Session {session_id} not found"
		
		# Add user message to session
		self._sessions[session_id].append({
			"role": "user",
			"content": message_content
		})
		
		# Generate mock response
		response = f"Mock response to: {message_content}"
		
		# Add assistant response to session
		self._sessions[session_id].append({
			"role": "assistant", 
			"content": response
		})
		
		return response 