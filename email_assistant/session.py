from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class Message:
	role: str
	content: str
	timestamp_iso: str

	@staticmethod
	def from_dict(data: Dict[str, Any]) -> "Message":
		return Message(
			role=data["role"],
			content=data["content"],
			timestamp_iso=data.get("timestamp_iso") or datetime.utcnow().isoformat() + "Z",
		)


class ChatSession:
	"""Maintains in-memory chat history and provides JSON persistence."""

	def __init__(self, system_prompt: Optional[str] = None) -> None:
		self.messages: List[Message] = []
		self.system_prompt = system_prompt
		if system_prompt:
			self.add_system_message(system_prompt)

	def add_system_message(self, content: str) -> None:
		self.messages.append(
			Message(role="system", content=content, timestamp_iso=datetime.utcnow().isoformat() + "Z")
		)

	def add_user_message(self, content: str) -> None:
		self.messages.append(
			Message(role="user", content=content, timestamp_iso=datetime.utcnow().isoformat() + "Z")
		)

	def add_assistant_message(self, content: str) -> None:
		self.messages.append(
			Message(role="assistant", content=content, timestamp_iso=datetime.utcnow().isoformat() + "Z")
		)

	def to_openai_messages(self) -> List[Dict[str, str]]:
		"""Converts messages to a generic OpenAI-like schema used by many LLMs."""
		return [{"role": m.role, "content": m.content} for m in self.messages]

	def to_json(self) -> str:
		return json.dumps([asdict(m) for m in self.messages], ensure_ascii=False, indent=2)

	@staticmethod
	def from_json(data: str) -> "ChatSession":
		items = json.loads(data)
		session = ChatSession()
		for item in items:
			session.messages.append(Message.from_dict(item))
		return session

	def save(self, path: str) -> None:
		with open(path, "w", encoding="utf-8") as f:
			f.write(self.to_json())

	@staticmethod
	def load(path: str, default_system_prompt: Optional[str] = None) -> "ChatSession":
		try:
			with open(path, "r", encoding="utf-8") as f:
				data = f.read()
			return ChatSession.from_json(data)
		except FileNotFoundError:
			return ChatSession(system_prompt=default_system_prompt) 