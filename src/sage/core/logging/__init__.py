"""SAGE Logging System.

Structured logging for SAGE Knowledge Base using structlog.

This module provides:
- configure_logging(): Configure the logging system
- get_logger(): Get a structured logger instance
- bind_context(): Add context to all subsequent logs
- logging_context(): Context manager for temporary context

Version: 0.1.0

Example:
    >>> from sage.core.logging import configure_logging, get_logger, LogLevel
    >>> configure_logging(level=LogLevel.DEBUG)
    >>> logger = get_logger("sage.core.loader")
    >>> logger.info("Loading knowledge base", layer="core")
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import structlog

from .config import (
    LogFormat,
    LogLevel,
    configure_logging,
    get_default_processors,
    reset_logging,
)
from .context import (
    bind_context,
    clear_context,
    get_context,
    logging_context,
    unbind_context,
)

if TYPE_CHECKING:
    from structlog.typing import FilteringBoundLogger

__all__ = [
    # Configuration
    "configure_logging",
    "reset_logging",
    "get_default_processors",
    "LogLevel",
    "LogFormat",
    # Logger factory
    "get_logger",
    # Context management
    "bind_context",
    "unbind_context",
    "clear_context",
    "get_context",
    "logging_context",
]


def get_logger(name: str | None = None) -> FilteringBoundLogger:
    """Get a structured logger instance.

    Creates a new structlog logger bound to the given name. The logger
    will automatically include any context set via bind_context().

    Args:
        name: Optional logger name (e.g., module name). If None, uses
              the caller's module name.

    Returns:
        A structlog FilteringBoundLogger instance.

    Example:
        >>> from sage.core.logging import get_logger
        >>> logger = get_logger("sage.core.loader")
        >>> logger.info("Loading started", layer="core")
        >>> logger.debug("Processing file", filename="index.md")
        >>> logger.error("Load failed", error="FileNotFound")
    """
    return structlog.get_logger(name)
