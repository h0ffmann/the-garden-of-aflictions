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

# Run tests (verbose with logs)
test:
    uv pip install -e ".[dev]"
    . .venv/bin/activate && pytest tests/ -v --log-level=INFO

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

# Run in development mode
dev:
    ${PYTHON} -m obsidian_analyzer.main test_data/sample_article.md -o analysis_output --langs en pt

# Export Rubem Alves subsection to Obsidian
export-alves output_dir="analysis_output":
    mkdir -p "{{output_dir}}"
    # Extract section using dedicated script
    @python -m obsidian_analyzer.extract_section \
        "ESSAY.md" \
        "{{output_dir}}/rubem_alves_ensaio.md" \
        "## Ensaio: O Jardim dos Espinhos Florescentes"
    # Run analysis with Portuguese only
    @python -m obsidian_analyzer.main \
        "{{output_dir}}/rubem_alves_ensaio.md" \
        -o "{{output_dir}}/rubem_alves_analysis" \
        --langs pt \
        --skip-multi \
        --skip-pairs
