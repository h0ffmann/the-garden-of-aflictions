import pytest
import httpx
import os
import time
import subprocess
from obsidian_analyzer.config import settings

@pytest.fixture(scope="module")
def mcp_server():
    """Ensure MCP server is running for tests"""
    if not settings.mcp_enabled:
        pytest.skip("MCP testing disabled in config")

    # Check if container exists and is running
    container_running = False
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "mcp-sequential-thinking"],
            capture_output=True,
            text=True
        )
        container_running = result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        pass

    if not container_running:
        # Start fresh container
        subprocess.run(
            ["docker", "rm", "-f", "mcp-sequential-thinking"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["docker", "run", "-d", "-p", "8080:8080", "--name", "mcp-sequential-thinking", "mcp/sequentialthinking"],
            check=True
        )
        time.sleep(2)  # Give server time to start

    # Try connecting with retries and better error handling
    max_retries = 5
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = httpx.get(f"{settings.mcp_server_url}/health", timeout=2)
            if response.status_code == 200:
                return
            print(f"Unexpected status code: {response.status_code}")
        except httpx.HTTPError as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                pytest.skip(f"Could not connect to MCP server after {max_retries} attempts")
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
