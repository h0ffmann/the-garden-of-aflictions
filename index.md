# Obsidian Analyzer Documentation

Welcome to the Obsidian Analyzer documentation! This tool helps analyze philosophical texts and generate Obsidian vaults with structured notes.

## Key Features

- **Text Analysis**: Extract entities, concepts and relationships
- **LLM Integration**: Powered by Deepseek AI
- **Obsidian Output**: Generate ready-to-use markdown vaults
- **Multi-language Support**: Analyze texts in multiple languages

## Quick Start

1. Install dependencies:
```bash
just install
```

2. Analyze a text file:
```bash
just analyze file=your_text.md lang=en
```

3. View results in the generated Obsidian vault

## Documentation Sections

- [Getting Started](docs/getting_started.md) - Installation and first steps
- [Commands](docs/commands.md) - Complete command reference
- [Architecture](docs/architecture.md) - System design overview
- [Local Setup](docs/running_locally.md) - Development environment guide

> Note: Make sure to set your Deepseek API key in `.env` file
