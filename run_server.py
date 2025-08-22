#!/usr/bin/env python3
"""
FastAPI server startup script for Email Assistant Agent.
"""

import uvicorn
from email_assistant.backend.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 