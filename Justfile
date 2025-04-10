# Development tasks
install:
    pip install -r requirements.txt

run file="test_data/sample_article.md":
    python -m obsidian_analyzer.main {{file}} -o analysis_output

test:
    python -m pytest tests/

clean:
    rm -rf analysis_output/*
    rm -rf __pycache__

format:
    black obsidian_analyzer/
    isort obsidian_analyzer/

lint:
    flake8 obsidian_analyzer/
    mypy obsidian_analyzer/

setup-nltk:
    python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
