"""
SAGE Knowledge Base - Dev Tools Package

This package provides development-only tools that aren't part of the runtime
capabilities. Runtime capabilities are in `src/sage/capabilities/`.

Dev Tools included:
- TimeoutManager: Production-grade timeout handling with circuit breaker
- KnowledgeGraphBuilder: Build knowledge graphs from content
- TimeoutMonitor: Monitor timeout statistics (monitors/)
- MigrationToolkit: Backup and migration utilities
- dev_scripts/: Development environment setup scripts

Architecture:
- Runtime Capabilities → src/sage/capabilities/ (exposed via MCP/API)
- Dev Tools → tools/ (this package, for development/CI only)

Note: These tools aren't imported at runtime but only used during
development, testing and CI/CD operations.

Author: SAGE AI Collab Team
Version: 0.1.0
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

__version__ = "0.1.0"
