# Project Optimizations

> SAGE-specific optimizations and preferences for AI collaboration

---

## Table of Contents

[1. Code Generation Preferences](#1-code-generation-preferences) · [2. Testing Strategy](#2-testing-strategy) · [3. Documentation Style](#3-documentation-style) · [4. Performance Optimizations](#4-performance-optimizations) · [5. Common Patterns](#5-common-patterns)

---

## 1. Code Generation Preferences

### 1.1 Preferred Patterns

| Category | Preference | Example |
|----------|------------|---------|
| **Async** | Always use async/await for IO | `async def load()` not `def load()` |
| **Type hints** | Full annotations on public APIs | `def process(data: str) -> Result:` |
| **Protocols** | Prefer Protocol over ABC | `class MyProtocol(Protocol):` |
| **Dataclasses** | Use for simple data containers | `@dataclass class Config:` |
| **Enums** | Use for fixed choices | `class Level(Enum):` |

### 1.2 Import Organization

```python
# 1. Future imports (if needed)
from __future__ import annotations

# 2. Standard library
import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

# 3. Third-party
import structlog
from pydantic import BaseModel

# 4. Local imports
from sage.core.config import get_config
from sage.core.exceptions import SAGEError

# 5. Type checking only imports
if TYPE_CHECKING:
    from sage.core.protocols import SourceProtocol
```

### 1.3 Error Handling

```python
# Preferred: Specific exceptions with context
try:
    result = await load_file(path)
except FileNotFoundError:
    raise LoadError(f"Knowledge file not found: {path}") from None
except PermissionError as e:
    raise LoadError(f"Cannot read {path}: {e}") from e

# Avoid: Bare except or generic Exception
try:
    result = await load_file(path)
except:  # Don't do this
    pass
```

### 1.4 Async Patterns

```python
# Preferred: Gather for concurrent operations
results = await asyncio.gather(
    load_layer("core"),
    load_layer("frameworks"),
    return_exceptions=True
)

# Preferred: Timeout wrapper for external calls
async with asyncio.timeout(5.0):
    result = await external_call()

# Preferred: Semaphore for rate limiting
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await process_item(item)
```

---

## 2. Testing Strategy

### 2.1 Test Structure

```python
# Preferred test file structure
"""Tests for sage.core.timeout module."""

import pytest
from sage.core.timeout import TimeoutManager, TimeoutLevel

# Group fixtures at top
@pytest.fixture
def timeout_manager():
    return TimeoutManager()

# Group tests by class/function
class TestTimeoutManager:
    """Tests for TimeoutManager class."""
    
    def test_default_timeout(self, timeout_manager):
        """Default timeout should be T3 level."""
        assert timeout_manager.default_level == TimeoutLevel.T3_LAYER
    
    @pytest.mark.asyncio
    async def test_execute_within_timeout(self, timeout_manager):
        """Operation completing within timeout returns result."""
        result = await timeout_manager.execute_with_timeout(
            coro=fast_operation(),
            level=TimeoutLevel.T2_FILE
        )
        assert result == expected_value
```

### 2.2 Test Naming

| Test Type | Pattern | Example |
|-----------|---------|---------|
| Success case | `test_<action>_<condition>` | `test_load_valid_file` |
| Failure case | `test_<action>_fails_when_<condition>` | `test_load_fails_when_file_missing` |
| Edge case | `test_<action>_with_<edge_case>` | `test_load_with_empty_file` |
| Async | `test_<action>_async` | `test_publish_async` |

### 2.3 Mock Preferences

```python
# Preferred: Use Protocol-compliant mocks
class MockLoader:
    """Mock implementing LoaderProtocol."""
    
    def __init__(self, content: str = "test"):
        self._content = content
    
    async def load(self, path: str) -> str:
        return self._content

# Preferred: Fixture-based mock injection
@pytest.fixture
def mock_loader():
    return MockLoader(content="mock content")

# Avoid: Patching internal implementation details
# (Only patch at boundaries)
```

### 2.4 Test Coverage Goals

| Layer | Target | Focus |
|-------|--------|-------|
| Core | 90%+ | All public APIs, error paths |
| Services | 80%+ | Integration points, CLI commands |
| Capabilities | 80%+ | Analyzer logic, edge cases |
| Integration | Key paths | End-to-end workflows |

---

## 3. Documentation Style

### 3.1 Docstring Format

```python
def load_knowledge(
    path: str,
    *,
    layer: str = "core",
    timeout_ms: int | None = None,
) -> Knowledge:
    """Load knowledge from the specified path.
    
    Loads and parses a knowledge file, applying appropriate transformations
    based on the file type and target layer.
    
    Args:
        path: Path to the knowledge file (relative to content/).
        layer: Target layer for context-specific processing.
        timeout_ms: Optional timeout override (uses T2 default if None).
    
    Returns:
        Parsed Knowledge object with metadata.
    
    Raises:
        LoadError: If the file cannot be read or parsed.
        TimeoutError: If loading exceeds the timeout.
    
    Example:
        >>> knowledge = load_knowledge("core/principles.md")
        >>> print(knowledge.title)
        'Core Principles'
    """
```

### 3.2 Module Docstrings

```python
"""SAGE Core Timeout Module.

This module provides timeout management for SAGE operations, implementing
the T1-T5 timeout hierarchy with graceful fallback behavior.

Key Components:
    - TimeoutManager: Main timeout orchestration class
    - TimeoutLevel: Enum of timeout levels (T1-T5)
    - execute_with_timeout(): Convenience function

Example:
    >>> from sage.core.timeout import TimeoutManager, TimeoutLevel
    >>> manager = TimeoutManager()
    >>> result = await manager.execute_with_timeout(
    ...     coro=load_data(),
    ...     level=TimeoutLevel.T2_FILE
    ... )

See Also:
    - ADR-0003: Timeout hierarchy design decision
    - .context/configurations/timeout_hierarchy.md: Configuration details
"""
```

### 3.3 Inline Comments

```python
# Preferred: Explain WHY, not WHAT
# Cache check skipped for core layer (always fresh)
if layer != "core":
    cached = await self._cache.get(key)

# Avoid: Redundant comments
# Get the config  <-- Don't do this
config = get_config()
```

### 3.4 Markdown Documentation

```markdown
# Document Title

> Brief one-line description

---

## Table of Contents
[Section 1](#section-1) · [Section 2](#section-2)

---

## Section 1

### 1.1 Subsection

Content with **bold** and `code`.

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |

---

## Related

- Link to related doc
- Another related doc

---

*Part of SAGE Knowledge Base - Category*
```

---

## 4. Performance Optimizations

### 4.1 Loading Optimizations

| Optimization | Implementation | Impact |
|--------------|----------------|--------|
| Parallel loading | `asyncio.gather()` for multiple files | 3-5x faster |
| Lazy initialization | Load on first access | Faster startup |
| Content caching | LRU cache with TTL | Reduced IO |
| Index preloading | Load index files first | Faster search |

### 4.2 Memory Optimizations

```python
# Preferred: Generator for large datasets
async def stream_knowledge() -> AsyncGenerator[Knowledge, None]:
    for path in paths:
        yield await load_knowledge(path)

# Preferred: Slots for frequently instantiated classes
@dataclass(slots=True)
class KnowledgeItem:
    path: str
    content: str
    metadata: dict

# Preferred: Weak references for caches
import weakref
cache: weakref.WeakValueDictionary[str, Knowledge] = weakref.WeakValueDictionary()
```

### 4.3 Query Optimizations

```python
# Preferred: Early filtering
async def search(query: str, layer: str | None = None) -> list[Knowledge]:
    # Filter by layer first (fast)
    candidates = self._index.get_by_layer(layer) if layer else self._index.all()
    
    # Then apply text search (slower)
    return [k for k in candidates if query.lower() in k.content.lower()]

# Preferred: Limit results early
async def search(query: str, limit: int = 10) -> list[Knowledge]:
    results = []
    async for item in self._search_stream(query):
        results.append(item)
        if len(results) >= limit:
            break
    return results
```

---

## 5. Common Patterns

### 5.1 Singleton Services

```python
# Preferred: Module-level singleton with lazy init
_instance: EventBus | None = None

def get_event_bus() -> EventBus:
    """Get the global EventBus instance."""
    global _instance
    if _instance is None:
        _instance = EventBus()
    return _instance

def reset_event_bus() -> None:
    """Reset for testing."""
    global _instance
    _instance = None
```

### 5.2 Configuration Access

```python
# Preferred: Get config once, use locally
def __init__(self):
    config = get_config()
    self._timeout = config.timeout.cache_lookup
    self._cache_enabled = config.features.enable_caching

# Avoid: Repeated get_config() calls
def process(self):
    if get_config().features.enable_caching:  # Don't repeat
        timeout = get_config().timeout.cache_lookup  # Don't repeat
```

### 5.3 Event Publishing

```python
# Preferred: Structured event data
await bus.publish(Event(
    type="knowledge.loaded",
    data={
        "layer": layer,
        "count": len(items),
        "duration_ms": duration * 1000,
    }
))

# Preferred: Event emission in try/finally
async def load_layer(self, layer: str) -> list[Knowledge]:
    await bus.publish(Event(type="knowledge.load.started", data={"layer": layer}))
    try:
        result = await self._do_load(layer)
        await bus.publish(Event(
            type="knowledge.load.completed",
            data={"layer": layer, "count": len(result)}
        ))
        return result
    except Exception as e:
        await bus.publish(Event(
            type="knowledge.load.failed",
            data={"layer": layer, "error": str(e)}
        ))
        raise
```

### 5.4 Protocol Implementation

```python
# Preferred: Explicit protocol compliance
class FileLoader:
    """File-based loader implementing LoaderProtocol."""
    
    async def load(self, path: str) -> str:
        """Load content from file path."""
        async with aiofiles.open(path) as f:
            return await f.read()
    
    async def exists(self, path: str) -> bool:
        """Check if path exists."""
        return Path(path).exists()

# Verify at registration time
def register_loader(loader: LoaderProtocol) -> None:
    if not isinstance(loader, LoaderProtocol):
        raise TypeError(f"Expected LoaderProtocol, got {type(loader)}")
    container.register_instance(LoaderProtocol, loader)
```

---

## 6. Project-Specific Shortcuts

### 6.1 Common File Locations

| Need | Location |
|------|----------|
| Add timeout level | `src/sage/core/timeout.py` |
| Add event type | `src/sage/core/events/events.py` |
| Add protocol | `src/sage/core/protocols.py` |
| Add exception | `src/sage/core/exceptions.py` |
| Add CLI command | `src/sage/services/cli.py` |
| Add MCP tool | `src/sage/services/mcp.py` |
| Add analyzer | `src/sage/capabilities/analyzers/` |

### 6.2 Quick Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/core/test_timeout.py -v

# Run with coverage
pytest tests/ --cov=src/sage --cov-report=html

# Type checking
mypy src/sage

# Linting
ruff check src/sage
ruff format src/sage
```

---

## Related

- `patterns.md` — AI interaction patterns
- `calibration.md` — Autonomy calibration
- `.context/conventions/` — Coding conventions
- `.junie/guidelines.md` — Project guidelines

---

*Part of SAGE Knowledge Base - AI Intelligence*
