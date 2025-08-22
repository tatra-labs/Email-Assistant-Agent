# Email-Assistant-Agent
A personal assistant AI agent to help with email intelligence

## Project Structure

```
Email-Assistant-Agent/
├── email_assistant/         # Main package
│   ├── backend/             # Backend logic and endpoints
│   │   ├── api/             # FastAPI endpoints
│   │   │   └── session_routes.py
│   │   ├── services/        # Business logic services
│   │   │   └── session_service.py
│   │   ├── models/          # Data models
│   │   │   ├── session_models.py
│   │   │   └── session_state.py
│   │   ├── engine/          # AI engine (LLM + LangGraph)
│   │   │   ├── llm/         # LLM providers
│   │   │   │   ├── base.py  # Base LLM interface
│   │   │   │   └── mock_llm.py
│   │   │   ├── langgraph/   # LangGraph workflows
│   │   │   │   └── email_workflow.py
│   │   │   └── agents/      # AI agents
│   │   │       └── email_assistant_agent.py
│   │   ├── main.py          # FastAPI application
│   ├── cli/                 # CLI interface
│   │   ├── cli.py           # Main CLI logic
│   │   ├── session.py       # Session management
│   │   ├── backends.py      # Backend factory
│   │   ├── dummy.py         # Local mock backend
│   │   └── fastapi_backend.py # FastAPI HTTP client
│   ├── core/                # Shared core functionality
│   │   └── session_manager.py # Core session manager
│   ├── __init__.py          # Package initializer
│   └── __main__.py          # Module entry point
├── run_server.py            # Server startup script
└── requirements.txt         # Python dependencies
```

## Architecture

### **Unified Design**
- **Single Package**: All functionality is contained within `email_assistant` package
- **Shared Core**: Both CLI and backend use the same core functions
- **Clean Separation**: Backend endpoints and CLI commands use identical business logic

### **Core Layer** (`email_assistant/core/`)
- **SessionManager**: Central session management used by both CLI and backend
- **Shared Functions**: Common functionality accessible to all components

### **Backend Layer** (`email_assistant/backend/`)
- **API Routes**: FastAPI endpoints for session management
- **Services**: Business logic that calls core functions
- **Engine**: AI processing with LangGraph and LLM integration

### **CLI Layer** (`email_assistant/cli/`)
- **Command Interface**: User-friendly command-line interface
- **Backend Adapters**: Pluggable backend implementations
- **Same Core**: Uses identical core functions as backend

## Quickstart

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Server

```bash
# Option 1: Using the startup script
python run_server.py

# Option 2: Using uvicorn directly
uvicorn email_assistant.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`

### 3. Use the CLI

```bash
# From the repository root
python -m email_assistant help
python -m email_assistant session_create --backend fastapi
python -m email_assistant session_chat --backend fastapi --session_id <session_id> --content "Hello, how are you?"
python -m email_assistant session_delete --backend fastapi --session_id <session_id>
```

### Available Commands

1. **help** - Show help message with all available commands
2. **session_create** - Create a new session and return session ID
3. **session_delete --session_id <id>** - Delete session with given ID
4. **session_edit --session_id <id> --element_id <msg_id> --content <content>** - Edit message in session
5. **session_chat --session_id <id> --content <content>** - Add message to session and get response

### Examples

```bash
# Create a new session
python -m email_assistant session_create --backend fastapi

# Chat with the assistant (replace abc123 with actual session ID)
python -m email_assistant session_chat --backend fastapi --session_id abc123 --content "Hello, can you help me draft an email?"

# Edit a message in the session
python -m email_assistant session_edit --backend fastapi --session_id abc123 --element_id 1 --content "Updated message content"

# Delete the session
python -m email_assistant session_delete --backend fastapi --session_id abc123
```

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

### Backend Options

The CLI supports multiple backends:
- `dummy` (default): Local mock implementation
- `fastapi`: Connect to FastAPI server with LangGraph engine

```bash
# Use dummy backend (no server required)
python -m email_assistant session_create --backend dummy

# Use FastAPI backend (requires server running)
python -m email_assistant session_create --backend fastapi
```

## Key Benefits

1. **Unified Architecture**: CLI and backend use identical core functions
2. **Single Source of Truth**: All business logic is in one place
3. **Easy Testing**: Core functions can be tested independently
4. **Consistent Behavior**: CLI and API behave identically
5. **Maintainable**: Changes to core logic affect both interfaces

## Roadmap

- Real LLM integration (Amazon Bedrock / Google Gemini)
- Email parsing (text/PDF) and structured extraction
- Draft reply generation and tone control
- Iterative refinement and saving drafts to file
- Database persistence for sessions
