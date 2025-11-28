"""Logging context management for SAGE Knowledge Base.

This module provides context management utilities for structured logging,
allowing contextual information to be automatically included in log messages.

Version: 0.1.0
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import structlog

if TYPE_CHECKING:
    from collections.abc import Generator

__all__ = [
    "bind_context",
    "clear_context",
    "get_context",
    "unbind_context",
    "logging_context",
]


def bind_context(**kwargs: Any) -> None:
    """Bind key-value pairs to the current logging context.

    All subsequent log messages in the current context will include
    these key-value pairs automatically.

    Args:
        **kwargs: Key-value pairs to add to the context.

    Example:
        >>> from sage.core.logging import bind_context, get_logger
        >>> bind_context(request_id="abc-123", user="admin")
        >>> logger = get_logger()
        >>> logger.info("Processing request")
        # Output includes request_id="abc-123" user="admin"
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_context(*keys: str) -> None:
    """Remove specific keys from the current logging context.

    Args:
        *keys: Keys to remove from the context.

    Example:
        >>> from sage.core.logging import bind_context, unbind_context
        >>> bind_context(request_id="abc-123", temp_value="xyz")
        >>> unbind_context("temp_value")
        # Only request_id remains in context
    """
    structlog.contextvars.unbind_contextvars(*keys)


def clear_context() -> None:
    """Clear all context variables.

    Removes all bound context from the current logging context.
    Useful at the start of a new request or operation.

    Example:
        >>> from sage.core.logging import clear_context
        >>> clear_context()
        # All context variables are now cleared
    """
    structlog.contextvars.clear_contextvars()


def get_context() -> dict[str, Any]:
    """Get the current logging context as a dictionary.

    Returns:
        Dictionary containing all bound context variables.

    Example:
        >>> from sage.core.logging import bind_context, get_context
        >>> bind_context(request_id="abc-123")
        >>> ctx = get_context()
        >>> print(ctx)
        {'request_id': 'abc-123'}
    """
    return structlog.contextvars.get_contextvars()


@contextmanager
def logging_context(**kwargs: Any) -> Generator[None, None, None]:
    """Context manager for temporary logging context.

    Binds the provided context for the duration of a block,
    then automatically clears only those keys when exiting.

    Args:
        **kwargs: Key-value pairs to temporarily add to context.

    Yields:
        None

    Example:
        >>> from sage.core.logging import logging_context, get_logger
        >>> logger = get_logger()
        >>> with logging_context(operation="load", layer="core"):
        ...     logger.info("Loading layer")
        ...     # Logs include operation="load" layer="core"
        >>> logger.info("After context")
        # Logs no longer include operation or layer
    """
    # Bind the new context
    bind_context(**kwargs)
    try:
        yield
    finally:
        # Only unbind the keys added
        unbind_context(*kwargs.keys())
