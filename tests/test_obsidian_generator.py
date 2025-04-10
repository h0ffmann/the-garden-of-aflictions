import pytest
import asyncio
import os
from pathlib import Path

import pytest
from unittest.mock import MagicMock

@pytest.fixture
def text_processor():
    processor = MagicMock()
    processor.llm = MagicMock()
    return processor

@pytest.fixture 
def obsidian_generator(text_processor):
    from obsidian_analyzer.obsidian_generator import ObsidianGenerator
    return ObsidianGenerator(text_processor)

class TestObsidianGenerator:
    @pytest.mark.asyncio
    async def test_generate_vault(self, obsidian_generator, text_processor, tmp_path):
        """Test vault generation functionality"""
        # Create test analysis results
        analysis_results = {
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

        # Generate vault to temporary directory
        output_dir = tmp_path / "test_vault"
        await obsidian_generator.generate_vault(analysis_results, str(output_dir))

        # Verify files were created
        expected_files = [
            "en/00 Index.md",
            "en/Metrics.md", 
            "en/Diagrams.md",
            "en/Concepts.md",
            "en/Multi-Correlations.md",
            "en/Nietzsche.md",
            "en/Kant.md"
        ]
        
        for file in expected_files:
            assert (output_dir / file).exists(), f"Expected file {file} not found"

    @pytest.mark.asyncio
    async def test_generate_lang_vault(self, obsidian_generator, tmp_path):
        """Test language-specific vault generation"""
        test_results = {
            "source_file": "test.md",
            "entities": ["TestEntity"],
            "langs": ["en"],
            "correlations": {"pairs": {}, "multi": {}},
            "key_concepts": {},
            "metrics": {},
            "diagrams": {}
        }
        output_dir = tmp_path / "lang_test"
        await obsidian_generator._generate_lang_vault("en", test_results, output_dir)
        
        assert (output_dir / "TestEntity.md").exists()
