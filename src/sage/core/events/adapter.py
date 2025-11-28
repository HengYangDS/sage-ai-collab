"""Plugin adapter for backward compatibility.

This module provides an adapter layer that allows existing plugins to work
with the new event-driven architecture without modification.

Version: 0.1.0
"""

from __future__ import annotations

import asyncio
import inspect
import logging
from typing import TYPE_CHECKING, Any, Callable

from sage.core.events.bus import EventBus, get_event_bus
from sage.core.events.events import (
    Event,
    EventType,
    LoadEvent,
    PluginEvent,
    SearchEvent,
    SystemEvent,
    TimeoutEvent,
)

if TYPE_CHECKING:
    from sage.plugins.base import PluginBase

__all__ = [
    "PluginAdapter",
    "adapt_plugin",
    "create_event_from_dict",
]

logger = logging.getLogger(__name__)


class PluginAdapter:
    """Adapter that wraps legacy plugins to work with EventBus.

    This adapter allows existing plugins that use the old callback-based
    API to work seamlessly with the new event-driven architecture.

    Example:
        >>> from sage.plugins.base import PluginBase
        >>>
        >>> class LegacyPlugin(PluginBase):
        ...     def on_load(self, layer: str, files: list) -> None:
        ...         print(f"Loaded {len(files)} files from {layer}")
        ...
        >>> adapter = PluginAdapter(LegacyPlugin())
        >>> adapter.register()  # Now the plugin receives events
    """

    # Mapping of event types to legacy method names
    EVENT_METHOD_MAP: dict[str, str] = {
        EventType.LOADER_START.value: "on_load_start",
        EventType.LOADER_COMPLETE.value: "on_load_complete",
        EventType.LOADER_ERROR.value: "on_load_error",
        EventType.LOADER_LAYER_LOADED.value: "on_layer_loaded",
        EventType.TIMEOUT_WARNING.value: "on_timeout_warning",
        EventType.TIMEOUT_EXCEEDED.value: "on_timeout_exceeded",
        EventType.TIMEOUT_RECOVERED.value: "on_timeout_recovered",
        EventType.SEARCH_START.value: "on_search_start",
        EventType.SEARCH_COMPLETE.value: "on_search_complete",
        EventType.SEARCH_ERROR.value: "on_search_error",
        EventType.PLUGIN_REGISTERED.value: "on_plugin_registered",
        EventType.PLUGIN_UNREGISTERED.value: "on_plugin_unregistered",
        EventType.PLUGIN_ERROR.value: "on_plugin_error",
        EventType.SYSTEM_STARTUP.value: "on_system_startup",
        EventType.SYSTEM_SHUTDOWN.value: "on_system_shutdown",
        EventType.SYSTEM_HEALTH_CHECK.value: "on_health_check",
    }

    def __init__(
        self,
        plugin: PluginBase | Any,
        event_bus: EventBus | None = None,
        priority: int = 100,
    ) -> None:
        """Initialize the plugin adapter.

        Args:
            plugin: The legacy plugin instance to adapt.
            event_bus: Optional EventBus instance. Uses global bus if not provided.
            priority: Handler priority for all adapted methods.
        """
        self._plugin = plugin
        self._event_bus = event_bus or get_event_bus()
        self._priority = priority
        self._subscription_ids: list[str] = []
        self._registered = False

    @property
    def plugin(self) -> PluginBase | Any:
        """Get the wrapped plugin instance."""
        return self._plugin

    @property
    def plugin_name(self) -> str:
        """Get the plugin name."""
        if hasattr(self._plugin, "name"):
            return str(self._plugin.name)
        return self._plugin.__class__.__name__

    @property
    def is_registered(self) -> bool:
        """Check if the adapter is registered with the event bus."""
        return self._registered

    def register(self) -> int:
        """Register the plugin with the event bus.

        Scans the plugin for methods matching event handlers and
        subscribes them to the appropriate events.

        Returns:
            Number of event handlers registered.
        """
        if self._registered:
            logger.warning(f"Plugin {self.plugin_name} already registered")
            return 0

        handlers_registered = 0

        for event_type, method_name in self.EVENT_METHOD_MAP.items():
            if hasattr(self._plugin, method_name):
                method = getattr(self._plugin, method_name)
                if callable(method):
                    handler = self._create_handler(method)
                    sub_id = self._event_bus.subscribe(
                        event_type,
                        handler,
                        priority=self._priority,
                    )
                    self._subscription_ids.append(sub_id)
                    handlers_registered += 1
                    logger.debug(
                        f"Registered {self.plugin_name}.{method_name} "
                        f"for {event_type}"
                    )

        # Also check for generic "on_event" handler
        if hasattr(self._plugin, "on_event"):
            method = getattr(self._plugin, "on_event")
            if callable(method):
                handler = self._create_handler(method)
                sub_id = self._event_bus.subscribe(
                    "*",  # Subscribe to all events
                    handler,
                    priority=self._priority + 500,  # Lower priority for catch-all
                )
                self._subscription_ids.append(sub_id)
                handlers_registered += 1
                logger.debug(f"Registered {self.plugin_name}.on_event for all events")

        self._registered = True
        logger.info(
            f"Plugin {self.plugin_name} registered with "
            f"{handlers_registered} handlers"
        )

        return handlers_registered

    def unregister(self) -> int:
        """Unregister the plugin from the event bus.

        Returns:
            Number of handlers unregistered.
        """
        if not self._registered:
            return 0

        count = 0
        for sub_id in self._subscription_ids:
            if self._event_bus.unsubscribe(sub_id):
                count += 1

        self._subscription_ids.clear()
        self._registered = False

        logger.info(f"Plugin {self.plugin_name} unregistered ({count} handlers)")
        return count

    def _create_handler(
        self, method: Callable[..., Any]
    ) -> Callable[[Event], Any]:
        """Create an async handler wrapper for a legacy method.

        Args:
            method: The legacy method to wrap.

        Returns:
            An async handler function compatible with EventBus.
        """

        async def handler(event: Event) -> None:
            try:
                # Check if the method is async
                if inspect.iscoroutinefunction(method):
                    await method(event)
                else:
                    # Run sync method in thread pool to avoid blocking
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, method, event)
            except Exception as e:
                logger.exception(
                    f"Error in plugin {self.plugin_name} "
                    f"handling {event.event_type}: {e}"
                )
                raise

        return handler


