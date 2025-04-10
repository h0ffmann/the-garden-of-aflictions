import os
from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Analysis settings
DEFAULT_LANGS = ["en", "pt"]
MAX_CONCURRENT_TASKS = 5
TEXT_CHUNK_SIZE = 4000
TEXT_CHUNK_OVERLAP = 300

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
import os
from pathlib import Path

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
GARDEN_DIR = PROJECT_ROOT / "garden_of_afflictions"
OUTPUT_DIR = PROJECT_ROOT / "analysis_output"
PROMPTS_DIR = PROJECT_ROOT / "prompts"

# Analysis settings
DEFAULT_LANGS = ["en", "pt"]
MAX_CONCURRENT_TASKS = 5
TEXT_CHUNK_SIZE = 4000  
TEXT_CHUNK_OVERLAP = 300

# Ensure directories exist
os.makedirs(GARDEN_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
