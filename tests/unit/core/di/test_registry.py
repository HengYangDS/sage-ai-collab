"""
Unit tests for TypeRegistry.

Tests cover:
- Type registration and resolution
- Factory registration
- Dynamic import resolution
- Default type registration
"""
import pytest

from sage.core.di import TypeRegistry, get_registry, register_default_types


class SampleService:
    """Sample service for testing."""
    def do_work(self) -> str:
        return "working"


class AnotherService:
    """Another sample service."""
    pass


class TestTypeRegistryBasics:
    """Test basic TypeRegistry functionality."""

    def setup_method(self) -> None:
        """Reset registry before each test."""
        TypeRegistry.reset_instance()
        self.registry = TypeRegistry()

    def test_create_registry(self) -> None:
        """Test registry creation."""
        assert self.registry is not None
        assert isinstance(self.registry, TypeRegistry)

    def test_register_type(self) -> None:
        """Test registering a type."""
        self.registry.register("SampleService", SampleService)
        
        resolved = self.registry.resolve("SampleService")
        assert resolved is SampleService

    def test_register_type_explicit(self) -> None:
        """Test register_type method."""
        self.registry.register_type("Sample", SampleService)
        
        resolved = self.registry.resolve("Sample")
        assert resolved is SampleService

    def test_resolve_unregistered_returns_none(self) -> None:
        """Test resolving unregistered type returns None."""
        result = self.registry.resolve("NonExistent")
        assert result is None

    def test_is_registered(self) -> None:
        """Test is_registered method."""
        assert not self.registry.is_registered("SampleService")
        
        self.registry.register("SampleService", SampleService)
        
        assert self.registry.is_registered("SampleService")

    def test_clear_registry(self) -> None:
        """Test clearing all registrations."""
        self.registry.register("SampleService", SampleService)
        
        self.registry.clear()
        
        assert not self.registry.is_registered("SampleService")

    def test_get_all_types(self) -> None:
        """Test getting all registered types."""
        self.registry.register("Sample1", SampleService)
        self.registry.register("Sample2", AnotherService)
        
        all_types = self.registry.get_all_types()
        
        assert "Sample1" in all_types
        assert "Sample2" in all_types
        assert all_types["Sample1"] is SampleService
        assert all_types["Sample2"] is AnotherService


class TestTypeRegistryFactories:
    """Test TypeRegistry factory functionality."""

    def setup_method(self) -> None:
        """Reset registry before each test."""
        TypeRegistry.reset_instance()
        self.registry = TypeRegistry()

    def test_register_factory(self) -> None:
        """Test registering a factory function."""
        def create_service() -> SampleService:
            return SampleService()
        
        self.registry.register_factory("ServiceFactory", create_service)
        
        factory = self.registry.resolve_factory("ServiceFactory")
        assert factory is create_service

    def test_register_callable_as_factory(self) -> None:
        """Test that callable non-types are registered as factories."""
        def my_factory() -> str:
            return "created"
        
        self.registry.register("MyFactory", my_factory)
        
        # Should be in factories, not types
        assert "MyFactory" in self.registry.get_all_factories()
        assert "MyFactory" not in self.registry.get_all_types()

    def test_resolve_factory_unregistered(self) -> None:
        """Test resolving unregistered factory returns None."""
        result = self.registry.resolve_factory("NonExistent")
        assert result is None

    def test_get_all_factories(self) -> None:
        """Test getting all registered factories."""
        def factory1() -> str:
            return "1"
        
        def factory2() -> str:
            return "2"
        
        self.registry.register_factory("F1", factory1)
        self.registry.register_factory("F2", factory2)
        
        all_factories = self.registry.get_all_factories()
        
        assert "F1" in all_factories
        assert "F2" in all_factories


class TestTypeRegistryDynamicImport:
    """Test TypeRegistry dynamic import functionality."""

    def setup_method(self) -> None:
        """Reset registry before each test."""
        TypeRegistry.reset_instance()
        self.registry = TypeRegistry()

    def test_resolve_with_full_path(self) -> None:
        """Test resolving type by full module path."""
        # Use a known type from the standard library
        resolved = self.registry.resolve("pathlib.Path")
        
        from pathlib import Path
        assert resolved is Path

    def test_resolve_sage_type_by_path(self) -> None:
        """Test resolving sage type by full path."""
        resolved = self.registry.resolve("sage.core.loader.KnowledgeLoader")
        
        from sage.core.loader import KnowledgeLoader
        assert resolved is KnowledgeLoader

    def test_resolve_invalid_path_returns_none(self) -> None:
        """Test resolving invalid path returns None."""
        result = self.registry.resolve("nonexistent.module.Type")
        assert result is None

    def test_resolve_invalid_attribute_returns_none(self) -> None:
        """Test resolving invalid attribute returns None."""
        result = self.registry.resolve("pathlib.NonExistentClass")
        assert result is None


class TestGlobalRegistry:
    """Test global registry singleton."""

    def setup_method(self) -> None:
        """Reset registry before each test."""
        TypeRegistry.reset_instance()

    def test_get_registry_returns_singleton(self) -> None:
        """Test get_registry returns same instance."""
        registry1 = get_registry()
        registry2 = get_registry()
        
        assert registry1 is registry2

    def test_reset_instance(self) -> None:
        """Test reset_instance creates new registry."""
        registry1 = get_registry()
        TypeRegistry.reset_instance()
        registry2 = get_registry()
        
        assert registry1 is not registry2


class TestDefaultTypeRegistration:
    """Test default type registration."""

    def setup_method(self) -> None:
        """Reset registry before each test."""
        TypeRegistry.reset_instance()

    def test_register_default_types(self) -> None:
        """Test registering default SAGE types."""
        registry = TypeRegistry()
        register_default_types(registry)
        
        # Should have KnowledgeLoader registered
        assert registry.is_registered("KnowledgeLoader")
        
        from sage.core.loader import KnowledgeLoader
        assert registry.resolve("KnowledgeLoader") is KnowledgeLoader

    def test_register_default_types_with_global_registry(self) -> None:
        """Test registering defaults to global registry."""
        register_default_types()
        
        registry = get_registry()
        assert registry.is_registered("KnowledgeLoader")

    def test_register_default_types_includes_events(self) -> None:
        """Test that EventBus is registered."""
        registry = TypeRegistry()
        register_default_types(registry)
        
        assert registry.is_registered("EventBus")

    def test_register_default_types_includes_memory(self) -> None:
        """Test that memory types are registered."""
        registry = TypeRegistry()
        register_default_types(registry)
        
        assert registry.is_registered("MemoryStore")
        assert registry.is_registered("TokenBudget")
        assert registry.is_registered("SessionContinuity")

    def test_register_default_types_includes_capabilities(self) -> None:
        """Test that capability types are registered."""
        registry = TypeRegistry()
        register_default_types(registry)
        
        assert registry.is_registered("ContentAnalyzer")
        assert registry.is_registered("QualityAnalyzer")
        assert registry.is_registered("HealthMonitor")