def adapt_plugin(
    plugin: PluginBase | Any,
    event_bus: EventBus | None = None,
    priority: int = 100,
    auto_register: bool = True,
) -> PluginAdapter:
    """Convenience function to adapt and optionally register a plugin.

    Args:
        plugin: The legacy plugin to adapt.
        event_bus: Optional EventBus instance.
        priority: Handler priority.
        auto_register: Whether to automatically register the plugin.

    Returns:
        The configured PluginAdapter instance.

    Example:
        >>> adapter = adapt_plugin(my_legacy_plugin)
        >>> # Plugin is now receiving events
    """
    adapter = PluginAdapter(plugin, event_bus, priority)
    if auto_register:
        adapter.register()
    return adapter


def create_event_from_dict(
    event_type: str | EventType,
    data: dict[str, Any],
    source: str = "adapter",
) -> Event:
    """Create an appropriate Event subclass from a dictionary.

    This helper creates the correct Event subclass based on the event type,
    useful for bridging between old dict-based APIs and new event objects.

    Args:
        event_type: The type of event to create.
        data: Dictionary of event data.
        source: The event source identifier.

    Returns:
        An Event instance of the appropriate subclass.

    Example:
        >>> event = create_event_from_dict(
        ...     EventType.LOADER_START,
        ...     {"layer": "core", "file_count": 5},
        ...     source="loader"
        ... )
    """
    event_type_str = (
        event_type.value if isinstance(event_type, EventType) else event_type
    )

    # Determine the appropriate Event subclass
    if event_type_str.startswith("loader."):
        return LoadEvent(
            event_type=event_type,
            source=source,
            layer=data.get("layer", ""),
            file_count=data.get("file_count", 0),
            duration_ms=data.get("duration_ms", 0.0),
        )
    elif event_type_str.startswith("timeout."):
        return TimeoutEvent(
            event_type=event_type,
            source=source,
            operation=data.get("operation", ""),
            timeout_level=data.get("timeout_level", "T2"),
            elapsed_ms=data.get("elapsed_ms", 0.0),
            limit_ms=data.get("limit_ms", 500.0),
        )
    elif event_type_str.startswith("search."):
        return SearchEvent(
            event_type=event_type,
            source=source,
            query=data.get("query", ""),
            results_count=data.get("results_count", 0),
            layers_searched=data.get("layers_searched", []),
            duration_ms=data.get("duration_ms", 0.0),
        )
    elif event_type_str.startswith("plugin."):
        return PluginEvent(
            event_type=event_type,
            source=source,
            plugin_name=data.get("plugin_name", ""),
            plugin_version=data.get("plugin_version", "0.0.0"),
            action=data.get("action", ""),
        )
    elif event_type_str.startswith("system."):
        return SystemEvent(
            event_type=event_type,
            source=source,
            component=data.get("component", ""),
            status=data.get("status", ""),
            message=data.get("message", ""),
        )
    else:
        # Generic event for unknown types
        return Event(
            event_type=event_type,
            source=source,
            data=data,
        )
