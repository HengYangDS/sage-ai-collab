# Python API Reference

> SAGE Knowledge Base Python Library Documentation

---

## Overview

The SAGE Python API provides programmatic access to the knowledge base. It supports both synchronous and asynchronous operations with built-in timeout protection.

---

## Installation

```bash
# Basic installation
pip install sage-kb

# With all dependencies
pip install sage-kb[all]
```

---

## Quick Start

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

## Core Classes

### KnowledgeLoader

Main class for loading knowledge from the knowledge base.

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader(config=None)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `SAGEConfig` | Optional configuration object |

#### Methods

##### load

Load knowledge asynchronously.

```python
async def load(
    layer: str,
    topic: str | None = None,
    timeout_ms: int = 2000
) -> LoadResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `layer` | `str` | required | Knowledge layer |
| `topic` | `str` | `None` | Specific topic |
| `timeout_ms` | `int` | `2000` | Timeout in ms |

**Returns:** `LoadResult`

##### load_sync

Synchronous wrapper for `load`.

```python
def load_sync(
    layer: str,
    topic: str | None = None,
    timeout_ms: int = 2000
) -> LoadResult
```

##### load_core

Load core knowledge layer.

```python
async def load_core(timeout_ms: int = 2000) -> LoadResult
```

##### load_for_task

Load knowledge optimized for a specific task type.

```python
async def load_for_task(
    task_type: TaskType,
    token_budget: int = 4000,
    timeout_ms: int = 5000
) -> LoadResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task_type` | `TaskType` | required | Type of task |
| `token_budget` | `int` | `4000` | Max tokens |
| `timeout_ms` | `int` | `5000` | Timeout in ms |

---

### LoadResult

Result object returned by loader methods.

```python
@dataclass
class LoadResult:
    content: str
    metadata: LoadMetadata
    complete: bool
    error: str | None
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `content` | `str` | Loaded content |
| `metadata` | `LoadMetadata` | Load metadata |
| `complete` | `bool` | Whether load completed |
| `error` | `str \| None` | Error message if any |

---

### LoadMetadata

Metadata about the load operation.

```python
@dataclass
class LoadMetadata:
    layer: str
    files_loaded: int
    load_time_ms: int
    from_cache: bool
    token_count: int
```

---

### SAGEConfig

Configuration class for SAGE.

```python
from sage.core.config import SAGEConfig, get_config

# Get default config
config = get_config()

# Custom config
config = SAGEConfig(
    knowledge_base_path="./content",
    timeout_t3=2000,
    cache_enabled=True
)
```

**Key Attributes:**

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `knowledge_base_path` | `str` | `"."` | KB root path |
| `timeout_t1` | `int` | `100` | T1 timeout (ms) |
| `timeout_t2` | `int` | `500` | T2 timeout (ms) |
| `timeout_t3` | `int` | `2000` | T3 timeout (ms) |
| `timeout_t4` | `int` | `5000` | T4 timeout (ms) |
| `timeout_t5` | `int` | `10000` | T5 timeout (ms) |
| `cache_enabled` | `bool` | `True` | Enable caching |

---

## Search API

### KnowledgeSearcher

Search the knowledge base.

```python
from sage.core.search import KnowledgeSearcher

searcher = KnowledgeSearcher()
```

#### Methods

##### search

Search for content.

```python
async def search(
    query: str,
    limit: int = 10,
    layer: str | None = None,
    timeout_ms: int = 2000
) -> SearchResult
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | required | Search query |
| `limit` | `int` | `10` | Max results |
| `layer` | `str` | `None` | Filter by layer |
| `timeout_ms` | `int` | `2000` | Timeout in ms |

**Returns:** `SearchResult`

---

### SearchResult

Search result object.

```python
@dataclass
class SearchResult:
    results: list[SearchHit]
    total: int
    query_time_ms: int
