"""
DI Container - Dependency Injection with lifetime management.

Features:
- Singleton, transient, and scoped lifetimes
- Auto-wiring from type hints
- YAML-driven configuration
- Protocol-based registration

Version: 0.1.0
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Optional, Type, TypeVar, get_type_hints
import threading
import logging

logger = logging.getLogger(__name__)

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
    factory: Optional[Callable[..., Any]] = None


@dataclass
class ServiceDescriptor:
    """Describes a service for registration."""

    implementation: Type
    lifetime: Lifetime = Lifetime.SINGLETON
    config_key: Optional[str] = None
    factory: Optional[Callable[..., Any]] = None


class DIContainerError(Exception):
    """Base exception for DI container errors."""

    pass


class ServiceNotFoundError(DIContainerError):
    """Raised when a service is not registered."""

    pass


class CircularDependencyError(DIContainerError):
    """Raised when circular dependency is detected."""

    pass


class ScopeRequiredError(DIContainerError):
    """Raised when scope ID is required but not provided."""

    pass


class DIContainer:
    """
    Dependency Injection Container.

    Provides:
    - Service registration with lifetime management
    - Auto-wiring based on type hints
    - Scoped instances for request-level isolation
    - YAML-based configuration support

    Example:
        >>> container = DIContainer()
        >>> container.register(SourceProtocol, TimeoutLoader, Lifetime.SINGLETON)
        >>> loader = container.resolve(SourceProtocol)
    """

    _instance: Optional["DIContainer"] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self._registrations: Dict[Type, Registration] = {}
        self._singletons: Dict[Type, Any] = {}
        self._scoped: Dict[str, Dict[Type, Any]] = {}
        self._config: Dict[str, Any] = {}
        self._resolving: set[Type] = set()  # Track resolution stack for circular deps

    @classmethod
    def get_instance(cls) -> "DIContainer":
        """Get singleton container instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        with cls._lock:
            cls._instance = None

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Load configuration from dict (typically from YAML).

        Args:
            config: Configuration dictionary with 'di' section
        """
        self._config = config
        di_config = config.get("di", {})

        # Register services from config
        services = di_config.get("services", {})
        for service_name, service_config in services.items():
            self._register_from_config(service_name, service_config)

        logger.debug(f"DI Container configured with {len(services)} services")

    def register(
        self,
        interface: Type[T],
        implementation: Optional[Type[T]] = None,
        lifetime: Lifetime = Lifetime.SINGLETON,
        config_key: Optional[str] = None,
        factory: Optional[Callable[..., T]] = None,
    ) -> None:
        """
        Register a service implementation.

        Args:
            interface: The interface/protocol type to register
            implementation: The concrete implementation class
            lifetime: Service lifetime (SINGLETON, TRANSIENT, SCOPED)
            config_key: Optional config key for injecting configuration
            factory: Optional factory function to create instances
        """
        if implementation is None and factory is None:
            implementation = interface  # Self-registration

        self._registrations[interface] = Registration(
            interface=interface,
            implementation=implementation or interface,
            lifetime=lifetime,
            config_key=config_key,
            factory=factory,
        )
        logger.debug(
            f"Registered {interface.__name__} -> {(implementation or interface).__name__} ({lifetime.value})"
        )

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register an existing instance as a singleton.

        Args:
            interface: The interface/protocol type
            instance: The pre-created instance
        """
        self._registrations[interface] = Registration(
            interface=interface,
            implementation=type(instance),
            lifetime=Lifetime.SINGLETON,
        )
        self._singletons[interface] = instance
        logger.debug(f"Registered instance for {interface.__name__}")

    def register_factory(
        self,
        interface: Type[T],
        factory: Callable[..., T],
        lifetime: Lifetime = Lifetime.SINGLETON,
    ) -> None:
        """
        Register a factory function for creating instances.

        Args:
            interface: The interface/protocol type
            factory: Factory function that returns instances
            lifetime: Service lifetime
        """
        self.register(interface, factory=factory, lifetime=lifetime)

    def is_registered(self, interface: Type) -> bool:
        """Check if a service is registered."""
        return interface in self._registrations

    def resolve(self, interface: Type[T], scope_id: Optional[str] = None) -> T:
        """
        Resolve a service instance.

        Args:
            interface: The interface/protocol type to resolve
            scope_id: Optional scope ID for scoped services

        Returns:
            The resolved service instance

        Raises:
            ServiceNotFoundError: If service is not registered
            CircularDependencyError: If circular dependency detected
            ScopeRequiredError: If scope ID required but not provided
        """
        if interface not in self._registrations:
            raise ServiceNotFoundError(
                f"No registration found for {interface.__name__}"
            )

        # Check for circular dependencies
        if interface in self._resolving:
            raise CircularDependencyError(
                f"Circular dependency detected while resolving {interface.__name__}"
            )

        registration = self._registrations[interface]

        # Singleton: return cached or create once
        if registration.lifetime == Lifetime.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(registration)
            return self._singletons[interface]

        # Scoped: return cached for scope or create
        if registration.lifetime == Lifetime.SCOPED:
            if scope_id is None:
                raise ScopeRequiredError(
                    f"Scope ID required for scoped service {interface.__name__}"
                )
            if scope_id not in self._scoped:
                self._scoped[scope_id] = {}
            if interface not in self._scoped[scope_id]:
                self._scoped[scope_id][interface] = self._create_instance(registration)
            return self._scoped[scope_id][interface]

        # Transient: always create new
        return self._create_instance(registration)

    def try_resolve(
        self, interface: Type[T], scope_id: Optional[str] = None
    ) -> Optional[T]:
        """
        Try to resolve a service, returning None if not found.

        Args:
            interface: The interface/protocol type to resolve
            scope_id: Optional scope ID for scoped services

        Returns:
            The resolved service instance or None
        """
        try:
            return self.resolve(interface, scope_id)
        except DIContainerError:
            return None

    def _create_instance(self, registration: Registration) -> Any:
        """Create instance with auto-wiring."""
        self._resolving.add(registration.interface)
        try:
            # Use factory if provided
            if registration.factory is not None:
                return registration.factory()

            impl = registration.implementation

            # Get constructor type hints for auto-wiring
            try:
                hints = get_type_hints(impl.__init__)
            except Exception:
                hints = {}

            # Auto-resolve dependencies
            kwargs: Dict[str, Any] = {}
            for param_name, param_type in hints.items():
                if param_name == "return":
                    continue
                if param_type in self._registrations:
                    kwargs[param_name] = self.resolve(param_type)

            # Add config if specified
            if registration.config_key:
                config_value = self._get_nested_config(registration.config_key)
                if config_value:
                    kwargs["config"] = config_value

            return impl(**kwargs)
        finally:
            self._resolving.discard(registration.interface)

    def _get_nested_config(self, key: str) -> Any:
        """
        Get nested config value by dot-separated key.

        Args:
            key: Dot-separated config path (e.g., "plugins.loader")

        Returns:
            The config value or empty dict if not found
        """
        value = self._config
        for part in key.split("."):
            if isinstance(value, dict):
                value = value.get(part, {})
            else:
                return {}
        return value

    def create_scope(self, scope_id: str) -> "DIScope":
        """
        Create a new scope for scoped services.

        Args:
            scope_id: Unique identifier for the scope

        Returns:
            A DIScope context manager
        """
        return DIScope(self, scope_id)

    def dispose_scope(self, scope_id: str) -> None:
        """
        Dispose all services in a scope.

        Args:
            scope_id: The scope ID to dispose
        """
        if scope_id in self._scoped:
            # Call dispose on disposable services
            for instance in self._scoped[scope_id].values():
                if hasattr(instance, "dispose"):
                    try:
                        instance.dispose()
                    except Exception as e:
                        logger.warning(f"Error disposing service: {e}")
            del self._scoped[scope_id]
            logger.debug(f"Disposed scope: {scope_id}")

    def _register_from_config(self, service_name: str, config: Dict[str, Any]) -> None:
        """
        Register service from YAML config.

        Args:
            service_name: The service interface name
            config: Service configuration dict
        """
        # This requires a type registry to map string names to types
        # For now, log a warning if used
        logger.debug(f"Config-based registration for {service_name}: {config}")

    def clear(self) -> None:
        """Clear all registrations and cached instances."""
        self._registrations.clear()
        self._singletons.clear()
        self._scoped.clear()
        self._config.clear()
        logger.debug("DI Container cleared")

    def get_registrations(self) -> Dict[Type, Registration]:
        """Get all current registrations (for debugging)."""
        return self._registrations.copy()


class DIScope:
    """
    Context manager for scoped service lifetime.

    Example:
        >>> with container.create_scope("request-123") as scope:
        ...     service = scope.resolve(MyService)
    """

    def __init__(self, container: DIContainer, scope_id: str) -> None:
        self._container = container
        self._scope_id = scope_id

    def __enter__(self) -> "DIScope":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._container.dispose_scope(self._scope_id)

    def resolve(self, interface: Type[T]) -> T:
        """Resolve a service within this scope."""
        return self._container.resolve(interface, self._scope_id)

    @property
    def scope_id(self) -> str:
        """Get the scope ID."""
        return self._scope_id


def get_container() -> DIContainer:
    """Get the global DI container instance."""
    return DIContainer.get_instance()
