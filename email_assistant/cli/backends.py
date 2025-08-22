from __future__ import annotations

from typing import Any

from .dummy import DummyBackend
from .fastapi_backend import FastAPIBackend


def get_backend(name: str, **kwargs: Any):
    """Return a backend instance by name. Extend with cloud backends later."""
    normalized = (name or "dummy").strip().lower()
    if normalized in ("dummy", "local"):
        return DummyBackend()
    elif normalized in ("fastapi", "api"):
        base_url = kwargs.get("base_url", "http://localhost:8000")
        return FastAPIBackend(base_url=base_url)
    raise ValueError(f"Unknown backend: {name}") 