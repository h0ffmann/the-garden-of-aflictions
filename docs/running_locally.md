# Local Development Setup

## Quick Start
```bash
git clone https://github.com/your/repo
cd repo
poetry install
cp .env.example .env
# Edit .env with API keys
```

## Common Tasks

### Run Analysis
```bash
poetry run python -m obsidian_analyzer analyze input.md --lang en
```

### Start Dev Server
```bash
poetry run mkdocs serve
```

### Debugging
```bash
DEBUG=1 poetry run pytest -xvs
```

## Requirements
- Python 3.10+
- Poetry 1.6+
- Deepseek API key
