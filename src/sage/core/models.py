"""
SAGE Protocol Data Classes.

These dataclasses define the request/response structures for all protocol operations.
Following the SAGE (Source-Analyze-Generate-Evolve) workflow pattern.

Version: 0.1.0
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class LoadStatus(str, Enum):
    """Status of a load operation."""

    SUCCESS = "success"
    PARTIAL = "partial"
    FALLBACK = "fallback"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class LoadRequest:
    """Knowledge load request."""

    layers: list[str] = field(default_factory=lambda: ["core"])
    query: str | None = None
    timeout_ms: int = 5000
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class LoadResult:
    """Knowledge load result."""

    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout
    duration_ms: int
    layers_loaded: list[str] = field(default_factory=list)
    files_loaded: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def tokens_estimate(self) -> int:
        """Alias for tokens for backward compatibility."""
        return self.tokens


@dataclass
class SearchResult:
    """Search result item."""

    path: str
    score: float
    preview: str
    layer: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceRequest:
    """Knowledge source request for SourceProtocol."""

    layers: list[str] = field(default_factory=lambda: ["core"])
    query: str | None = None
    timeout_ms: int = 5000
    include_metadata: bool = False
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceResult:
    """Knowledge source result from SourceProtocol."""

    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout | error
    duration_ms: int
    source_path: str | None = None
    layers_loaded: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisRequest:
    """Content analysis request."""

    content: str
    task: str
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """Content analysis result."""

    task: str
    findings: dict[str, Any] = field(default_factory=dict)
    score: float | None = None
    suggestions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateRequest:
    """Output generation request."""

    data: Any
    format: str = "markdown"
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateResult:
    """Output generation result."""

    content: str
    format: str
    tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricsSnapshot:
    """Metrics snapshot for EvolveProtocol."""

    timestamp: datetime = field(default_factory=datetime.now)
    load_count: int = 0
    search_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_load_time_ms: float = 0.0
    avg_tokens_per_load: float = 0.0
    error_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckpointData:
    """Session checkpoint data."""

    checkpoint_id: str
    session_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    state: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


# Type aliases for convenience
LayerList = list[str]
TokenCount = int
DurationMs = int
