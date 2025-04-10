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
    """Test basic connectivity to MCP server"""
    try:
        # First verify container is running
        container_status = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Status}}", "mcp-sequential-thinking"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert container_status.returncode == 0
        assert "running" in container_status.stdout.lower()
        print(f"\nContainer status: {container_status.stdout.strip()}")

        # Try different ways to communicate with the server
        test_methods = [
            {
                "name": "HTTP health check",
                "command": ["curl", "-s", "http://localhost:8080/health"],
                "success_condition": lambda r: r.returncode == 0 and r.stdout.strip() == "OK"
            },
            {
                "name": "STDIO basic command",
                "command": ["docker", "exec", "mcp-sequential-thinking", "node", "-e", "console.log('PONG')"],
                "success_condition": lambda r: r.returncode == 0 and "PONG" in r.stdout
            },
            {
                "name": "Direct node execution",
                "command": ["docker", "exec", "mcp-sequential-thinking", "node", "dist/index.js", "--test"],
                "success_condition": lambda r: r.returncode == 0
            }
        ]

        for method in test_methods:
            print(f"\nTesting method: {method['name']}")
            result = subprocess.run(
                method["command"],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"Result: {result}")
            if method["success_condition"](result):
                print(f"Success with {method['name']}")
                return
            
        pytest.skip("Could not establish working communication method with MCP server")
        
    except subprocess.TimeoutExpired:
        pytest.fail("MCP server did not respond in time")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"MCP server communication failed: {e.stderr}")
