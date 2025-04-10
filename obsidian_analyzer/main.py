import argparse
import asyncio
import logging
import os
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('obsidian_analyzer.log')
    ]
)
logger = logging.getLogger(__name__)
from itertools import combinations
from pathlib import Path
from dotenv import load_dotenv

from .config import GARDEN_DIR, OUTPUT_DIR
from . import file_handler
from .text_processor import TextProcessor, sanitize_filename
from .obsidian_generator import ObsidianGenerator

async def main():
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
        print("LLM initialization failed")
        sys.exit(1)

    if not os.path.isfile(os.path.join(GARDEN_DIR, args.input_file)):
        print(f"Input file not found: {args.input_file}")
        return

    try:
        os.makedirs(args.out, exist_ok=True)
    except OSError as e:
        print(f"Error creating output directory: {e}")
        return

    print(f"Analyzing: {args.input_file}...")
    st = time.time()

    # Rest of analysis logic would go here...

    print(f"Analysis completed in {time.time()-st:.2f}s")
    print(f"Output saved to: {args.out}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
