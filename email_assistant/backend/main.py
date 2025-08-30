from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from.api.person_routes import router as person_router
from .api.esession_routes import router as esession_router
from .api.aisession_routes import router as aisession_router

# Initialize FastAPI app
app = FastAPI(
    title="Email Assistant Agent API",
    description="AI-powered email assistant with session management",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(person_router)
app.include_router(esession_router)
app.include_router(aisession_router)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Email Assistant Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "engine": "langgraph"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 