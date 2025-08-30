from typing import Literal, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

from langchain_core.messages import AnyMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, InjectedState
from langgraph.graph import (
    add_messages,
    StateGraph, 
    START, 
    END
)
from langgraph.types import Command

from ..llm.aws_llm import AWS_LLM
from ..agents.prompts import *

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    subject: str
    email_session: str 
    user_profile: dict
    contact_profile: dict 

class Router(BaseModel):
    result: Literal["SUMMARIZE", "MAIN"] = Field(..., description="Result from triage model")

class SoxAgent:
    def __init__(self, 
            model_provider: Literal["aws","gcp"],
            model_id: str,
            checkpointer,
        ):
        if model_provider == "aws":
            self.llm = AWS_LLM(model_id=model_id)
        self.context = None
        self.tools = [write_reply_to_file]
        self.toolkit={
            "write_reply_to_file": write_reply_to_file
        }
        self.tool_node = ToolNode(self.tools)

        workflow = StateGraph(AgentState) 
        workflow.add_node("triage_node", self.triage_func)
        workflow.add_node("main_node", self.main_func)
        workflow.add_node("summarizer_node", self.summarizer_func)
        workflow.add_node("tool_node", self.tool_node)

        workflow.add_edge(START, "triage_node")
        workflow.add_edge("tool_node", "main_node")
        workflow.add_edge("summarizer_node", END)
        workflow.add_conditional_edges(
            "main_node", self.exists_action, {True: "tool_node", False: END}
        )

        self.graph = workflow.compile(checkpointer)

    def triage_func(self, state: AgentState) -> Command[
        Literal["main_node", "summarizer_node"]
    ]:
        # Call triage model to determine next steps
        messages = state["messages"]
        goto = "main_node" 
        update = None

        system_prompt = sox_triage_system_prompt_template.format(
            full_name=state["user_profile"]["full_name"],
            contact_full_name=state["contact_profile"]["full_name"],
            conversation=state["email_session"]
        )
        llm_router = self.llm.with_structured_output(Router) # type: ignore 
        resposne = llm_router.invoke(
            [
                {"role": "user", "content": system_prompt},
                *messages
            ]
        )
        if resposne.result == "SUMMARIZE":  # type: ignore
            goto = "summarizer_node"
        elif resposne.result == "MAIN": # type: ignore
            goto = "main_node"
        else:
            raise ValueError(f"Unexpected triage result: {resposne.result}") # type: ignore

        return Command(goto=goto, update=update)

    def main_func(self, state: AgentState):
        messages = state["messages"]
        system_prompt = sox_main_system_prompt_template.format(
            full_name=state["user_profile"]["full_name"],
            contact_full_name=state["contact_profile"]["full_name"],
            user_email_address=state["user_profile"]["email_address"],
            user_phone_number=state["user_profile"]["phone_number"],
            contact_email_address=state["contact_profile"]["email_address"],
            contact_phone_number=state["contact_profile"]["phone_number"],
            conversation=state["email_session"]
        ) 
        message = self.llm.bind_tools(self.tools).invoke( # type: ignore
            [
                {"role": "user", "content": system_prompt},
                *messages
            ]
        )
        return {
            "messages": [message]
        }
    
    def exists_action(self, state: AgentState) -> bool:
        try:
            result = state["messages"][-1]
            return len(result.tool_calls) > 0 # type: ignore
        except:
            return False
        
    def summarizer_func(self, state: AgentState):
        messages = state["messages"]
        system_prompt = sox_summarizer_system_prompt
        if self.context:
            system_prompt += context_prompt_template.format(context=str(self.context))
        message = self.llm.invoke( # type: ignore
            [
                {"role": "user", "content": system_prompt},
                *messages
            ]
        )
        return {
            "messages": [message]
        }

    def tool_func(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls # type: ignore 
        results = []
        for t in tool_calls:
            print(f"Calling tool: {t['name']} with args: {t['args']}") 
            if not t["name"] in self.toolkit:
                print("\n ... Tool not found! Skipping ... \n") 
                result = "bad tool name, retry"
            else:
                t["args"]["state"] = state
                result = self.toolkit[t["name"]].invoke(t["args"]) 

            # results.append({
            #     "type": "tool_result",
            #     "tool_use_id": t["id"],
            #     "content": result
            # })
            results.append(AIMessage(content=result, tool_call_id=t["id"]))
        print("Back to main node!") 
        return {
            "messages": results
        }
    
    
    def invoke(self, input, config, context):
        self.context = context
        result = self.graph.invoke(
            input=input,
            config=config,
        )
        return result

@tool
def write_reply_to_file(state: Annotated[dict, InjectedState], content: str) -> str:
    """
    Write the email content to the file.

    Args:
    from_user: My email address
    to_user: Email address I'm currently writing to 
    subject: Subject of the conversation
    content: Draft of reply
    """
    try:
        message = "From: {from_user} \n\nTo: {to_user} \n\nSubject: {subject} \n\nContent: \n\n{content}".format(
            from_user=state["user_profile"]["email_address"],
            to_user=state["contact_profile"]["email_address"],
            subject=state["subject"],
            content=content
        )
        with open("draft.txt", 'w') as f:
            f.write(message) 

        return "Successfully wrote a reply to a file!\n\nHere is email content.\n\n" + message
    except:
        return "Failed to write a reply to a file!"