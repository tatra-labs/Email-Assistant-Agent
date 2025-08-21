from __future__ import annotations

from typing import Any

from .dummy import DummyBackend


def get_backend(name: str, **kwargs: Any):
	"""Return a backend instance by name. Extend with cloud backends later."""
	normalized = (name or "dummy").strip().lower()
	if normalized in ("dummy", "local"):
		return DummyBackend()
	raise ValueError(f"Unknown backend: {name}") 