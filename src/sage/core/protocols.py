"""
SAGE Protocol - Domain-specific interfaces for Knowledge Base.

Source-Analyze-Generate-Evolve: A knowledge workflow protocol.
Zero-coupling design: All components communicate via these protocols,
never through direct imports.

Version: 0.1.0

Protocol Philosophy (信达雅):
- 信 (Faithfulness): Protocol interfaces accurately describe knowledge workflows
- 达 (Clarity): Clear separation of concerns across 4 stages
- 雅 (Elegance): "SAGE" forms a meaningful word (智者/wise person)
"""

from typing import Any, Protocol, runtime_checkable

from sage.core.models import (
    AnalysisResult,
    CheckpointData,
    GenerateResult,
    MetricsSnapshot,
    SearchResult,
    SourceRequest,
    SourceResult,
)


@runtime_checkable
class SourceProtocol(Protocol):
    """
    S - Source Protocol: Knowledge sourcing interface.

    Responsibilities:
    - Source knowledge content with timeout protection
    - Validate content integrity
    - Provide fallback content on failure

    Example:
        >>> class KnowledgeLoader(SourceProtocol):
        ...     async def source(self, request: SourceRequest) -> SourceResult:
        ...         # Load knowledge with timeout
        ...         return SourceResult(content="...", tokens=100, ...)
    """

    async def source(self, request: SourceRequest) -> SourceResult:
        """Source knowledge with timeout protection."""
        ...

    async def validate(self, content: str) -> tuple[bool, list[str]]:
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

    Example:
        >>> class ContentAnalyzer(AnalyzeProtocol):
        ...     async def search(self, query: str) -> list[SearchResult]:
        ...         # Search and return results
        ...         return [SearchResult(path="...", score=0.9, ...)]
    """

    async def search(self, query: str, max_results: int = 10) -> list[SearchResult]:
        """Search knowledge base."""
        ...

    async def analyze(self, content: str, task: str) -> AnalysisResult:
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

    Example:
        >>> class OutputGenerator(GenerateProtocol):
        ...     async def generate(self, data: Any) -> GenerateResult:
        ...         # Format and return content
        ...         return GenerateResult(content="...", format="markdown")
    """

    async def generate(self, data: Any, format: str = "markdown") -> GenerateResult:
        """Generate output in specified format."""
        ...

    async def serve(self, channel: str, config: dict[str, Any]) -> None:
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
    - Enable continuous learning and improvement

    Example:
        >>> class MetricsCollector(EvolveProtocol):
        ...     async def collect_metrics(self) -> MetricsSnapshot:
        ...         return MetricsSnapshot(load_count=100, ...)
    """

    async def collect_metrics(self) -> MetricsSnapshot:
        """Collect current metrics snapshot."""
        ...

    async def optimize(self, metrics: MetricsSnapshot) -> dict[str, Any]:
        """Suggest optimizations based on metrics."""
        ...

    async def checkpoint(self, session_id: str) -> CheckpointData:
        """Create a session checkpoint."""
        ...

    async def restore(self, checkpoint_id: str) -> dict[str, Any]:
        """Restore from a checkpoint."""
        ...


# Composite Protocol for full SAGE workflow
@runtime_checkable
class SAGEProtocol(
    SourceProtocol, AnalyzeProtocol, GenerateProtocol, EvolveProtocol, Protocol
):
    """
    Complete SAGE Protocol combining all four stages.

    This is the full interface for a complete knowledge management system.
    Implementations can choose to implement individual protocols or the full SAGE.
    """

    pass


# Protocol type aliases for type hints
SourceProvider = SourceProtocol
Analyzer = AnalyzeProtocol
Generator = GenerateProtocol
Evolver = EvolveProtocol
