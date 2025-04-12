# Tone Analysis Prompt

## Purpose
Analyzes rhetorical style and philosophical tone in texts.

## Template Variables
- `{text}`: The input text to analyze
- `{lang}`: Language code (en/pt)
- `{options}`: Analysis options JSON

## Example Usage
```python
from obsidian_analyzer.prompt_loader import load_prompt

prompt = load_prompt("analyze_tone_en", {
    "text": sample_text,
    "lang": "en"
})
```

## Output Structure
```markdown
### Tone Assessment
**Dominant Tone**: [Descriptor]
**Key Features**: 
- [Feature]: [Example] → [Analysis]

### Rhetorical Map
```mermaid
flowchart TD
    A[Key Passage] --> B[Tone]
    A --> C[Devices]
```

### Recommendations
- For Students: [Tips]
- For Critics: [Approaches]
```

[View Full Prompt Template](../prompts/analyze_tone_en.md)
