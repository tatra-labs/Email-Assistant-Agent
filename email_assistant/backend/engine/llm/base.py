from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseLLM(ABC):
    """Base interface for LLM providers."""
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response from a list of messages."""
        pass
    
    @abstractmethod
    async def generate_structured_output(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate structured output matching a schema."""
        pass 