```

### SearchHit

Individual search hit.

```python
@dataclass
class SearchHit:
    path: str
    title: str
    snippet: str
    score: float
```

---

## Events

### EventBus

Pub/sub system for decoupled communication.

```python
from sage.core.events import EventBus, Event

bus = EventBus()

# Subscribe to events
@bus.subscribe("knowledge.loaded")
async def on_load(event: Event):
    print(f"Loaded: {event.data}")

# Publish events
await bus.publish(Event(
    type="knowledge.loaded",
    data={"layer": "core"}
))
```

---

## Enums

### TaskType

Task types for context loading.

```python
from sage.domain.knowledge import TaskType

class TaskType(Enum):
    CODING = "coding"
    DEBUGGING = "debugging"
    REVIEWING = "reviewing"
    PLANNING = "planning"
    DOCUMENTING = "documenting"
```

### TimeoutLevel

Timeout levels.

```python
from sage.core.timeout import TimeoutLevel

class TimeoutLevel(Enum):
    T1 = 100    # Cache lookup
    T2 = 500    # Single file
    T3 = 2000   # Layer load
    T4 = 5000   # Full KB
    T5 = 10000  # Complex analysis
```

---

## Exceptions

### SAGEError

Base exception for all SAGE errors.

```python
from sage.core.exceptions import SAGEError

try:
    result = await loader.load("invalid")
except SAGEError as e:
    print(f"Error: {e}")
```

### TimeoutError

Raised when operation exceeds timeout.

```python
from sage.core.exceptions import TimeoutError

try:
    result = await loader.load("all", timeout_ms=100)
except TimeoutError as e:
    print(f"Timeout at level {e.level}: {e.elapsed_ms}ms")
    # Use fallback content
    print(e.partial_result)
```

### NotFoundError

Raised when content is not found.

```python
from sage.core.exceptions import NotFoundError

try:
    result = await loader.load("core", topic="nonexistent")
except NotFoundError as e:
    print(f"Not found: {e.path}")
```

---

## Context Managers

### timeout_context

Context manager for timeout protection.

```python
from sage.core.timeout import timeout_context

async with timeout_context(TimeoutLevel.T3) as ctx:
    result = await long_operation()
    if ctx.remaining_ms < 100:
        # Running low on time
        return partial_result
```

---

## Usage Examples

### Basic Loading

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()

# Load different layers
core = await loader.load("core")
guidelines = await loader.load("guidelines")
frameworks = await loader.load("frameworks")

# Load specific topic
python_guide = await loader.load("guidelines", topic="python")
```

### Task-Based Loading

```python
from sage.core.loader import KnowledgeLoader
from sage.domain.knowledge import TaskType

loader = KnowledgeLoader()

# Load context for coding task
context = await loader.load_for_task(
    task_type=TaskType.CODING,
    token_budget=4000
)

print(f"Loaded {context.metadata.token_count} tokens")
```

### Search with Filters

```python
from sage.core.search import KnowledgeSearcher

searcher = KnowledgeSearcher()

# Basic search
results = await searcher.search("timeout")

# Search specific layer
results = await searcher.search(
    "pattern",
    layer="frameworks",
    limit=5
)

for hit in results.results:
    print(f"{hit.title}: {hit.snippet}")
```

### Error Handling

```python
from sage.core.loader import KnowledgeLoader
from sage.core.exceptions import SAGEError, TimeoutError

loader = KnowledgeLoader()

try:
    result = await loader.load("all", timeout_ms=1000)
except TimeoutError as e:
    # Use partial result
    print(f"Partial load: {e.partial_result.content[:100]}...")
except SAGEError as e:
    print(f"Error: {e}")
```

---

## Related

- [API Index](index.md) — API overview
- [CLI Reference](cli.md) — CLI documentation
- [MCP Protocol](mcp.md) — MCP server
- `docs/design/01-architecture.md` — Architecture design

---

*SAGE Knowledge Base - Python API Reference*
