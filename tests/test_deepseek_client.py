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

    # Simple math test with random number
    import random
    random_num = random.randint(1, 100)
    test_query = f"How much is 1+1? Then add {random_num} to that result and give just the final number."
    
    try:
        response = await client.ainvoke(test_query)
        print(f"\nDeepseek API Response: {response}")
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Verify the response contains the expected final number
        expected = 2 + random_num
        assert str(expected) in response, f"Expected {expected} not found in response: {response}"
    except Exception as e:
        pytest.fail(f"Client test failed: {str(e)}")
