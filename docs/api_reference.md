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
