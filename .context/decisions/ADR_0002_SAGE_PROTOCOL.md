# ADR-0002: SAGE Protocol Design

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

SAGE Knowledge Base requires a unified processing model that:

1. Provides consistent interface for knowledge operations
2. Supports the complete lifecycle from sourcing to optimization
3. Enables extensibility at each processing stage
4. Aligns with the project name (SAGE = Source, Analyze, Generate, Evolve)

### Requirements

- Clear separation of processing phases
- Protocol-based extensibility
- Async-first design
- Observable and measurable stages

---

## Decision

Adopt the **SAGE Protocol** — a four-phase processing model:

```text
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌────────┐
│ Source  │ →  │ Analyze │ →  │ Generate │ →  │ Evolve │
│   (S)   │    │   (A)   │    │    (G)   │    │   (E)  │
└─────────┘    └─────────┘    └──────────┘    └────────┘
```

### Phase Definitions

| Phase        | Purpose                 | Input           | Output           |
|:-------------|:------------------------|:----------------|:-----------------|
| **Source**   | Knowledge acquisition   | Paths, queries  | Raw content      |
| **Analyze**  | Processing & enrichment | Raw content     | Structured data  |
| **Generate** | Multi-channel output    | Structured data | Formatted output |
| **Evolve**   | Metrics & optimization  | Usage data      | Improvements     |

### Protocol Interfaces

```python
@runtime_checkable
class SourceProtocol(Protocol):
    """S - Knowledge sourcing."""

    async def load(self, path: str) -> Knowledge: ...

    async def search(self, query: str) -> list[Knowledge]: ...

    async def list_layers(self) -> list[str]: ...


@runtime_checkable
class AnalyzeProtocol(Protocol):
    """A - Processing & analysis."""

    async def analyze(self, content: Knowledge) -> AnalysisResult: ...

    async def extract(self, content: Knowledge) -> Metadata: ...

    async def validate(self, content: Knowledge) -> ValidationResult: ...


@runtime_checkable
class GenerateProtocol(Protocol):
    """G - Multi-channel output."""

    async def format(self, data: Any, format: str) -> str: ...

    async def render(self, template: str, context: dict) -> str: ...

    async def export(self, data: Any, target: str) -> None: ...


@runtime_checkable
class EvolveProtocol(Protocol):
    """E - Metrics & optimization."""

    async def track(self, event: str, data: dict) -> None: ...

    async def optimize(self, feedback: Feedback) -> None: ...

    async def report(self) -> MetricsReport: ...
```

---

## Alternatives Considered

### Alternative 1: CRUD Model

Standard Create-Read-Update-Delete operations.

- **Pros**: Familiar, simple
- **Cons**: Doesn't capture knowledge lifecycle; too generic
- **Rejected**: Knowledge management needs richer semantics

### Alternative 2: ETL Pipeline

Extract-Transform-Load pattern.

- **Pros**: Well-understood data pipeline
- **Cons**: Missing analysis/evolution phases; batch-oriented
- **Rejected**: Need real-time, interactive operations

### Alternative 3: Generic Pipeline

Arbitrary stages without semantic meaning.

- **Pros**: Maximum flexibility
- **Cons**: No guidance, inconsistent implementations
- **Rejected**: SAGE acronym provides valuable semantic structure

---

## Consequences

### Positive

1. **Semantic clarity**: Each phase has clear purpose
2. **Memorable**: SAGE acronym aids understanding
3. **Extensible**: New implementations can be added per phase
4. **Observable**: Each phase can emit events for monitoring
5. **Testable**: Phases can be unit tested independently

### Negative

1. **Rigid structure**: Four phases may not fit all use cases
2. **Naming constraint**: Must maintain SAGE acronym alignment
3. **Complexity**: Simple operations may feel over-structured

### Mitigations

1. **Phase composition**: Phases can be composed or skipped
2. **Default implementations**: Provide sensible defaults
3. **Convenience methods**: High-level APIs that hide phase complexity

---

## Implementation

### Event Flow

```python
# Each phase emits lifecycle events
"source.started"    → "source.completed" | "source.failed"
"analyze.started"   → "analyze.completed" | "analyze.failed"
"generate.started"  → "generate.completed" | "generate.failed"
"evolve.started"    → "evolve.completed" | "evolve.failed"
```

### Usage Example

```python
# Full pipeline
async def process_knowledge(query: str) -> str:
    # Source
    knowledge = await source.search(query)

    # Analyze
    analysis = await analyzer.analyze(knowledge[0])

    # Generate
    output = await generator.format(analysis, "markdown")

    # Evolve
    await evolver.track("query.completed", {"query": query})

    return output
```

### Phase Skipping

```python
# Direct source-to-generate (skip analyze)
content = await source.load("path/to/file.md")
output = await generator.format(content, "json")
```

---

## Related

- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Three-layer architecture
- `.context/decisions/ADR_0006_PROTOCOL_FIRST.md` — Protocol-first design
- `docs/design/02-sage-protocol.md` — Full protocol documentation

---

*AI Collaboration Knowledge Base*
