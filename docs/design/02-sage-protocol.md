---
title: SAGE Knowledge Base - Protocol Design
version: 0.1.0
date: 2025-11-28
status: production-ready
---

# SAGE Protocol Design

> **Source-Analyze-Generate-Evolve: Domain-specific protocol for knowledge management**

## Protocol Overview

The SAGE Protocol defines a four-stage workflow for knowledge management:

| Stage | Name     | Purpose                                    |
|-------|----------|--------------------------------------------|
| **S** | Source   | Knowledge sourcing with timeout protection |
| **A** | Analyze  | Processing, search, analysis               |
| **G** | Generate | Multi-channel output (CLI/MCP/API)         |
| **E** | Evolve   | Metrics, optimization, memory              |

### Philosophy (信达雅)

- **信 (Faithfulness)**: Protocol interfaces accurately describe knowledge workflows
- **达 (Clarity)**: Clear separation of concerns across 4 stages
- **雅 (Elegance)**: "SAGE" forms a meaningful word (智者/wise person)

---

## Data Classes

```python
# src/sage/core/models.py
"""
SAGE Protocol Data Classes.

These dataclasses define the request/response structures for all protocol operations.
"""
from dataclasses import dataclass, field
from typing import Any, Optional, List, Dict


@dataclass
class LoadRequest:
    """Knowledge load request."""
    layers: List[str] = field(default_factory=lambda: ["core"])
    query: Optional[str] = None
    timeout_ms: int = 5000
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoadResult:
    """Knowledge load result."""
    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout
    duration_ms: int
    layers_loaded: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """Search result item."""
    path: str
    score: float
    preview: str
    layer: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceRequest:
    """Knowledge source request for SourceProtocol."""
    layers: List[str] = field(default_factory=lambda: ["core"])
    query: Optional[str] = None
    timeout_ms: int = 5000
    include_metadata: bool = False
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceResult:
    """Knowledge source result from SourceProtocol."""
    content: str
    tokens: int
    status: str  # success | partial | fallback | timeout | error
    duration_ms: int
    source_path: Optional[str] = None
    layers_loaded: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

---

## Protocol Interfaces

```python
# src/sage/core/protocols.py
"""
SAGE Protocol - Domain-specific interfaces for Knowledge Base.

Source-Analyze-Generate-Evolve: A knowledge workflow protocol.
Zero-coupling design: All components communicate via these protocols,
never through direct imports.
"""
from typing import Protocol, runtime_checkable, Any, Dict, List, Optional
from sage.core.models import SourceRequest, SourceResult, SearchResult


@runtime_checkable
class SourceProtocol(Protocol):
    """
    S - Source Protocol: Knowledge sourcing interface.
    
    Responsibilities:
    - Source knowledge content with timeout protection
    - Validate content integrity
    - Provide fallback content on failure
    """

    async def source(self, request: SourceRequest) -> SourceResult:
        """Source knowledge with timeout protection."""
        ...

    async def validate(self, content: str) -> tuple[bool, List[str]]:
        """Validate content integrity. Returns (is_valid, errors)."""
        ...

    async def get_fallback(self) -> str:
        """Get fallback content for emergency situations."""
        ...


@runtime_checkable
class AnalyzeProtocol(Protocol):
    """
    A - Analyze Protocol: Processing and analysis interface.
    
    Responsibilities:
    - Search knowledge base
    - Analyze content for specific tasks
    - Summarize content for token efficiency
    """

    async def search(
        self,
        query: str,
        max_results: int = 10
    ) -> List[SearchResult]:
        """Search knowledge base."""
        ...

    async def analyze(
        self,
        content: str,
        task: str
    ) -> Dict[str, Any]:
        """Analyze content for specific task."""
        ...

    async def summarize(
        self,
        content: str,
        max_tokens: int = 500
    ) -> str:
        """Summarize content for token efficiency."""
        ...


@runtime_checkable
class GenerateProtocol(Protocol):
    """
    G - Generate Protocol: Multi-channel output generation interface.
    
    Responsibilities:
    - Generate content in various formats
    - Serve content via different channels (CLI/MCP/API)
    """

    async def generate(
        self,
        data: Any,
        format: str = "markdown"
    ) -> str:
        """Generate output in specified format."""
        ...

    async def serve(
        self,
        channel: str,
        config: Dict[str, Any]
    ) -> None:
        """Start serving on specified channel."""
        ...


