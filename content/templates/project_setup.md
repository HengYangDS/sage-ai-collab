# Project Setup Templates

> Ready-to-use templates for project initialization

---

## Table of Contents

[1. Template Overview](#1-template-overview) · [2. Thin Layer](#2-thin-layer-junieguidelines-md) · [3. Python Project](#3-python-project) · [4. README Template](#4-readme-template) · [5. .gitignore Template](#5-gitignore-template) · [6. Docker Template](#6-docker-template) · [7. CI/CD Template](#7-cicd-template) · [8. Quick Setup Script](#8-quick-setup-script)

---

## 1. Template Overview

| Template                                     | Purpose               | Lines |
|----------------------------------------------|-----------------------|-------|
| [Thin Layer](#thin-layer-junieguidelines-md) | Minimal local config  | ~20   |
| [pyproject.toml](#python-project)            | Python project config | ~15   |
| [README](#readme-template)                   | Project documentation | ~25   |
| [.gitignore](#gitignore-template)            | Git ignore patterns   | ~15   |
| [Docker](#docker-template)                   | Containerization      | ~20   |
| [CI/CD](#cicd-template)                      | GitHub Actions        | ~20   |

---

## 2. Thin Layer .junie/guidelines.md

```markdown
# Project Guidelines

**Name**: [Project Name] | **Type**: [Python Backend/Web/etc.] | **Language**: [Python 3.12/etc.]

## Knowledge Base

Uses AI Collaboration KB v0.1.0 — Load: `sage get --scenario python_backend`

## Project-Specific

- Naming: [overrides if any]
- Structure: [notes if any]
- Dependencies: [key constraints]

## Autonomy

Default: L4 | Elevated: [routine tasks → L5] | Lowered: [sensitive areas → L1-L2]

## Commands

`[dev cmd]` · `[test cmd]` · `[build cmd]`
```

---

## 3. Python Project

### 3.1 pyproject.toml

```toml
[project]
name = "project-name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pydantic>=2.0", "httpx>=0.24"]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov>=4.0", "mypy>=1.0", "ruff>=0.1"]

[tool.ruff]
line-length = 88

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

### 3.2 Directory Structure

| Path                   | Purpose                                       |
|------------------------|-----------------------------------------------|
| `src/project_name/`    | Source code (models/, services/, api/)        |
| `tests/`               | Test suite (unit/, integration/, conftest.py) |
| `docs/`                | Documentation                                 |
| `.junie/guidelines.md` | AI collaboration config                       |
| `pyproject.toml`       | Project config                                |

---

## 4. README Template

```markdown
# Project Name

Brief description.

## Quick Start

`pip install project-name`

```python
from project_name import main_function
result = main_function()
```

## Development

`git clone <url> && cd project-name && pip install -e ".[dev]"`

**Test**: `pytest` | **Lint**: `ruff check . && mypy src/`

## Contributing

Fork → Branch → Changes + Tests → PR

## License

MIT

```

---

## 5. .gitignore Template

```gitignore
# Python
__pycache__/ | *.py[cod] | *.egg-info/ | dist/ | build/ | .eggs/

# Virtual env
.env | .venv | venv/

# IDE
.idea/ | .vscode/ | *.swp

# Testing
.coverage | htmlcov/ | .pytest_cache/ | .mypy_cache/

# Local
.env.local | *.local.yaml | secrets.yaml
```

---

## 6. Docker Template

### 6.1 Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY src/ src/
CMD ["python", "-m", "project_name"]
```

### 6.2 docker-compose.yml

```yaml
services:
  app:
    build: .
    ports: [ "8000:8000" ]
    environment: [ DATABASE_URL=postgresql://user:pass@db:5432/dbname ]
    depends_on: [ db ]
  db:
    image: postgres:15
    environment: [ POSTGRES_USER=user, POSTGRES_PASSWORD=pass, POSTGRES_DB=dbname ]
    volumes: [ postgres_data:/var/lib/postgresql/data ]
volumes:
  postgres_data:
```

---

## 7. CI/CD Template

### 7.1 .github/workflows/ci.yml

```yaml
name: CI
on:
  push: { branches: [ main, develop ] }
  pull_request: { branches: [ main ] }

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { python-version: [ '3.11', '3.12' ] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '${{ matrix.python-version }}' }
      - run: pip install -e ".[dev]"
      - run: ruff check . && mypy src/
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## 8. Quick Setup Script

```bash
#!/bin/bash
# Usage: ./setup_project.sh <project-name>
PROJECT=$1
[[ -z "$PROJECT" ]] && echo "Usage: ./setup_project.sh <name>" && exit 1
mkdir -p "$PROJECT"/{src/"$PROJECT",tests/{unit,integration},docs,.junie}
touch "$PROJECT"/{src/"$PROJECT"/__init__.py,tests/conftest.py,README.md,.gitignore}
echo "# Guidelines\nUses AI Collaboration KB v0.1.0" > "$PROJECT"/.junie/guidelines.md
echo "Created $PROJECT! Next: cd $PROJECT && sage get"
```

---

## Related

- `content/scenarios/python_backend/context.md` — Python backend context
- `content/guidelines/python.md` — Python guidelines
- `content/practices/engineering/patterns.md` — Design patterns

---

*Part of SAGE Knowledge Base*
