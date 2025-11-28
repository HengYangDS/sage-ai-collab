"""
DI (Dependency Injection) Module.

Provides dependency injection container with lifetime management,
auto-wiring, and YAML configuration support.

Example:
    >>> from sage.core.di import get_container, Lifetime
    >>> 
    >>> container = get_container()
    >>> container.register(MyProtocol, MyImplementation, Lifetime.SINGLETON)
    >>> service = container.resolve(MyProtocol)

Version: 0.1.0
"""
from sage.core.di.container import (
    DIContainer,
    DIContainerError,
    DIScope,
    CircularDependencyError,
    Lifetime,
    Registration,
    ScopeRequiredError,
    ServiceDescriptor,
    ServiceNotFoundError,
    get_container,
)
from sage.core.di.registry import (
    TypeRegistry,
    get_registry,
    register_default_types,
)

__all__ = [
    # Main container
    "DIContainer",
    "DIScope",
    "get_container",
    # Type registry
    "TypeRegistry",
    "get_registry",
    "register_default_types",
    # Enums and data classes
    "Lifetime",
    "Registration",
    "ServiceDescriptor",
    # Exceptions
    "DIContainerError",
    "ServiceNotFoundError",
    "CircularDependencyError",
    "ScopeRequiredError",
]
