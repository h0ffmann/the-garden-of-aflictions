import pytest
import os
from unittest.mock import MagicMock
from dotenv import load_dotenv
from obsidian_analyzer import TextProcessor, ObsidianGenerator

load_dotenv()

@pytest.fixture(scope="module")
def mock_llm():
    """Fixture providing mock LLM"""
    llm = MagicMock()
    llm.ainvoke = MagicMock(return_value="Mocked response")
    return llm

@pytest.fixture(scope="module")
def text_processor(mock_llm):
    """Fixture providing initialized TextProcessor with mock LLM"""
    processor = TextProcessor()
    processor.llm = mock_llm
    return processor

@pytest.fixture(scope="module")
def obsidian_generator(text_processor):
    """Fixture providing initialized ObsidianGenerator"""
    return ObsidianGenerator(text_processor)

@pytest.fixture
def sample_md_text():
    """Fixture providing sample markdown text"""
    return """
# Sample Philosophical Text

This is a test text containing some philosophical concepts like:
- Nietzsche's will to power
- Kant's categorical imperative
- Descartes' cogito
"""

@pytest.fixture
def sample_analysis_results():
    """Fixture providing sample analysis results"""
    return {
        "source_file": "test.md",
        "entities": ["Nietzsche", "Kant"],
        "correlations": {
            "pairs": {"Nietzsche-Kant": "Contrast"},
            "multi": {"Modernity": ["Nietzsche", "Kant"]}
        },
        "key_concepts": {"Will to Power": "Nietzsche"},
        "metrics": {"complexity": 7.5},
        "diagrams": {"relations": "graph TD\nA[Nietzsche] --> B[Kant]"},
        "langs": ["en"]
    }
