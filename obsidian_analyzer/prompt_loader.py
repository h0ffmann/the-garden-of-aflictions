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
        # Handle language codes - don't modify names with valid language suffixes
        parts = prompt_name.split('_')
        if len(parts) > 1 and parts[-1] in ('en', 'pt'):  # Valid language code
            prompt_name = prompt_name  # Keep as-is
            
        # Try possible filename variations
        possible_paths = []
        
        # First try exact name
        possible_paths.append(PROMPTS_DIR / f"{prompt_name}.md")
        
        # If name has a language code, try without it
        parts = prompt_name.split('_')
        if len(parts) > 1 and parts[-1] in ('en', 'pt'):
            possible_paths.append(PROMPTS_DIR / f"{'_'.join(parts[:-1])}.md")
        
        file_path = None
        for path in possible_paths:
            if path.is_file():
                file_path = path
                break
                
        if not file_path:
            raise FileNotFoundError(
                f"Prompt file not found for: {prompt_name}\n"
                f"Tried paths:\n- " + "\n- ".join(str(p) for p in possible_paths)
            )
        
        try:
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
            
            # Validate required variables
            required_vars = re.findall(r'\{(\w+)\}', content)
            for var in required_vars:
                if var not in variables:
                    raise ValueError(f"Missing required template variable '{var}' in prompt {prompt_name}")
            
            # Provide defaults for optional variables
            safe_vars = {
                'options': variables.get('options', '{}'),
                'lang': variables.get('lang', 'en'),
                'entities': variables.get('entities', '[]'),
                **variables
            }
                
            try:
                formatted = content.format(**safe_vars)
            except KeyError as e:
                print(f"Missing required template variable {e} in prompt {prompt_name}")
                return None
                
            # Revalidate after templating
            html = markdown.markdown(formatted)
            soup = BeautifulSoup(html, 'html.parser')
            if not soup.find():
                raise ValueError("Templating resulted in invalid markdown")
                
            return formatted
        except Exception as e:
            print(f"Error formatting prompt {prompt_name}: {e}")
            return None
            
    return content
    
    return content

def clear_prompt_cache() -> None:
    """Clear the prompt cache."""
    _prompt_cache.clear()
