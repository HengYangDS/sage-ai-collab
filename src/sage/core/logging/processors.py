"""Custom structlog processors for SAGE Knowledge Base.

This module provides SAGE-specific structlog processors for:
- Timeout context injection
- Request ID tracking
- Layer identification
- Performance metrics

Version: 0.1.0
"""

from __future__ import annotations

import time
import uuid
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from structlog.typing import EventDict, WrappedLogger

__all__ = [
    "add_request_id",
    "add_timeout_context",
    "add_layer_info",
    "add_performance_metrics",
    "filter_sensitive_data",
    "RequestIdProcessor",
    "TimeoutContextProcessor",
    "LayerInfoProcessor",
]


def add_request_id(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Add a unique request ID to each log entry.

    If a request_id is not already present in the event dict,
    generates a new UUID for tracking purposes.

    Args:
        logger: The wrapped logger instance.
        method_name: The name of the log method called.
        event_dict: The event dictionary to process.

    Returns:
        The event dictionary with request_id added.
    """
    if "request_id" not in event_dict:
        event_dict["request_id"] = str(uuid.uuid4())[:8]
    return event_dict


def add_timeout_context(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Add timeout context information to log entries.

    Injects timeout-related context such as timeout level (T1-T5),
    remaining time, and timeout configuration.

    Args:
        logger: The wrapped logger instance.
        method_name: The name of the log method called.
        event_dict: The event dictionary to process.

    Returns:
        The event dictionary with timeout context added.
    """
    # Import here to avoid circular imports
    from sage.core.logging.context import get_context

    context = get_context()

    # Add timeout level if available
    if "timeout_level" in context:
        event_dict.setdefault("timeout_level", context["timeout_level"])

    # Add timeout deadline if available
    if "timeout_deadline" in context:
        remaining = context["timeout_deadline"] - time.time()
        event_dict.setdefault("timeout_remaining_ms", int(remaining * 1000))

    return event_dict


def add_layer_info(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Add SAGE layer information to log entries.

    Identifies which layer (core, services, capabilities, tools)
    the log entry originates from based on the logger name.

    Args:
        logger: The wrapped logger instance.
        method_name: The name of the log method called.
        event_dict: The event dictionary to process.

    Returns:
        The event dictionary with layer info added.
    """
    logger_name = event_dict.get("logger", "")

    if "layer" not in event_dict and logger_name:
        if ".core." in logger_name:
            event_dict["layer"] = "core"
        elif ".services." in logger_name:
            event_dict["layer"] = "services"
        elif ".capabilities." in logger_name:
            event_dict["layer"] = "capabilities"
        elif ".plugins." in logger_name:
            event_dict["layer"] = "plugins"
        elif "tools." in logger_name:
            event_dict["layer"] = "tools"

    return event_dict


def add_performance_metrics(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Add performance metrics to log entries.

    Calculates and adds timing information for operations
    that have start_time in their context.

    Args:
        logger: The wrapped logger instance.
        method_name: The name of the log method called.
        event_dict: The event dictionary to process.

    Returns:
        The event dictionary with performance metrics added.
    """
    if "start_time" in event_dict:
        start_time = event_dict.pop("start_time")
        event_dict["duration_ms"] = int((time.time() - start_time) * 1000)

    return event_dict


def filter_sensitive_data(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Filter sensitive data from log entries.

    Masks or removes sensitive information such as tokens,
    API keys, and passwords from log output.

    Args:
        logger: The wrapped logger instance.
        method_name: The name of the log method called.
        event_dict: The event dictionary to process.

    Returns:
        The event dictionary with sensitive data filtered.
    """
    sensitive_keys = {"password", "token", "api_key", "secret", "credential"}

    for key in list(event_dict.keys()):
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            event_dict[key] = "***REDACTED***"

    return event_dict


class RequestIdProcessor:
    """Processor class for request ID injection.

    Allows configuration of request ID prefix and format.
    """

    def __init__(self, prefix: str = "req") -> None:
        """Initialize the processor.

        Args:
            prefix: Prefix for generated request IDs.
        """
        self.prefix = prefix

    def __call__(
        self,
        logger: WrappedLogger,
        method_name: str,
        event_dict: EventDict,
    ) -> EventDict:
        """Process the event dict to add request ID."""
        if "request_id" not in event_dict:
            event_dict["request_id"] = f"{self.prefix}-{uuid.uuid4().hex[:8]}"
        return event_dict


class TimeoutContextProcessor:
    """Processor class for timeout context injection.

    Provides configurable timeout context logging with
    threshold warnings.
    """

    def __init__(self, warn_threshold_ms: int = 100) -> None:
        """Initialize the processor.

        Args:
            warn_threshold_ms: Threshold for timeout warnings in milliseconds.
        """
        self.warn_threshold_ms = warn_threshold_ms

    def __call__(
        self,
        logger: WrappedLogger,
        method_name: str,
        event_dict: EventDict,
    ) -> EventDict:
        """Process the event dict to add timeout context."""
        event_dict = add_timeout_context(logger, method_name, event_dict)

        # Add warning flag if timeout is approaching
        remaining = event_dict.get("timeout_remaining_ms")
        if remaining is not None and remaining < self.warn_threshold_ms:
            event_dict["timeout_warning"] = True

        return event_dict


class LayerInfoProcessor:
    """Processor class for layer information injection.

    Provides configurable layer detection with custom mappings.
    """

    DEFAULT_LAYER_MAPPING: dict[str, str] = {
        ".core.": "core",
        ".services.": "services",
        ".capabilities.": "capabilities",
        ".plugins.": "plugins",
        "tools.": "tools",
    }

    def __init__(
        self,
        layer_mapping: dict[str, str] | None = None,
        default_layer: str = "unknown",
    ) -> None:
        """Initialize the processor.

        Args:
            layer_mapping: Custom mapping of logger name patterns to layers.
            default_layer: Default layer name when no pattern matches.
        """
        self.layer_mapping = layer_mapping or self.DEFAULT_LAYER_MAPPING
        self.default_layer = default_layer

    def __call__(
        self,
        logger: WrappedLogger,
        method_name: str,
        event_dict: EventDict,
    ) -> EventDict:
        """Process the event dict to add layer info."""
        if "layer" in event_dict:
            return event_dict

        logger_name = event_dict.get("logger", "")
        for pattern, layer in self.layer_mapping.items():
            if pattern in logger_name:
                event_dict["layer"] = layer
                return event_dict

        event_dict["layer"] = self.default_layer
        return event_dict


def get_sage_processors() -> list[Any]:
    """Get the recommended SAGE processor chain.

    Returns a list of processors optimized for SAGE logging,
    including request tracking, timeout context, and layer info.

    Returns:
        List of structlog processors.
    """
    return [
        RequestIdProcessor(prefix="sage"),
        TimeoutContextProcessor(warn_threshold_ms=100),
        LayerInfoProcessor(),
        add_performance_metrics,
        filter_sensitive_data,
    ]
