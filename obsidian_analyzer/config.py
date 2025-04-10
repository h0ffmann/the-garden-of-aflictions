from pathlib import Path
import os
from typing import List
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Base directories
    project_root: Path = Path(__file__).parent.parent
    garden_dir: Path = project_root / "garden_of_afflictions"
    output_dir: Path = project_root / "analysis_output"
    prompts_dir: Path = project_root / "prompts"
    
    # Analysis settings
    default_langs: List[str] = ["en", "pt"]
    max_concurrent_tasks: int = 5
    text_chunk_size: int = 4000
    text_chunk_overlap: int = 300
    max_entity_pairs: int = 8
    
    class Config:
        env_prefix = "obsidian_analyzer_"
        case_sensitive = False

# Initialize settings
settings = Settings()

# Ensure directories exist
os.makedirs(settings.garden_dir, exist_ok=True)
os.makedirs(settings.output_dir, exist_ok=True)
