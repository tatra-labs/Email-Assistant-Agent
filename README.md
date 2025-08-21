# Email-Assistant-Agent
A personal assistant AI agent to help with email intelligence

## Quickstart (CLI)

1. Ensure Python 3.9+ is installed.
2. Create and activate a virtual environment (recommended).
3. Run the CLI commands:

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

### Command Help

Each command provides its own help:

```bash
python -m email_assistant session_chat --help
python -m email_assistant session_edit --help
```

## Architecture

- **CLI Interface**: Command-line interface with 5 main commands using named arguments
- **Session Management**: Backend handles session creation, deletion, and message management
- **LLM Backend**: Pluggable backend system (currently dummy implementation)
- **Mock Implementation**: All backend functions are currently mocked for testing

## Roadmap

- Pluggable LLM backends (Amazon Bedrock / Google Gemini)
- Email parsing (text/PDF) and structured extraction
- Draft reply generation and tone control
- Iterative refinement and saving drafts to file
