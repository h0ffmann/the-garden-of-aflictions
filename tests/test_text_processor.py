import pytest
import asyncio
from pathlib import Path

class TestTextProcessor:
    @pytest.mark.asyncio
    async def test_analyze_text_basic(self, text_processor):
        """Test basic text analysis functionality"""
        test_text = "Nietzsche and Dostoevski discussed the death of God."
        chunks = text_processor.split_text(test_text)
        assert len(chunks) > 0
        
        results = await text_processor.analyze_text("test_data/sample_article.md", ["en"], {})
        assert isinstance(results, dict)
        assert "entities" in results
        assert "correlations" in results

    @pytest.mark.asyncio
    async def test_identify_entities(self, text_processor):
        """Test entity identification"""
        test_text = "Nietzsche's concept of eternal return contrasts with Kierkegaard's leap of faith."
        chunks = text_processor.split_text(test_text)
        entities = await text_processor.identify_entities_async(chunks)
        
        assert isinstance(entities, list)
        assert len(entities) >= 2  # Should at least find Nietzsche and Kierkegaard
        assert any("Nietzsche" in e for e in entities)
        assert any("Kierkegaard" in e for e in entities)

    def test_split_text(self, text_processor):
        """Test text splitting functionality"""
        long_text = " ".join(["Philosophy"] * 5000)  # Create long text
        chunks = text_processor.split_text(long_text)
        assert len(chunks) > 1  # Should be split into multiple chunks
        assert all(len(chunk.page_content) <= 4000 for chunk in chunks)  # Respect chunk size
