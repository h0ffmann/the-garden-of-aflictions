from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def ainvoke(self, prompt: str) -> str:
        """Invoke the API with a single prompt and return the response"""
        pass
        
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Make a chat completion request"""
        pass
        
    @abstractmethod
    async def close(self):
        """Close any open resources"""
        pass
