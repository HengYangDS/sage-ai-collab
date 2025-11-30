---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~1200
---

# DI Container & EventBus

> Dependency Injection and async pub/sub messaging for SAGE Protocol

---

## Table of Contents

- [1. DI Container](#1-di-container)
- [2. EventBus](#2-eventbus)
- [3. Usage Examples](#3-usage-examples)

---

## 1. DI Container

### 1.1 Overview

The Dependency Injection Container manages service lifecycle and provides auto-wiring capabilities.

```python
# src/sage/core/di.py
"""
DI Container - Dependency Injection with lifetime management.

Features:
- Singleton, transient, and scoped lifetimes
- Auto-wiring from type hints
- YAML-driven configuration
- Protocol-based registration
"""
from typing import TypeVar, Type, Dict, Any, Optional, get_type_hints
from enum import Enum
from dataclasses import dataclass
import threading

T = TypeVar("T")


class Lifetime(Enum):
    """Service lifetime options."""
    SINGLETON = "singleton"  # One instance for entire application
    TRANSIENT = "transient"  # New instance every time
    SCOPED = "scoped"  # One instance per scope (e.g., request)


@dataclass
class Registration:
    """Service registration info."""
    interface: Type
    implementation: Type
    lifetime: Lifetime
    config_key: Optional[str] = None
```

### 1.2 DIContainer Class

```python
class DIContainer:
    """
    Dependency Injection Container.
    
    Provides:
    - Service registration with lifetime management
    - Auto-wiring based on type hints
    - Scoped instances for request-level isolation
    - YAML-based configuration support
    """

    _instance: Optional["DIContainer"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._registrations: Dict[Type, Registration] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped: Dict[str, Dict[Type, Any]] = {}
        self._config: Dict[str, Any] = {}

    @classmethod
    def get_instance(cls) -> "DIContainer":
        """Get singleton container instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def register(
        self,
        interface: Type[T],
        implementation: Type[T],
        lifetime: Lifetime = Lifetime.SINGLETON,
        config_key: Optional[str] = None
    ) -> None:
        """Register a service implementation."""
        self._registrations[interface] = Registration(
            interface=interface,
            implementation=implementation,
            lifetime=lifetime,
            config_key=config_key
        )

    def resolve(self, interface: Type[T], scope_id: Optional[str] = None) -> T:
        """Resolve a service instance."""
        if interface not in self._registrations:
            raise KeyError(f"No registration found for {interface}")

        registration = self._registrations[interface]

        # Singleton: return cached or create once
        if registration.lifetime == Lifetime.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(registration)
            return self._singletons[interface]

        # Scoped: return cached for scope or create
        if registration.lifetime == Lifetime.SCOPED:
            if scope_id is None:
                raise ValueError("Scope ID required for scoped services")
            if scope_id not in self._scoped:
                self._scoped[scope_id] = {}
            if interface not in self._scoped[scope_id]:
                self._scoped[scope_id][interface] = self._create_instance(registration)
            return self._scoped[scope_id][interface]

        # Transient: always create new
        return self._create_instance(registration)
```

### 1.3 Lifetime Types

| Lifetime    | Description                         | Use Case                           |
|-------------|-------------------------------------|------------------------------------|
| `singleton` | One instance for entire application | EventBus, Config, Cache            |
| `transient` | New instance per resolution         | Request handlers, DTOs             |
| `scoped`    | One instance per scope (request)    | Database sessions, request context |

---

## 2. EventBus

### 2.1 Overview

Async pub/sub message broker with S.A.G.E. aligned event channels.

| Channel      | Purpose                      |
|--------------|------------------------------|
| `source.*`   | Knowledge sourcing events    |
| `analyze.*`  | Processing & analysis events |
| `generate.*` | Multi-channel output events  |
| `evolve.*`   | Metrics & optimization events|

### 2.2 Event Types

```python
# src/sage/core/events/types.py
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class EventType(str, Enum):
    """Standard event types for SAGE."""
    # Loader events
    PRE_LOAD = "loader.pre_load"
    POST_LOAD = "loader.post_load"
    LOAD_ERROR = "loader.error"

    # Knowledge events
    PRE_SEARCH = "knowledge.pre_search"
    POST_SEARCH = "knowledge.post_search"

    # Timeout events
    TIMEOUT = "timeout.triggered"
    CIRCUIT_OPEN = "timeout.circuit_open"
    CIRCUIT_CLOSE = "timeout.circuit_close"


@dataclass
class Event:
    """Base event class."""
    type: EventType | str
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def cancel(self) -> None:
        """Cancel event propagation."""
        self._cancelled = True
```

### 2.3 EventBus Implementation

```python
# src/sage/core/events/bus.py
"""
EventBus - Async pub/sub message broker (S.A.G.E. aligned).

Features:
- Async and sync handler support
- Priority-based execution order
- Event filtering per subscription
- Error isolation between handlers
- Timeout protection for handlers
- Wildcard matching (e.g., "source.*")
"""
from typing import Callable, Awaitable, Any
from collections import defaultdict
import asyncio


class EventBus:
    """Async event bus with wildcard support."""

    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(
        self,
        event_pattern: str,
        handler: Callable,
        priority: int = 0
    ) -> None:
        """Subscribe to events matching pattern."""
        self._handlers[event_pattern].append((priority, handler))
        self._handlers[event_pattern].sort(key=lambda x: -x[0])

    async def publish(self, event: Event) -> Event:
        """Publish event to all matching handlers."""
        for pattern, handlers in self._handlers.items():
            if self._matches(pattern, event.type):
                for _, handler in handlers:
                    if event.is_cancelled:
                        break
                    await self._invoke(handler, event)
        return event
```

---

## 3. Usage Examples

### 3.1 DI Container Usage

```python
from sage.core.di import get_container
from sage.core.protocols import SourceProtocol, AnalyzeProtocol

# Get container
container = get_container()

# Resolve services
loader = container.resolve(SourceProtocol)
analyzer = container.resolve(AnalyzeProtocol)

# Use services
async def main():
    result = await loader.source(SourceRequest(layers=["core"]))
    results = await analyzer.search("autonomy")
```

### 3.2 EventBus Usage

```python
from sage.core.events import EventBus, Event, EventType, LoadEvent

bus = EventBus()

# Subscribe with priority
@bus.subscribe("source.*", priority=10)
async def on_source_event(event: Event):
    print(f"Source event: {event.type}")

# Wildcard subscription
bus.subscribe("source.*", on_any_source_event)

# Publish event
async def main():
    event = LoadEvent(type=EventType.PRE_LOAD, layer="core")
    result = await bus.publish(event)
```

---

## Related

- `docs/design/02-sage-protocol.md` — Protocol overview
- `docs/design/02b-bootstrap.md` — Application bootstrap
- `.knowledge/practices/engineering/dependency_injection.md` — DI patterns

---

*Part of SAGE Knowledge Base*
