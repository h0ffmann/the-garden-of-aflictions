from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator
import httpx
import json
from pydantic import BaseModel

class MCPRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 2000

class MCPResponse(BaseModel):
    text: str
    tokens_used: int

class MCPClient(LLMProvider):
    """MCP (Model Context Protocol) client implementation"""
    
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 60):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout
        )

    async def ainvoke(self, prompt: str) -> str:
        """Make a request to MCP server"""
        request = MCPRequest(
            prompt=prompt,
            model=self.model
        )
        response = await self.client.post(
            "/v1/completions",
            json=request.dict()
        )
        response.raise_for_status()
        return MCPResponse(**response.json()).text

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """MCP chat completion"""
        raise NotImplementedError("MCP doesn't support chat completions yet")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

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
