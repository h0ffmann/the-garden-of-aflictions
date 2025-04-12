# API Reference

## Core Modules

### TextProcessor
```python
class TextProcessor:
    async def analyze_text(file_path: str, langs: List[str], options: Dict) -> Dict
    async def identify_entities_async(chunks: List[Document]) -> List[str]
```

### ObsidianGenerator
```python
class ObsidianGenerator:
    async def generate_vault(analysis_results: Dict, output_dir: str) -> None
```

### LLMProvider
```python
class LLMProvider(ABC):
    async def ainvoke(prompt: str) -> str
    async def chat_completion(messages: List[Dict[str, str]], stream: bool) -> str
```

### Prompt System
```python
def load_prompt(prompt_name: str, variables: Dict[str, str] = None) -> str | None
def clear_prompt_cache() -> None
```

**Prompt Files**:
- Located in `prompts/` directory
- Format: Markdown with template variables like `{text}`
- Types:
  - `analyze_tone_en.prompt` - Tone/style analysis
  - `concepts_map_pt.prompt` - Portuguese concept mapping  
  - `metaphor_analysis_en.prompt` - Metaphor/poetic analysis

**Usage**:
```python
from obsidian_analyzer.prompt_loader import load_prompt

# Load and format a prompt
prompt = load_prompt("analyze_tone_en", {"text": sample_text})
```
