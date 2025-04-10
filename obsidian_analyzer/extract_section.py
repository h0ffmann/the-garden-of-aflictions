import re
import sys
from pathlib import Path

def extract_section(input_file: Path, output_file: Path, start_marker: str, end_marker: str = "^---"):
    """Extract a section between markers and save to output file"""
    try:
        content = input_file.read_text(encoding='utf-8')
        pattern = fr"{re.escape(start_marker)}.*?(?={end_marker})"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        
        if match:
            output_file.write_text(match.group(0), encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error extracting section: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: extract_section.py <input_file> <output_file> <start_marker>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    start_marker = sys.argv[3]
    
    if not extract_section(input_path, output_path, start_marker):
        print(f"Section not found starting with: {start_marker}")
        sys.exit(1)
