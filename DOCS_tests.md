# Testing Guide

## Test Types
- Unit: Isolated components
- Integration: LLM interactions  
- E2E: Full analysis pipeline

## Running Tests
```bash
# Complete suite
pytest tests/

# Specific module
pytest tests/test_text_processor.py -v

# With coverage
pytest --cov --cov-report=term-missing
```

## Test Data
Location: `test_data/`
- `sample_article.md` - Markdown content
- `sample_romance.txt` - Fiction text
- `sample_article.txt` - Technical writing

## Writing Tests
Follow existing patterns in:
- `test_text_processor.py`
- `test_obsidian_generator.py`
