# Prompt System Overview

The Obsidian Analyzer uses structured prompts to guide the LLM analysis. These markdown templates define the analysis frameworks.

## Core Prompts

### Tone Analysis (`analyze_tone_en.prompt`)
- Analyzes rhetorical style and philosophical tone
- Identifies linguistic patterns and devices
- Outputs structured assessment with examples

### Concept Mapping (`concepts_map_pt.prompt`)
- Portuguese-language concept analysis
- Maps conceptual relationships
- Provides historical context

### Metaphor Analysis (`metaphor_analysis_en.prompt`)  
- Identifies metaphorical structures
- Analyzes poetic elements
- Evaluates philosophical implications

## Customization

1. Create `prompts/custom/` directory
2. Add modified prompt files
3. Keep same naming convention
4. Maintain required template variables

## Template Variables

Common variables used across prompts:
- `{text}` - The input text to analyze
- `{lang}` - Language code (en/pt)
- `{options}` - Analysis options JSON