@runtime_checkable
class EvolveProtocol(Protocol):
    """
    E - Evolve Protocol: Metrics, optimization and evolution interface.
    
    Responsibilities:
    - Collect usage metrics
    - Optimize performance
    - Manage session checkpoints
    - Enable continuous learning and improvement
    """

    async def collect_metrics(
        self,
        context: Dict[str, Any]
    ) -> None:
        """Collect metrics for monitoring."""
        ...

    async def optimize(
        self,
        target: str
    ) -> Dict[str, Any]:
        """Optimize specified target."""
        ...

    async def checkpoint(
        self,
        session_id: str
    ) -> str:
        """Create session checkpoint, return checkpoint ID."""
        ...
```

### Protocol Benefits

| Benefit           | Description                                         |
|-------------------|-----------------------------------------------------|
| **Zero Coupling** | Components depend on protocols, not implementations |
| **Testability**   | Easy to mock protocols for unit testing             |
| **Flexibility**   | Multiple implementations can satisfy same protocol  |
| **Type Safety**   | `@runtime_checkable` enables isinstance() checks    |
| **Documentation** | Protocols serve as interface contracts              |

---

## DI Container

### Overview

The Dependency Injection Container manages service lifecycle and provides auto-wiring capabilities:

```python
# src/sage/core/di.py
"""
DI Container - Dependency Injection with lifetime management.

Features:
- Singleton, transient, and scoped lifetimes
- Auto-wiring from type hints
- YAML-driven configuration
- Protocol-based registration
"""
from typing import TypeVar, Type, Dict, Any, Optional, get_type_hints
from enum import Enum
from dataclasses import dataclass
import threading

T = TypeVar("T")


class Lifetime(Enum):
    """Service lifetime options."""
    SINGLETON = "singleton"  # One instance for entire application
    TRANSIENT = "transient"  # New instance every time
    SCOPED = "scoped"  # One instance per scope (e.g., request)


@dataclass
class Registration:
    """Service registration info."""
    interface: Type
    implementation: Type
    lifetime: Lifetime
    config_key: Optional[str] = None


