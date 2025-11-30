# SAGE Code Patterns

> Project-specific code patterns and idioms for SAGE Knowledge Base

---

## Table of Contents

- [1. Dependency Injection](#1-dependency-injection)
- [2. Event Bus](#2-event-bus)
- [3. Timeout Handling](#3-timeout-handling)
- [4. Error Handling](#4-error-handling)
- [5. Protocol Implementation](#5-protocol-implementation)
- [6. Configuration](#6-configuration)
- [7. Async Patterns](#7-async-patterns)

---

## 1. Dependency Injection

### 1.1 Container Access

```python
from sage.core.di import get_container, DIContainer, Lifetime

# Get global container instance
container = get_container()
```

### 1.2 Service Registration

```python
# Register with interface and implementation
container.register(
    interface=SourceProtocol,
    implementation=KnowledgeSource,
    lifetime=Lifetime.SINGLETON
)

# Register existing instance
container.register_instance(ConfigProtocol, config)

# Register with factory
container.register_factory(
    interface=AnalyzerProtocol,
    factory=lambda: CodeAnalyzer(get_config()),
    lifetime=Lifetime.TRANSIENT
)
```

### 1.3 Lifetime Selection

| Lifetime    | Use Case                         | Example                            |
|:------------|:---------------------------------|:-----------------------------------|
| `SINGLETON` | Shared state, expensive creation | `EventBus`, `ConfigManager`        |
| `TRANSIENT` | Stateless, lightweight           | `Validator`, `Formatter`           |
| `SCOPED`    | Per-request/session              | `SessionContext`, `RequestHandler` |

### 1.4 Service Resolution

```python
# Resolve service (raises if not found)
source = container.resolve(SourceProtocol)

# Try resolve (returns None if not found)
analyzer = container.try_resolve(AnalyzerProtocol)

# Scoped resolution
with container.create_scope("request-123") as scope:
    handler = scope.resolve(RequestHandler)
```

### 1.5 Configuration-Driven Registration

```yaml
# In sage.yaml
services:
  knowledge_loader:
    class: sage.core.loader.KnowledgeLoader
    lifetime: singleton
    config_key: loader
```

---

## 2. Event Bus

### 2.1 Bus Access

```python
from sage.core.events import get_event_bus, Event, EventType

# Get global event bus instance
bus = get_event_bus()
```

### 2.2 Publishing Events

```python
from sage.core.events import Event

# Create and publish event
event = Event(
    type=EventType.KNOWLEDGE_LOADED,
    data={"layer": "core", "count": 42}
)
await bus.publish(event)

# Or use string type
event = Event(type="knowledge.loaded", data={...})
```

### 2.3 Subscribing to Events

```python
# Subscribe with async handler
async def on_knowledge_loaded(event: Event) -> None:
    layer = event.data.get("layer")
    logger.info(f"Layer {layer} loaded")


subscription = bus.subscribe(
    event_pattern=EventType.KNOWLEDGE_LOADED,
    handler=on_knowledge_loaded,
    priority=100,  # Lower = higher priority
    timeout_ms=5000
)

# Wildcard subscription
bus.subscribe("knowledge.*", handle_all_knowledge_events)
```

### 2.4 Unsubscribing

```python
# Unsubscribe by ID
bus.unsubscribe(subscription.id)
```

### 2.5 Event Patterns

| Pattern            | Matches                                 |
|:-------------------|:----------------------------------------|
| `knowledge.loaded` | Exact match                             |
| `knowledge.*`      | `knowledge.loaded`, `knowledge.updated` |
| `*.loaded`         | `knowledge.loaded`, `config.loaded`     |
| `*`                | All events                              |

---

## 3. Timeout Handling

### 3.1 Timeout Manager Usage

```python
from sage.core.timeout import TimeoutManager, TimeoutLevel

manager = TimeoutManager()

# Execute with timeout
result = await manager.execute_with_timeout(
    coro=load_knowledge(),
    level=TimeoutLevel.T3_LAYER,
    fallback=partial_knowledge
)
```

### 3.2 Timeout Levels

```python
from sage.core.timeout import TimeoutLevel

# Use appropriate level for operation scope
TimeoutLevel.T1_CACHE  # 100ms - Cache lookup
TimeoutLevel.T2_FILE  # 500ms - Single file
TimeoutLevel.T3_LAYER  # 2s    - Full layer
TimeoutLevel.T4_FULL  # 5s    - Complete KB
TimeoutLevel.T5_COMPLEX  # 10s   - Analysis
```

### 3.3 Timeout Decorator Pattern

```python
from sage.core.timeout import with_timeout


@with_timeout(TimeoutLevel.T2_FILE)
async def load_file(path: str) -> str:
    async with aiofiles.open(path) as f:
        return await f.read()
```

### 3.4 Fallback Strategy

```python
# Always provide fallback for graceful degradation
async def load_with_fallback() -> Knowledge:
    try:
        return await manager.execute_with_timeout(
            coro=full_load(),
            level=TimeoutLevel.T4_FULL,
            fallback=None
        )
    except TimeoutError:
        return await load_core_only()  # Emergency fallback
```

---

## 4. Error Handling

### 4.1 Exception Hierarchy

```python
from sage.core.exceptions import (
    SAGEError,  # Base for all SAGE errors
    ConfigurationError,  # Config-related errors
    LoadError,  # Knowledge loading errors
    TimeoutError,  # Timeout exceeded
    ValidationError,  # Input validation errors
)
```

### 4.2 Error Handling Pattern

```python
from sage.core.exceptions import SAGEError, LoadError


async def safe_operation() -> Result:
    try:
        return await risky_operation()
    except LoadError as e:
        logger.warning(f"Load failed: {e}", exc_info=True)
        return fallback_result()
    except SAGEError as e:
        logger.error(f"SAGE error: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise SAGEError(f"Operation failed: {e}") from e
```

### 4.3 Error Context Pattern

```python
# Add context to errors
try:
    result = await process(data)
except Exception as e:
    raise LoadError(
        f"Failed to process {data.name}"
    ) from e
```

### 4.4 Result Pattern (Optional)

```python
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def is_success(self) -> bool:
        return self.error is None
```

---

## 5. Protocol Implementation

### 5.1 Defining Protocols

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class SourceProtocol(Protocol):
    """Protocol for knowledge sourcing."""

    async def load(self, path: str) -> Knowledge:
        """Load knowledge from path."""
        ...

    async def search(self, query: str) -> list[Knowledge]:
        """Search for knowledge."""
        ...
```

### 5.2 Implementing Protocols

```python
class FileSource:
    """File-based knowledge source."""

    async def load(self, path: str) -> Knowledge:
        content = await read_file(path)
        return Knowledge(content=content)

    async def search(self, query: str) -> list[Knowledge]:
        # Implementation
        ...


# Type checking verifies protocol compliance
source: SourceProtocol = FileSource()
```

### 5.3 Protocol Composition

```python
class FullSourceProtocol(SourceProtocol, CacheableProtocol):
    """Combined protocol for full-featured sources."""
    pass
```

---

## 6. Configuration

### 6.1 Config Access

```python
from sage.core.config import get_config, SAGEConfig

# Get global config
config = get_config()

# Access values
timeout = config.timeout.cache_lookup
layers = config.knowledge.layers
```

### 6.2 Environment Override

```python
# Environment variables override YAML config
# Pattern: SAGE__SECTION__KEY

# YAML: timeout.cache_lookup: 100
# Env:  SAGE__TIMEOUT__CACHE_LOOKUP=200
```

### 6.3 Config Validation

```python
from pydantic import BaseModel, validator


class TimeoutConfig(BaseModel):
    cache_lookup: int = 100
    file_read: int = 500

    @validator("cache_lookup")
    def validate_cache_lookup(cls, v):
        if v < 10:
            raise ValueError("cache_lookup must be >= 10ms")
        return v
```

---

## 7. Async Patterns

### 7.1 Async Context Manager

```python
class AsyncResource:
    async def __aenter__(self) -> "AsyncResource":
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.cleanup()


# Usage
async with AsyncResource() as resource:
    await resource.process()
```

### 7.2 Concurrent Operations

```python
import asyncio


async def load_all_layers() -> list[Knowledge]:
    tasks = [
        load_layer("core"),
        load_layer("frameworks"),
        load_layer("practices"),
    ]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

### 7.3 Semaphore for Rate Limiting

```python
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent


async def rate_limited_load(path: str) -> Knowledge:
    async with semaphore:
        return await load_file(path)
```

### 7.4 Async Generator

```python
async def stream_knowledge() -> AsyncGenerator[Knowledge, None]:
    for path in knowledge_paths:
        yield await load_knowledge(path)


# Usage
async for knowledge in stream_knowledge():
    process(knowledge)
```

---

## 8. Logging Patterns

### 8.1 Structured Logging

```python
import structlog

logger = structlog.get_logger(__name__)

# Log with context
logger.info(
    "knowledge_loaded",
    layer="core",
    count=42,
    duration_ms=150
)
```

### 8.2 Context Binding

```python
# Bind context for all subsequent logs
logger = logger.bind(request_id="abc-123")
logger.info("processing_started")  # Includes request_id
logger.info("processing_completed")  # Includes request_id
```

---

## 9. Testing Patterns

### 9.1 Fixture for DI

```python
import pytest
from sage.core.di import DIContainer


@pytest.fixture
def container():
    container = DIContainer()
    yield container
    container.clear()
```

### 9.2 Mock Event Bus

```python
@pytest.fixture
def mock_bus():
    bus = get_event_bus()
    yield bus
    bus.clear()
```

### 9.3 Async Test

```python
import pytest


@pytest.mark.asyncio
async def test_async_load():
    result = await load_knowledge("test.md")
    assert result is not None
```

---

## Related

- `.context/conventions/naming.md` — Naming conventions
- `.context/conventions/file_structure.md` — File organization
- `docs/design/01-architecture.md` — Architecture details
- `src/sage/core/` — Core implementations

---

*AI Collaboration Knowledge Base*
