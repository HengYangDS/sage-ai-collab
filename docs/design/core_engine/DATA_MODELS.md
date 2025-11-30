# Data Models

> Core data structures and types for SAGE

---

## 1. Overview

Data models define the core types and structures used throughout SAGE, ensuring consistent data representation across all layers.

---

## 2. Model Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **Knowledge** | Knowledge representation | KnowledgeAsset, KnowledgeGraph |
| **Operation** | Operation tracking | Result, ValidationResult |
| **Configuration** | Config structures | Config, LayerConfig |
| **Session** | Session state | Session, SessionContext |

---

## 3. Knowledge Models

### 3.1 KnowledgeAsset

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class KnowledgeAsset:
    """Fundamental unit of knowledge."""
    id: str
    path: str
    content: str
    metadata: dict[str, Any]
    fingerprint: str
    created_at: datetime
    updated_at: datetime
    
    @property
    def title(self) -> str:
        return self.metadata.get("title", self.path)
    
    @property
    def tags(self) -> set[str]:
        return set(self.metadata.get("tags", []))
```

### 3.2 KnowledgeLayer

```python
@dataclass
class KnowledgeLayer:
    """A layer in the knowledge hierarchy."""
    name: str
    path: str
    priority: int
    assets: list[KnowledgeAsset]
    
    # Layer types
    UNIVERSAL = "knowledge"   # .knowledge/
    PROJECT = "context"       # .context/
    ASSISTANT = "junie"       # .junie/
    DOCS = "docs"             # docs/
```

### 3.3 KnowledgeGraph

```python
@dataclass
class KnowledgeNode:
    """Node in the knowledge graph."""
    id: str
    asset: KnowledgeAsset
    labels: set[str]

@dataclass
class KnowledgeEdge:
    """Edge connecting knowledge nodes."""
    source_id: str
    target_id: str
    relation_type: str
    weight: float = 1.0

@dataclass
class KnowledgeGraph:
    """Graph of related knowledge."""
    nodes: dict[str, KnowledgeNode]
    edges: list[KnowledgeEdge]
    
    def get_related(self, node_id: str) -> list[KnowledgeNode]:
        """Get nodes related to a given node."""
        ...
```

---

## 4. Operation Models

### 4.1 Result

```python
from typing import Generic, TypeVar

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """Generic operation result."""
    success: bool
    value: T | None
    error: str | None
    duration_ms: float
    
    @classmethod
    def ok(cls, value: T, duration_ms: float = 0) -> "Result[T]":
        return cls(True, value, None, duration_ms)
    
    @classmethod
    def fail(cls, error: str, duration_ms: float = 0) -> "Result[T]":
        return cls(False, None, error, duration_ms)
```

### 4.2 ValidationResult

```python
@dataclass
class ValidationError:
    path: str
    line: int | None
    message: str
    severity: str  # error, warning, info

@dataclass
class ValidationResult:
    """Result of validation operation."""
    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]
    checked_count: int
    duration_ms: float
```

### 4.3 OperationContext

```python
@dataclass
class OperationContext:
    """Context for an operation."""
    operation_id: str
    started_at: datetime
    timeout_ms: int
    correlation_id: str | None
    metadata: dict[str, Any]
```

---

## 5. Configuration Models

### 5.1 Config

```python
@dataclass
class TimeoutConfig:
    cache_lookup: int = 50
    file_read: int = 200
    processing: int = 1000
    external_api: int = 5000
    batch: int = 30000

@dataclass
class LoadingConfig:
    strategy: str = "lazy"
    max_token_budget: int = 50000
    cache_enabled: bool = True

@dataclass
class Config:
    """Root configuration."""
    version: str
    timeout: TimeoutConfig
    loading: LoadingConfig
    plugins: dict[str, Any]
```

---

## 6. Session Models

### 6.1 Session

```python
@dataclass
class Session:
    """User/AI interaction session."""
    id: str
    started_at: datetime
    user_type: str  # human, ai
    context: "SessionContext"

@dataclass
class SessionContext:
    """State within a session."""
    loaded_knowledge: list[str]
    token_usage: int
    operation_history: list[str]
    preferences: dict[str, Any]
```

---

## 7. Protocol Types

### 7.1 SAGE Protocol Types

```python
# Source phase
@dataclass
class RawKnowledge:
    source: str
    content: bytes
    encoding: str | None
    collected_at: datetime

@dataclass
class NormalizedKnowledge:
    id: str
    source: str
    content: str
    metadata: dict[str, Any]
    fingerprint: str

# Analyze phase
@dataclass
class ParsedKnowledge:
    id: str
    structure: dict[str, Any]
    content_blocks: list[dict]
    references: list[str]

@dataclass
class ClassifiedKnowledge:
    id: str
    classifications: list[str]
    tags: set[str]
    confidence: float

# Generate phase
@dataclass
class FormattedContent:
    format_type: str
    content: str | dict
    metadata: dict[str, Any]

@dataclass
class RenderedContent:
    content: str
    content_type: str
    byte_size: int
    token_count: int | None
```

---

## 8. Type Aliases

```python
from typing import TypeAlias

# Common type aliases
AssetId: TypeAlias = str
NodeId: TypeAlias = str
Path: TypeAlias = str
Fingerprint: TypeAlias = str

# Collection aliases
Assets: TypeAlias = list[KnowledgeAsset]
Nodes: TypeAlias = dict[NodeId, KnowledgeNode]
Edges: TypeAlias = list[KnowledgeEdge]
```

---

## 9. Validation

### 9.1 Pydantic Models

```python
from pydantic import BaseModel, Field

class KnowledgeAssetModel(BaseModel):
    id: str = Field(..., min_length=1)
    path: str = Field(..., pattern=r"^[\w/.-]+$")
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        frozen = True
```

---

## 10. Best Practices

| Practice | Description |
|----------|-------------|
| **Immutable** | Use frozen dataclasses where possible |
| **Typed** | Full type annotations |
| **Validated** | Use Pydantic for external data |
| **Documented** | Docstrings on all models |

---

## Related

- `DI_CONTAINER.md` — Dependency injection
- `EXCEPTIONS.md` — Error handling
- `../protocols/SAGE_PROTOCOL.md` — Protocol types

---

*AI Collaboration Knowledge Base*
