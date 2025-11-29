# SAGE File Structure Conventions

> Project-specific file organization standards for SAGE Knowledge Base

---

## Table of Contents

- [1. Directory Layout](#1-directory-layout)
- [2. Knowledge Organization](#2-knowledge-organization)
- [3. Source Code Organization](#3-source-code-organization)
- [4. Test Organization](#4-test-organization)
- [5. Configuration Files](#5-configuration-files)
- [6. Documentation](#6-documentation)
- [7. Source Code Packages](#7-source-code-packages)
- [8. Module Structure](#8-module-structure)
- [9. Special Files](#9-special-files)

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
├── .knowledge/             # Generic knowledge content (distributable)
├── docs/                # User-facing documentation
├── src/sage/            # Source code
├── tests/               # Test suite
└── tools/               # Development utilities
```

### 1.2 Directory Visibility

| Prefix    | Visibility | Purpose               |
|-----------|------------|-----------------------|
| `.` (dot) | Hidden     | Internal/system files |
| No prefix | Visible    | User-facing content   |

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

### 1.4 Output File Convention

**All temporary and intermediate output files MUST be placed in `.outputs/` directory.**

| File Type         | Correct Location      | Incorrect Location    |
|-------------------|-----------------------|-----------------------|
| Process output    | `.outputs/result.txt` | `./result.txt` (root) |
| Temporary files   | `.outputs/temp_*.txt` | `./temp_*.txt` (root) |
| Generated reports | `.outputs/report.md`  | `./report.md` (root)  |
| Debug logs        | `.logs/debug.log`     | `./debug.log` (root)  |

**Why this matters:**

1. **Clean root directory**: Keeps project root organized and professional
2. **Git hygiene**: `.outputs/` is git-ignored, preventing accidental commits
3. **Easy cleanup**: All temporary files in one location
4. **Tool compatibility**: External tools (MCP, scripts) should respect this convention

**For external tools (MCP, Terminal, etc.):**

When generating output files, always specify the full path to `.outputs/`:

```bash
# Correct
command > .outputs/output.txt

# Incorrect
command > output.txt
command > .output.txt
```

**Note**: Files like `.output.txt`, `output.txt`, `*.output.txt` in root are git-ignored as a safety measure, but should
still be avoided.

---

## 2. Knowledge Organization

This section defines the rules for organizing knowledge across the project's directories.

### 2.1 Directory Purpose Matrix

| Directory     | Content Type       | Scope            | Distributable |
|---------------|--------------------|------------------|---------------|
| `.knowledge/` | Generic knowledge  | Universal        | ✅ Yes         |
| `.context/`   | Project-specific   | SAGE only        | ❌ No          |
| `docs/`       | User documentation | SAGE users       | ✅ Yes         |
| `.history/`   | Session records    | AI collaboration | ❌ No          |

### 2.2 Content Directory (`.knowledge/`)

**Purpose**: Generic, reusable knowledge that can be distributed and used across different projects.

| Should Include                      | Should NOT Include           |
|-------------------------------------|------------------------------|
| Universal best practices            | SAGE-specific configurations |
| Generic frameworks (autonomy, etc.) | Project ADRs                 |
| Reusable patterns and guidelines    | Internal calibration data    |
| Language/technology references      | SAGE API documentation       |
| Industry-standard conventions       | Session history or handoffs  |

**Example**: `.knowledge/practices/engineering/common_pitfalls.md` — Generic engineering pitfalls applicable to any
project.

### 2.3 Context Directory (`.context/`)

**Purpose**: Project-specific knowledge, conventions, and decisions unique to SAGE.

| Should Include                       | Should NOT Include             |
|--------------------------------------|--------------------------------|
| Architecture Decision Records (ADRs) | Generic best practices         |
| SAGE-specific coding conventions     | Universal frameworks           |
| Project policies (timeout hierarchy) | Reusable patterns              |
| AI calibration data for SAGE         | Content meant for distribution |
| Internal optimization notes          | User-facing documentation      |

**Example**: `.context/decisions/ADR-0001-architecture.md` — SAGE-specific architecture decisions.

### 2.4 Documentation Directory (`docs/`)

**Purpose**: User-facing documentation for SAGE users and contributors.

| Should Include            | Should NOT Include                     |
|---------------------------|----------------------------------------|
| Design documents          | Internal conventions                   |
| API documentation         | AI session records                     |
| User guides and tutorials | Generic knowledge (belongs in content) |
| Architecture overviews    | ADRs (belong in .context)              |
| Quick reference guides    | Calibration data                       |

**Example**: `docs/design/01-architecture.md` — SAGE architecture design document.

### 2.5 History Directory (`.history/`)

**Purpose**: AI collaboration records, session history, and task handoffs.

| Should Include         | Should NOT Include          |
|------------------------|-----------------------------|
| Session state records  | Permanent documentation     |
| Conversation summaries | Code or configuration       |
| Task handoff documents | Design decisions (use ADRs) |
| Lessons learned        | Generic knowledge           |

**Example**: `.history/conversations/2025-11-30-knowledge-reorganization.md`

### 2.6 Migration Decision Rules

When deciding where content belongs, apply these rules in order:

```
1. Is it SAGE-specific implementation/decision?
   YES → .context/ (ADRs, conventions, policies)
   NO  → Continue to step 2

2. Is it user-facing documentation?
   YES → docs/ (design, API, guides)
   NO  → Continue to step 3

3. Is it AI session/collaboration record?
   YES → .history/ (sessions, handoffs)
   NO  → Continue to step 4

4. Is it generic, reusable knowledge?
   YES → .knowledge/ (frameworks, practices, guidelines)
   NO  → Ask: Does this need to exist?
```

---

## 3. Source Code Organization

### 3.1 Package Structure

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

### 3.2 Core Layer (`core/`)

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

### 3.3 Services Layer (`services/`)

```
services/
├── __init__.py          # Service exports
├── cli.py               # CLI service (Typer)
├── mcp.py               # MCP service (FastMCP)
└── api.py               # API service (FastAPI)
```

### 3.4 Capabilities Layer (`capabilities/`)

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

## 4. Test Organization

### 4.1 Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── fixtures/            # Test data and mocks
│   ├── configs/         # Test configurations
│   ├── mock_responses/  # Mock API responses
│   └── sample_.knowledge/  # Sample knowledge files
├── unit/                # Unit tests (mirror src/)
│   ├── core/
│   ├── services/
│   └── capabilities/
├── integration/         # Integration tests
└── performance/         # Performance benchmarks
    └── benchmarks/
```

### 4.2 Test File Naming

| Source File                     | Test File                              |
|---------------------------------|----------------------------------------|
| `src/sage/core/config.py`       | `tests/unit/core/test_config.py`       |
| `src/sage/services/cli.py`      | `tests/unit/services/test_cli.py`      |
| `src/sage/core/di/container.py` | `tests/unit/core/di/test_container.py` |

### 4.3 Test File Structure

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

## 5. Configuration Files

### 5.1 Config Directory Structure

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

### 5.2 Main Config Location

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

### 5.3 Config Precedence

1. Environment variables (`SAGE_*`)
2. Command-line arguments
3. `config/sage.yaml` (main entry point)
4. `config/<category>/*.yaml` (modular configs)
5. Default values in code

### 5.4 Config Include Pattern

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

## 6. Documentation

### 6.1 Documentation Structure

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

### 6.2 Knowledge Content Structure

```
.knowledge/
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

### 6.3 Context Directory Structure

```
.context/
├── index.md             # Navigation index
├── policies/            # Project-specific policies
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

## 7. Source Code Packages

### 7.1 Package Responsibilities

The `src/sage/` directory contains several packages with distinct responsibilities:

| Package         | Purpose                | Contains                               |
|-----------------|------------------------|----------------------------------------|
| `domain/`       | Business domain models | Pure data structures, enums, no logic  |
| `core/`         | Infrastructure & logic | Loaders, timeout, config, DI, events   |
| `interfaces/`   | Protocol re-exports    | Convenience imports from core          |
| `services/`     | External interfaces    | CLI, MCP, HTTP API                     |
| `capabilities/` | Runtime features       | Analyzers, checkers, monitors          |
| `plugins/`      | Extension system       | Plugin base, registry, bundled plugins |

### 7.2 Domain vs Core Distinction

**Domain Package** (`domain/`):

- Pure data structures with no business logic
- Dataclasses and enums representing business concepts
- No dependencies on infrastructure (no I/O, no external services)
- Examples: `KnowledgeAsset`, `CollaborationSession`, `AutonomyLevel`

**Core Package** (`core/`):

- Infrastructure components with actual logic
- Handles I/O, configuration, timing, events
- Implements the SAGE protocol behaviors
- Examples: `KnowledgeLoader`, `TimeoutManager`, `EventBus`, `DIContainer`

```
domain/                     core/
├── knowledge.py            ├── loader.py      (uses domain models)
│   └── KnowledgeAsset      │   └── KnowledgeLoader
│   └── KnowledgeLayer      ├── timeout.py     (infrastructure)
│   └── KnowledgeCycle      ├── config.py      (infrastructure)
└── session.py              ├── di/            (infrastructure)
    └── CollaborationSession├── events/        (infrastructure)
    └── SessionContext      ├── logging/       (infrastructure)
    └── HandoffPackage      └── memory/        (infrastructure)
```

### 7.3 Interfaces Package

The `interfaces/` package provides a convenience layer for importing protocols and models:

```python
# Instead of multiple imports:
from sage.core.protocols import SourceProtocol, AnalyzeProtocol
from sage.core.models import LoadResult, SearchResult

# Use single import:
from sage.interfaces import SourceProtocol, AnalyzeProtocol, LoadResult, SearchResult
```

This supports the **Protocol-First** design principle (ADR-0006).

---

## 8. Module Structure

### 8.1 `__init__.py` Pattern

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

### 8.2 Module File Order

Within each module directory, files should be organized:

1. `__init__.py` - Package initialization
2. `protocols.py` - Protocol definitions (if any)
3. `models.py` - Data models (if any)
4. `exceptions.py` - Custom exceptions (if any)
5. Feature files (alphabetically)
6. `utils.py` - Utility functions (if any)

### 8.3 Single Module File Structure

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

## 9. Special Files

### 9.1 Project Root Files

| File              | Purpose                      |
|-------------------|------------------------------|
| `pyproject.toml`  | Python project configuration |
| `sage.yaml`       | Main SAGE configuration      |
| `README.md`       | Project overview             |
| `Makefile`        | Development commands         |
| `environment.yml` | Conda environment            |
| `index.md`        | Knowledge base entry point   |

### 9.2 Hidden Configuration

| File/Directory    | Purpose                   |
|-------------------|---------------------------|
| `.junie/`         | JetBrains Junie AI config |
| `.context/`       | Project knowledge         |
| `.gitignore`      | Git ignore rules          |
| `.python-version` | Python version (pyenv)    |

---

## Related

- `naming.md` — Naming conventions
- `code_patterns.md` — Code patterns
- `docs/design/01-architecture.md` — Architecture
- `.knowledge/practices/documentation/project_directory_structure.md` — General directory practices

---

*Part of SAGE Knowledge Base - Project Conventions*
