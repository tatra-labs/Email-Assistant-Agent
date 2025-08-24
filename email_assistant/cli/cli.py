from __future__ import annotations

import argparse
import sys
from typing import Optional

from .session import ChatSession
from .backends import get_backend


HELP_MESSAGE = """
Email Assistant Agent - CLI Commands

Available commands:
1. help                    - Show this help message
2. session_create          - Create a new session and return session ID
3. session_delete <id>     - Delete session with given ID
4. session_edit <id> <msg_id> <content> - Edit message in session
5. session_chat <id> <content> - Add message to session and get response

Examples:
  python -m email_assistant help
  python -m email_assistant session_create
  python -m email_assistant session_delete --session_id abc123
  python -m email_assistant session_edit --session_id abc123 --element_id 1 --content "Updated content"
  python -m email_assistant session_chat --session_id abc123 --content "Hello"
"""


def handle_help() -> int:
    """Display help message."""
    print(HELP_MESSAGE)
    return 0


def handle_session_create() -> int:
    """Create a new session and return session ID."""
    try:
        backend = get_backend()
        session_id = backend.session_create()
        print(f"Session created successfully. Session ID: {session_id}")
        return 0
    except Exception as e:
        print(f"Error creating session: {e}")
        return 1


def handle_session_delete(session_id: str, backend_name: str = "fastapi") -> int:
    """Delete session with given ID."""
    if not session_id:
        print("Error: session_id is required")
        return 1
    
    try:
        backend = get_backend()
        success = backend.session_delete(session_id)
        if success:
            print(f"Session {session_id} deleted successfully")
            return 0
        else:
            print(f"Session {session_id} not found or could not be deleted")
            return 1
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        return 1


def handle_session_edit(session_id: str, message_id: str, message_content: str, backend_name: str = "fastapi") -> int:
    """Edit message in session."""
    if not session_id or not message_id or not message_content:
        print("Error: session_id, message_id, and message_content are required")
        return 1
    
    try:
        backend = get_backend()
        success = backend.session_edit(session_id, message_id, message_content)
        if success:
            print(f"Message {message_id} in session {session_id} edited successfully")
            return 0
        else:
            print(f"Failed to edit message {message_id} in session {session_id}")
            return 1
    except Exception as e:
        print(f"Error editing message {message_id} in session {session_id}: {e}")
        return 1


def handle_session_chat(session_id: str, message_content: str, backend_name: str = "fastapi") -> int:
    """Add message to session and get response."""
    if not session_id or not message_content:
        print("Error: session_id and message_content are required")
        return 1
    
    try:
        backend = get_backend()
        response = backend.session_chat(session_id, message_content)
        print(f"Message added to session {session_id} successfully")
        print(f"Response: {response}")
        return 0
    except Exception as e:
        print(f"Error processing message in session {session_id}: {e}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="email-assistant",
        description="Email Assistant Agent CLI",
        add_help=False  # We'll handle help ourselves
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show help message")
    
    # Session create command
    create_parser = subparsers.add_parser("session_create", help="Create a new session")
    
    # Session delete command
    delete_parser = subparsers.add_parser("session_delete", help="Delete a session")
    delete_parser.add_argument("--session_id", required=True, help="Session ID to delete")
    
    # Session edit command
    edit_parser = subparsers.add_parser("session_edit", help="Edit a message in a session")
    edit_parser.add_argument("--session_id", required=True, help="Session ID")
    edit_parser.add_argument("--element_id", required=True, help="Message ID to edit")
    edit_parser.add_argument("--content", required=True, help="New message content")
    
    # Session chat command
    chat_parser = subparsers.add_parser("session_chat", help="Add message to session and get response")
    chat_parser.add_argument("--session_id", required=True, help="Session ID")
    chat_parser.add_argument("--content", required=True, help="Message content")
    
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    
    command = args.command or "help"
    
    if command == "help":
        sys.exit(handle_help())
    elif command == "session_create":
        sys.exit(handle_session_create())
    elif command == "session_delete":
        sys.exit(handle_session_delete(args.session_id))
    elif command == "session_edit":
        sys.exit(handle_session_edit(args.session_id, args.element_id, args.content))
    elif command == "session_chat":
        sys.exit(handle_session_chat(args.session_id, args.content))
    else:
        print(f"Unknown command: {command}")
        print("Use 'help' command to see available commands")
        sys.exit(1) 