# Continuous Integration & Deployment

## Workflows

### test.yml
- Runs on: push & PR
- Python 3.10-3.12 matrix
- Steps:
  1. Install dependencies
  2. Run pytest suite
  3. Upload coverage

### docs.yml  
- Runs on: main branch
- Builds mkdocs site
- Deploys to GitHub Pages

## Configuration
- Poetry dependency management
- pytest configuration
- Coverage thresholds
- MkDocs material theme
