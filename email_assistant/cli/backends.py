from __future__ import annotations

import os
from dotenv import load_dotenv
from typing import Any

from .fastapi_backend import FastAPIBackend

load_dotenv()
fastapi_base_url = os.environ.get("FASTAPI_BASE_URL", "http://localhost:8000")

def get_backend(**kwargs: Any):
    """Return a backend instance by name. Extend with cloud backends later."""
    base_url = kwargs.get("base_url", fastapi_base_url)
    return FastAPIBackend(base_url=base_url)
    