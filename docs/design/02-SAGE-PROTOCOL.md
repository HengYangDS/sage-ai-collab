---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~800
---

# SAGE Protocol Design

> Source-Analyze-Generate-Evolve: Domain-specific protocol for knowledge management

---

## Document Series

This document is part of the SAGE Protocol Design series:

| Document                  | Content                              |
|---------------------------|--------------------------------------|
| **02-SAGE-PROTOCOL.MD** (this) | Protocol overview, data classes, interfaces |
| `02A-DI-EVENTBUS.md`      | DI Container and EventBus            |
| `02B-BOOTSTRAP.md`        | Application bootstrap and configuration |

---

## Table of Contents

- [1. Protocol Overview](#1-protocol-overview)
- [2. Data Classes](#2-data-classes)
- [3. Protocol Interfaces](#3-protocol-interfaces)

---

## 1. Protocol Overview

The SAGE Protocol defines a four-stage workflow for knowledge management:

| Stage | Name     | Purpose                                    |
|-------|----------|--------------------------------------------|
| **S** | Source   | Knowledge sourcing with timeout protection |
| **A** | Analyze  | Processing, search, analysis               |
| **G** | Generate | Multi-channel output (CLI/MCP/API)         |
| **E** | Evolve   | Metrics, optimization, memory              |

### 1.1 Philosophy (信达雅)

- **信 (Faithfulness)**: Protocol interfaces accurately describe knowledge workflows
- **达 (Clarity)**: Clear separation of concerns across 4 stages
- **雅 (Elegance)**: "SAGE" forms a meaningful word (智者/wise person)

---

## 2. Data Classes

```python
# src/sage/core/models.py
"""
SAGE Protocol Data Classes.

These dataclasses define the request/response structures for all protocol operations.
"""
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict


@dataclass
class LoadRequest:
    """Knowledge load request."""
    layers: List[str] = field(default_factory=lambda: ["core"])
    query: Optional[str] = None
    timeout_ms: int = 5000
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoadResult:
    """Knowledge load result."""
    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout
    duration_ms: int
    layers_loaded: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Search result item."""
    path: str
    score: float
    preview: str
    layer: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceRequest:
    """Knowledge source request for SourceProtocol."""
    layers: List[str] = field(default_factory=lambda: ["core"])
    query: Optional[str] = None
    timeout_ms: int = 5000
    include_metadata: bool = False
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceResult:
    """Knowledge source result from SourceProtocol."""
    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout | error
    duration_ms: int
    source_path: Optional[str] = None
    layers_loaded: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## 3. Protocol Interfaces

```python
# src/sage/core/protocols.py
"""
SAGE Protocol - Domain-specific interfaces for Knowledge Base.

Source-Analyze-Generate-Evolve: A knowledge workflow protocol.
Zero-coupling design: All components communicate via these protocols,
never through direct imports.
"""
from typing import Protocol, runtime_checkable, Any, Dict, List
from sage.core.models import SourceRequest, SourceResult, SearchResult


@runtime_checkable
class SourceProtocol(Protocol):
    """
    S - Source Protocol: Knowledge sourcing interface.
    
    Responsibilities:
    - Source knowledge content with timeout protection
    - Validate content integrity
    - Provide fallback content on failure
    """

    async def source(self, request: SourceRequest) -> SourceResult:
        """Source knowledge with timeout protection."""
        ...

    async def validate(self, content: str) -> tuple[bool, List[str]]:
        """Validate content integrity. Returns (is_valid, errors)."""
        ...

    async def get_fallback(self) -> str:
        """Get fallback content for emergency situations."""
        ...


@runtime_checkable
class AnalyzeProtocol(Protocol):
    """
    A - Analyze Protocol: Processing and analysis interface.
    
    Responsibilities:
    - Search knowledge base
    - Analyze content for specific tasks
    - Summarize content for token efficiency
    """

    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """Search knowledge base."""
        ...

    async def analyze(self, content: str, task: str) -> Dict[str, Any]:
        """Analyze content for specific task."""
        ...

    async def summarize(self, content: str, max_tokens: int = 500) -> str:
        """Summarize content for token efficiency."""
        ...


@runtime_checkable
class GenerateProtocol(Protocol):
    """
    G - Generate Protocol: Multi-channel output generation interface.
    
    Responsibilities:
    - Generate content in various formats
    - Serve content via different channels (CLI/MCP/API)
    """

    async def generate(self, data: Any, format: str = "markdown") -> str:
        """Generate output in specified format."""
        ...

    async def serve(self, channel: str, config: Dict[str, Any]) -> None:
        """Start serving on specified channel."""
        ...


@runtime_checkable
class EvolveProtocol(Protocol):
    """
    E - Evolve Protocol: Metrics, optimization and evolution interface.
    
    Responsibilities:
    - Collect usage metrics
    - Optimize performance
    - Manage session checkpoints
    """

    async def collect_metrics(self, context: Dict[str, Any]) -> None:
        """Collect metrics for monitoring."""
        ...

    async def optimize(self, target: str) -> Dict[str, Any]:
        """Optimize specified target."""
        ...

    async def checkpoint(self, session_id: str) -> str:
        """Create session checkpoint, return checkpoint ID."""
        ...
```

### 3.1 Protocol Benefits

| Benefit           | Description                                         |
|-------------------|-----------------------------------------------------|
| **Zero Coupling** | Components depend on protocols, not implementations |
| **Testability**   | Easy to mock protocols for unit testing             |
| **Flexibility**   | Multiple implementations can satisfy same protocol  |
| **Type Safety**   | `@runtime_checkable` enables isinstance() checks    |
| **Documentation** | Protocols serve as interface contracts              |

---

## Related

- `docs/design/02A-DI-EVENTBUS.md` — DI Container and EventBus details
- `docs/design/02B-BOOTSTRAP.md` — Application bootstrap and configuration
- `docs/design/01-ARCHITECTURE.md` — Overall architecture
- `docs/design/03-SERVICES.md` — Service layer implementation

---

*Part of SAGE Knowledge Base*
