import pytest
from obsidian_analyzer import prompt_loader

class TestPromptLoader:
    def test_load_prompt_basic(self):
        """Test loading a basic prompt"""
        prompt = prompt_loader.load_prompt("analyze_tone_en")
        assert prompt is not None
        assert "Philosophical Tone Analysis Task" in prompt
        assert "{text}" in prompt

    def test_load_prompt_with_vars(self):
        """Test loading prompt with variable substitution"""
        prompt = prompt_loader.load_prompt("analyze_tone_en", {"text": "TEST_TEXT"})
        assert prompt is not None
        assert "TEST_TEXT" in prompt
        assert "{text}" not in prompt

    def test_load_nonexistent_prompt(self):
        """Test loading non-existent prompt"""
        prompt = prompt_loader.load_prompt("nonexistent_prompt")
        assert prompt is None

    def test_clear_cache(self):
        """Test prompt cache clearing"""
        # Load a prompt to populate cache
        prompt_loader.load_prompt("analyze_tone_en")
        assert "analyze_tone_en" in prompt_loader._prompt_cache
        
        prompt_loader.clear_prompt_cache()
        assert len(prompt_loader._prompt_cache) == 0
