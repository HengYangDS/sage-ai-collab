# ADR-0005: Event Bus Architecture

> Architecture Decision Record for SAGE Knowledge Base

---

## Table of Contents

- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Alternatives Considered](#alternatives-considered)
- [Consequences](#consequences)
- [Implementation](#implementation)
- [Related](#related)

---

## Status

**Accepted** | Date: 2025-11-28

---

## Context

SAGE Knowledge Base requires decoupled communication between layers:

1. Core should not depend on Services or Capabilities
2. Services should not directly depend on each other
3. Operations should be observable without tight coupling
4. Support for async event handlers
5. Enable plugin integration through events

### Requirements

- Async-first event handling
- Pattern-based subscriptions (wildcards)
- Priority-based handler ordering
- Timeout protection for handlers
- Error isolation between handlers

---

## Decision

Implement an **async Event Bus** with pattern matching and priority-based dispatch.

### Event Bus Design

```python
class EventBus:
    """Async pub/sub message broker."""

    def subscribe(self, pattern, handler, priority, timeout_ms): ...

    def unsubscribe(self, subscription_id): ...

    async def publish(self, event): ...
```

### Event Structure

```python
@dataclass
class Event:
    type: str  # e.g., "knowledge.loaded"
    data: dict  # Event payload
    timestamp: float  # When event occurred
    source: str | None  # Origin identifier
```

### Pattern Matching

| Pattern            | Matches                                       |
|:-------------------|:----------------------------------------------|
| `knowledge.loaded` | Exact match only                              |
| `knowledge.*`      | `knowledge.loaded`, `knowledge.updated`, etc. |
| `*.loaded`         | `knowledge.loaded`, `config.loaded`, etc.     |
| `*`                | All events                                    |

---

## Alternatives Considered

### Alternative 1: Direct Method Calls

Services call each other directly.

- **Pros**: Simple, synchronous
- **Cons**: Tight coupling, circular dependencies
- **Rejected**: Violates layer isolation

### Alternative 2: Callback Registry

Simple callback list without pattern matching.

- **Pros**: Very simple
- **Cons**: No flexibility, verbose subscriptions
- **Rejected**: Need pattern matching for extensibility

### Alternative 3: External Message Queue (Redis, RabbitMQ)

Use external messaging infrastructure.

- **Pros**: Scalable, persistent, distributed
- **Cons**: Heavy dependency, deployment complexity
- **Rejected**: Overkill for single-process knowledge base

---

## Consequences

### Positive

1. **Decoupling**: Publishers don't know subscribers
2. **Extensibility**: New handlers without modifying publishers
3. **Observability**: Easy to log/monitor all events
4. **Async-native**: Non-blocking event processing
5. **Pattern flexibility**: Subscribe to event categories

### Negative

1. **Indirection**: Harder to trace event flow
2. **Ordering**: Handler order may be non-obvious
3. **Error handling**: Failures in handlers need careful handling

### Mitigations

1. **Event logging**: Log all events for traceability
2. **Priority system**: Explicit handler ordering
3. **Error isolation**: One handler failure doesn't break others
4. **Timeout protection**: Handlers can't hang indefinitely

---

## Implementation

### Publishing Events

```python
from sage.core.events import get_event_bus, Event

bus = get_event_bus()

# Publish event
event = Event(
    type="knowledge.loaded",
    data={"layer": "core", "count": 42}
)
await bus.publish(event)
```

### Subscribing to Events

```python
# Simple subscription
async def on_loaded(event: Event) -> None:
    print(f"Loaded: {event.data}")


bus.subscribe("knowledge.loaded", on_loaded)

# With priority and timeout
bus.subscribe(
    event_pattern="knowledge.*",
    handler=log_all_knowledge_events,
    priority=10,  # Lower = higher priority
    timeout_ms=1000  # Handler timeout
)

# Wildcard subscription
bus.subscribe("*", audit_logger, priority=1000)
```

### Handler Priority

```
Priority 10:  Security check
Priority 50:  Business logic
Priority 100: Default handlers (default)
Priority 500: Logging/auditing
Priority 1000: Cleanup
```

Lower priority number = earlier execution.

### Error Handling

```python
# Custom error handler
def on_handler_error(error, event, subscription):
    logger.error(
        "Handler failed",
        error=str(error),
        event_type=event.type,
        handler=subscription.handler.__name__
    )


bus = EventBus(error_handler=on_handler_error)
```

### SAGE Protocol Events

```python
# Standard event types for SAGE phases
class EventType(str, Enum):
    # Source events
    SOURCE_STARTED = "source.started"
    SOURCE_COMPLETED = "source.completed"
    SOURCE_FAILED = "source.failed"

    # Analyze events
    ANALYZE_STARTED = "analyze.started"
    ANALYZE_COMPLETED = "analyze.completed"

    # Generate events
    GENERATE_STARTED = "generate.started"
    GENERATE_COMPLETED = "generate.completed"

    # Evolve events
    EVOLVE_METRICS = "evolve.metrics"

    # Knowledge events
    KNOWLEDGE_LOADED = "knowledge.loaded"
    KNOWLEDGE_UPDATED = "knowledge.updated"
```

### Testing with EventBus

```python
@pytest.fixture
def event_bus():
    bus = get_event_bus()
    yield bus
    bus.clear()  # Clean up subscriptions


async def test_event_publishing(event_bus):
    received = []

    async def handler(event):
        received.append(event)

    event_bus.subscribe("test.*", handler)
    await event_bus.publish(Event(type="test.event", data={}))

    assert len(received) == 1
```

---

## Related

- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Layer architecture
- `.context/decisions/ADR_0002_SAGE_PROTOCOL.md` — SAGE phase events
- `.context/conventions/code_patterns.md` — EventBus patterns
- `src/sage/core/events/` — Implementation

---

*AI Collaboration Knowledge Base*
