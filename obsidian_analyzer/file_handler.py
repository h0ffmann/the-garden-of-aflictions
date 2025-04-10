import os
from pypdf import PdfReader

def read_file(file_path: str) -> str | None:
    """Read file from garden directory or absolute path"""
    from .config import GARDEN_DIR
    if not os.path.isabs(file_path):
        file_path = os.path.join(GARDEN_DIR, file_path)
    _, extension = os.path.splitext(file_path)
    content = ""
    try:
        if extension.lower() in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: 
                content = f.read()
        elif extension.lower() == '.pdf':
            reader = PdfReader(file_path)
            if reader.is_encrypted:
                try: 
                    reader.decrypt('')
                except:
                    print(f"Warn: Encrypted PDF failed decrypt.")
            content = "\n\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        else: 
            print(f"Error: Unsupported file type: {extension}")
            return None
        return content
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
