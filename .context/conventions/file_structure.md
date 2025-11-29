# SAGE File Structure Conventions

> Project-specific file organization standards for SAGE Knowledge Base

---

## Table of Contents

[1. Directory Layout](#1-directory-layout) · [2. Source Code Organization](#2-source-code-organization) · [3. Test Organization](#3-test-organization) · [4. Configuration Files](#4-configuration-files) · [5. Documentation](#5-documentation) · [6. Module Structure](#6-module-structure)

---

## 1. Directory Layout

### 1.1 Top-Level Structure

```
sage-kb/
├── .junie/              # JetBrains Junie AI configuration
├── .context/            # Project-specific knowledge (ADRs, conventions)
├── .history/            # AI session history and handoffs
├── .archive/            # Historical/deprecated content
├── .logs/               # Runtime log files (git-ignored)
├── .outputs/            # Intermediate process files (git-ignored)
├── config/              # Configuration files (YAML)
├── content/             # Generic knowledge content (distributable)
├── docs/                # User-facing documentation
├── src/sage/            # Source code
├── tests/               # Test suite
└── tools/               # Development utilities
```

### 1.2 Directory Visibility

| Prefix | Visibility | Purpose |
|--------|------------|---------|
| `.` (dot) | Hidden | Internal/system files |
| No prefix | Visible | User-facing content |

### 1.3 Git-Ignored Directories

```gitignore
.logs/
.outputs/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
*.egg-info/
```

---

## 2. Source Code Organization

### 2.1 Package Structure

```
src/sage/
├── __init__.py          # Package exports
├── __main__.py          # Entry point: python -m sage
├── core/                # Core infrastructure
├── services/            # Service implementations
├── capabilities/        # Runtime capabilities
├── domain/              # Domain models
├── interfaces/          # Protocol re-exports
├── plugins/             # Plugin system
└── data/                # Static data files
```

### 2.2 Core Layer (`core/`)

```
core/
├── __init__.py          # Core exports
├── config.py            # Configuration management
├── exceptions.py        # Exception hierarchy
├── loader.py            # Knowledge loader
├── models.py            # Core data models
├── protocols.py         # Protocol definitions
├── timeout.py           # Timeout management
├── di/                  # Dependency injection
│   ├── __init__.py
│   ├── container.py     # DI container
│   └── registry.py      # Service registry
├── events/              # Event system
│   ├── __init__.py
│   ├── bus.py           # Event bus
│   ├── events.py        # Event definitions
│   └── protocols.py     # Event protocols
├── logging/             # Logging infrastructure
│   ├── __init__.py
│   ├── config.py        # Log configuration
│   ├── context.py       # Log context
│   └── processors.py    # Log processors
└── memory/              # Memory management
    ├── __init__.py
    ├── session.py       # Session memory
    ├── store.py         # Memory store
    └── token_budget.py  # Token budget
```

### 2.3 Services Layer (`services/`)

```
services/
├── __init__.py          # Service exports
├── cli.py               # CLI service (Typer)
├── mcp.py               # MCP service (FastMCP)
└── api.py               # API service (FastAPI)
```

### 2.4 Capabilities Layer (`capabilities/`)

```
capabilities/
├── __init__.py          # Capability exports
├── analyzers/           # Analysis capabilities
│   ├── __init__.py
│   ├── code.py          # Code analyzer
│   └── content.py       # Content analyzer
├── checkers/            # Validation capabilities
│   ├── __init__.py
│   ├── health.py        # Health checker
│   └── config.py        # Config checker
└── monitors/            # Monitoring capabilities
    ├── __init__.py
    ├── performance.py   # Performance monitor
    └── usage.py         # Usage monitor
```

---

## 3. Test Organization

### 3.1 Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── fixtures/            # Test data and mocks
│   ├── configs/         # Test configurations
│   ├── mock_responses/  # Mock API responses
│   └── sample_content/  # Sample knowledge files
├── unit/                # Unit tests (mirror src/)
│   ├── core/
│   ├── services/
│   └── capabilities/
├── integration/         # Integration tests
└── performance/         # Performance benchmarks
    └── benchmarks/
```

### 3.2 Test File Naming

| Source File | Test File |
|-------------|-----------|
| `src/sage/core/config.py` | `tests/unit/core/test_config.py` |
| `src/sage/services/cli.py` | `tests/unit/services/test_cli.py` |
| `src/sage/core/di/container.py` | `tests/unit/core/di/test_container.py` |

### 3.3 Test File Structure

```python
# tests/unit/core/test_config.py

"""Tests for sage.core.config module."""

import pytest
from sage.core.config import SAGEConfig, get_config

# --- Fixtures ---

@pytest.fixture
def sample_config():
    """Create sample configuration."""
    return SAGEConfig(...)

# --- Test Classes (grouped by feature) ---

class TestSAGEConfig:
    """Tests for SAGEConfig class."""
    
    def test_default_values(self):
        """Test default configuration values."""
        ...
    
    def test_env_override(self):
        """Test environment variable override."""
        ...

class TestGetConfig:
    """Tests for get_config function."""
    
    def test_singleton_behavior(self):
        """Test singleton pattern."""
        ...
```

---

## 4. Configuration Files

### 4.1 Config Directory Structure

The configuration system uses a modular YAML structure organized by functional area:

```
config/
├── sage.yaml              # Main configuration entry point
├── index.md               # Configuration documentation
├── core/                  # Core infrastructure configs
│   ├── timeout.yaml       # 5-level timeout hierarchy (T1-T5)
│   ├── logging.yaml       # Structured logging (structlog)
│   ├── memory.yaml        # Memory and persistence settings
│   └── di.yaml            # Dependency injection container
├── services/              # Service layer configs
│   ├── cli.yaml           # CLI (Typer) configuration
│   ├── mcp.yaml           # MCP server configuration
│   └── api.yaml           # REST API (FastAPI) configuration
├── knowledge/             # Knowledge management configs
│   ├── content.yaml       # Content directory structure
│   ├── loading.yaml       # Smart loading strategies
│   ├── search.yaml        # Search parameters
│   ├── guidelines.yaml    # Section to guideline mapping
│   ├── triggers.yaml      # Context triggers
│   └── token_budget.yaml  # Token budget allocation
└── capabilities/          # Feature and plugin configs
    ├── features.yaml      # Feature flags
    ├── plugins.yaml       # Plugin loader settings
    ├── autonomy.yaml      # Autonomy levels (L1-L6)
    ├── quality.yaml       # Quality thresholds
    └── documentation.yaml # Documentation standards
```

### 4.2 Main Config Location

The main `sage.yaml` is located inside the `config/` directory:

```
sage-kb/
├── config/
│   ├── sage.yaml          # ← Main config entry point
│   ├── core/              # Core configs
│   ├── services/          # Service configs
│   ├── knowledge/         # Knowledge configs
│   └── capabilities/      # Capability configs
└── src/
```

The `sage.yaml` file includes references to all modular config files via the `includes:` directive.

### 4.3 Config Precedence

1. Environment variables (`SAGE_*`)
2. Command-line arguments
3. `config/sage.yaml` (main entry point)
4. `config/<category>/*.yaml` (modular configs)
5. Default values in code

### 4.4 Config Include Pattern

The main `sage.yaml` uses an `includes:` directive to load modular configs:

```yaml
includes:
  - config/core/timeout.yaml
  - config/core/logging.yaml
  - config/services/cli.yaml
  # ... etc.
```

This pattern enables:
- **Separation of concerns**: Each functional area has its own config
- **Easy navigation**: Find settings by category
- **Selective overrides**: Override specific areas without touching others

---

## 5. Documentation

### 5.1 Documentation Structure

```
docs/
├── design/              # Design documents
│   ├── 00-overview.md
│   ├── 01-architecture.md
│   ├── 02-sage-protocol.md
│   └── ...
├── api/                 # API documentation
├── guides/              # User guides
└── examples/            # Example usage
```

### 5.2 Knowledge Content Structure

```
content/
├── core/                # Core principles
│   ├── principles.md
│   └── defaults.md
├── frameworks/          # Conceptual frameworks
│   ├── autonomy/
│   ├── cognitive/
│   ├── design/
│   ├── patterns/
│   └── resilience/
├── guidelines/          # General guidelines
├── practices/           # Best practices
│   ├── ai_collaboration/
│   ├── decisions/
│   ├── documentation/
│   └── engineering/
├── scenarios/           # Usage scenarios
│   └── python_backend/
└── templates/           # Document templates
```

### 5.3 Context Directory Structure

```
.context/
├── index.md             # Navigation index
├── configurations/      # Project-specific configs
│   ├── timeout_hierarchy.md
│   ├── loading_configurations.md
│   └── runtime_settings.md
├── conventions/         # Coding conventions
│   ├── naming.md
│   ├── code_patterns.md
│   └── file_structure.md
├── decisions/           # Architecture Decision Records
│   ├── ADR-0001-architecture.md
│   └── ...
└── intelligence/        # AI collaboration patterns
    ├── patterns.md
    └── calibration.md
```

---

## 6. Module Structure

### 6.1 `__init__.py` Pattern

```python
# src/sage/core/__init__.py
"""SAGE Core module.

This module provides core infrastructure for the SAGE Knowledge Base.
"""

from sage.core.config import SAGEConfig, get_config
from sage.core.exceptions import SAGEError
from sage.core.loader import KnowledgeLoader
from sage.core.timeout import TimeoutManager

__all__ = [
    "SAGEConfig",
    "get_config",
    "SAGEError",
    "KnowledgeLoader",
    "TimeoutManager",
]
```

### 6.2 Module File Order

Within each module directory, files should be organized:

1. `__init__.py` - Package initialization
2. `protocols.py` - Protocol definitions (if any)
3. `models.py` - Data models (if any)
4. `exceptions.py` - Custom exceptions (if any)
5. Feature files (alphabetically)
6. `utils.py` - Utility functions (if any)

### 6.3 Single Module File Structure

```python
"""Module docstring with brief description.

Extended description if needed.
"""

# --- Imports ---
# Standard library
from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

# Third-party
import structlog

# Local
from sage.core.exceptions import SAGEError

if TYPE_CHECKING:
    from sage.core.config import SAGEConfig

# --- Constants ---
DEFAULT_TIMEOUT_MS = 5000
MAX_RETRIES = 3

# --- Module Logger ---
logger = structlog.get_logger(__name__)

# --- Classes ---
class MyClass:
    """Class docstring."""
    ...

# --- Functions ---
def my_function() -> None:
    """Function docstring."""
    ...

# --- Private Helpers ---
def _helper_function() -> None:
    """Private helper."""
    ...
```

---

## 7. Special Files

### 7.1 Project Root Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python project configuration |
| `sage.yaml` | Main SAGE configuration |
| `README.md` | Project overview |
| `Makefile` | Development commands |
| `environment.yml` | Conda environment |
| `index.md` | Knowledge base entry point |

### 7.2 Hidden Configuration

| File/Directory | Purpose |
|----------------|---------|
| `.junie/` | JetBrains Junie AI config |
| `.context/` | Project knowledge |
| `.gitignore` | Git ignore rules |
| `.python-version` | Python version (pyenv) |

---

## Related

- `naming.md` — Naming conventions
- `code_patterns.md` — Code patterns
- `docs/design/01-architecture.md` — Architecture
- `content/practices/documentation/project_directory_structure.md` — General directory practices

---

*Part of SAGE Knowledge Base - Project Conventions*
