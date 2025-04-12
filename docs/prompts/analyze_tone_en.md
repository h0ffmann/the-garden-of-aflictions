# Tone Analysis Prompt (English)

## Purpose
Analyze rhetorical style and tone in texts, with special attention to language-specific characteristics.

## Language Notes
- For English texts:
  - Note formality levels (academic, conversational, etc.)
  - Identify regional variations (US/UK/AU English)
  - Highlight rhetorical devices common in English
- For Portuguese texts:
  - Analyze use of informal pronouns (você/tu)
  - Note regional expressions and cultural references
  - Pay attention to levels of formality which may differ from English

## Template Variables
- `{text}`: The input text to analyze
- `{lang}`: Language code (en/pt)
- `{options}`: Analysis options JSON

## Example Usage
```python
from obsidian_analyzer.prompt_loader import load_prompt

prompt = load_prompt("analyze_tone_en", {
    "text": sample_text,
    "lang": "en"  # or "pt" for Portuguese
})
```

## Output Structure
```markdown
### Tone Assessment
**Dominant Tone**: [Descriptor]
**Language Characteristics**:
- Formality: [Level]
- Regional Features: [Notes]
- Cultural References: [If present]

### Key Features
- [Feature]: [Example] → [Analysis]
- [Language-specific observation]: [Details]

### Recommendations
- For Translation: [Notes on tone preservation]
- For Analysis: [Approaches for this language]
```

**Analysis Guidelines**:
1. First determine the base language and regional variety
2. Identify formal/informal markers specific to that language
3. Note any culture-specific references or idioms
4. Analyze how tone is created through language-specific devices
