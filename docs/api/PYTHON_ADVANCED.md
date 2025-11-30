---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~700
---

# Python API Advanced Reference

> Search, events, enums, exceptions, and usage examples for SAGE Python API

---

## Table of Contents

- [1. Search API](#1-search-api)
- [2. Events](#2-events)
- [3. Enums](#3-enums)
- [4. Exceptions](#4-exceptions)
- [5. Context Managers](#5-context-managers)
- [6. Usage Examples](#6-usage-examples)

---

## 1. Search API

### 1.1 KnowledgeSearcher

Search the knowledge base.

```python
from sage.core.search import KnowledgeSearcher

searcher = KnowledgeSearcher()
```

#### search

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

| Parameter    | Type  | Default  | Description     |
|--------------|-------|----------|-----------------|
| `query`      | `str` | required | Search query    |
| `limit`      | `int` | `10`     | Max results     |
| `layer`      | `str` | `None`   | Filter by layer |
| `timeout_ms` | `int` | `2000`   | Timeout in ms   |

**Returns:** `SearchResult`

### 1.2 SearchResult

Search result object.

```python
@dataclass
class SearchResult:
    results: list[SearchHit]
    total: int
    query_time_ms: int
```

### 1.3 SearchHit

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

## 2. Events

### 2.1 EventBus

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

## 3. Enums

### 3.1 TaskType

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

### 3.2 TimeoutLevel

Timeout levels for operations.

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

## 4. Exceptions

### 4.1 SAGEError

Base exception for all SAGE errors.

```python
from sage.core.exceptions import SAGEError

try:
    result = await loader.load("invalid")
except SAGEError as e:
    print(f"Error: {e}")
```

### 4.2 TimeoutError

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

### 4.3 NotFoundError

Raised when content is not found.

```python
from sage.core.exceptions import NotFoundError

try:
    result = await loader.load("core", topic="nonexistent")
except NotFoundError as e:
    print(f"Not found: {e.path}")
```

---

## 5. Context Managers

### 5.1 timeout_context

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

## 6. Usage Examples

### 6.1 Basic Loading

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

### 6.2 Task-Based Loading

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

### 6.3 Search with Filters

```python
from sage.core.search import KnowledgeSearcher

searcher = KnowledgeSearcher()

# Basic search
results = await searcher.search("timeout")

# Search with filters
results = await searcher.search(
    query="python",
    layer="guidelines",
    limit=5
)

for hit in results.results:
    print(f"{hit.title}: {hit.snippet}")
```

### 6.4 Event-Driven Architecture

```python
from sage.core.events import EventBus, Event
from sage.core.loader import KnowledgeLoader

bus = EventBus()
loader = KnowledgeLoader(event_bus=bus)

@bus.subscribe("knowledge.loaded")
async def log_load(event: Event):
    print(f"Loaded {event.data['layer']} in {event.data['load_time_ms']}ms")

@bus.subscribe("knowledge.error")
async def handle_error(event: Event):
    print(f"Error: {event.data['error']}")

# Loading will trigger events
result = await loader.load("core")
```

---

## Related

- `docs/api/python.md` — Python API basics
- `docs/api/index.md` — API overview
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout patterns

---

*Part of SAGE Knowledge Base*
