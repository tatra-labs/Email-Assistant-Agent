from typing import List, Dict, Any
from .base import BaseLLM


class MockLLM(BaseLLM):
    """Mock LLM implementation for testing and development."""
    
    async def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a mock response."""
        if not messages:
            return "Hello! How can I help you today?"
        
        last_message = messages[-1]
        if last_message.get("role") == "user":
            return f"Mock response to: {last_message.get('content', '')}"
        
        return "I'm here to help! What would you like to know?"
    
    async def generate_structured_output(self, prompt: str, schema: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Generate mock structured output."""
        result = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                result[key] = await self.generate_structured_output(prompt, value, **kwargs)
            elif isinstance(value, list):
                result[key] = []
            else:
                result[key] = f"Mock_{key}"
        return result 