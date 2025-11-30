# SAGE Knowledge Base

> Production-grade knowledge management system for AI-human collaboration

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/HengYangDS/sage-kb/actions/workflows/ci.yml/badge.svg)](https://github.com/HengYangDS/sage-kb/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/HengYangDS/sage-kb/branch/main/graph/badge.svg)](https://codecov.io/gh/HengYangDS/sage-kb)

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Philosophy](#2-philosophy)
- [3. Installation](#3-installation)
- [4. Quick Start](#4-quick-start)
- [5. Architecture](#5-architecture)
- [6. Development](#6-development)
- [7. Documentation](#7-documentation)
- [8. License](#8-license)

---

## 1. Overview

SAGE (Source, Analyze, Generate, Evolve) is a knowledge management system designed for AI-human collaboration, featuring:

- **5-level timeout hierarchy** (100 ms ~ 10 s) for guaranteed response times
- **Circuit breaker pattern** for fault tolerance
- **Smart task-based loading** with 95% token efficiency
- **Graceful degradation** – never hangs, always returns useful content
- **Plugin architecture** with 7 extension points

## 2. Philosophy

| Principle        | Chinese | Meaning              | Application                             |
|------------------|---------|----------------------|-----------------------------------------|
| **Faithfulness** | 信 (Xin) | Accurate, reliable   | Complete knowledge preservation         |
| **Clarity**      | 达 (Da)  | Clear, accessible    | Unified structure, intuitive navigation |
| **Elegance**     | 雅 (Ya)  | Refined, sustainable | Minimal dependencies, extensible        |

## 3. Installation

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

## 4. Quick Start

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

## 5. Architecture

SAGE uses a 3-layer architecture:

```text
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

## 6. Development

### 6.1 Setup

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

### 6.2 Code Quality

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

### 6.3 Pre-commit Hooks

The project uses pre-commit hooks for code quality:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Bandit**: Security checks
- **Commitizen**: Conventional commits

### 6.4 CI/CD

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

## 7. Documentation

See `docs/` for comprehensive documentation:

### 7.1 Design Documents

| Document | Purpose |
|----------|---------|
| `docs/design/OVERVIEW.md` | Project overview |
| `docs/design/architecture/THREE_LAYER.md` | Three-layer architecture |
| `docs/design/protocols/SAGE_PROTOCOL.md` | SAGE protocol specification |
| `docs/design/services/SERVICE_LAYER.md` | Service layer design |
| `docs/design/timeout_resilience/TIMEOUT_HIERARCHY.md` | Timeout hierarchy |
| `docs/design/plugins/PLUGIN_ARCHITECTURE.md` | Plugin system |
| `docs/design/knowledge_system/LAYER_HIERARCHY.md` | Knowledge organization |
| `docs/design/evolution/ROADMAP.md` | Implementation roadmap |
| `docs/design/configuration/CONFIG_HIERARCHY.md` | Configuration management |

### 7.2 API Reference

| Document | Purpose |
|----------|---------|
| `docs/api/CLI.md` | Command-line interface |
| `docs/api/MCP.md` | MCP (Model Context Protocol) API |
| `docs/api/PYTHON.md` | Python SDK reference |

### 7.3 User Guides

| Document | Purpose |
|----------|---------|
| `docs/guides/QUICKSTART.md` | Quick start guide |
| `docs/guides/CONFIGURATION.md` | Configuration guide |
| `docs/guides/MIGRATION.md` | Migration guide |

## 8. License

MIT License – see LICENSE file for details.

---

## Related

- `INDEX.md` — Project navigation entry
- `CONTRIBUTING.md` — Contribution guidelines
- `CHANGELOG.md` — Version history and changes
- `docs/design/OVERVIEW.md` — Design overview
- `.knowledge/core/PRINCIPLES.md` — Core philosophy (信达雅)

---

*AI Collaboration Knowledge Base*
