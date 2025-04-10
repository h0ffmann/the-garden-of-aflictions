import pytest
import httpx
from obsidian_analyzer.config import settings

@pytest.mark.asyncio
async def test_mcp_connectivity():
    """Test basic connectivity to MCP server"""
    if not settings.mcp_enabled:
        pytest.skip("MCP testing disabled in config")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.mcp_server_url}/health")
            response.raise_for_status()
            assert response.status_code == 200
    except httpx.ConnectError:
        pytest.fail("Failed to connect to MCP server - is it running?")
