import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from pathlib import Path
from langchain_core.documents import Document

class TestTextProcessor:
    @pytest.mark.asyncio
    async def test_analyze_text_basic(self, text_processor):
        """Test basic text analysis functionality"""
        with patch('obsidian_analyzer.text_processor.TextProcessor.identify_entities_async', 
                 new_callable=AsyncMock) as mock_identify:
            mock_identify.return_value = ["Nietzsche", "Dostoevski"]
            
            results = await text_processor.analyze_text("test_data/sample_article.md", ["en"], {})
            
            assert isinstance(results, dict)
            assert "entities" in results
            assert "correlations" in results
            assert results["entities"] == ["Nietzsche", "Dostoevski"]
            mock_identify.assert_called_once()

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
        
        with patch.object(text_processor.llm, 'ainvoke', 
                         new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = "Nietzsche, Kierkegaard"
            entities = await text_processor.identify_entities_async(chunks)
            
            assert isinstance(entities, list)
            assert len(entities) == 2
            assert "Nietzsche" in entities
            assert "Kierkegaard" in entities

    def test_split_text(self, text_processor):
        """Test text splitting functionality"""
        # Test long text splitting
        long_text = " ".join(["Philosophy"] * 5000)
        chunks = text_processor.split_text(long_text)
        assert len(chunks) > 1
        assert all(len(chunk.page_content) <= 4000 for chunk in chunks)
        
        # Test short text
        short_text = "Short text"
        chunks = text_processor.split_text(short_text)
        assert len(chunks) == 1
        assert chunks[0].page_content == short_text

    @pytest.mark.asyncio
    async def test_llm_initialization(self, text_processor):
        """Test LLM initialization with env vars"""
        assert text_processor.llm is not None
        assert text_processor.llm.temperature == 0.2
        assert text_processor.llm.request_timeout == 120
