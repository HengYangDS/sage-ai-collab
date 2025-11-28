"""Event system for SAGE Knowledge Base.

This module provides an event-driven architecture for async decoupling
between components, enabling flexible plugin integration and monitoring.

Version: 0.1.0

Example:
    >>> from sage.core.events import EventBus, Event, EventType, get_event_bus
    >>>
    >>> # Get the global event bus
    >>> bus = get_event_bus()
    >>>
    >>> # Subscribe to events
    >>> async def on_load(event: Event) -> None:
    ...     print(f"Loading: {event.data}")
    ...
    >>> bus.subscribe("loader.*", on_load)
    >>>
    >>> # Publish events
    >>> await bus.publish(LoadEvent(
    ...     event_type=EventType.LOADER_START,
    ...     source="loader",
    ...     layer="core"
    ... ))
"""

from sage.core.events.adapter import (
    PluginAdapter,
    adapt_plugin,
    create_event_from_dict,
)
from sage.core.events.bus import (
    EventBus,
    Subscription,
    get_event_bus,
    reset_event_bus,
)
from sage.core.events.events import (
    Event,
    EventType,
    LoadEvent,
    PluginEvent,
    SearchEvent,
    SystemEvent,
    TimeoutEvent,
)
from sage.core.events.protocols import (
    EventHandler,
    LoaderHandler,
    PluginHandler,
    SearchHandler,
    SystemHandler,
    TimeoutHandler,
)

__all__ = [
    # Bus
    "EventBus",
    "Subscription",
    "get_event_bus",
    "reset_event_bus",
    # Events
    "Event",
    "EventType",
    "LoadEvent",
    "TimeoutEvent",
    "SearchEvent",
    "PluginEvent",
    "SystemEvent",
    # Protocols
    "EventHandler",
    "LoaderHandler",
    "TimeoutHandler",
    "SearchHandler",
    "PluginHandler",
    "SystemHandler",
    # Adapter
    "PluginAdapter",
    "adapt_plugin",
    "create_event_from_dict",
]
