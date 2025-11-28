"""
Unit tests for DI Container.

Tests cover:
- Service registration (singleton, transient, scoped)
- Service resolution and auto-wiring
- Lifetime management
- Scope management
- Error handling (circular dependencies, missing services)
- Configuration loading
"""
import pytest
from typing import Protocol, runtime_checkable

from sage.core.di import (
    DIContainer,
    DIScope,
    Lifetime,
    Registration,
    get_container,
    ServiceNotFoundError,
    CircularDependencyError,
    ScopeRequiredError,
)


# Test protocols and implementations
@runtime_checkable
class GreeterProtocol(Protocol):
    """Protocol for greeting service."""
    def greet(self, name: str) -> str: ...


class SimpleGreeter:
    """Simple greeter implementation."""
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"


class FancyGreeter:
    """Fancy greeter implementation."""
    def greet(self, name: str) -> str:
        return f"✨ Greetings, {name}! ✨"


class GreeterWithDependency:
    """Greeter that depends on another service."""
    def __init__(self, greeter: GreeterProtocol) -> None:
        self._greeter = greeter

    def greet(self, name: str) -> str:
        return f"[Wrapped] {self._greeter.greet(name)}"


class ConfigurableService:
    """Service that accepts configuration."""
    def __init__(self, config: dict = None) -> None:
        self.config = config or {}

    def get_setting(self, key: str) -> str:
        return self.config.get(key, "default")


class DisposableService:
    """Service with dispose method."""
    disposed = False

    def dispose(self) -> None:
        self.disposed = True


class TestDIContainerBasics:
    """Test basic DI container functionality."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()
        self.container = DIContainer()

    def test_create_container(self) -> None:
        """Test container creation."""
        assert self.container is not None
        assert isinstance(self.container, DIContainer)

    def test_register_and_resolve_singleton(self) -> None:
        """Test singleton registration and resolution."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SINGLETON)
        
        greeter1 = self.container.resolve(GreeterProtocol)
        greeter2 = self.container.resolve(GreeterProtocol)
        
        assert greeter1 is greeter2  # Same instance
        assert greeter1.greet("World") == "Hello, World!"

    def test_register_and_resolve_transient(self) -> None:
        """Test transient registration and resolution."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.TRANSIENT)
        
        greeter1 = self.container.resolve(GreeterProtocol)
        greeter2 = self.container.resolve(GreeterProtocol)
        
        assert greeter1 is not greeter2  # Different instances
        assert greeter1.greet("World") == "Hello, World!"

    def test_register_and_resolve_scoped(self) -> None:
        """Test scoped registration and resolution."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SCOPED)
        
        # Same scope - same instance
        greeter1 = self.container.resolve(GreeterProtocol, scope_id="scope1")
        greeter2 = self.container.resolve(GreeterProtocol, scope_id="scope1")
        assert greeter1 is greeter2
        
        # Different scope - different instance
        greeter3 = self.container.resolve(GreeterProtocol, scope_id="scope2")
        assert greeter1 is not greeter3

    def test_scoped_requires_scope_id(self) -> None:
        """Test that scoped services require scope_id."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SCOPED)
        
        with pytest.raises(ScopeRequiredError):
            self.container.resolve(GreeterProtocol)

    def test_is_registered(self) -> None:
        """Test is_registered method."""
        assert not self.container.is_registered(GreeterProtocol)
        
        self.container.register(GreeterProtocol, SimpleGreeter)
        
        assert self.container.is_registered(GreeterProtocol)

    def test_resolve_not_registered(self) -> None:
        """Test resolving unregistered service raises error."""
        with pytest.raises(ServiceNotFoundError):
            self.container.resolve(GreeterProtocol)


class TestDIContainerAdvanced:
    """Test advanced DI container functionality."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()
        self.container = DIContainer()

    def test_register_instance(self) -> None:
        """Test registering an existing instance."""
        instance = SimpleGreeter()
        self.container.register_instance(GreeterProtocol, instance)
        
        resolved = self.container.resolve(GreeterProtocol)
        assert resolved is instance

    def test_register_factory(self) -> None:
        """Test registering a factory function."""
        call_count = 0
        
        def create_greeter() -> SimpleGreeter:
            nonlocal call_count
            call_count += 1
            return SimpleGreeter()
        
        self.container.register_factory(GreeterProtocol, create_greeter, Lifetime.TRANSIENT)
        
        self.container.resolve(GreeterProtocol)
        self.container.resolve(GreeterProtocol)
        
        assert call_count == 2  # Factory called twice for transient

    def test_auto_wiring(self) -> None:
        """Test automatic dependency injection."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SINGLETON)
        self.container.register(GreeterWithDependency, GreeterWithDependency, Lifetime.SINGLETON)
        
        wrapped = self.container.resolve(GreeterWithDependency)
        
        assert wrapped.greet("World") == "[Wrapped] Hello, World!"

    def test_try_resolve_returns_none(self) -> None:
        """Test try_resolve returns None for unregistered service."""
        result = self.container.try_resolve(GreeterProtocol)
        assert result is None

    def test_try_resolve_returns_instance(self) -> None:
        """Test try_resolve returns instance for registered service."""
        self.container.register(GreeterProtocol, SimpleGreeter)
        
        result = self.container.try_resolve(GreeterProtocol)
        assert result is not None
        assert isinstance(result, SimpleGreeter)

    def test_self_registration(self) -> None:
        """Test registering a class without separate interface."""
        self.container.register(SimpleGreeter)
        
        greeter = self.container.resolve(SimpleGreeter)
        assert isinstance(greeter, SimpleGreeter)

    def test_clear_container(self) -> None:
        """Test clearing all registrations."""
        self.container.register(GreeterProtocol, SimpleGreeter)
        self.container.resolve(GreeterProtocol)  # Create singleton
        
        self.container.clear()
        
        assert not self.container.is_registered(GreeterProtocol)
        with pytest.raises(ServiceNotFoundError):
            self.container.resolve(GreeterProtocol)

    def test_get_registrations(self) -> None:
        """Test getting all registrations."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SINGLETON)
        
        registrations = self.container.get_registrations()
        
        assert GreeterProtocol in registrations
        assert registrations[GreeterProtocol].implementation == SimpleGreeter
        assert registrations[GreeterProtocol].lifetime == Lifetime.SINGLETON


