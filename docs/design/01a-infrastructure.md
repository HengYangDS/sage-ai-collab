---
title: SAGE Knowledge Base - Infrastructure
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~1500
---

# Infrastructure Design

> **Logging, toolchain, packaging, and platform support**

---

## Table of Contents

- [1. Unified Logging](#1-unified-logging)
- [2. Development Toolchain](#2-development-toolchain)
- [3. Package Distribution](#3-package-distribution)
- [4. Python Version Features](#4-python-version-features)
- [5. Cross-Platform Support](#5-cross-platform-support)

---

## 1. Unified Logging

### 1.1 Technology Selection

| Component       | Choice                      | Rationale                                |
|-----------------|-----------------------------|------------------------------------------|
| **Core**        | structlog                   | Structured logging, context binding      |
| **Integration** | stdlib logging              | Compatibility with third-party libraries |
| **Output**      | JSON (prod) / Console (dev) | Machine-readable in production           |

### 1.2 Configuration

```python
# src/sage/core/logging/config.py
import structlog
import logging
import sys


def configure_logging(
    level: str = "INFO",
    format: str = "console",  # "console" or "json"
) -> None:
    """Configure unified logging for the application."""
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
```

### 1.3 Usage

```python
from sage.core.logging import get_logger, bind_context

logger = get_logger(__name__)

# Basic logging
logger.info("loading layer", layer="core", tokens=500)

# Context binding
with bind_context(request_id="req-123"):
    logger.info("processing request")
```

### 1.4 Output Formats

| Environment | Format  | Example                                                    |
|-------------|---------|------------------------------------------------------------|
| Development | Console | `2025-11-28T14:30:00 [info] loading layer layer=core`      |
| Production  | JSON    | `{"timestamp": "...", "level": "info", "event": "..."}` |

---

## 2. Development Toolchain

### 2.1 Makefile Commands

```makefile
install:        ## Install production dependencies
	pip install -e .

dev:            ## Install dev dependencies + pre-commit
	pip install -e ".[dev]"
	pre-commit install

test:           ## Run all tests with coverage
	pytest tests/ -v --cov=sage

lint:           ## Run ruff + mypy
	ruff check src/ tests/
	mypy src/

format:         ## Format code with ruff
	ruff format src/ tests/

serve:          ## Start MCP server
	python -m sage serve
```

### 2.2 justfile (Cross-Platform)

```just
default:
    @just --list

install:
    pip install -e .

dev:
    pip install -e ".[dev]"
    pre-commit install

test:
    pytest tests/ -v --cov=sage

lint:
    ruff check src/ tests/
    mypy src/
```

### 2.3 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [ --fix ]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
```

---

## 3. Package Distribution

### 3.1 Build Backend

This project uses `hatchling` (PEP 517/518/621 compliant). No `MANIFEST.in` needed.

| Approach       | Era                 | Configuration                              |
|----------------|---------------------|--------------------------------------------|
| MANIFEST.in    | Legacy (setuptools) | Separate file with glob patterns           |
| pyproject.toml | Modern (hatchling)  | `[tool.hatch.build.targets.sdist]` section |

### 3.2 Key Configuration

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sage-kb"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "pyyaml>=6.0.2",
    "pydantic>=2.8",
    "structlog>=24.4",
    "typer>=0.12",
    "rich>=13.8",
]

[project.scripts]
sage = "sage.services.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/sage"]
```

---

## 4. Python Version Features

### 4.1 Python 3.12 Features (Required)

| Feature               | PEP     | Code Example                       |
|-----------------------|---------|------------------------------------|
| Type parameter syntax | PEP 695 | `class Loader[T]:`                 |
| Type aliases          | PEP 695 | `type LoadResult = dict[str, Any]` |
| Union syntax          | -       | `value: str \| None`               |
| @override decorator   | PEP 698 | `@override def load():`            |

### 4.2 Modern Code Patterns

```python
# Python 3.12+ Style
from typing import override

# PEP 695: Type parameter syntax
class Container[T]:
    def __init__(self, value: T | None = None) -> None:
        self.value = value

# PEP 695: Type aliases
type LoadResult = dict[str, str | int | list[str]]

# PEP 698: Override decorator
class CustomLoader(BaseLoader):
    @override
    async def load(self, layers: list[str]) -> LoadResult:
        ...
```

### 4.3 Migration Guidelines

1. **New code**: Always use Python 3.12+ syntax
2. **Type hints**: Prefer `list[T]` over `List[T]`
3. **Optionals**: Use `T | None` instead of `Optional[T]`
4. **Generics**: Use `class Foo[T]:` instead of `class Foo(Generic[T]):`

---

## 5. Cross-Platform Support

### 5.1 Platform-Specific Paths

Using `platformdirs` for cross-platform directory handling:

```python
from platformdirs import user_config_dir, user_cache_dir
from pathlib import Path

def get_platform_paths() -> dict[str, Path]:
    app_name = "sage"
    return {
        "config": Path(user_config_dir(app_name)),
        "cache": Path(user_cache_dir(app_name)),
    }
```

### 5.2 Platform Paths Table

| Platform    | Config                                | Cache                          |
|-------------|---------------------------------------|--------------------------------|
| **Linux**   | `~/.config/sage/`                     | `~/.cache/sage/`               |
| **macOS**   | `~/Library/Application Support/sage/` | `~/Library/Caches/sage/`       |
| **Windows** | `C:\Users\<user>\AppData\Local\sage\` | `...\AppData\Local\sage\Cache\`|

### 5.3 Path Handling Best Practices

```python
from pathlib import Path

# ✅ CORRECT: Use pathlib (cross-platform)
config_file = Path("content") / "core" / "principles.md"

# ⚠️ AVOID: Hardcoded paths
config_file = "content\\core\\principles.md"  # Windows-only
```

---

## Related

- `docs/design/01-architecture.md` — Main architecture design
- `docs/design/01b-configuration.md` — Configuration design
- `docs/design/01c-usage.md` — Usage patterns
- `docs/guides/configuration.md` — Configuration guide

---

*Part of SAGE Knowledge Base*
