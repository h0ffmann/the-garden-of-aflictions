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

## Viewing Prompts

Prompt templates can be viewed directly in the documentation by clicking the "View Full Prompt Template" links. 

## Customization

1. Create `prompts/custom/` directory
2. Add modified prompt files with same names
3. Maintain required template variables
4. Keep Markdown formatting

Example directory structure:
```
prompts/
├── custom/
│   ├── analyze_tone_en.md
│   └── concepts_map_pt.md
└── original/
    ├── analyze_tone_en.md
    └── concepts_map_pt.md
```

## Template Variables

Common variables used across prompts:
- `{text}` - The input text to analyze
- `{lang}` - Language code (en/pt)
- `{options}` - Analysis options JSON
