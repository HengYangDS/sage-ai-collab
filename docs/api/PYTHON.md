---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---

# Python API Reference

> SAGE Knowledge Base Python Library Documentation

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Installation](#2-installation)
- [3. Quick Start](#3-quick-start)
- [4. Core Classes](#4-core-classes)
- [5. Configuration](#5-configuration)
- [6. Advanced Topics](#6-advanced-topics)

---

## 1. Overview

The SAGE Python API provides programmatic access to the knowledge base. It supports both synchronous and asynchronous operations with built-in timeout protection.

---

## 2. Installation

```bash
# Basic installation
pip install sage-kb

# With all dependencies
pip install sage-kb[all]
```

---

## 3. Quick Start

```python
from sage.core.loader import KnowledgeLoader
from sage.core.config import get_config

# Initialize loader
loader = KnowledgeLoader()

# Load core knowledge (sync)
result = loader.load_sync("core", timeout_ms=2000)
print(result.content)

# Load with async
import asyncio

async def main():
    result = await loader.load("core", timeout_ms=2000)
    print(result.content)

asyncio.run(main())
```

---

## 4. Core Classes

### 4.1 KnowledgeLoader

Main class for loading knowledge from the knowledge base.

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader(config=None)
```

**Parameters:**

| Parameter | Type         | Description                   |
|-----------|--------------|-------------------------------|
| `config`  | `SAGEConfig` | Optional configuration object |

#### load

Load knowledge asynchronously.

```python
async def load(
    layer: str,
    topic: str | None = None,
    timeout_ms: int = 2000
) -> LoadResult
```

**Parameters:**

| Parameter    | Type  | Default  | Description     |
|--------------|-------|----------|-----------------|
| `layer`      | `str` | required | Knowledge layer |
| `topic`      | `str` | `None`   | Specific topic  |
| `timeout_ms` | `int` | `2000`   | Timeout in ms   |

**Returns:** `LoadResult`

#### load_sync

Synchronous wrapper for `load`.

```python
def load_sync(
    layer: str,
    topic: str | None = None,
    timeout_ms: int = 2000
) -> LoadResult
```

#### load_core

Load core knowledge layer.

```python
async def load_core(timeout_ms: int = 2000) -> LoadResult
```

#### load_for_task

Load context optimized for a specific task type.

```python
async def load_for_task(
    task_type: TaskType,
    token_budget: int = 4000
) -> LoadResult
```

### 4.2 LoadResult

Result object from loading operations.

```python
@dataclass
class LoadResult:
    content: str
    metadata: LoadMetadata
```

### 4.3 LoadMetadata

Metadata about load operation.

```python
@dataclass
class LoadMetadata:
    layer: str
    files_loaded: int
    load_time_ms: int
    token_count: int
    from_cache: bool
```

---

## 5. Configuration

### 5.1 SAGEConfig

Configuration object for SAGE operations.

```python
from sage.core.config import SAGEConfig, get_config

# Load from default location
config = get_config()

# Load from custom path
config = SAGEConfig.from_file("custom/config.yaml")
```

**Key Attributes:**

| Attribute             | Type   | Default | Description     |
|-----------------------|--------|---------|-----------------|
| `knowledge_base_path` | `str`  | `"."`   | KB root path    |
| `timeout_t1`          | `int`  | `100`   | T1 timeout (ms) |
| `timeout_t2`          | `int`  | `500`   | T2 timeout (ms) |
| `timeout_t3`          | `int`  | `2000`  | T3 timeout (ms) |
| `timeout_t4`          | `int`  | `5000`  | T4 timeout (ms) |
| `timeout_t5`          | `int`  | `10000` | T5 timeout (ms) |
| `cache_enabled`       | `bool` | `True`  | Enable caching  |

---

## 6. Advanced Topics

For advanced features, see [Python API Advanced Reference](python_advanced.md):

| Topic            | Description                        |
|------------------|------------------------------------|
| Search API       | KnowledgeSearcher and SearchResult |
| Events           | EventBus pub/sub system            |
| Enums            | TaskType and TimeoutLevel          |
| Exceptions       | SAGEError, TimeoutError, etc.      |
| Context Managers | timeout_context                    |
| Usage Examples   | Complete code examples             |

---

## Related

- `docs/api/python_advanced.md` — Advanced Python API
- `docs/api/index.md` — API overview
- `docs/api/mcp.md` — MCP protocol reference
- `docs/guides/quickstart.md` — Quick start guide

---

*Part of SAGE Knowledge Base*
