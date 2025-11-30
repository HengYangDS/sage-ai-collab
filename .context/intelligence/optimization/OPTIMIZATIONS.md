# SAGE Project Optimizations

> SAGE-specific optimizations, shortcuts, and code patterns

---

## Generic References

For comprehensive guides on general development practices, see:

| Topic                | Reference                                                      |
|:---------------------|:---------------------------------------------------------------|
| **Code Patterns**    | `.knowledge/practices/engineering/patterns.md`                 |
| **Testing Strategy** | `.knowledge/practices/engineering/testing_strategy.md`         |
| **Documentation**    | `.knowledge/practices/documentation/`                          |
| **Performance**      | `.knowledge/frameworks/performance/optimization_strategies.md` |
| **Caching**          | `.knowledge/frameworks/performance/caching_patterns.md`        |

---

## Table of Contents

- [1. SAGE Code Preferences](#1-sage-code-preferences)
- [2. Performance Optimizations](#2-performance-optimizations)
- [3. Common Patterns](#3-common-patterns)
- [4. Project Shortcuts](#4-project-shortcuts)

---

## 1. SAGE Code Preferences

### 1.1 Import Organization (SAGE-specific)

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

### 1.2 Test Coverage Goals

| Layer        | Target    | Focus                            |
|:-------------|:----------|:---------------------------------|
| Core         | 90%+      | All public APIs, error paths     |
| Services     | 80%+      | Integration points, CLI commands |
| Capabilities | 80%+      | Analyzer logic, edge cases       |
| Integration  | Key paths | End-to-end workflows             |

---

## 2. Performance Optimizations

### 2.1 Loading Optimizations

| Optimization        | Implementation                        | Impact         |
|:--------------------|:--------------------------------------|:---------------|
| Parallel loading    | `asyncio.gather()` for multiple files | 3-5x faster    |
| Lazy initialization | Load on first access                  | Faster startup |
| Content caching     | LRU cache with TTL                    | Reduced IO     |
| Index preloading    | Load index files first                | Faster search  |

### 2.2 Query Optimizations

```python
# Preferred: Early filtering in SAGE
async def search(query: str, layer: str | None = None) -> list[Knowledge]:
    # Filter by layer first (fast)
    candidates = self._index.get_by_layer(layer) if layer else self._index.all()
    # Then apply text search (slower)
    return [k for k in candidates if query.lower() in k.content.lower()]
```

---

## 3. Common Patterns

### 3.1 Singleton Services

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

### 3.2 Configuration Access

```python
# Preferred: Get config once, use locally
def __init__(self):
    config = get_config()
    self._timeout = config.timeout.cache_lookup
    self._cache_enabled = config.features.enable_caching

# Avoid: Repeated get_config() calls
```

### 3.3 Event Publishing

```python
# Preferred: Event emission in try/finally
async def load_layer(self, layer: str) -> list[Knowledge]:
    await bus.publish(Event(type="knowledge.load.started", data={"layer": layer}))
    try:
        result = await self._do_load(layer)
        await bus.publish(Event(type="knowledge.load.completed", data={"layer": layer, "count": len(result)}))
        return result
    except Exception as e:
        await bus.publish(Event(type="knowledge.load.failed", data={"layer": layer, "error": str(e)}))
        raise
```

### 3.4 Protocol Implementation

```python
# Preferred: Explicit protocol compliance
class FileLoader:
    """File-based loader implementing LoaderProtocol."""

    async def load(self, path: str) -> str:
        async with aiofiles.open(path) as f:
            return await f.read()

    async def exists(self, path: str) -> bool:
        return Path(path).exists()
```

---

## 4. Project Shortcuts

### 4.1 Common File Locations

| Need              | Location                           |
|:------------------|:-----------------------------------|
| Add timeout level | `src/sage/core/timeout.py`         |
| Add event type    | `src/sage/core/events/events.py`   |
| Add protocol      | `src/sage/core/protocols.py`       |
| Add exception     | `src/sage/core/exceptions.py`      |
| Add CLI command   | `src/sage/services/cli.py`         |
| Add MCP tool      | `src/sage/services/mcp.py`         |
| Add analyzer      | `src/sage/capabilities/analyzers/` |

### 4.2 Quick Commands

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

- `.knowledge/practices/engineering/patterns.md` — Generic code patterns
- `.knowledge/frameworks/performance/` — Performance optimization guides
- `.context/intelligence/calibration/patterns.md` — SAGE AI interaction patterns
- `.context/intelligence/calibration/calibration.md` — Autonomy calibration
- `.context/conventions/` — SAGE coding conventions

---

*Last updated: 2025-11-30*
*AI Collaboration Knowledge Base*
