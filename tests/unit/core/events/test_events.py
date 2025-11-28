"""Unit tests for SAGE event system.

Tests cover:
- Event classes and serialization
- EventType enum
- EventBus subscribe/publish
- Priority-based ordering
- Wildcard matching
- Timeout protection
- PluginAdapter
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from sage.core.events import (
    Event,
    EventBus,
    EventType,
    LoadEvent,
    PluginAdapter,
    PluginEvent,
    SearchEvent,
    Subscription,
    SystemEvent,
    TimeoutEvent,
    adapt_plugin,
    create_event_from_dict,
    get_event_bus,
    reset_event_bus,
)


class TestEventType:
    """Tests for EventType enum."""

    def test_loader_events_exist(self) -> None:
        """Test loader event types are defined."""
        assert EventType.LOADER_START.value == "loader.start"
        assert EventType.LOADER_COMPLETE.value == "loader.complete"
        assert EventType.LOADER_ERROR.value == "loader.error"
        assert EventType.LOADER_LAYER_LOADED.value == "loader.layer_loaded"

    def test_timeout_events_exist(self) -> None:
        """Test timeout event types are defined."""
        assert EventType.TIMEOUT_WARNING.value == "timeout.warning"
        assert EventType.TIMEOUT_EXCEEDED.value == "timeout.exceeded"
        assert EventType.TIMEOUT_RECOVERED.value == "timeout.recovered"

    def test_search_events_exist(self) -> None:
        """Test search event types are defined."""
        assert EventType.SEARCH_START.value == "search.start"
        assert EventType.SEARCH_COMPLETE.value == "search.complete"
        assert EventType.SEARCH_ERROR.value == "search.error"

    def test_plugin_events_exist(self) -> None:
        """Test plugin event types are defined."""
        assert EventType.PLUGIN_REGISTERED.value == "plugin.registered"
        assert EventType.PLUGIN_UNREGISTERED.value == "plugin.unregistered"
        assert EventType.PLUGIN_ERROR.value == "plugin.error"

    def test_system_events_exist(self) -> None:
        """Test system event types are defined."""
        assert EventType.SYSTEM_STARTUP.value == "system.startup"
        assert EventType.SYSTEM_SHUTDOWN.value == "system.shutdown"
        assert EventType.SYSTEM_HEALTH_CHECK.value == "system.health_check"


class TestEvent:
    """Tests for Event base class."""

    def test_event_creation(self) -> None:
        """Test basic event creation."""
        event = Event(event_type=EventType.LOADER_START, source="test")
        assert event.event_type == EventType.LOADER_START
        assert event.source == "test"
        assert event.event_id is not None
        assert isinstance(event.timestamp, datetime)

    def test_event_with_custom_data(self) -> None:
        """Test event with custom data."""
        event = Event(
            event_type=EventType.LOADER_START,
            source="test",
            data={"key": "value"},
            metadata={"trace_id": "123"},
        )
        assert event.data["key"] == "value"
        assert event.metadata["trace_id"] == "123"

    def test_event_to_dict(self) -> None:
        """Test event serialization to dict."""
        event = Event(
            event_type=EventType.LOADER_START,
            source="test",
            data={"layer": "core"},
        )
        d = event.to_dict()
        assert d["event_type"] == "loader.start"
        assert d["source"] == "test"
        assert d["data"]["layer"] == "core"
        assert "timestamp" in d
        assert "event_id" in d

    def test_event_from_dict(self) -> None:
        """Test event deserialization from dict."""
        now = datetime.now(timezone.utc)
        d = {
            "event_type": "loader.start",
            "timestamp": now.isoformat(),
            "event_id": "test-id",
            "source": "test",
            "data": {"layer": "core"},
            "metadata": {},
        }
        event = Event.from_dict(d)
        assert event.event_type == EventType.LOADER_START
        assert event.source == "test"
        assert event.event_id == "test-id"

    def test_event_with_custom_event_type(self) -> None:
        """Test event with custom string event type."""
        event = Event(event_type="custom.event", source="test")
        assert event.event_type == "custom.event"


class TestLoadEvent:
    """Tests for LoadEvent class."""

    def test_load_event_creation(self) -> None:
        """Test LoadEvent creation with specific fields."""
        event = LoadEvent(
            event_type=EventType.LOADER_START,
            source="loader",
            layer="core",
            file_count=10,
            duration_ms=150.5,
        )
        assert event.layer == "core"
        assert event.file_count == 10
        assert event.duration_ms == 150.5
        assert event.data["layer"] == "core"
        assert event.data["file_count"] == 10


class TestTimeoutEvent:
    """Tests for TimeoutEvent class."""

    def test_timeout_event_creation(self) -> None:
        """Test TimeoutEvent creation with specific fields."""
        event = TimeoutEvent(
            event_type=EventType.TIMEOUT_WARNING,
            source="timeout_manager",
            operation="load_layer",
            timeout_level="T3",
            elapsed_ms=1800.0,
            limit_ms=2000.0,
        )
        assert event.operation == "load_layer"
        assert event.timeout_level == "T3"
        assert event.elapsed_ms == 1800.0
        assert event.limit_ms == 2000.0


class TestSearchEvent:
    """Tests for SearchEvent class."""

    def test_search_event_creation(self) -> None:
        """Test SearchEvent creation with specific fields."""
        event = SearchEvent(
            event_type=EventType.SEARCH_COMPLETE,
            source="search",
            query="timeout",
            results_count=5,
            layers_searched=["core", "guidelines"],
            duration_ms=50.0,
        )
        assert event.query == "timeout"
        assert event.results_count == 5
        assert event.layers_searched == ["core", "guidelines"]


class TestSubscription:
    """Tests for Subscription class."""

    def test_subscription_creation(self) -> None:
        """Test subscription creation."""

        async def handler(event: Event) -> None:
            pass

        sub = Subscription(
            event_pattern="loader.*",
            handler=handler,
            priority=50,
        )
        assert sub.event_pattern == "loader.*"
        assert sub.priority == 50
        assert sub.subscription_id.startswith("sub_")

    def test_subscription_exact_match(self) -> None:
        """Test exact pattern matching."""

        async def handler(event: Event) -> None:
            pass

        sub = Subscription(event_pattern="loader.start", handler=handler)
        assert sub.matches("loader.start") is True
        assert sub.matches("loader.complete") is False

    def test_subscription_wildcard_match(self) -> None:
        """Test wildcard pattern matching."""

        async def handler(event: Event) -> None:
            pass

        sub = Subscription(event_pattern="loader.*", handler=handler)
        assert sub.matches("loader.start") is True
        assert sub.matches("loader.complete") is True
        assert sub.matches("search.start") is False

    def test_subscription_all_match(self) -> None:
        """Test match-all pattern."""

        async def handler(event: Event) -> None:
            pass

        sub = Subscription(event_pattern="*", handler=handler)
        assert sub.matches("loader.start") is True
        assert sub.matches("search.complete") is True
        assert sub.matches("anything") is True


class TestEventBus:
    """Tests for EventBus class."""

    @pytest.fixture
    def bus(self) -> EventBus:
        """Create a fresh EventBus for each test."""
        return EventBus()

    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self, bus: EventBus) -> None:
        """Test basic subscribe and publish."""
        received: list[Event] = []

        async def handler(event: Event) -> None:
            received.append(event)

        bus.subscribe("loader.start", handler)
        event = Event(event_type=EventType.LOADER_START, source="test")
        count = await bus.publish(event)

        assert count == 1
        assert len(received) == 1
        assert received[0].event_id == event.event_id

    @pytest.mark.asyncio
    async def test_wildcard_subscription(self, bus: EventBus) -> None:
        """Test wildcard pattern subscription."""
        received: list[Event] = []

        async def handler(event: Event) -> None:
            received.append(event)

        bus.subscribe("loader.*", handler)

        await bus.publish(Event(event_type=EventType.LOADER_START, source="test"))
        await bus.publish(Event(event_type=EventType.LOADER_COMPLETE, source="test"))
        await bus.publish(Event(event_type=EventType.SEARCH_START, source="test"))

        assert len(received) == 2

    @pytest.mark.asyncio
    async def test_priority_ordering(self, bus: EventBus) -> None:
        """Test handlers are called in priority order."""
        order: list[int] = []

        async def handler_low(event: Event) -> None:
            order.append(1000)

        async def handler_high(event: Event) -> None:
            order.append(10)

        async def handler_medium(event: Event) -> None:
            order.append(100)

        bus.subscribe("test.event", handler_low, priority=1000)
        bus.subscribe("test.event", handler_high, priority=10)
        bus.subscribe("test.event", handler_medium, priority=100)

        await bus.publish(Event(event_type="test.event", source="test"))

        assert order == [10, 100, 1000]

    @pytest.mark.asyncio
    async def test_unsubscribe(self, bus: EventBus) -> None:
        """Test unsubscribe removes handler."""
        received: list[Event] = []

        async def handler(event: Event) -> None:
            received.append(event)

        sub_id = bus.subscribe("test.event", handler)
        await bus.publish(Event(event_type="test.event", source="test"))
        assert len(received) == 1

        bus.unsubscribe(sub_id)
        await bus.publish(Event(event_type="test.event", source="test"))
        assert len(received) == 1  # No new events

    @pytest.mark.asyncio
    async def test_handler_timeout(self, bus: EventBus) -> None:
        """Test handler timeout protection."""
        errors: list[Exception] = []

        def error_handler(
            error: Exception, event: Event, sub: Subscription
        ) -> None:
            errors.append(error)

        bus = EventBus(default_timeout_ms=100, error_handler=error_handler)

        async def slow_handler(event: Event) -> None:
            await asyncio.sleep(1.0)  # Will timeout

        bus.subscribe("test.event", slow_handler, timeout_ms=50)
        await bus.publish(Event(event_type="test.event", source="test"))

        assert len(errors) == 1
        assert isinstance(errors[0], asyncio.TimeoutError)

    @pytest.mark.asyncio
    async def test_handler_error_isolation(self, bus: EventBus) -> None:
        """Test handler errors don't affect other handlers."""
        received: list[str] = []

        async def handler_ok1(event: Event) -> None:
            received.append("ok1")

        async def handler_error(event: Event) -> None:
            raise ValueError("Test error")

        async def handler_ok2(event: Event) -> None:
            received.append("ok2")

        bus.subscribe("test.event", handler_ok1, priority=10)
        bus.subscribe("test.event", handler_error, priority=50)
        bus.subscribe("test.event", handler_ok2, priority=100)

        await bus.publish(Event(event_type="test.event", source="test"))

        assert "ok1" in received
        assert "ok2" in received

    def test_subscription_count(self, bus: EventBus) -> None:
        """Test subscription count property."""

        async def handler(event: Event) -> None:
            pass

        assert bus.subscription_count == 0
        bus.subscribe("event1", handler)
        assert bus.subscription_count == 1
        bus.subscribe("event2", handler)
        assert bus.subscription_count == 2

    def test_clear(self, bus: EventBus) -> None:
        """Test clear removes all subscriptions."""

        async def handler(event: Event) -> None:
            pass

        bus.subscribe("event1", handler)
        bus.subscribe("event2", handler)
        assert bus.subscription_count == 2

        bus.clear()
        assert bus.subscription_count == 0


