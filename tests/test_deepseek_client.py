import pytest
import asyncio
from unittest.mock import patch
from obsidian_analyzer.deepseek_client import DeepseekClient

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_client_basic_query():
    """Test basic client functionality with a simple query"""
    # Require API key to be set
    import os
    if not os.getenv("DEEPSEEK_API_KEY"):
        pytest.fail("DEEPSEEK_API_KEY environment variable must be set for this test")

    client = DeepseekClient(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
        model=os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat"),
        temperature=0.2,
        timeout=30
    )

    # Simple test query
    test_query = "What time is it now? Just respond with the current time in HH:MM format."
    
    try:
        response = await client.ainvoke(test_query)
        print(f"\nDeepseek API Response: {response}")
        assert isinstance(response, str)
        assert len(response) > 0
        # Basic check for time format (HH:MM)
        assert ":" in response
    except Exception as e:
        pytest.fail(f"Client test failed: {str(e)}")
