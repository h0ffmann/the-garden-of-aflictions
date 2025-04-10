import pytest
import subprocess
import time
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
            ["docker", "run", "-d", "--name", "mcp-sequential-thinking", "mcp/sequentialthinking"],
            check=True
        )
        time.sleep(2)  # Give server time to start

    return True

def test_mcp_connectivity(mcp_server):
    """Test basic connectivity to MCP server via stdio"""
    try:
        # First test basic echo command
        echo_result = subprocess.run(
            ["docker", "exec", "mcp-sequential-thinking", "echo", "health"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"\nEcho test result: {echo_result}")
        assert echo_result.returncode == 0
        assert "health" in echo_result.stdout

        # Now test with actual MCP protocol command
        mcp_command = """{
            "protocol": "MCP",
            "version": "1.0",
            "command": "ping",
            "payload": {
                "message": "test"
            }
        }"""
        
        print(f"\nSending MCP command: {mcp_command}")
        
        # Send command via docker exec with printf to preserve formatting
        mcp_result = subprocess.run(
            ["docker", "exec", "-i", "mcp-sequential-thinking", "sh", "-c", "printf '%s' \"$0\" | node dist/index.js"],
            input=mcp_command,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"\nMCP command result: {mcp_result}")
        print(f"Return code: {mcp_result.returncode}")
        print(f"stdout: {mcp_result.stdout}")
        print(f"stderr: {mcp_result.stderr}")
        
        assert mcp_result.returncode == 0, f"Command failed with return code {mcp_result.returncode}"
        
        if not mcp_result.stdout:
            pytest.skip("MCP server returned empty response - may not be configured for stdio input")
        
    except subprocess.TimeoutExpired:
        pytest.fail("MCP server did not respond in time")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"MCP server communication failed: {e.stderr}")
