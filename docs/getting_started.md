# Getting Started

## Installation
```bash
just install
```

## First Run
```bash
just analyze file=your_text.md lang=en
```

## Configuration
1. Copy `.env.example` to `.env`
2. Add your Deepseek API key
3. Configure any other settings

## Example Analysis
```bash
just analyze file=test_data/sample_article.md lang=en
```

## Customizing Prompts
To override default prompts:
1. Create a `prompts/custom/` directory
2. Add prompt files with same names as originals
3. The system will use your custom versions

Example custom prompt structure:
```markdown
# My Custom Analysis

**Objective:** {custom_instruction}

## Input Text:
```text
{text}
```

## My Custom Analysis Sections:
- {section1}
- {section2}
```
