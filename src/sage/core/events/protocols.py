"""Protocol interfaces for SAGE event handlers.

This module defines the Protocol interfaces that event handlers must implement,
enabling type-safe event handling with static type checking support.

Version: 0.1.0
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from sage.core.events.events import (
        Event,
        LoadEvent,
        PluginEvent,
        SearchEvent,
        SystemEvent,
        TimeoutEvent,
    )

__all__ = [
    "EventHandler",
    "LoaderHandler",
    "TimeoutHandler",
    "SearchHandler",
    "PluginHandler",
    "SystemHandler",
]


@runtime_checkable
class EventHandler(Protocol):
    """Base protocol for all event handlers.

    All event handlers must implement this protocol to be registered
    with the EventBus.

    Example:
        >>> class MyHandler:
        ...     @staticmethod
        ...     async def handle( event: Event) -> None:
        ...         print(f"Handling event: {event.event_type}")
        ...
        ...     @property
        ...     def priority(self) -> int:
        ...         return 100
    """

    async def handle(self, event: Event) -> None:
        """Handle an event.

        Args:
            event: The event to handle.

        Raises:
            Exception: EventBus should catch Handler-specific exceptions.
        """
        ...

    @property
    def priority(self) -> int:
        """Handler priority (lower = earlier execution).

        Returns:
            Priority value. Default is 100. Range: 0-1000.
            - 0-99: High priority (system handlers)
            - 100-499: Normal priority (default)
            - 500-999: Low priority (logging, metrics)
            - 1000: Lowest priority (cleanup)
        """
        ...


@runtime_checkable
class LoaderHandler(Protocol):
    """Protocol for handlers that process loading events.

    Implement this protocol to handle knowledge loading lifecycle events
    such as start, complete, error, and layer loaded.

    Example:
        >>> class LoadMetricsHandler:
        ...     async def on_load_start(self, event: LoadEvent) -> None:
        ...         # noinspection PyAttributeOutsideInit
        ...         self.start_time = time.time()
        ...
        ...     async def on_load_complete(self, event: LoadEvent) -> None:
        ...         duration = time.time() - self.start_time
        ...         print(f"Load completed in {duration:.2f}s")
    """

    async def on_load_start(self, event: LoadEvent) -> None:
        """Called when loading starts.

        Args:
            event: The load event with the initial state.
        """
        ...

    async def on_load_complete(self, event: LoadEvent) -> None:
        """Called when loading completes successfully.

        Args:
            event: The load event with final state and metrics.
        """
        ...

    async def on_load_error(self, event: LoadEvent) -> None:
        """Called when loading encounters an error.

        Args:
            event: The load event with error information.
        """
        ...

    async def on_layer_loaded(self, event: LoadEvent) -> None:
        """Called when a specific layer is loaded.

        Args:
            event: The load event with layer-specific information.
        """
        ...


@runtime_checkable
class TimeoutHandler(Protocol):
    """Protocol for handlers that process timeout events.

    Implement this protocol to handle timeout warnings, exceeded limits,
    and recovery scenarios.

    Example:
        >>> class TimeoutAlertHandler:
        ...     async def on_timeout_warning(self, event: TimeoutEvent) -> None:
        ...         if event.elapsed_ms > event.limit_ms * 0.9:
        ...             await self.send_alert("Approaching timeout!")
    """

    async def on_timeout_warning(self, event: TimeoutEvent) -> None:
        """Called when an operation approaches its timeout limit.

        Args:
            event: The timeout event with timing information.
        """
        ...

    async def on_timeout_exceeded(self, event: TimeoutEvent) -> None:
        """Called when an operation exceeds its timeout limit.

        Args:
            event: The timeout event with exceeded timing details.
        """
        ...

    async def on_timeout_recovered(self, event: TimeoutEvent) -> None:
        """Called when an operation recovers from a timeout situation.

        Args:
            event: The timeout event with recovery information.
        """
        ...


@runtime_checkable
class SearchHandler(Protocol):
    """Protocol for handlers that process search events.

    Implement this protocol to handle search lifecycle events
    including start, complete, and error scenarios.

    Example:
        >>> class SearchAnalyticsHandler:
        ...     async def on_search_complete(self, event: SearchEvent) -> None:
        ...         await self.log_search_metrics(
        ...             query=event.query,
        ...             results=event.results_count,
        ...             duration=event.duration_ms
        ...         )
    """

    async def on_search_start(self, event: SearchEvent) -> None:
        """Called when a search operation starts.

        Args:
            event: The search event with query information.
        """
        ...

    async def on_search_complete(self, event: SearchEvent) -> None:
        """Called when a search operation completes.

        Args:
            event: The search event with results and metrics.
        """
        ...

    async def on_search_error(self, event: SearchEvent) -> None:
        """Called when a search operation encounters an error.

        Args:
            event: The search event with error information.
        """
        ...


@runtime_checkable
class PluginHandler(Protocol):
    """Protocol for handlers that process plugin lifecycle events.

    Implement this protocol to handle plugin registration,
    unregistration, and error events.

    Example:
        >>> class PluginLifecycleLogger:
        ...     @staticmethod
        ...     async def on_plugin_registered( event: PluginEvent) -> None:
        ...         logger.info(f"Plugin {event.plugin_name} v{event.plugin_version} registered")
    """

    async def on_plugin_registered(self, event: PluginEvent) -> None:
        """Called when a plugin is registered.

        Args:
            event: The plugin event with registration details.
        """
        ...

    async def on_plugin_unregistered(self, event: PluginEvent) -> None:
        """Called when a plugin is unregistered.

        Args:
            event: The plugin event with unregistration details.
        """
        ...

    async def on_plugin_error(self, event: PluginEvent) -> None:
        """Called when a plugin encounters an error.

        Args:
            event: The plugin event with error information.
        """
        ...


@runtime_checkable
class SystemHandler(Protocol):
    """Protocol for handlers that process system events.

    Implement this protocol to handle system startup, shutdown, and health check events.

    Example:
        >>> class SystemMonitor:
        ...     async def on_system_startup(self, event: SystemEvent) -> None:
        ...         await self.initialize_monitoring()
        ...
        ...     async def on_system_shutdown(self, event: SystemEvent) -> None:
        ...         await self.flush_metrics()
    """

    async def on_system_startup(self, event: SystemEvent) -> None:
        """Called when the system starts up.

        Args:
            event: The system event with startup information.
        """
        ...

    async def on_system_shutdown(self, event: SystemEvent) -> None:
        """Called when the system shuts down.

        Args:
            event: The system event with shutdown information.
        """
        ...

    async def on_health_check(self, event: SystemEvent) -> None:
        """Called during health check operations.

        Args:
            event: The system event with health check information.
        """
        ...
