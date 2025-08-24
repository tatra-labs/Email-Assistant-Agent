from __future__ import annotations

from typing import Any

from .fastapi_backend import FastAPIBackend


def get_backend(**kwargs: Any):
    """Return a backend instance by name. Extend with cloud backends later."""
    base_url = kwargs.get("base_url", "http://localhost:8000")
    return FastAPIBackend(base_url=base_url)
    