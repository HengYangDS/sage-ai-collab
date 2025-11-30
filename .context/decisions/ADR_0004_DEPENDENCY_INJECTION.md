# ADR-0004: Dependency Injection Container

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

SAGE Knowledge Base requires a mechanism for:

1. Managing service dependencies across layers
2. Supporting different object lifetimes (singleton, transient, scoped)
3. Enabling testability through dependency substitution
4. Configuration-driven service registration
5. Auto-wiring from type hints

### Requirements

- Lightweight (no heavy frameworks)
- Type-safe resolution
- Support for singleton, transient, and scoped lifetimes
- Factory pattern support
- YAML-driven registration option

---

## Decision

Implement a **custom lightweight DI container** with three lifetime modes and auto-wiring support.

### Container Design

```python
class DIContainer:
    """Lightweight dependency injection container."""

    def register(self, interface, implementation, lifetime): ...

    def register_instance(self, interface, instance): ...

    def register_factory(self, interface, factory, lifetime): ...

    def resolve(self, interface, scope_id=None): ...

    def try_resolve(self, interface, scope_id=None): ...

    def create_scope(self, scope_id): ...
```

### Lifetime Modes

| Lifetime      | Behavior                            | Use Case                          |
|:--------------|:------------------------------------|:----------------------------------|
| **SINGLETON** | One instance for container lifetime | Config, EventBus, shared state    |
| **TRANSIENT** | New instance per resolution         | Stateless services, validators    |
| **SCOPED**    | One instance per scope              | Request handlers, session context |

### Global Access Pattern

```python
# Single global container instance
container = get_container()

# Registration
container.register(SourceProtocol, FileSource, Lifetime.SINGLETON)

# Resolution
source = container.resolve(SourceProtocol)
```

---

## Alternatives Considered

### Alternative 1: No DI (Direct Instantiation)

Create objects directly where needed.

- **Pros**: Simple, no abstraction
- **Cons**: Tight coupling, hard to test, no lifetime management
- **Rejected**: Testing and modularity requirements

### Alternative 2: Third-Party Framework (dependency-injector)

Use established DI library.

- **Pros**: Feature-rich, well-tested
- **Cons**: Heavy dependency, learning curve, may be overkill
- **Rejected**: Prefer lightweight, custom solution

### Alternative 3: Service Locator Pattern

Global registry without interface contracts.

- **Pros**: Simple lookup
- **Cons**: Hidden dependencies, no compile-time safety
- **Rejected**: Type safety important for maintainability

---

## Consequences

### Positive

1. **Testability**: Easy to substitute mocks
2. **Loose coupling**: Services depend on interfaces
3. **Lifetime control**: Clear ownership semantics
4. **Configuration-driven**: Services can be registered via YAML
5. **Type safety**: Resolution typed by interface

### Negative

1. **Indirection**: Extra layer between creation and use
2. **Learning curve**: Developers must understand DI patterns
3. **Debugging**: Stack traces pass through container

### Mitigations

1. **Documentation**: Clear examples in conventions
2. **Simple API**: Minimal methods to learn
3. **Error messages**: Descriptive resolution errors

---

## Implementation

### Registration Patterns

```python
# Interface + Implementation
container.register(
    interface=SourceProtocol,
    implementation=FileSource,
    lifetime=Lifetime.SINGLETON
)

# Pre-created instance
container.register_instance(ConfigProtocol, loaded_config)

# Factory function
container.register_factory(
    interface=AnalyzerProtocol,
    factory=create_analyzer,
    lifetime=Lifetime.TRANSIENT
)
```

### Scoped Resolution

```python
# Create scope for request
with container.create_scope("request-123") as scope:
    handler = scope.resolve(RequestHandler)
    # handler is scoped to this request
# Scope disposed, scoped instances cleaned up
```

### YAML Configuration

```yaml
# sage.yaml
services:
  knowledge_loader:
    class: sage.core.loader.KnowledgeLoader
    lifetime: singleton
    config_key: loader

  code_analyzer:
    class: sage.capabilities.analyzers.CodeAnalyzer
    lifetime: transient
```

### Auto-Wiring

```python
class ServiceA:
    def __init__(self, dep: ServiceB):  # Auto-resolved
        self.dep = dep


# Container auto-wires ServiceB when resolving ServiceA
container.register(ServiceA, ServiceA, Lifetime.SINGLETON)
container.register(ServiceB, ServiceB, Lifetime.SINGLETON)
service_a = container.resolve(ServiceA)  # dep auto-injected
```

### Error Handling

```python
from sage.core.di import ServiceNotFoundError, CircularDependencyError

try:
    service = container.resolve(UnknownProtocol)
except ServiceNotFoundError as e:
    logger.error(f"Service not registered: {e}")
except CircularDependencyError as e:
    logger.error(f"Circular dependency detected: {e}")
```

---

## Related

- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Layer architecture
- `.context/decisions/ADR_0006_PROTOCOL_FIRST.md` — Protocol-based interfaces
- `.context/conventions/code_patterns.md` — DI usage patterns
- `src/sage/core/di/` — Implementation

---

*AI Collaboration Knowledge Base*
