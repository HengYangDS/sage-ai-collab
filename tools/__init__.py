"""
AI Collaboration Knowledge Base - Dev Tools Package

This package provides development-only tools that are NOT part of the runtime
capabilities. Runtime capabilities are in `src/ai_collab_kb/capabilities/`.

Dev Tools included:
- TimeoutManager: Production-grade timeout handling with circuit breaker
- KnowledgeGraphBuilder: Build knowledge graphs from content
- TimeoutMonitor: Monitor timeout statistics (monitors/)
- MigrationToolkit: Backup and migration utilities

Architecture (Plan D):
- Runtime Capabilities → src/ai_collab_kb/capabilities/ (exposed via MCP)
- Dev Tools → tools/ (this package, for development/CI only)

Author: SAGE AI Collab Team
Version: 3.0.0
"""

from .timeout_manager import (
    EMBEDDED_CORE,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitState,
    TimeoutConfig,
    TimeoutLevel,
    TimeoutManager,
    TimeoutResult,
    get_default_timeout_manager,
    get_timeout_manager,
)

__all__ = [
    # Timeout Management
    "TimeoutLevel",
    "TimeoutConfig",
    "TimeoutResult",
    "CircuitState",
    "CircuitBreakerConfig",
    "CircuitBreaker",
    "TimeoutManager",
    "EMBEDDED_CORE",
    "get_default_timeout_manager",
    "get_timeout_manager",
]

__version__ = "3.0.0"
