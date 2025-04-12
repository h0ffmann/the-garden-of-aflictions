# Development Guide

## Setup
```bash
just init
```

## Workflow
- Write code in feature branches
- Run tests before committing:
```bash
just test
```
- Format code:
```bash
just format
```

## Documentation
Build locally:
```bash
just docs-serve
```

## Release Process
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Create release tag
