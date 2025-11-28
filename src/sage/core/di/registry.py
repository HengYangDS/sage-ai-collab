"""
Type Registry - Maps string names to concrete types for YAML configuration.

This module provides a registry for mapping service names in YAML config
to actual Python types, enabling YAML-driven dependency injection.

Version: 0.1.0
"""

from typing import Any, Callable, Dict, Optional, Type, TypeVar
import logging
import importlib

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TypeRegistry:
    """
    Registry for mapping string names to Python types.

    Supports both explicit registration and dynamic import-based resolution.

    Example:
        >>> registry = TypeRegistry()
        >>> registry.register("TimeoutLoader", TimeoutLoader)
        >>> loader_cls = registry.resolve("TimeoutLoader")
    """

    _instance: Optional["TypeRegistry"] = None

    def __init__(self) -> None:
        self._types: Dict[str, Type] = {}
        self._factories: Dict[str, Callable[..., Any]] = {}

    @classmethod
    def get_instance(cls) -> "TypeRegistry":
        """Get singleton registry instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        cls._instance = None

    def register(self, name: str, type_or_factory: Type | Callable[..., Any]) -> None:
        """
        Register a type or factory by name.

        Args:
            name: The string name to register
            type_or_factory: The type class or factory function
        """
        if callable(type_or_factory) and not isinstance(type_or_factory, type):
            self._factories[name] = type_or_factory
            logger.debug(f"Registered factory: {name}")
        else:
            self._types[name] = type_or_factory
            logger.debug(f"Registered type: {name} -> {type_or_factory}")

    def register_type(self, name: str, type_cls: Type[T]) -> None:
        """Register a type by name."""
        self._types[name] = type_cls
        logger.debug(f"Registered type: {name} -> {type_cls}")

    def register_factory(self, name: str, factory: Callable[..., Any]) -> None:
        """Register a factory function by name."""
        self._factories[name] = factory
        logger.debug(f"Registered factory: {name}")

    def resolve(self, name: str) -> Optional[Type]:
        """
        Resolve a type by name.

        First checks explicit registrations, then attempts dynamic import.

        Args:
            name: The type name to resolve

        Returns:
            The resolved type or None if not found
        """
        # Check explicit registration first
        if name in self._types:
            return self._types[name]

        # Try dynamic import (e.g., "sage.core.loader.TimeoutLoader")
        if "." in name:
            try:
                return self._import_type(name)
            except (ImportError, AttributeError) as e:
                logger.warning(f"Failed to import {name}: {e}")
                return None

        return None

    def resolve_factory(self, name: str) -> Optional[Callable[..., Any]]:
        """Resolve a factory by name."""
        return self._factories.get(name)

    def _import_type(self, full_path: str) -> Type:
        """
        Import a type from a fully qualified path.

        Args:
            full_path: Full module path (e.g., "sage.core.loader.TimeoutLoader")

        Returns:
            The imported type
        """
        parts = full_path.rsplit(".", 1)
        if len(parts) != 2:
            raise ImportError(f"Invalid import path: {full_path}")

        module_path, class_name = parts
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def is_registered(self, name: str) -> bool:
        """Check if a name is registered."""
        return name in self._types or name in self._factories

    def clear(self) -> None:
        """Clear all registrations."""
        self._types.clear()
        self._factories.clear()

    def get_all_types(self) -> Dict[str, Type]:
        """Get all registered types."""
        return self._types.copy()

    def get_all_factories(self) -> Dict[str, Callable[..., Any]]:
        """Get all registered factories."""
        return self._factories.copy()


def get_registry() -> TypeRegistry:
    """Get the global type registry instance."""
    return TypeRegistry.get_instance()


def register_default_types(registry: Optional[TypeRegistry] = None) -> None:
    """
    Register default SAGE types in the registry.

    This function registers all built-in types that can be referenced
    by name in YAML configuration.

    Args:
        registry: Optional registry instance (uses global if not provided)
    """
    if registry is None:
        registry = get_registry()

    # Core types
    try:
        from sage.core.loader import KnowledgeLoader

        registry.register("KnowledgeLoader", KnowledgeLoader)
    except ImportError:
        pass

    # Event types
    try:
        from sage.core.events import EventBus

        registry.register("EventBus", EventBus)
        registry.register("AsyncEventBus", EventBus)  # Alias
    except ImportError:
        pass

    # Memory types
    try:
        from sage.core.memory import MemoryStore, TokenBudget, SessionContinuity

        registry.register("MemoryStore", MemoryStore)
        registry.register("TokenBudget", TokenBudget)
        registry.register("SessionContinuity", SessionContinuity)
    except ImportError:
        pass

    # Capability types
    try:
        from sage.capabilities import (
            ContentAnalyzer,
            QualityAnalyzer,
            StructureChecker,
            LinkChecker,
            HealthMonitor,
        )

        registry.register("ContentAnalyzer", ContentAnalyzer)
        registry.register("QualityAnalyzer", QualityAnalyzer)
        registry.register("StructureChecker", StructureChecker)
        registry.register("LinkChecker", LinkChecker)
        registry.register("HealthMonitor", HealthMonitor)
    except ImportError:
        pass

    logger.debug(f"Registered {len(registry._types)} default types")
