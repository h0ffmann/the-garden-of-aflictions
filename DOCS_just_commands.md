# Just Commands Cheat Sheet

## Development Workflow
```bash
just format   # Auto-format code
just lint     # Run linters
just types    # Check type hints
```

## Analysis Tasks
```bash
just analyze file=path lang=en  # Single file
just batch dir=path lang=pt    # Directory
just clean                    # Clear cache
```

## Testing
```bash
just test        # Run all tests
just test-cov    # With coverage
just test-fast   # Skip slow tests
```

## Documentation
```bash
just docs       # Build docs
just docs-serve # Live preview
```
