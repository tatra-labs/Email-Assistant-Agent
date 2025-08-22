# CLI package for email_assistant
from .cli import main
from .backends import get_backend

__all__ = [
    "main",
    "get_backend",
] 