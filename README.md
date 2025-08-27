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
│   │   ├── database/        # Database configuration and models
│   │   │   ├── config.py    # Database connection
│   │   │   ├── models.py    # SQLAlchemy models
│   │   │   ├── repositories.py # Data access layer
│   │   │   └── init_db.py   # Database initialization
│   │   ├── engine/          # AI engine (LLM + LangGraph)
│   │   │   ├── llm/         # LLM providers
│   │   │   │   ├── base.py  # Base LLM interface
│   │   │   │   └── mock_llm.py
│   │   │   ├── langgraph/   # LangGraph workflows
│   │   │   │   └── email_workflow.py
│   │   │   ├── agents/      # AI agents
│   │   │   │   └── email_assistant_agent.py
│   │   │   └── utils/       # Utilities 
│   │   │       └── pdf_parser.py 
│   │   └── main.py          # FastAPI application
│   ├── cli/                 # CLI interface
│   │   ├── cli.py           # Main CLI logic
│   │   ├── backends.py      # Backend factory
│   │   └── fastapi_backend.py # FastAPI HTTP client
│   ├── __init__.py          # Package initializer
│   └── __main__.py          # Module entry point
├── run_server.py            # Server startup script
├── init_database.py         # Database initialization script
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
- **Database**: SQLAlchemy models and repositories for data persistence
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

### 2. Initialize Database

```bash
# Initialize database with tables and sample data
python init_database.py
```

This will create:
- `email_assistant.db` SQLite database file
- Tables for sessions, messages, persons, and files
- Sample data for testing

### 3. Start the FastAPI Server

```bash
# Option 1: Using the startup script
python run_server.py

# Option 2: Using uvicorn directly
uvicorn email_assistant.backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at `http://localhost:8000`

### 4. Use the CLI

```bash
# From the repository root
python -m email_assistant help
python -m email_assistant session_create
python -m email_assistant session_chat --session_id <session_id> --content "Hello, how are you?"
python -m email_assistant session_delete --session_id <session_id>
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
python -m email_assistant session_create

# Chat with the assistant (replace abc123 with actual session ID)
python -m email_assistant session_chat --session_id abc123 --content "Hello, can you help me draft an email?"

# Edit a message in the session
python -m email_assistant session_edit --session_id abc123 --element_id 1 --content "Updated message content"

# Delete the session
python -m email_assistant session_delete --session_id abc123
```

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## Database Schema

### **Core Entities**

1. **Person** - Message sender and receiver
   - `id`: UUID primary key
   - `full_name`: Full name
   - `email_address`: Email address
   - `phone_number`: Phone number

2. **Session** - Email conversation session
   - `session_id`: UUID primary key
   - `summary`: Session summary text
   - `created_at`: Creation timestamp
   - `updated_at`: Last update timestamp

3. **Message** - Individual messages within a session
   - `message_id`: UUID primary key
   - `session_id`: Foreign key to Session
   - `sender_id`: Foreign key to Person (sender)
   - `receiver_id`: Foreign key to Person (receiver)
   - `message_text`: Message content
   - `created_at`: Creation timestamp

4. **MessageFile** - File attachments for messages
   - `id`: UUID primary key
   - `message_id`: Foreign key to Message
   - `file_path`: File path on disk
   - `file_content`: Parsed text content
   - `file_type`: File type (pdf, docx, txt, etc.)
   - `file_size`: File size

### **Relationships**
- One Session has many Messages
- One Message has many MessageFiles
- One Person can be sender/receiver of many Messages
- Cascade deletes ensure data integrity

## Key Benefits

1. **Unified Architecture**: CLI and backend use identical core functions
2. **Single Source of Truth**: All business logic is in one place
3. **Persistent Storage**: SQLite database for session and message persistence
4. **Easy Testing**: Core functions can be tested independently
5. **Consistent Behavior**: CLI and API behave identically
6. **Scalable**: Easy to add new LLM providers and workflows

## Roadmap

- Real LLM integration (Amazon Bedrock / Google Gemini)
- Email parsing (text/PDF) and structured extraction
- Draft reply generation and tone control
- Iterative refinement and saving drafts to file
- PostgreSQL/MySQL support for production
- File upload and parsing endpoints
