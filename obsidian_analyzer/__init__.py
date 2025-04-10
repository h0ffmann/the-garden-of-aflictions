"""Obsidian Analyzer - Philosophical text analysis tool for Obsidian"""

from .main import main
from .core.text_processor import TextProcessor
from .core.obsidian_generator import ObsidianGenerator
from .utils.file_handler import read_file
from .utils.prompt_loader import load_prompt

__version__ = "0.1.0"
__all__ = [
    'main',
    'TextProcessor',
    'ObsidianGenerator', 
    'read_file',
    'load_prompt'
]
