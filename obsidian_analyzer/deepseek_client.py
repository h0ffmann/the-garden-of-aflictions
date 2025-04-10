import os
import httpx
from typing import Optional, Dict, Any, AsyncGenerator
import json

class DeepseekClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.deepseek.com/v1",
        model: str = "deepseek-chat",
        temperature: float = 0.2,
        timeout: int = 120
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=timeout
        )

    async def chat_completion(
        self,
        messages: list[Dict[str, str]],
        stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Make a chat completion request to Deepseek API"""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": stream
        }

        async with self.client as client:
            if stream:
                async with client.stream(
                    "POST",
                    "/chat/completions",
                    json=payload
                ) as response:
                    async for chunk in response.aiter_lines():
                        if chunk.startswith("data:"):
                            data = chunk[5:].strip()
                            if data == "[DONE]":
                                break
                            yield json.loads(data)
            else:
                response = await client.post(
                    "/chat/completions",
                    json=payload
                )
                response.raise_for_status()
                yield response.json()

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
