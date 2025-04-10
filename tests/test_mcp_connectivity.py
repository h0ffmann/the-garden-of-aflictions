import pytest
import httpx
import os
from obsidian_analyzer.config import settings

@pytest.fixture(scope="module")
def mcp_server():
    """Ensure MCP server is running for tests"""
    if not settings.mcp_enabled:
        pytest.skip("MCP testing disabled in config")
    
    # Check if server is running
    try:
        httpx.get(f"{settings.mcp_server_url}/health", timeout=1)
        return
    except httpx.ConnectError:
        pytest.skip("MCP server not running - run 'just install-mcp-server' first")
    
    # Check if server is already running
    try:
        httpx.get(f"{settings.mcp_server_url}/health", timeout=1)
        return
    except httpx.ConnectError:
        pass
    
    # Start server if not running
    os.system("just install-mcp-server")
    import time
    time.sleep(2)  # Give server time to start

@pytest.mark.asyncio
async def test_mcp_connectivity(mcp_server):
    """Test basic connectivity to MCP server"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.mcp_server_url}/health",
            timeout=settings.mcp_timeout
        )
        assert response.status_code == 200
