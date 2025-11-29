# SAGE Knowledge Base

> **Production-grade knowledge management for AI-human collaboration**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/HengYangDS/sage-kb/actions/workflows/ci.yml/badge.svg)](https://github.com/HengYangDS/sage-kb/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/HengYangDS/sage-kb/branch/main/graph/badge.svg)](https://codecov.io/gh/HengYangDS/sage-kb)

## Overview

SAGE (Smart AI-Guided Expertise) is a knowledge management system designed for AI-human collaboration, featuring:

- **5-level timeout hierarchy** (100 ms ~ 10 s) for guaranteed response times
- **Circuit breaker pattern** for fault tolerance
- **Smart task-based loading** with 95% token efficiency
- **Graceful degradation** – never hangs, always returns useful content
- **Plugin architecture** with 7 extension points

## Philosophy (信达雅 · Xin-Da-Ya)

| Principle        | Chinese | Meaning              | Application                             |
|------------------|---------|----------------------|-----------------------------------------|
| **Faithfulness** | 信 (Xin) | Accurate, reliable   | Complete knowledge preservation         |
| **Clarity**      | 达 (Da)  | Clear, accessible    | Unified structure, intuitive navigation |
| **Elegance**     | 雅 (Ya)  | Refined, sustainable | Minimal dependencies, extensible        |

## Installation

```bash
# Install from source
pip install -e .

# Install with MCP support
pip install -e ".[mcp]"

# Install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

### CLI Usage

```bash
# Get core knowledge
sage get core

# Search knowledge base
sage search "timeout"

# Start MCP server
sage serve
```

### Python API

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = await loader.load_core(timeout_ms=2000)
print(result.content)
```

## Architecture

SAGE uses a 3-layer architecture:

```
┌────────────────────────────────────────────────┐
│              Services Layer                    │
│   CLI (Typer) | MCP (FastMCP) | API (FastAPI)  │
├────────────────────────────────────────────────┤
│            Capabilities Layer                  │
│   Analyzers | Checkers | Monitors              │
├────────────────────────────────────────────────┤
│               Core Layer                       │
│   Loader | Timeout | Config | EventBus         │
└────────────────────────────────────────────────┘
```

## Development

### Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### Code Quality

```bash
# Run linting
ruff check src/ tests/

# Run formatting
ruff format src/ tests/

# Run type checking
mypy src/sage

# Run tests with coverage
pytest tests/ --cov=sage
```

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Bandit**: Security checks
- **Commitizen**: Conventional commits

### CI/CD

GitHub Actions workflows:

- **CI** (`ci.yml`): Runs on push/PR to main/develop
  - Lint & format check (Ruff)
  - Type check (MyPy)
  - Tests (Python 3.12-3.14, Linux/Windows/macOS)
  - Build package verification

- **Release** (`release.yml`): Runs on version tags
  - Pre-release tests
  - Build & publish to PyPI
  - Create GitHub release

## Documentation

See `docs/design/` for comprehensive design documents:

- `00-overview.md` - Project overview
- `01-architecture.md` - Architecture design
- `07-roadmap.md` - Implementation roadmap

## License

MIT License – see LICENSE file for details.

---

**Version**: 0.1.0
**Author**: SAGE AI Collab Team