class TestGlobalEventBus:
    """Tests for global event bus singleton."""

    def setup_method(self) -> None:
        """Reset global bus before each test."""
        reset_event_bus()

    def teardown_method(self) -> None:
        """Reset global bus after each test."""
        reset_event_bus()

    def test_get_event_bus_singleton(self) -> None:
        """Test get_event_bus returns same instance."""
        bus1 = get_event_bus()
        bus2 = get_event_bus()
        assert bus1 is bus2

    def test_reset_event_bus(self) -> None:
        """Test reset creates new instance."""
        bus1 = get_event_bus()

        async def handler(event: Event) -> None:
            pass

        bus1.subscribe("test", handler)
        assert bus1.subscription_count == 1

        reset_event_bus()
        bus2 = get_event_bus()
        assert bus2.subscription_count == 0


class TestPluginAdapter:
    """Tests for PluginAdapter class."""

    def setup_method(self) -> None:
        """Reset global bus before each test."""
        reset_event_bus()

    def teardown_method(self) -> None:
        """Reset global bus after each test."""
        reset_event_bus()

    def test_adapter_creation(self) -> None:
        """Test adapter creation."""

        class TestPlugin:
            name = "test-plugin"

        plugin = TestPlugin()
        adapter = PluginAdapter(plugin)
        assert adapter.plugin_name == "test-plugin"
        assert adapter.is_registered is False

    def test_adapter_register_with_methods(self) -> None:
        """Test adapter registers plugin methods."""

        class TestPlugin:
            name = "test-plugin"

            def on_load_start(self, event: Event) -> None:
                pass

            def on_search_complete(self, event: Event) -> None:
                pass

        plugin = TestPlugin()
        adapter = PluginAdapter(plugin)
        count = adapter.register()

        assert count == 2
        assert adapter.is_registered is True

    def test_adapter_unregister(self) -> None:
        """Test adapter unregisters plugin."""

        class TestPlugin:
            def on_load_start(self, event: Event) -> None:
                pass

        plugin = TestPlugin()
        adapter = PluginAdapter(plugin)
        adapter.register()
        assert adapter.is_registered is True

        adapter.unregister()
        assert adapter.is_registered is False

    @pytest.mark.asyncio
    async def test_adapted_plugin_receives_events(self) -> None:
        """Test adapted plugin receives events."""
        received: list[Event] = []

        class TestPlugin:
            def on_load_start(self, event: Event) -> None:
                received.append(event)

        plugin = TestPlugin()
        adapter = PluginAdapter(plugin)
        adapter.register()

        bus = get_event_bus()
        event = LoadEvent(
            event_type=EventType.LOADER_START,
            source="test",
            layer="core",
        )
        await bus.publish(event)

        assert len(received) == 1
        assert received[0].event_id == event.event_id


