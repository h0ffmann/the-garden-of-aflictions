import re
from pathlib import Path
from typing import Dict, Optional
import markdown
from bs4 import BeautifulSoup

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
_prompt_cache: Dict[str, str] = {}

def load_prompt(prompt_name: str, variables: Dict[str, str] = None) -> Optional[str]:
    """
    Loads and formats a markdown prompt template from the /prompts directory.
    
    Args:
        prompt_name: Name of the prompt file (without .md extension)
        variables: Dictionary of template variables to interpolate
        
    Returns:
        Formatted markdown content or None if error occurs
    """
    if prompt_name in _prompt_cache:
        content = _prompt_cache[prompt_name]
    else:
        file_path = PROMPTS_DIR / f"{prompt_name}.md"
        try:
            if not file_path.is_file():
                raise FileNotFoundError(f"Markdown prompt not found: {file_path}")
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Validate basic markdown structure
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            if not soup.find():
                raise ValueError(f"Prompt {prompt_name} appears to be empty or invalid markdown")
                
            _prompt_cache[prompt_name] = content
            
        except Exception as e:
            print(f"Error loading prompt {prompt_name}: {e}")
            return None
    
    if variables:
        try:
            # Handle both {var} and {{var}} style templates
            content = re.sub(r'\{\{(\w+)\}\}', r'{\1}', content)
            formatted = content.format(**variables)
            
            # Revalidate after templating
            html = markdown.markdown(formatted)
            soup = BeautifulSoup(html, 'html.parser')
            if not soup.find():
                raise ValueError("Templating resulted in invalid markdown")
                
            return formatted
            
        except KeyError as e:
            print(f"Missing template variable {e} in prompt {prompt_name}")
        except Exception as e:
            print(f"Error formatting prompt {prompt_name}: {e}")
            
        return None
    
    return content

def clear_prompt_cache() -> None:
    """Clear the prompt cache."""
    _prompt_cache.clear()
