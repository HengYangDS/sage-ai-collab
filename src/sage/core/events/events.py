"""Event definitions for SAGE Knowledge Base.

This module defines the event types and base classes for the event-driven
plugin architecture, enabling async decoupling between components.

Version: 0.1.0
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

__all__ = [
    "EventType",
    "Event",
    "LoadEvent",
    "TimeoutEvent",
    "SearchEvent",
    "PluginEvent",
    "SystemEvent",
]


class EventType(str, Enum):
    """Standard event types with namespacing.

    Event types follow a hierarchical naming convention:
    - loader.* : Events related to knowledge loading
    - timeout.* : Events related to timeout handling
    - search.* : Events related to search operations
    - plugin.* : Events related to plugin lifecycle
    - system.* : System-level events
    """

    # Loader events
    LOADER_START = "loader.start"
    LOADER_COMPLETE = "loader.complete"
    LOADER_ERROR = "loader.error"
    LOADER_LAYER_LOADED = "loader.layer_loaded"

    # Timeout events
    TIMEOUT_WARNING = "timeout.warning"
    TIMEOUT_EXCEEDED = "timeout.exceeded"
    TIMEOUT_RECOVERED = "timeout.recovered"

    # Search events
    SEARCH_START = "search.start"
    SEARCH_COMPLETE = "search.complete"
    SEARCH_ERROR = "search.error"

    # Plugin events
    PLUGIN_REGISTERED = "plugin.registered"
    PLUGIN_UNREGISTERED = "plugin.unregistered"
    PLUGIN_ERROR = "plugin.error"

    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_HEALTH_CHECK = "system.health_check"


@dataclass
class Event:
    """Base event class for all SAGE events.

    Attributes:
        event_type: The type of event (from EventType enum or custom string).
        timestamp: When the event was created (UTC).
        event_id: Unique identifier for this event instance.
        source: The component that generated this event.
        data: Additional event-specific data.
        metadata: Optional metadata for tracing and debugging.
    """

    event_type: EventType | str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "unknown"
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize event data."""
        if isinstance(self.event_type, str) and not isinstance(
            self.event_type, EventType
        ):
            # Allow custom event types as strings
            pass

    def to_dict(self) -> dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_type": (
                self.event_type.value
                if isinstance(self.event_type, EventType)
                else self.event_type
            ),
            "timestamp": self.timestamp.isoformat(),
            "event_id": self.event_id,
            "source": self.source,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Event:
        """Create an event from a dictionary."""
        event_type_str = data.get("event_type", "")
        try:
            event_type: EventType | str = EventType(event_type_str)
        except ValueError:
            event_type = event_type_str

        return cls(
            event_type=event_type,
            timestamp=datetime.fromisoformat(data.get("timestamp", "")),
            event_id=data.get("event_id", str(uuid.uuid4())),
            source=data.get("source", "unknown"),
            data=data.get("data", {}),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LoadEvent(Event):
    """Event for knowledge loading operations.

    Attributes:
        layer: The layer being loaded (core, guidelines, frameworks, etc.).
        file_count: Number of files involved.
        duration_ms: Duration of the operation in milliseconds.
    """

    layer: str = ""
    file_count: int = 0
    duration_ms: float = 0.0

    def __post_init__(self) -> None:
        """Initialize load event with layer data."""
        super().__post_init__()
        self.data.update(
            {
                "layer": self.layer,
                "file_count": self.file_count,
                "duration_ms": self.duration_ms,
            }
        )


@dataclass
class TimeoutEvent(Event):
    """Event for timeout-related occurrences.

    Attributes:
        operation: The operation that timed out or is at risk.
        timeout_level: The timeout level (T1-T5).
        elapsed_ms: Time elapsed so far.
        limit_ms: The timeout limit.
    """

    operation: str = ""
    timeout_level: str = "T2"
    elapsed_ms: float = 0.0
    limit_ms: float = 500.0

    def __post_init__(self) -> None:
        """Initialize timeout event with timing data."""
        super().__post_init__()
        self.data.update(
            {
                "operation": self.operation,
                "timeout_level": self.timeout_level,
                "elapsed_ms": self.elapsed_ms,
                "limit_ms": self.limit_ms,
            }
        )


@dataclass
class SearchEvent(Event):
    """Event for search operations.

    Attributes:
        query: The search query.
        results_count: Number of results found.
        layers_searched: List of layers searched.
        duration_ms: Duration of the search in milliseconds.
    """

    query: str = ""
    results_count: int = 0
    layers_searched: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

    def __post_init__(self) -> None:
        """Initialize a search event with search data."""
        super().__post_init__()
        self.data.update(
            {
                "query": self.query,
                "results_count": self.results_count,
                "layers_searched": self.layers_searched,
                "duration_ms": self.duration_ms,
            }
        )


@dataclass
class PluginEvent(Event):
    """Event for plugin lifecycle operations.

    Attributes:
        plugin_name: Name of the plugin.
        plugin_version: Version of the plugin.
        action: The action performed (registered, unregistered, error).
    """

    plugin_name: str = ""
    plugin_version: str = "0.0.0"
    action: str = ""

    def __post_init__(self) -> None:
        """Initialize plugin event with plugin data."""
        super().__post_init__()
        self.data.update(
            {
                "plugin_name": self.plugin_name,
                "plugin_version": self.plugin_version,
                "action": self.action,
            }
        )


@dataclass
class SystemEvent(Event):
    """Event for system-level operations.

    Attributes:
        component: The system component involved.
        status: Current status (starting, running, stopped, error).
        message: Optional status message.
    """

    component: str = ""
    status: str = ""
    message: str = ""

    def __post_init__(self) -> None:
        """Initialize system event with system data."""
        super().__post_init__()
        self.data.update(
            {
                "component": self.component,
                "status": self.status,
                "message": self.message,
            }
        )
