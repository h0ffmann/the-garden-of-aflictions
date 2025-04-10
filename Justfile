# Development tasks using UV
VENV := ".venv"
PYTHON := "${VENV}/bin/python"

# Initialize project with UV
init:
    uv venv
    uv pip install -e .

# Install dependencies
install:
    uv pip install -e ".[dev]"

# Run the analyzer
run file="test_data/sample_article.md":
    ${PYTHON} -m obsidian_analyzer.main {{file}} -o analysis_output

# Run tests
test:
    uv pip install -e ".[dev]"
    . ${VENV}/bin/activate && pytest tests/ -v

# Run tests with coverage
test-cov:
    uv pip install -e ".[dev]"
    . ${VENV}/bin/activate && pytest tests/ --cov=obsidian_analyzer --cov-report=term-missing

# Run specific test file
test-file file="tests/test_text_processor.py":
    uv pip install -e ".[dev]"
    . ${VENV}/bin/activate && pytest {{file}} -v

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

# Run in development mode
dev:
    ${PYTHON} -m obsidian_analyzer.main test_data/sample_article.md -o analysis_output --langs en pt
