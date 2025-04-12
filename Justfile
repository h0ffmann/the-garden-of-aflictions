# Development tasks using UV
VENV := ".venv"
PYTHON := "${VENV}/bin/python"

# Initialize project with UV
init:
    uv venv
    uv pip install -e ".[dev]"

# Install dependencies
install:
    uv pip install -e ".[dev]"

# Run the analyzer
run file="test_data/sample_article.md":
    ${PYTHON} -m obsidian_analyzer.main {{file}} -o analysis_output

# Run tests (verbose with logs)
test:
    uv pip install -e ".[dev]"
    uv test tests/ -v --log-level=INFO

# Run tests quietly (no logs)
test-quiet:
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest tests/ --log-level=CRITICAL

# Run tests with coverage (verbose)
test-cov:
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest tests/ --cov=obsidian_analyzer --cov-report=term-missing -v --log-level=INFO

# Run tests with coverage (quiet)
test-cov-quiet:
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest tests/ --cov=obsidian_analyzer --cov-report=term-missing --log-level=CRITICAL

# Run specific test file (verbose)
test-file file="tests/test_text_processor.py":
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest {{file}} -v --log-level=INFO

# Run specific test file (quiet)
test-file-quiet file="tests/test_text_processor.py":
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest {{file}} --log-level=CRITICAL

# Clean project
clean:
    rm -rf analysis_output/*
    rm -rf __pycache__
    rm -rf .mypy_cache
    rm -rf .pytest_cache

# Format code
format:
    black obsidian_analyzer/
    isort obsidian_analyzer/

# Lint code
lint:
    flake8 obsidian_analyzer/
    mypy obsidian_analyzer/
    ruff check obsidian_analyzer/

# Format code with ruff
ruff-format:
    ruff format obsidian_analyzer/

# Fix lint issues
ruff-fix:
    ruff check --fix obsidian_analyzer/

# Setup NLTK data
setup-nltk:
    ${PYTHON} -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Update dependencies
update:
    uv pip compile --upgrade
    uv pip sync

# Build documentation
docs:
    uv pip install -e ".[docs]"
    mkdocs build

# Serve documentation locally
docs-serve:
    uv pip install -e ".[docs]"
    mkdocs serve

# Run in development mode
dev:
    ${PYTHON} -m obsidian_analyzer.main test_data/sample_article.md -o analysis_output --langs en pt

# Print all implementation files (excluding prompts and markdown)
show-code:
    @echo "=== MAIN IMPLEMENTATION FILES ==="
    @find obsidian_analyzer -name "*.py" -not -path "*__pycache__*" -exec cat {} \;

# Export Rubem Alves subsection to Obsidian
export-alves output_dir="analysis_output":
    mkdir -p "{{output_dir}}"
    # Extract section using dedicated script
    @python -c "from obsidian_analyzer.extract_section import extract_section; from pathlib import Path; extract_section(Path('ESSAY.md'), Path('{{output_dir}}')/'rubem_alves_ensaio.md', '## Ensaio: O Jardim dos Espinhos Florescentes')" || exit 1
    # Verify extraction was successful
    @test -f "{{output_dir}}/rubem_alves_ensaio.md" || { echo "Failed to extract section"; exit 1; }
    # Run analysis with Portuguese only
    @python -m obsidian_analyzer.main \
        "{{output_dir}}/rubem_alves_ensaio.md" \
        -o "{{output_dir}}/rubem_alves_analysis" \
        --langs pt \
        --skip-multi \
        --skip-pairs
# MCP Server Management
install-mcp-server:
    # Pull and run the MCP Sequential Thinking server
    docker pull mcp/sequentialthinking:latest
    docker run -d -p 8080:8080 --name mcp-sequential-thinking mcp/sequentialthinking

stop-mcp-server:
    # Stop and remove the MCP server container
    docker stop mcp-sequential-thinking
    docker rm mcp-sequential-thinking

test-mcp-connectivity:
    # Test connectivity to MCP server using UV virtualenv
    uv pip install -e ".[dev]"
    OBSIDIAN_ANALYZER_MCP_ENABLED=true .venv/bin/pytest tests/test_mcp_connectivity.py -v --log-level=INFO

test-mcp-connectivity-quiet:
    # Test connectivity to MCP server quietly using UV virtualenv
    uv pip install -e ".[dev]"
    OBSIDIAN_ANALYZER_MCP_ENABLED=true .venv/bin/pytest tests/test_mcp_connectivity.py --log-level=CRITICAL

manual-test-mcp:
    # Manual test of MCP server
    @echo "Starting MCP server..."
    docker run -d -p 8080:8080 --name mcp-sequential-thinking mcp/sequentialthinking
    @echo "Waiting for server to start..."
    sleep 5
    @echo "Testing connection..."
    curl -X POST http://localhost:8080/v1/invoke \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer test-key" \
      -d '{"tool":"sequential_thinking","inputs":{"thought":"Test thought","nextThoughtNeeded":false,"thoughtNumber":1,"totalThoughts":1},"model":"sequential-thinking"}'
    @echo "\nStopping server..."
    docker stop mcp-sequential-thinking
    docker rm mcp-sequential-thinking
