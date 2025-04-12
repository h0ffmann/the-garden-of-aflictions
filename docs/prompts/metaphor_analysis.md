# Metaphor Analysis Prompt

## Purpose
Identifies and analyzes metaphorical structures in philosophical texts.

## Template Variables  
- `{text}`: Input text
- `{lang}`: Language code (en/pt)
- `{options}`: Analysis options

## Language-Specific Notes

### English (en)
- Focus on conceptual metaphors
- Note scientific/technological metaphors
- Analyze argumentative function

### Portuguese (pt)
- Include cultural/literary metaphors
- Note hybrid metaphors from Brazilian culture
- Consider oral tradition influences

## Example Usage
```python
prompt = load_prompt("metaphor_analysis", {
    "text": poetic_text,
    "lang": "en"  # or "pt"
})
```

## Output Structure
```markdown
### Key Metaphors  
```mermaid
flowchart LR
    S[Source] --> T[Target]
```

### Poetic Analysis
- [Device]: [Example] → [Effect]

### Evaluation
**Strengths**:
- [Conceptual clarity]
```
