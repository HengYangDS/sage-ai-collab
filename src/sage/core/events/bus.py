"""EventBus implementation for SAGE Knowledge Base.

This module provides an async event bus with support for:
- Subscribe/publish pattern
- Wildcard event matching
- Priority-based handler ordering
- Per-handler timeout protection

Version: 0.1.0
"""

from __future__ import annotations

import asyncio
import fnmatch
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine

from sage.core.events.events import Event, EventType

__all__ = [
    "EventBus",
    "Subscription",
    "get_event_bus",
    "reset_event_bus",
]

logger = logging.getLogger(__name__)

# Type alias for async event handlers
AsyncHandler = Callable[[Event], Coroutine[Any, Any, None]]


@dataclass
class Subscription:
    """Represents a subscription to an event type.

    Attributes:
        event_pattern: The event type or wildcard pattern to match.
        handler: The async function to call when the event matches.
        priority: Handler priority (lower = earlier execution).
        timeout_ms: Per-handler timeout in milliseconds.
        subscription_id: Unique identifier for this subscription.
    """

    event_pattern: str
    handler: AsyncHandler
    priority: int = 100
    timeout_ms: float = 5000.0
    subscription_id: str = field(default_factory=lambda: "")

    _id_counter: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        """Generate unique subscription ID if not provided."""
        if not self.subscription_id:
            Subscription._id_counter += 1
            self.subscription_id = f"sub_{Subscription._id_counter}"

    def matches(self, event_type: str) -> bool:
        """Check if this subscription matches the given event type.

        Supports wildcard patterns:
        - "loader.*" matches "loader.start", "loader.complete", etc.
        - "*" matches all events
        - "*.error" matches "loader.error", "search.error", etc.

        Args:
            event_type: The event type to match against.

        Returns:
            True if the pattern matches the event type.
        """
        return fnmatch.fnmatch(event_type, self.event_pattern)


