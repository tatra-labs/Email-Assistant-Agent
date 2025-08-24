from __future__ import annotations

from typing import List, Dict, Any, Protocol


class BaseLLMBackend(Protocol):
	"""Protocol for LLM backends. Implementations should be stateless.

	Two primary operations are required:
	- chat_completion: generate an assistant reply from a chat history
	- get_structured_output: extract structured data matching a schema
	
	Session management operations:
	- session_create: create a new session and return session ID
	- session_delete: delete a session by ID
	- session_edit: edit a message in a session
	- session_chat: add a message to a session and get response
	"""
	
	def session_create(self) -> str:
		"""Create a new session and return session ID."""
		...

	def session_delete(self, session_id: str) -> bool:
		"""Delete a session by ID. Returns success status."""
		...

	def session_edit(self, session_id: str, message_id: str, message_content: str) -> bool:
		"""Edit a message in a session. Returns success status."""
		...

	def session_chat(self, session_id: str, message_content: str) -> str:
		"""Add a message to a session and get response."""
		... 