class DIContainer:
    """
    Dependency Injection Container.
    
    Provides:
    - Service registration with lifetime management
    - Auto-wiring based on type hints
    - Scoped instances for request-level isolation
    - YAML-based configuration support
    """

    _instance: Optional["DIContainer"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._registrations: Dict[Type, Registration] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped: Dict[str, Dict[Type, Any]] = {}
        self._config: Dict[str, Any] = {}

    @classmethod
    def get_instance(cls) -> "DIContainer":
        """Get singleton container instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def configure(self, config: Dict[str, Any]) -> None:
        """Load configuration from dict (typically from YAML)."""
        self._config = config

        # Register services from config
        for service_name, service_config in config.get("di", {}).get("services", {}).items():
            self._register_from_config(service_name, service_config)

    def register(
        self,
        interface: Type[T],
        implementation: Type[T],
        lifetime: Lifetime = Lifetime.SINGLETON,
        config_key: Optional[str] = None
    ) -> None:
        """Register a service implementation."""
        self._registrations[interface] = Registration(
            interface=interface,
            implementation=implementation,
            lifetime=lifetime,
            config_key=config_key
        )

    def resolve(self, interface: Type[T], scope_id: Optional[str] = None) -> T:
        """Resolve a service instance."""
        if interface not in self._registrations:
            raise KeyError(f"No registration found for {interface}")

        registration = self._registrations[interface]

        # Singleton: return cached or create once
        if registration.lifetime == Lifetime.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(registration)
            return self._singletons[interface]

        # Scoped: return cached for scope or create
        if registration.lifetime == Lifetime.SCOPED:
            if scope_id is None:
                raise ValueError("Scope ID required for scoped services")
            if scope_id not in self._scoped:
                self._scoped[scope_id] = {}
            if interface not in self._scoped[scope_id]:
                self._scoped[scope_id][interface] = self._create_instance(registration)
            return self._scoped[scope_id][interface]

        # Transient: always create new
        return self._create_instance(registration)

    def _create_instance(self, registration: Registration) -> Any:
        """Create instance with auto-wiring."""
        impl = registration.implementation

        # Get constructor type hints for auto-wiring
        try:
            hints = get_type_hints(impl.__init__)
        except Exception:
            hints = {}

        # Auto-resolve dependencies
        kwargs = {}
        for param_name, param_type in hints.items():
            if param_name == "return":
                continue
            if param_type in self._registrations:
                kwargs[param_name] = self.resolve(param_type)

        # Add config if specified
        if registration.config_key:
            kwargs["config"] = self._get_nested_config(registration.config_key)

        return impl(**kwargs)

    def _get_nested_config(self, key: str) -> Any:
        """Get nested config value by dot-separated key."""
        value = self._config
        for part in key.split("."):
            if isinstance(value, dict):
                value = value.get(part, {})
            else:
                return {}
        return value

    def dispose_scope(self, scope_id: str) -> None:
        """Dispose all services in a scope."""
        if scope_id in self._scoped:
            del self._scoped[scope_id]

    def _register_from_config(self, service_name: str, config: Dict) -> None:
        """Register service from YAML config."""
        # Implementation depends on type registry
        pass


def get_container() -> DIContainer:
    """Get the global DI container instance."""
    return DIContainer.get_instance()
```

### DI Configuration (YAML)

```yaml
# sage.yaml - DI Container Configuration
di:
  auto_wire: true

  services:
    EventBus: # S.A.G.E. aligned event bus
      lifetime: singleton
      implementation: AsyncEventBus      # source.*/analyze.*/generate.*/evolve.* channels

    SourceProtocol:
      lifetime: singleton
      implementation: TimeoutLoader
      config_key: plugins.loader

    AnalyzeProtocol:
      lifetime: transient
      implementation: KnowledgeService

    GenerateProtocol:
      lifetime: scoped
      implementation: MultiChannelOutput

    EvolveProtocol:
      lifetime: singleton
      implementation: MetricsCollector
```

### Usage Example

```python
from sage.core.di import get_container, Lifetime
from sage.core.protocols import SourceProtocol, AnalyzeProtocol

# Get container
container = get_container()

# Register services
container.register(SourceProtocol, TimeoutLoader, Lifetime.SINGLETON)
container.register(AnalyzeProtocol, KnowledgeService, Lifetime.TRANSIENT)

# Resolve services
loader = container.resolve(SourceProtocol)
analyzer = container.resolve(AnalyzeProtocol)

# Use services
result = await loader.source(SourceRequest(layers=["core"]))
results = await analyzer.search("autonomy")
```

---

## EventBus

> **Async pub/sub message broker with S.A.G.E. aligned event channels: source.*/analyze.*/generate.*/evolve.***

### Event Types

```python
# src/sage/core/events/types.py
"""Event type definitions for the EventBus (S.A.G.E. aligned)."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid


class EventType(str, Enum):
    """Standard event types for SAGE."""
    # Loader events
    PRE_LOAD = "loader.pre_load"
    POST_LOAD = "loader.post_load"
    LOAD_ERROR = "loader.error"

    # Knowledge events
    PRE_SEARCH = "knowledge.pre_search"
    POST_SEARCH = "knowledge.post_search"

    # Output events
    PRE_FORMAT = "output.pre_format"
    POST_FORMAT = "output.post_format"

    # Memory events
    CHECKPOINT = "memory.checkpoint"
    RESTORE = "memory.restore"

    # Timeout events
    TIMEOUT = "timeout.triggered"
    CIRCUIT_OPEN = "timeout.circuit_open"
    CIRCUIT_CLOSE = "timeout.circuit_close"


@dataclass
class Event:
    """Base event class."""
    type: EventType | str
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    _cancelled: bool = field(default=False, repr=False)
    _results: List[Any] = field(default_factory=list, repr=False)

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    def cancel(self) -> None:
        """Cancel event propagation."""
        self._cancelled = True

    def add_result(self, result: Any) -> None:
        """Add handler result."""
        self._results.append(result)

    @property
    def results(self) -> List[Any]:
        return self._results.copy()


@dataclass
class LoadEvent(Event):
    """Event for load operations."""
    layer: str = ""
    path: str = ""
    content: Optional[str] = None
    modified_content: Optional[str] = None


@dataclass
class TimeoutEvent(Event):
    """Event for timeout occurrences."""
    layer: str = ""
    elapsed_ms: int = 0
    timeout_ms: int = 0
    fallback_content: Optional[str] = None
```

### EventBus Implementation

```python
# src/sage/core/events/bus.py
"""
EventBus - Async pub/sub message broker (S.A.G.E. aligned).

Event channels aligned with S.A.G.E. protocol:
- source.*    (S) - Knowledge sourcing events
- analyze.*   (A) - Processing & analysis events
- generate.*  (G) - Multi-channel output events
- evolve.*    (E) - Metrics & optimization events

Features:
- Async and sync handler support
- Priority-based execution order
- Event filtering per subscription
- Error isolation between handlers
- Timeout protection for handlers
- Wildcard matching (e.g., "source.*")
"""
from typing import Callable, Awaitable, Any, Optional
from collections import defaultdict
from dataclasses import dataclass
import asyncio
import logging

from sage.core.events.types import Event

logger = logging.getLogger(__name__)


@dataclass
class Subscription:
    """Represents an event subscription."""
    id: str
    event_type: str
    handler: Callable[[Event], Awaitable[Any] | Any]
    priority: int = 100
    filter_fn: Optional[Callable[[Event], bool]] = None
    once: bool = False


class EventBus:
    """
    Async event bus for component communication (S.A.G.E. aligned).
    
    Event channels aligned with S.A.G.E. protocol:
    - source.*    (S) - Knowledge sourcing events
    - analyze.*   (A) - Processing & analysis events
    - generate.*  (G) - Multi-channel output events
    - evolve.*    (E) - Metrics & optimization events
    
    Features:
    - Async and sync handler support
    - Priority-based execution order
    - Event filtering per subscription
    - Error isolation between handlers
    - Timeout protection for handlers
    - Wildcard matching (e.g., "source.*")
    """

    _instance: Optional["EventBus"] = None

    def __init__(self):
        self._subscriptions: dict[str, list[Subscription]] = defaultdict(list)
        self._handler_timeout_ms: int = 1000
        self._subscription_counter: int = 0

    @classmethod
    def get_instance(cls) -> "EventBus":
        """Get singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def subscribe(
        self,
        event_type: str,
        handler: Callable,
        priority: int = 100,
        filter_fn: Optional[Callable[[Event], bool]] = None,
        once: bool = False,
    ) -> str:
        """
        Subscribe to events.
        
        Args:
            event_type: Event type to subscribe to (supports wildcards like "source.*")
            handler: Async or sync handler function
            priority: Lower number = higher priority (default: 100)
            filter_fn: Optional filter function
            once: If True, unsubscribe after first call
            
        Returns:
            Subscription ID for later unsubscription
        """
        self._subscription_counter += 1
        sub_id = f"sub_{self._subscription_counter}"

        subscription = Subscription(
            id=sub_id,
            event_type=event_type,
            handler=handler,
            priority=priority,
            filter_fn=filter_fn,
            once=once,
        )

        self._subscriptions[event_type].append(subscription)
        self._subscriptions[event_type].sort(key=lambda s: s.priority)
        return sub_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe by subscription ID."""
        for event_type, subs in self._subscriptions.items():
            for sub in subs:
                if sub.id == subscription_id:
                    subs.remove(sub)
                    return True
        return False

    async def publish(
        self,
        event: Event,
        timeout_ms: Optional[int] = None
    ) -> Event:
        """
        Publish event to all subscribers with error isolation.
        
        Args:
            event: Event to publish
            timeout_ms: Per-handler timeout (default: 1000ms)
            
        Returns:
            Event with results from handlers
        """
        handlers = self._get_matching_handlers(str(event.type))
        to_remove = []

        for sub in handlers:
            if event.is_cancelled:
                break

            if sub.filter_fn and not sub.filter_fn(event):
                continue

            try:
                handler_timeout = (timeout_ms or self._handler_timeout_ms) / 1000

                if asyncio.iscoroutinefunction(sub.handler):
                    result = await asyncio.wait_for(
                        sub.handler(event),
                        timeout=handler_timeout
                    )
                else:
                    result = await asyncio.wait_for(
                        asyncio.get_event_loop().run_in_executor(
                            None, sub.handler, event
                        ),
                        timeout=handler_timeout
                    )

                if result is not None:
                    event.add_result(result)

                if sub.once:
                    to_remove.append(sub.id)

            except asyncio.TimeoutError:
                logger.warning(f"Handler {sub.id} timed out")
            except Exception as e:
                logger.error(f"Handler {sub.id} failed: {e}")

        # Remove one-time subscriptions
        for sub_id in to_remove:
            self.unsubscribe(sub_id)

        return event

    def _get_matching_handlers(self, event_type: str) -> list[Subscription]:
        """Get handlers matching event type (supports wildcards)."""
        handlers = list(self._subscriptions.get(event_type, []))

        # Wildcard matching: "source.*" matches "source.pre_load" (S.A.G.E. channels)
        for pattern, subs in self._subscriptions.items():
            if pattern.endswith(".*"):
                prefix = pattern[:-2]
                if event_type.startswith(prefix + "."):
                    handlers.extend(subs)

        # Global wildcard "*"
        handlers.extend(self._subscriptions.get("*", []))
        handlers.sort(key=lambda s: s.priority)
        return handlers


def get_event_bus() -> EventBus:
    """Get the global event bus instance (S.A.G.E. aligned)."""
    return EventBus.get_instance()
```

### EventBus Usage

```python
from sage.core.events import get_event_bus, LoadEvent, EventType

bus = get_event_bus()


# Subscribe to S.A.G.E. events
async def on_pre_load(event: LoadEvent) -> LoadEvent:
    print(f"Loading layer: {event.layer}")
    return event


bus.subscribe(EventType.PRE_LOAD, on_pre_load, priority=10)


# Subscribe with wildcard (S.A.G.E. channels: source.*/analyze.*/generate.*/evolve.*)
async def on_any_source_event(event: Event):
    print(f"Source event: {event.type}")


bus.subscribe("source.*", on_any_source_event)

# Publish event
event = LoadEvent(type=EventType.PRE_LOAD, layer="core", path=".knowledge/core/")
result = await bus.publish(event)
```

---

## Application Bootstrap

```python
# src/sage/core/bootstrap.py
"""
Application Bootstrap - Declarative initialization.

Handles:
- Configuration loading
- DI container setup
- EventBus initialization (S.A.G.E. aligned pub/sub)
- Service registration
"""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

from sage.core.di import DIContainer, get_container, Lifetime
from sage.core.events import EventBus, get_event_bus
from sage.core.logging import configure_logging, get_logger
from sage.core.protocols import SourceProtocol, AnalyzeProtocol, GenerateProtocol, EvolveProtocol

logger = get_logger(__name__)


async def bootstrap(
    config_path: Optional[Path] = None,
    config_override: Optional[Dict[str, Any]] = None
) -> DIContainer:
    """
    Bootstrap the SAGE application.
    
    Args:
        config_path: Path to sage.yaml (default: ./sage.yaml)
        config_override: Override config values
        
    Returns:
        Configured DI container
    """
    # Load configuration
    config = _load_config(config_path or Path("sage.yaml"))
    if config_override:
        config = _merge_config(config, config_override)

    # Configure logging
    log_config = config.get("logging", {})
    configure_logging(
        level=log_config.get("level", "INFO"),
        format=log_config.get("format", "console"),
    )

    logger.info("bootstrapping application", config_path=str(config_path))

    # Setup DI container
    container = get_container()
    container.configure(config)

    # Register core services
    _register_core_services(container, config)

    # Setup EventBus subscriptions (S.A.G.E. aligned channels)
    event_bus = get_event_bus()
    _setup_event_subscriptions(event_bus, config)

    logger.info("bootstrap complete", services=len(container._registrations))
    return container


def _load_config(path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not path.exists():
        logger.warning("config file not found, using defaults", path=str(path))
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _merge_config(base: Dict, override: Dict) -> Dict:
    """Deep merge configuration dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_config(result[key], value)
        else:
            result[key] = value
    return result


def _register_core_services(container: DIContainer, config: Dict) -> None:
    """Register core protocol implementations."""
    from sage.core.loader import TimeoutLoader
    from sage.core.knowledge import KnowledgeService
    from sage.core.output import MultiChannelOutput
    from sage.core.metrics import MetricsCollector

    container.register(SourceProtocol, TimeoutLoader, Lifetime.SINGLETON)
    container.register(AnalyzeProtocol, KnowledgeService, Lifetime.TRANSIENT)
    container.register(GenerateProtocol, MultiChannelOutput, Lifetime.SCOPED)
    container.register(EvolveProtocol, MetricsCollector, Lifetime.SINGLETON)


def _setup_event_subscriptions(event_bus: EventBus, config: Dict) -> None:
    """Setup event subscriptions from config (S.A.G.E. aligned)."""
    subscriptions = config.get("events", {}).get("subscriptions", [])

    for sub in subscriptions:
        event_pattern = sub.get("event")
        handlers = sub.get("handlers", [])

        for handler_name in handlers:
            logger.debug("subscribing handler", event=event_pattern, handler=handler_name)
            # Handler registration based on handler registry
```

### Entry Point

```python
# src/sage/__main__.py
"""
Unified Entry Point.

Usage:
    python -m sage serve [--service cli|mcp|api|all]
    python -m sage --version
"""
import asyncio
import sys
import argparse

from sage import __version__
from sage.core.bootstrap import bootstrap


async def main():
    parser = argparse.ArgumentParser(prog="sage")
    parser.add_argument("--version", action="store_true")

    subparsers = parser.add_subparsers(dest="command")

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start services")
    serve_parser.add_argument(
        "--service",
        choices=["cli", "mcp", "api", "all"],
        default="all",
        help="Service to start"
    )
    serve_parser.add_argument("--host", default="localhost")
    serve_parser.add_argument("--port", type=int)

    args = parser.parse_args()

    if args.version:
        print(f"sage {__version__}")
        return 0

    if args.command == "serve":
        # Bootstrap application
        container = await bootstrap()

        # Start requested service(s)
        if args.service in ("mcp", "all"):
            from sage.services.mcp_server import start_mcp_server
            await start_mcp_server(host=args.host, port=args.port or 8000)

        if args.service in ("api", "all"):
            from sage.services.http_server import start_api_server
            start_api_server(host=args.host, port=args.port or 8080)

        if args.service == "cli":
            from sage.services.cli import app
            app()

        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
```

---

## Configuration Settings

```python
# src/sage/core/config.py
"""
Configuration Management with pydantic-settings.

Supports:
- Environment variables (SAGE_*)
- User config file
- Project config file
- Package defaults
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Literal, Optional


class SageSettings(BaseSettings):
    """Zero-coupling configuration with multiple sources."""

    model_config = SettingsConfigDict(
        env_prefix="SAGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Version
    version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)

    # Timeout settings
    timeout_global_max_ms: int = Field(default=10000, description="Global max timeout")
    timeout_default_ms: int = Field(default=5000, description="Default timeout")

    # Loading settings
    loading_max_tokens: int = Field(default=4000, description="Max tokens per request")
    loading_cache_enabled: bool = Field(default=True, description="Enable caching")
    loading_cache_ttl_seconds: int = Field(default=300, description="Cache TTL")

    # Logging settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    log_format: Literal["console", "json"] = Field(default="console")

    # CORS settings (for API)
    cors_origins: list[str] = Field(default_factory=list)

    # Paths
    config_path: Optional[Path] = Field(default=None)
    content_root: Path = Field(default=Path("content"))

    @classmethod
    def load(cls, project_config: Optional[Path] = None) -> "SageSettings":
        """Load settings from all sources with proper precedence."""
        if project_config and project_config.exists():
            import yaml
            with open(project_config) as f:
                yaml_config = yaml.safe_load(f) or {}
            return cls(**yaml_config)
        return cls()


def get_settings() -> SageSettings:
    """Get application settings."""
    return SageSettings.load(Path("sage.yaml"))
```

---

## References

### Design Documents

- **Architecture**: See `01-architecture.md`
- **Services**: See `03-services.md`
- **Plugin System**: See `05-plugin-memory.md`

### Architecture Decision Records

- **ADR-0002**: `.context/decisions/ADR-0002-sage-protocol.md` — SAGE Protocol design decisions

---

**Document Status**: Pending Level 5 Expert Committee Evaluation  
**Last Updated**: 2025-11-29
