from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_core.messages import BaseMessage


class BaseLLM(ABC):
    """Base interface for LLM providers."""
    
    @abstractmethod
    async def invoke(self, messages, **kwargs):
        """Generate a response from a list of messages."""
        pass
    
    @abstractmethod
    async def generate_structured_output(self, messages: List[List[BaseMessage]], schema: type[BaseModel], **kwargs) -> BaseModel:
        """Generate structured output matching a schema."""
        pass 

    @abstractmethod
    async def tool_call(self, messages, tools):
        """Call the necessary tools"""
        pass 

    @abstractmethod
    def return_tool_calling_model(self, tools) -> Any:
        """Return a model capable of tool calling"""
        pass