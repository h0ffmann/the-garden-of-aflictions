# Tone Analysis Prompt (Multilingual)

## Purpose
Analyze rhetorical style and tone in texts, with special attention to language-specific characteristics.

## Supported Languages
- English (en)
- Portuguese (pt)

## Language-Specific Analysis
For each language, analyze:
1. **Formality Levels**:
   - English: academic, conversational, colloquial
   - Portuguese: formal/informal pronouns (você/tu), verb conjugations

2. **Regional Variations**:
   - English: US/UK/AU differences
   - Portuguese: PT-BR vs PT-PT differences

3. **Cultural References**:
   - Note any culture-specific idioms or references
   - For Portuguese: analyze use of diminutives and local expressions

4. **Rhetorical Devices**:
   - Language-specific rhetorical patterns
   - Common stylistic devices in each language

## Template Variables
- `{text}`: The input text to analyze
- `{lang}`: Language code (en/pt)
- `{options}`: Analysis options JSON

## Example Usage
```python
from obsidian_analyzer.prompt_loader import load_prompt

# For English analysis
prompt = load_prompt("analyze_tone_en", {
    "text": sample_text,
    "lang": "en"
})

# For Portuguese analysis (will automatically use English prompt with Portuguese guidance)
prompt = load_prompt("analyze_tone_pt", {
    "text": sample_text, 
    "lang": "pt"
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
