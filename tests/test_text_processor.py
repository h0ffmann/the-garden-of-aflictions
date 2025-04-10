import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from pathlib import Path
from langchain_core.documents import Document

class TestTextProcessor:
    @pytest.mark.asyncio
    async def test_analyze_text_basic(self, text_processor):
        """Test basic text analysis functionality"""
        with patch('obsidian_analyzer.file_handler.read_file', return_value="Test content"):
            results = await text_processor.analyze_text("test.md", ["en"], {})
            
            assert isinstance(results, dict)
            assert "entities" in results
            assert "correlations" in results
            assert isinstance(results["entities"], list)

    @pytest.mark.asyncio
    async def test_analyze_text_empty(self, text_processor):
        """Test analysis with empty input"""
        with patch('obsidian_analyzer.file_handler.read_file', return_value=""):
            results = await text_processor.analyze_text("empty.md", ["en"], {})
            assert results == {"error": "Failed to read file"}

    @pytest.mark.asyncio
    async def test_identify_entities(self, text_processor):
        """Test entity identification"""
        test_text = "Nietzsche's concept of eternal return contrasts with Kierkegaard's leap of faith."
        chunks = [Document(page_content=test_text)]
        
        entities = await text_processor.identify_entities_async(chunks)
        assert isinstance(entities, list)
        assert len(entities) > 0

    def test_split_text(self, text_processor):
        """Test text splitting functionality"""
        # Test long text splitting
        long_text = " ".join(["Philosophy"] * 5000)
        chunks = text_processor.split_text(long_text)
        assert len(chunks) > 1
        
        # Test short text
        short_text = "Short text"
        chunks = text_processor.split_text(short_text)
        assert len(chunks) == 1

    @pytest.mark.asyncio
    async def test_llm_initialization(self, text_processor):
        """Test LLM initialization with env vars"""
        assert text_processor.llm is not None
