"""Logging configuration for SAGE Knowledge Base.

This module provides a centralized logging configuration using structlog
for structured, context-rich logging throughout the application.

Version: 0.1.0
"""

from __future__ import annotations

import logging
import sys
from enum import Enum
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__ = [
    "LogLevel",
    "LogFormat",
    "configure_logging",
    "get_default_processors",
    "reset_logging",
]


class LogLevel(str, Enum):
    """Supported log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(str, Enum):
    """Output format for log messages."""

    CONSOLE = "console"  # Human-readable, colored output
    JSON = "json"  # Machine-readable JSON output


def get_default_processors(
    format_type: LogFormat = LogFormat.CONSOLE,
) -> Sequence[structlog.types.Processor]:
    """Get the default processor chain for the structlog.

    Args:
        format_type: The output format (console or JSON).

    Returns:
        Sequence of structlog processors.
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if format_type == LogFormat.JSON:
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        shared_processors.append(
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            )
        )

    return shared_processors


def configure_logging(
    level: LogLevel | str = LogLevel.INFO,
    format_type: LogFormat | str = LogFormat.CONSOLE,
    *,
    cache_logger: bool = True,
) -> None:
    """Configure the logging system for SAGE.

    This function sets up both the structlog and the standard library logging
    to work together, providing structured logging throughout the application.

    Args:
        level: The minimum log level to display.
        format_type: Output format (console or JSON).
        cache_logger: Whether to cache logger instances for performance.

    Example:
        >>> from sage.core.logging import configure_logging, LogLevel
        >>> configure_logging(level=LogLevel.DEBUG)
        >>> # Now all loggers will output DEBUG and above
    """
    # Normalize inputs
    if isinstance(level, str):
        level = LogLevel(level.upper())
    if isinstance(format_type, str):
        format_type = LogFormat(format_type.lower())

    # Get numeric level
    numeric_level = getattr(logging, level.value)

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=numeric_level,
        force=True,
    )

    # Get processors for the specified format
    processors = get_default_processors(format_type)

    # Configure structlog
    structlog.configure(
        processors=list(processors),
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=cache_logger,
    )


def reset_logging() -> None:
    """Reset logging configuration to defaults.

    Useful for testing or reconfiguration scenarios.
    """
    structlog.reset_defaults()
    logging.root.handlers.clear()
