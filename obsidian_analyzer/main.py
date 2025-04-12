import argparse
import asyncio
import logging
import os
import sys
import time

# Configure colored logging
class ColorFormatter(logging.Formatter):
    """Custom formatter with colored output"""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with colored formatter
ch = logging.StreamHandler()
ch.setFormatter(ColorFormatter())

# Create file handler
fh = logging.FileHandler('obsidian_analyzer.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add handlers
logger.addHandler(ch)
logger.addHandler(fh)
from itertools import combinations
from pathlib import Path
from dotenv import load_dotenv

from .config import GARDEN_DIR, OUTPUT_DIR
from . import file_handler
from .text_processor import TextProcessor, sanitize_filename
from .obsidian_generator import ObsidianGenerator

async def main():
    """Main entry point for the Obsidian Analyzer CLI.
    
    Handles:
    - Command line argument parsing
    - Text processing pipeline setup
    - Analysis execution
    - Results generation
    
    Example:
        $ obsidian-analyzer sample.md --langs en pt --out ./analysis_results
    """
    psr = argparse.ArgumentParser(description="Analyze text documents for philosophical concepts")
    from .config import GARDEN_DIR, OUTPUT_DIR
    psr.add_argument("input_file", help="File name relative to garden_of_afflictions directory")
    psr.add_argument("-o", "--out", default=OUTPUT_DIR, help="Output directory path") 
    psr.add_argument("--langs", nargs='+', default=['en'], choices=['en', 'pt'])
    psr.add_argument("--skip-pairs", action="store_true")
    psr.add_argument("--skip-multi", action="store_true")
    psr.add_argument("--skip-concepts", action="store_true")
    psr.add_argument("--skip-metrics", action="store_true")
    psr.add_argument("--skip-diagrams", action="store_true")
    psr.add_argument("--skip-ai", action="store_true")
    psr.add_argument("--max-pairs", type=int, default=8)
    
    args = psr.parse_args()
    
    text_processor = TextProcessor()
    if text_processor.llm is None:
        logger.error("LLM initialization failed")
        sys.exit(1)

    input_path = Path(args.input_file)
    if not input_path.is_absolute():
        # Try all possible locations
        possible_paths = [
            Path.cwd() / args.input_file,
            GARDEN_DIR / args.input_file,
            Path(__file__).parent.parent / args.input_file
        ]
        
        for path in possible_paths:
            if path.exists():
                input_path = path
                break
    
    if not input_path.exists():
        print(f"Input file not found: {args.input_file}")
        print("Searched in:")
        for path in possible_paths:
            print(f"  - {path}")
        return

    try:
        os.makedirs(args.out, exist_ok=True)
    except OSError as e:
        logger.error(f"Error creating output directory: {e}")
        return

    logger.info(f"Analyzing: {args.input_file}...")
    st = time.time()

    # Rest of analysis logic would go here...

    logger.info(f"Analysis completed in {time.time()-st:.2f}s")
    logger.info(f"Output saved to: {args.out}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