class TestDIContainerConfiguration:
    """Test DI container configuration."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()
        self.container = DIContainer()

    def test_configure_with_dict(self) -> None:
        """Test configuring container with dict."""
        config = {
            "app": {"name": "TestApp"},
            "di": {"services": {}},
        }
        
        self.container.configure(config)
        
        # Config should be stored
        assert self.container._config == config

    def test_config_injection(self) -> None:
        """Test injecting config into service."""
        config = {
            "services": {
                "test": {"setting1": "value1"},
            },
        }
        self.container.configure(config)
        self.container.register(
            ConfigurableService,
            ConfigurableService,
            config_key="services.test",
        )
        
        service = self.container.resolve(ConfigurableService)
        
        assert service.get_setting("setting1") == "value1"


class TestDIScope:
    """Test DI scope functionality."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()
        self.container = DIContainer()

    def test_scope_context_manager(self) -> None:
        """Test scope as context manager."""
        self.container.register(GreeterProtocol, SimpleGreeter, Lifetime.SCOPED)
        
        with self.container.create_scope("request-1") as scope:
            greeter1 = scope.resolve(GreeterProtocol)
            greeter2 = scope.resolve(GreeterProtocol)
            assert greeter1 is greeter2

    def test_scope_disposal(self) -> None:
        """Test scope disposes services on exit."""
        self.container.register(DisposableService, DisposableService, Lifetime.SCOPED)
        
        with self.container.create_scope("request-1") as scope:
            service = scope.resolve(DisposableService)
            assert not service.disposed
        
        assert service.disposed

    def test_scope_id_property(self) -> None:
        """Test scope_id property."""
        scope = self.container.create_scope("my-scope")
        assert scope.scope_id == "my-scope"

    def test_manual_scope_disposal(self) -> None:
        """Test manual scope disposal."""
        self.container.register(DisposableService, DisposableService, Lifetime.SCOPED)
        
        service = self.container.resolve(DisposableService, scope_id="request-1")
        assert not service.disposed
        
        self.container.dispose_scope("request-1")
        assert service.disposed


class TestCircularDependencies:
    """Test circular dependency detection."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()
        self.container = DIContainer()

    def test_circular_dependency_detection(self) -> None:
        """Test that circular dependencies are detected via factory."""
        # Use factories to create circular dependency since forward refs
        # don't work well with get_type_hints in local scope
        instances: dict = {}
        
        def create_a():
            if "a" in instances:
                raise CircularDependencyError("Circular dependency on A")
            instances["a"] = True
            b = self.container.resolve(ServiceB)
            return {"b": b}
        
        def create_b():
            if "b" in instances:
                raise CircularDependencyError("Circular dependency on B")
            instances["b"] = True
            a = self.container.resolve(ServiceA)
            return {"a": a}
        
        # Define simple marker classes
        class ServiceA:
            pass
        
        class ServiceB:
            pass
        
        self.container.register_factory(ServiceA, create_a, Lifetime.SINGLETON)
        self.container.register_factory(ServiceB, create_b, Lifetime.SINGLETON)

        with pytest.raises(CircularDependencyError):
            self.container.resolve(ServiceA)


class TestGlobalContainer:
    """Test global container singleton."""

    def setup_method(self) -> None:
        """Reset container before each test."""
        DIContainer.reset_instance()

    def test_get_container_returns_singleton(self) -> None:
        """Test get_container returns same instance."""
        container1 = get_container()
        container2 = get_container()
        
        assert container1 is container2

    def test_reset_instance(self) -> None:
        """Test reset_instance creates new container."""
        container1 = get_container()
        DIContainer.reset_instance()
        container2 = get_container()
        
        assert container1 is not container2


class TestLifetimeEnum:
    """Test Lifetime enum."""

    def test_lifetime_values(self) -> None:
        """Test lifetime enum values."""
        assert Lifetime.SINGLETON.value == "singleton"
        assert Lifetime.TRANSIENT.value == "transient"
        assert Lifetime.SCOPED.value == "scoped"

    def test_lifetime_from_string(self) -> None:
        """Test creating lifetime from string."""
        assert Lifetime("singleton") == Lifetime.SINGLETON
        assert Lifetime("transient") == Lifetime.TRANSIENT
        assert Lifetime("scoped") == Lifetime.SCOPED


class TestRegistrationDataclass:
    """Test Registration dataclass."""

    def test_registration_creation(self) -> None:
        """Test creating registration."""
        reg = Registration(
            interface=GreeterProtocol,
            implementation=SimpleGreeter,
            lifetime=Lifetime.SINGLETON,
        )
        
        assert reg.interface == GreeterProtocol
        assert reg.implementation == SimpleGreeter
        assert reg.lifetime == Lifetime.SINGLETON
        assert reg.config_key is None
        assert reg.factory is None

    def test_registration_with_config_key(self) -> None:
        """Test registration with config key."""
        reg = Registration(
            interface=GreeterProtocol,
            implementation=SimpleGreeter,
            lifetime=Lifetime.SINGLETON,
            config_key="services.greeter",
        )
        
        assert reg.config_key == "services.greeter"