class TestAdaptPluginFunction:
    """Tests for adapt_plugin convenience function."""

    def setup_method(self) -> None:
        """Reset global bus before each test."""
        reset_event_bus()

    def teardown_method(self) -> None:
        """Reset global bus after each test."""
        reset_event_bus()

    def test_adapt_plugin_auto_register(self) -> None:
        """Test adapt_plugin with auto_register=True."""

        class TestPlugin:
            def on_load_start(self, event: Event) -> None:
                pass

        adapter = adapt_plugin(TestPlugin())
        assert adapter.is_registered is True

    def test_adapt_plugin_no_auto_register(self) -> None:
        """Test adapt_plugin with auto_register=False."""

        class TestPlugin:
            def on_load_start(self, event: Event) -> None:
                pass

        adapter = adapt_plugin(TestPlugin(), auto_register=False)
        assert adapter.is_registered is False


class TestCreateEventFromDict:
    """Tests for create_event_from_dict function."""

    def test_create_load_event(self) -> None:
        """Test creating LoadEvent from dict."""
        event = create_event_from_dict(
            EventType.LOADER_START,
            {"layer": "core", "file_count": 5},
            source="test",
        )
        assert isinstance(event, LoadEvent)
        assert event.layer == "core"
        assert event.file_count == 5

    def test_create_timeout_event(self) -> None:
        """Test creating TimeoutEvent from dict."""
        event = create_event_from_dict(
            EventType.TIMEOUT_WARNING,
            {"operation": "load", "timeout_level": "T3"},
            source="test",
        )
        assert isinstance(event, TimeoutEvent)
        assert event.operation == "load"
        assert event.timeout_level == "T3"

    def test_create_search_event(self) -> None:
        """Test creating SearchEvent from dict."""
        event = create_event_from_dict(
            EventType.SEARCH_START,
            {"query": "test", "layers_searched": ["core"]},
            source="test",
        )
        assert isinstance(event, SearchEvent)
        assert event.query == "test"

    def test_create_plugin_event(self) -> None:
        """Test creating PluginEvent from dict."""
        event = create_event_from_dict(
            EventType.PLUGIN_REGISTERED,
            {"plugin_name": "test-plugin", "plugin_version": "1.0.0"},
            source="test",
        )
        assert isinstance(event, PluginEvent)
        assert event.plugin_name == "test-plugin"

    def test_create_system_event(self) -> None:
        """Test creating SystemEvent from dict."""
        event = create_event_from_dict(
            EventType.SYSTEM_STARTUP,
            {"component": "mcp", "status": "starting"},
            source="test",
        )
        assert isinstance(event, SystemEvent)
        assert event.component == "mcp"

    def test_create_generic_event(self) -> None:
        """Test creating generic Event for unknown type."""
        event = create_event_from_dict(
            "custom.event",
            {"key": "value"},
            source="test",
        )
        assert isinstance(event, Event)
        assert event.data["key"] == "value"
