import pytest
import os
from dotenv import load_dotenv
from obsidian_analyzer import TextProcessor, ObsidianGenerator

load_dotenv()

@pytest.fixture(scope="module")
def text_processor():
    """Fixture providing initialized TextProcessor"""
    return TextProcessor()

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
