# Project Setup Templates

> **Load Time**: On-demand (~100 tokens)  
> **Purpose**: Ready-to-use templates for project initialization

---

## Thin Layer .junie/guidelines.md

Minimal local configuration pointing to global knowledge base:

```markdown
# Project Guidelines

## Project Info

- **Name**: [Project Name]
- **Type**: [Python Backend / Web Frontend / Data Analysis / etc.]
- **Language**: [Python 3.12 / TypeScript / etc.]

## Knowledge Base

This project uses AI Collaboration Knowledge Base.

- **Version**: 0.1.0
- **Load**: `sage get --scenario python_backend`

## Project-Specific Rules

### Naming Conventions

- [Any overrides to standard naming]

### File Organization

- [Project-specific structure notes]

### Dependencies

- [Key dependencies and version constraints]

### Testing

- [Project-specific test requirements]

## Autonomy Calibration

- **Default Level**: L4 (Medium-High)
- **Elevated for**: [routine tasks that can be L5+]
- **Lowered for**: [sensitive areas requiring L1-L2]

## Quick Commands

```bash
# Development
[dev command]

# Test
[test command]

# Build
[build command]
```

```

---

## Python Project Template

### pyproject.toml
```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "ruff>=0.1",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

### Directory Structure

```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── models/
│       ├── services/
│       └── api/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
├── .junie/
│   └── guidelines.md
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## README Template

```markdown
# Project Name

Brief description of the project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites

- Python 3.11+
- [Other requirements]

### Installation

```bash
pip install project-name
```

### Usage

```python
from project_name import main_function

result = main_function()
```

## Development

### Setup

```bash
git clone https://github.com/user/project-name
cd project-name
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

### Code Quality

```bash
ruff check .
mypy src/
```

## Documentation

See [docs/](docs/) for full documentation.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - see LICENSE file.

```

---

## .gitignore Template

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.tox/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.mypy_cache/

# Build
*.manifest
*.spec

# Local config
.env.local
*.local.yaml
secrets.yaml
```

---

## Docker Template

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source
COPY src/ src/

# Run
CMD ["python", "-m", "project_name"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## CI/CD Template (GitHub Actions)

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [ '3.11', '3.12' ]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"

      - name: Lint
        run: |
          ruff check .
          mypy src/

      - name: Test
        run: |
          pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Quick Setup Script

```bash
#!/bin/bash
# setup_project.sh - Initialize new project with AI Collab KB

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup_project.sh <project-name>"
    exit 1
fi

# Create structure
mkdir -p "$PROJECT_NAME"/{src/"$PROJECT_NAME",tests/{unit,integration},docs,.junie}

# Create files
touch "$PROJECT_NAME"/src/"$PROJECT_NAME"/__init__.py
touch "$PROJECT_NAME"/tests/conftest.py
touch "$PROJECT_NAME"/README.md
touch "$PROJECT_NAME"/.gitignore

# Create thin layer guidelines
cat > "$PROJECT_NAME"/.junie/guidelines.md << 'EOF'
# Project Guidelines

## Knowledge Base
Uses AI Collaboration Knowledge Base v2.0.0

## Project-Specific
[Add project-specific rules here]
EOF

echo "Project $PROJECT_NAME initialized!"
echo "Next: cd $PROJECT_NAME && sage get"
```

---

*Part of AI Collaboration Knowledge Base v2.0.0*
