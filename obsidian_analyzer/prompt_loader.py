import os
import re
from pathlib import Path
from typing import Dict

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
_prompt_cache: Dict[str, str] = {}

def load_prompt(prompt_name: str, variables: Dict[str, str] = None) -> str | None:
    """Loads and formats a prompt template from the /prompts directory."""
    if prompt_name in _prompt_cache:
        content = _prompt_cache[prompt_name]
    else:
        file_path = PROMPTS_DIR / f"{prompt_name}.prompt"
        try:
            if not file_path.is_file():
                raise FileNotFoundError(f"Prompt file not found: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            _prompt_cache[prompt_name] = content
        except Exception as e:
            print(f"Error loading prompt {prompt_name}: {e}")
            return None
    
    if variables:
        # Handle both {var} and {{var}} style templates
        content = re.sub(r'\{\{(\w+)\}\}', r'{\1}', content)  # Convert {{var}} to {var}
        try:
            return content.format(**variables)
        except KeyError as e:
            print(f"Missing variable {e} in prompt {prompt_name}")
            return None
    
    return content

def clear_prompt_cache() -> None:
    """Clear the prompt cache."""
    _prompt_cache.clear()
