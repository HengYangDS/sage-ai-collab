# ADR-0006: Protocol-First Interface Design

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

SAGE Knowledge Base requires a consistent approach to interface definition:

1. Services need to depend on abstractions, not implementations
2. Runtime type checking for plugin validation
3. Clear contracts between layers
4. IDE support for auto-completion and type hints
5. Easy mocking for testing

### Requirements

- Static type checking support (mypy)
- Runtime type checking option
- No ABC boilerplate
- Structural subtyping (duck typing with types)
- Python 3.12+ compatibility

---

## Decision

Adopt **Protocol-First Design** using `typing.Protocol` for all cross-layer interfaces.

### Protocol Pattern

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class SourceProtocol(Protocol):
    """Interface for knowledge sources."""

    async def load(self, path: str) -> Knowledge:
        """Load knowledge from path."""
        ...

    async def search(self, query: str) -> list[Knowledge]:
        """Search for knowledge."""
        ...
```

### Key Characteristics

| Feature              | Protocol | ABC             |
|:---------------------|:---------|:----------------|
| Inheritance required | No       | Yes             |
| Runtime checkable    | Optional | Always          |
| Structural subtyping | Yes      | No              |
| Multiple protocols   | Clean    | Diamond problem |
| Boilerplate          | Minimal  | More verbose    |

---

## Alternatives Considered

### Alternative 1: Abstract Base Classes (ABC)

Use `abc.ABC` for interface definitions.

- **Pros**: Familiar, enforces implementation
- **Cons**: Requires inheritance, diamond problem, verbose
- **Rejected**: Structural subtyping preferred

### Alternative 2: Duck Typing Only

No explicit interfaces, rely on duck typing.

- **Pros**: Pythonic, flexible
- **Cons**: No type safety, no IDE support, no documentation
- **Rejected**: Need type hints for maintainability

### Alternative 3: Zope Interfaces

Use `zope.interface` library.

- **Pros**: Mature, powerful
- **Cons**: External dependency, different paradigm
- **Rejected**: stdlib Protocol sufficient

---

## Consequences

### Positive

1. **Structural subtyping**: No inheritance required
2. **Type safety**: Static checking with mypy
3. **IDE support**: Auto-completion, refactoring
4. **Documentation**: Protocols serve as contracts
5. **Testing**: Easy to create mocks

### Negative

1. **Learning curve**: Developers must understand Protocols
2. **Runtime overhead**: `@runtime_checkable` has cost
3. **Incomplete methods**: `...` syntax may confuse

### Mitigations

1. **Documentation**: Clear examples in conventions
2. **Selective runtime checks**: Only where needed
3. **Consistent style**: Always use `...` for protocol methods

---

## Implementation

### Defining Protocols

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class LoaderProtocol(Protocol):
    """Protocol for knowledge loaders."""

    def load(self, path: str) -> str:
        """Load content from path."""
        ...

    def exists(self, path: str) -> bool:
        """Check if path exists."""
        ...
```

### Implementing Protocols

```python
# No inheritance needed - structural subtyping
class FileLoader:
    """File-based loader implementation."""

    def load(self, path: str) -> str:
        with open(path) as f:
            return f.read()

    def exists(self, path: str) -> bool:
        return Path(path).exists()


# Type checker verifies compliance
loader: LoaderProtocol = FileLoader()  # OK
```

### Runtime Checking

```python
# Check at runtime (when @runtime_checkable)
def process(loader: LoaderProtocol) -> None:
    if not isinstance(loader, LoaderProtocol):
        raise TypeError("Expected LoaderProtocol")
    # ...


# Plugin validation
def register_plugin(plugin: Any) -> None:
    if isinstance(plugin, SourceProtocol):
        register_source(plugin)
    elif isinstance(plugin, AnalyzeProtocol):
        register_analyzer(plugin)
```

### Protocol Composition

```python
class CacheableProtocol(Protocol):
    """Protocol for cacheable resources."""

    def cache_key(self) -> str: ...

    def is_stale(self) -> bool: ...


class CacheableLoaderProtocol(LoaderProtocol, CacheableProtocol):
    """Combined protocol for cacheable loaders."""
    pass
```

### Generic Protocols

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class RepositoryProtocol(Protocol[T]):
    """Generic repository protocol."""

    def get(self, id: str) -> T | None: ...

    def save(self, entity: T) -> None: ...

    def delete(self, id: str) -> bool: ...
```

### SAGE Core Protocols

```python
# Core protocols in sage.core.protocols

@runtime_checkable
class SourceProtocol(Protocol):
    """S - Knowledge sourcing."""

    async def load(self, path: str) -> Knowledge: ...

    async def search(self, query: str) -> list[Knowledge]: ...


@runtime_checkable
class AnalyzeProtocol(Protocol):
    """A - Processing & analysis."""

    async def analyze(self, content: Knowledge) -> AnalysisResult: ...


@runtime_checkable
class GenerateProtocol(Protocol):
    """G - Multi-channel output."""

    async def format(self, data: Any, format: str) -> str: ...


@runtime_checkable
class EvolveProtocol(Protocol):
    """E - Metrics & optimization."""

    async def track(self, event: str, data: dict) -> None: ...
```

### Testing with Protocols

```python
# Easy to create test doubles
class MockLoader:
    def __init__(self, content: str):
        self._content = content

    def load(self, path: str) -> str:
        return self._content

    def exists(self, path: str) -> bool:
        return True


# Use in tests
def test_processor():
    loader: LoaderProtocol = MockLoader("test content")
    processor = Processor(loader)
    result = processor.process()
    assert result == "processed: test content"
```

---

## Related

- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Layer architecture
- `.context/decisions/ADR_0002_SAGE_PROTOCOL.md` — SAGE protocols
- `.context/decisions/ADR_0004_DEPENDENCY_INJECTION.md` — DI with protocols
- `.context/conventions/code_patterns.md` — Protocol patterns
- `src/sage/core/protocols.py` — Core protocol definitions

---

*AI Collaboration Knowledge Base*
