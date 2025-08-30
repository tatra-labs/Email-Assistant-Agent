import os 
from dotenv import load_dotenv

from typing import Optional, Dict, Any


from ..database.aisession_service_db import AISessionService
from ..database.session_service_db import DatabaseSessionService
from ..database.person_service_db import DatabasePersonService 

from ..engine.agents.sox_chat import SoxChat 

class SessionService:
    """Service layer for session management and AI coordination using the database."""

    def __init__(self):
        self.ai_session_service = AISessionService()

    async def create_session(self, esession_id: str) -> str:
        """Create a new session using the database service."""
        aisession_id = self.ai_session_service.create_session(esession_id)

        # Fetch session info from email service 
        db_session_service = DatabaseSessionService() 
        session_info = db_session_service.get_session_info(esession_id) 

        _ = load_dotenv("../../../../.env")
        self_user_id = os.getenv("SELF_USER_ID")

        session_info = sanitize_session_info(session_info, self_user_id)

        # Invoke Sox - email assistant agent initially
        sox_chat = SoxChat(
            aisession_id=aisession_id,
        ) 
        sox_chat.initialize(session_info) 

        return aisession_id

    def chat_with_sox(self, aisession_id: str, message: str, context: Optional[Dict[str, Any]] = None):
        """Chat with Sox using the database service."""
        ai_session = self.ai_session_service.get_session(aisession_id)
        esession_id = str(ai_session.esession_id)
        
        # Fetch session info from email service 
        db_session_service = DatabaseSessionService() 
        session_info = db_session_service.get_session_info(esession_id) 

        # session_info = sanitize_session_info(session_info)

        sox_chat = SoxChat(
            aisession_id=aisession_id,
        ) 
        response = sox_chat.invoke_with_checkpointer(message, context) 
        
        return response
    
def sanitize_session_info(session_info, self_user_id):
    """Sanitize session info.""" 
    def message_template(msg) -> str:
        result = ""
        result += "From: " + msg["from"]
        result += "\nTo: " + msg["to"] 
        result += "\nMessage: " + msg["message_text"] 
        if msg["file_text"]:
            result += "\nAttached File: \n" + msg["file_text"]
        return result

    db_person_service = DatabasePersonService()

    sanitized_session_info = {
        "subject": session_info["subject"],
    }

    sender = db_person_service.seek_person_by_id(session_info["sender_id"]) 
    receiver = db_person_service.seek_person_by_id(session_info["receiver_id"])

    users = {}
    if session_info["sender_id"] == self_user_id:
        users["sender"] = "user_profile"
        users["receiver"] = "contact_profile"
    else:
        users["sender"] = "contact_profile"
        users["receiver"] = "user_profile"

    person_data = {
        session_info["sender_id"]: {
            "full_name": sender.full_name,
            "email_address": sender.email_address,
            "phone_number": sender.phone_number,
        },
        session_info["receiver_id"]: {
            "full_name": receiver.full_name,
            "email_address": receiver.email_address,
            "phone_number": receiver.phone_number,
        }
    }

    sanitized_messages = [
        {
            "from": person_data[msg["sender_id"]]["full_name"],
            "to": person_data[msg["receiver_id"]]["full_name"],
            "message_text": msg["message_text"],
            "file_text": msg["file_text"] if msg["file_text"] else "",
        } for msg in session_info["messages"]
    ]

    sanitized_session_info = {
        **sanitized_session_info,
        users["sender"]: {
            "full_name": sender.full_name,
            "email_address": sender.email_address,
            "phone_number": sender.phone_number,
        },
        users["receiver"]: {
            "full_name": receiver.full_name,
            "email_address": receiver.email_address,
            "phone_number": receiver.phone_number,
        },
        "messages": sanitized_messages,
    }

    email_session="\n\n".join([message_template(msg) for msg in sanitized_messages])

    sanitized_session_info["email_session"] = email_session

    return sanitized_session_info