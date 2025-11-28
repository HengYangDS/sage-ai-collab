"""
SAGE Interfaces Package.

Centralized protocol definitions for the knowledge base system.
All components communicate via these interfaces for zero-coupling design.

Version: 0.1.0

This package re-exports protocols from core for convenience:
- SourceProtocol (S) - Knowledge sourcing
- AnalyzeProtocol (A) - Processing & analysis
- GenerateProtocol (G) - Multi-channel output
- EvolveProtocol (E) - Metrics & optimization
- SAGEProtocol - Complete workflow interface
"""

# Re-export SAGE protocols from core
# Re-export data models
from sage.core.models import (
    AnalysisRequest,
    AnalysisResult,
    CheckpointData,
    GenerateRequest,
    GenerateResult,
    LoadRequest,
    LoadResult,
    LoadStatus,
    MetricsSnapshot,
    SearchResult,
    SourceRequest,
    SourceResult,
)
from sage.core.protocols import (
    AnalyzeProtocol,
    Analyzer,
    EvolveProtocol,
    Evolver,
    GenerateProtocol,
    Generator,
    SAGEProtocol,
    SourceProtocol,
    SourceProvider,
)

__all__ = [
    # SAGE Protocols
    "SourceProtocol",
    "AnalyzeProtocol",
    "GenerateProtocol",
    "EvolveProtocol",
    "SAGEProtocol",
    # Protocol aliases
    "SourceProvider",
    "Analyzer",
    "Generator",
    "Evolver",
    # Data models
    "LoadRequest",
    "LoadResult",
    "LoadStatus",
    "SearchResult",
    "SourceRequest",
    "SourceResult",
    "AnalysisRequest",
    "AnalysisResult",
    "GenerateRequest",
    "GenerateResult",
    "MetricsSnapshot",
    "CheckpointData",
]
