# SAGE Knowledge Base

> **Production-grade knowledge management for AI-human collaboration**
>
> ⚠️ **Status: Alpha (v0.1.0)** - Under active development and testing

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

### Prerequisites

- Python 3.12+
- Miniconda (recommended) or venv

### Setup Environment (Recommended)

```bash
# Create conda environment (recommended)
conda env create -f environment.yml
conda activate sage-kb

# Or use venv as alternative:
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows
```

### Install Package

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
import asyncio
from sage.core.loader import KnowledgeLoader


async def main():
    loader = KnowledgeLoader()
    result = await loader.load_core(timeout_ms=2000)
    print(result.content)


asyncio.run(main())
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
# 1. Setup conda environment (see Installation section above)
conda env create -f environment.yml
conda activate sage-kb

# 2. Install with development dependencies
pip install -e ".[dev]"

# 3. Install pre-commit hooks
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

See `docs/` for comprehensive documentation:

### Design Documents (`docs/design/`)

- `00-overview.md` — Project overview
- `01-architecture.md` — Three-layer architecture
- `02-sage-protocol.md` — SAGE protocol specification
- `03-services.md` — Service layer design
- `04-timeout-loading.md` — Timeout hierarchy and smart loading
- `05-plugin-memory.md` — Plugin system and memory
- `06-content-structure.md` — Knowledge content organization
- `07-roadmap.md` — Implementation roadmap
- `08-evaluation.md` — Evaluation criteria
- `09-configuration.md` — Configuration management

### API Reference (`docs/api/`)

- `cli.md` — Command-line interface
- `mcp.md` — MCP (Model Context Protocol) API
- `python.md` — Python SDK reference

### User Guides (`docs/guides/`)

- `quickstart.md` — Quick start guide
- `configuration.md` — Configuration guide
- `plugin_development.md` — Plugin development

## License

MIT License – see LICENSE file for details.

---

**Version**: 0.1.0
**Author**: SAGE AI Collab Team
