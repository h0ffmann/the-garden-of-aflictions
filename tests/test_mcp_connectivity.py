import pytest
import httpx
import os
import time
from obsidian_analyzer.config import settings

@pytest.fixture(scope="module")
def mcp_server():
    """Ensure MCP server is running for tests"""
    if not settings.mcp_enabled:
        pytest.skip("MCP testing disabled in config")

    # Try connecting with retries
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            httpx.get(f"{settings.mcp_server_url}/health", timeout=1)
            return  # Server is running
        except httpx.ConnectError:
            if attempt == max_retries - 1:
                # Last attempt failed, try starting the server
                try:
                    os.system("docker start mcp-sequential-thinking")
                    time.sleep(2)  # Give server time to start
                    httpx.get(f"{settings.mcp_server_url}/health", timeout=1)
                    return
                except httpx.ConnectError:
                    pytest.skip("MCP server not running - run 'just install-mcp-server' first")
            time.sleep(retry_delay)

@pytest.mark.asyncio
async def test_mcp_connectivity(mcp_server):
    """Test basic connectivity to MCP server"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.mcp_server_url}/health",
            timeout=settings.mcp_timeout
        )
        assert response.status_code == 200