class EventBus:
    """Async event bus with priority-based subscription ordering.

    The EventBus provides a central hub for event-driven communication
    between components. It supports:

    - Wildcard subscriptions (e.g., "loader.*" matches all loader events)
    - Priority-based handler ordering (lower priority executes first)
    - Per-handler timeout protection (prevents slow handlers from blocking)
    - Error isolation (handler errors don't affect other handlers)

    Example:
        >>> bus = EventBus()
        >>> async def on_load(event: Event) -> None:
        ...     print(f"Loading: {event.data}")
        ...
        >>> bus.subscribe("loader.*", on_load, priority=100)
        >>> await bus.publish(LoadEvent(
        ...     event_type=EventType.LOADER_START,
        ...     source="test",
        ...     layer="core"
        ... ))
    """

    def __init__(
        self,
        default_timeout_ms: float = 5000.0,
        error_handler: Callable[[Exception, Event, Subscription], None] | None = None,
    ) -> None:
        """Initialize the EventBus.

        Args:
            default_timeout_ms: Default timeout for handlers in milliseconds.
            error_handler: Optional callback for handler errors.
        """
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._all_subscriptions: list[Subscription] = []
        self._default_timeout_ms = default_timeout_ms
        self._error_handler = error_handler or self._default_error_handler
        self._is_publishing = False
        self._pending_unsubscribes: list[str] = []

    def subscribe(
        self,
        event_pattern: str | EventType,
        handler: AsyncHandler,
        *,
        priority: int = 100,
        timeout_ms: float | None = None,
    ) -> str:
        """Subscribe to events matching a pattern.

        Args:
            event_pattern: Event type or wildcard pattern (e.g., "loader.*").
            handler: Async function to call when the event matches.
            priority: Handler priority (lower = earlier execution). Default: 100.
            timeout_ms: Per-handler timeout in milliseconds. Default: bus default.

        Returns:
            Subscription ID that can be used to unsubscribe.

        Example:
            >>> sub_id = bus.subscribe("loader.start", handle_start)
            >>> bus.subscribe("loader.*", handle_all_loader, priority=50)
            >>> bus.subscribe("*", log_all_events, priority=1000)
        """
        pattern = (
            event_pattern.value
            if isinstance(event_pattern, EventType)
            else event_pattern
        )

        subscription = Subscription(
            event_pattern=pattern,
            handler=handler,
            priority=priority,
            timeout_ms=timeout_ms or self._default_timeout_ms,
        )

        self._subscriptions[pattern].append(subscription)
        self._all_subscriptions.append(subscription)

        # Sort by priority (lower = earlier)
        self._all_subscriptions.sort(key=lambda s: s.priority)

        logger.debug(
            f"Subscribed to '{pattern}' with priority {priority}, "
            f"id={subscription.subscription_id}"
        )

        return subscription.subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe a handler by subscription ID.

        Args:
            subscription_id: The ID returned from subscribe().

        Returns:
            True if the subscription was found and removed.
        """
        if self._is_publishing:
            # Defer unsubscribing until publish completes
            self._pending_unsubscribes.append(subscription_id)
            return True

        return self._do_unsubscribe(subscription_id)

    def _do_unsubscribe(self, subscription_id: str) -> bool:
        """Actually perform the unsubscribe operation."""
        found = False

        # Remove from all_subscriptions
        self._all_subscriptions = [
            s for s in self._all_subscriptions if s.subscription_id != subscription_id
        ]

        # Remove from pattern-specific lists
        for pattern, subs in list(self._subscriptions.items()):
            original_len = len(subs)
            self._subscriptions[pattern] = [
                s for s in subs if s.subscription_id != subscription_id
            ]
            if len(self._subscriptions[pattern]) < original_len:
                found = True
            if not self._subscriptions[pattern]:
                del self._subscriptions[pattern]

        if found:
            logger.debug(f"Unsubscribed: {subscription_id}")

        return found

    async def publish(self, event: Event) -> int:
        """Publish an event to all matching subscribers.

        Handlers are called in priority order (lower priority first).
        Each handler has timeout protection and error isolation.

        Args:
            event: The event to publish.

        Returns:
            Number of handlers called.

        Example:
            >>> count = await bus.publish(LoadEvent(
            ...     event_type=EventType.LOADER_START,
            ...     source="loader",
            ...     layer="core"
            ... ))
            >>> print(f"Notified {count} handlers")
        """
        event_type = (
            event.event_type.value
            if isinstance(event.event_type, EventType)
            else event.event_type
        )

        # Find matching subscriptions
        matching = [s for s in self._all_subscriptions if s.matches(event_type)]

        if not matching:
            logger.debug(f"No subscribers for event: {event_type}")
            return 0

        logger.debug(
            f"Publishing {event_type} to {len(matching)} handlers, "
            f"event_id={event.event_id}"
        )

        self._is_publishing = True
        handlers_called = 0

        try:
            for subscription in matching:
                try:
                    await self._call_handler_with_timeout(subscription, event)
                    handlers_called += 1
                except asyncio.TimeoutError:
                    logger.warning(
                        f"Handler timeout for {event_type}: "
                        f"{subscription.subscription_id} "
                        f"(limit: {subscription.timeout_ms}ms)"
                    )
                    self._error_handler(
                        asyncio.TimeoutError(
                            f"Handler exceeded {subscription.timeout_ms}ms timeout"
                        ),
                        event,
                        subscription,
                    )
                except Exception as e:
                    logger.exception(
                        f"Handler error for {event_type}: "
                        f"{subscription.subscription_id}: {e}"
                    )
                    self._error_handler(e, event, subscription)
        finally:
            self._is_publishing = False
            # Process pending unsubscribes
            for sub_id in self._pending_unsubscribes:
                self._do_unsubscribe(sub_id)
            self._pending_unsubscribes.clear()

        return handlers_called

    @staticmethod
    async def _call_handler_with_timeout(
        subscription: Subscription, event: Event
    ) -> None:
        """Call a handler with timeout protection.

        Args:
            subscription: The subscription containing the handler.
            event: The event to pass to the handler.

        Raises:
            asyncio.TimeoutError: If handler exceeds timeout.
        """
        timeout_seconds = subscription.timeout_ms / 1000.0
        await asyncio.wait_for(subscription.handler(event), timeout=timeout_seconds)

    @staticmethod
    def _default_error_handler(
        error: Exception, event: Event, subscription: Subscription
    ) -> None:
        """Default error handler that logs errors."""
        logger.error(
            f"Event handler error: {error}, "
            f"event_type={event.event_type}, "
            f"subscription={subscription.subscription_id}"
        )

    def clear(self) -> None:
        """Remove all subscriptions."""
        self._subscriptions.clear()
        self._all_subscriptions.clear()
        logger.debug("EventBus cleared all subscriptions")

    @property
    def subscription_count(self) -> int:
        """Get the total number of active subscriptions."""
        return len(self._all_subscriptions)

    def get_subscriptions(self, event_pattern: str | None = None) -> list[Subscription]:
        """Get a list of subscriptions, optionally filtered by pattern.

        Args:
            event_pattern: Optional pattern to filter subscriptions.

        Returns:
            List of matching subscriptions.
        """
        if event_pattern is None:
            return list(self._all_subscriptions)
        return list(self._subscriptions.get(event_pattern, []))


# Global event bus instance (singleton pattern)
_global_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """Get the global EventBus instance.

    Returns:
        The singleton EventBus instance.

    Example:
        >>> bus = get_event_bus()
        >>> bus.subscribe("loader.*", my_handler)
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def reset_event_bus() -> None:
    """Reset the global EventBus instance.

    Useful for testing to ensure a clean state.
    """
    global _global_event_bus
    if _global_event_bus is not None:
        _global_event_bus.clear()
    _global_event_bus = None
