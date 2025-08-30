from typing import Optional, Dict, Any

from langchain.schema import HumanMessage
from langchain_core.messages import (
    RemoveMessage
)

import sqlite3 
from langgraph.checkpoint.sqlite import SqliteSaver 

from ...engine.agents.prompts import *
from ...engine.agents.sox_agent import SoxAgent 

conn = sqlite3.connect('checkpoints.sqlite', check_same_thread=False)
memory = SqliteSaver(conn)

class SoxChat:
    """Sox chat manager class.""" 
    def __init__(self, aisession_id: str):
        self.aisession_id = aisession_id
        self.agent = SoxAgent(
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            model_provider="aws",
            checkpointer=memory,
        )
    
    def initialize(self, session_info):
        """Initialize Sox chat."""
        initial_message = """
        My name is {full_name}. Here is information you can reference for the tasks.

        < Background > 
        I had a conversation using email with {contact_full_name}.

        Here is contact information of me and {contact_full_name}.

        My contact information:
        - Email: {user_email_address}
        - Phone: {user_phone_number}

        {contact_full_name}:
        - Email: {contact_email_address}
        - Phone: {contact_phone_number}

        Here is all of the conversation. 
        {conversation}
        </ Background >

        < Guideline >
        1. Do not call me by my name. You can call me friendly, maybe 'you' or 'your email', ...
        2. Be friendly. 
        </ Guideline >
        """.format(
            full_name=session_info["user_profile"]["full_name"],
            contact_full_name=session_info["contact_profile"]["full_name"],
            user_email_address=session_info["user_profile"]["email_address"],
            user_phone_number=session_info["user_profile"]["phone_number"],
            contact_email_address=session_info["contact_profile"]["email_address"],
            contact_phone_number=session_info["contact_profile"]["phone_number"],
            conversation=session_info["email_session"]
        )
        inputs = {
            "messages": [],
            "subject": session_info["subject"],
            "email_session": session_info["email_session"], 
            "user_profile": session_info["user_profile"],
            "contact_profile": session_info["contact_profile"],
        }
        config = {
            "configurable": {
                "thread_id": self.aisession_id,
            }
        }
        result = self.agent.invoke(
            input=inputs,
            config=config,
            context=None
        )
        # agent_state = self.agent.graph.get_state(config=config)  # type: ignore
        # remove_messages = []
        # for i in range(1, len(agent_state.values["messages"])):
        #     remove_messages.append(RemoveMessage(id=agent_state.values["messages"][i].id))
        self.agent.graph.update_state(
            config, # type: ignore
            {
                "messages": [
                    {"role": "user", "content": initial_message}
                ]
            }
        )
    
    def invoke_with_checkpointer(self, message, context):
        """Invoke Sox with a checkpointer."""
        inputs = {
            "messages": [
                HumanMessage(content=message)
            ],
        }
        config = {
            "configurable": {
                "thread_id": self.aisession_id,
            }
        }
        result = self.agent.invoke(
            input=inputs,
            config=config,
            context=context
        )
        return result["messages"][-1].content 
