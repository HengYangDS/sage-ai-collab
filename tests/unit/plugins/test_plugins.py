"""Tests for Plugin system.

Version: 0.1.0
"""

import pytest
from pathlib import Path
from typing import Any

from sage.plugins.base import (
    PluginBase,
    PluginMetadata,
    LoaderPlugin,
    AnalyzerPlugin,
    FormatterPlugin,
    SearchPlugin,
)
from sage.plugins.registry import (
    PluginRegistry,
    get_plugin_registry,
    register_plugin,
    get_hooks,
)


class TestPluginMetadata:
    """Tests for PluginMetadata dataclass."""

    def test_metadata_creation(self):
        """Test creating plugin metadata."""
        meta = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
        )
        assert meta.name == "test-plugin"
        assert meta.version == "1.0.0"
        assert meta.description == "A test plugin"
        assert meta.author == "Test Author"

    def test_metadata_defaults(self):
        """Test metadata with defaults."""
        meta = PluginMetadata(
            name="minimal",
            version="0.1.0",
        )
        assert meta.name == "minimal"
        assert meta.description == ""
        assert meta.author == "Unknown"  # Default is "Unknown", not empty

    def test_to_dict(self):
        """Test conversion to dictionary."""
        meta = PluginMetadata(
            name="test",
            version="1.0.0",
            description="Test",
            author="Author",
        )
        d = meta.to_dict()
        assert isinstance(d, dict)
        assert d["name"] == "test"
        assert d["version"] == "1.0.0"


class SampleLoaderPlugin(LoaderPlugin):
    """Sample loader plugin for testing."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="sample-loader",
            version="1.0.0",
            description="Sample loader plugin",
        )

    def pre_load(self, layer: str, path: str) -> str | None:
        return path

    def post_load(self, layer: str, content: str) -> str:
        return content + "\n<!-- Loaded by sample-loader -->"

    def on_timeout(self, layer: str, elapsed_ms: int) -> None:
        pass


class SampleAnalyzerPlugin(AnalyzerPlugin):
    """Sample analyzer plugin for testing."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="sample-analyzer",
            version="1.0.0",
        )

    def analyze(self, content: str, context: dict[str, Any]) -> dict[str, Any]:
        return {"word_count": len(content.split())}


class SampleFormatterPlugin(FormatterPlugin):
    """Sample formatter plugin for testing."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="sample-formatter",
            version="1.0.0",
        )

    def format(self, content: str, format_type: str) -> str:
        return content.upper()


class SampleSearchPlugin(SearchPlugin):
    """Sample search plugin for testing."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="sample-search",
            version="1.0.0",
        )

    def pre_search(self, query: str, options: dict[str, Any]) -> tuple[str, dict]:
        return query.lower(), options

    def post_search(
        self, results: list[dict[str, Any]], query: str
    ) -> list[dict[str, Any]]:
        return results


class TestPluginBase:
    """Tests for PluginBase abstract class."""

    def test_loader_plugin_lifecycle(self):
        """Test loader plugin lifecycle methods."""
        plugin = SampleLoaderPlugin()

        # Test metadata
        assert plugin.metadata.name == "sample-loader"

        # Test lifecycle
        plugin.on_load({})
        plugin.on_enable()
        plugin.on_disable()
        plugin.on_unload()

    def test_loader_plugin_hooks(self):
        """Test loader plugin hook methods."""
        plugin = SampleLoaderPlugin()

        # Test pre_load
        result = plugin.pre_load("core", "/path/to/file")
        assert result == "/path/to/file"

        # Test post_load
        result = plugin.post_load("core", "Content")
        assert "sample-loader" in result

        # Test on_timeout
        plugin.on_timeout("core", 1000)

    def test_analyzer_plugin(self):
        """Test analyzer plugin."""
        plugin = SampleAnalyzerPlugin()

        result = plugin.analyze("Hello world test", {})
        assert result["word_count"] == 3

    def test_formatter_plugin(self):
        """Test formatter plugin."""
        plugin = SampleFormatterPlugin()

        result = plugin.format("hello", "plain")
        assert result == "HELLO"

    def test_search_plugin(self):
        """Test search plugin."""
        plugin = SampleSearchPlugin()

        query, options = plugin.pre_search("HELLO", {})
        assert query == "hello"

        results = plugin.post_search([{"title": "Test"}], "hello")
        assert len(results) == 1

    def test_configure(self):
        """Test plugin configuration."""
        plugin = SampleLoaderPlugin()
        plugin.configure({"key": "value"})
        # Should not raise


class TestPluginRegistry:
    """Tests for PluginRegistry singleton."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry for each test."""
        reg = PluginRegistry()
        reg.clear()
        return reg

    def test_singleton(self):
        """Test that registry is a singleton."""
        reg1 = PluginRegistry()
        reg2 = PluginRegistry()
        assert reg1 is reg2

    def test_register_plugin(self, registry):
        """Test registering a plugin."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)
        
        # list_plugins returns list of PluginMetadata objects
        plugins = registry.list_plugins()
        plugin_names = [p.name for p in plugins]
        assert "sample-loader" in plugin_names

    def test_unregister_plugin(self, registry):
        """Test unregistering a plugin."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)
        registry.unregister("sample-loader")
        
        plugins = registry.list_plugins()
        plugin_names = [p.name for p in plugins]
        assert "sample-loader" not in plugin_names

    def test_get_plugin(self, registry):
        """Test getting a registered plugin."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        retrieved = registry.get_plugin("sample-loader")
        assert retrieved is plugin

    def test_get_plugin_not_found(self, registry):
        """Test getting non-existent plugin."""
        result = registry.get_plugin("nonexistent")
        assert result is None

    def test_list_plugins(self, registry):
        """Test listing all plugins."""
        registry.register(SampleLoaderPlugin())
        registry.register(SampleAnalyzerPlugin())
        
        plugins = registry.list_plugins()
        assert len(plugins) == 2
        plugin_names = [p.name for p in plugins]
        assert "sample-loader" in plugin_names
        assert "sample-analyzer" in plugin_names

    def test_enable_disable_plugin(self, registry):
        """Test enabling and disabling plugins."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        registry.disable_plugin("sample-loader")
        registry.enable_plugin("sample-loader")
        # Should not raise

    def test_configure_plugin(self, registry):
        """Test configuring a plugin."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        registry.configure_plugin("sample-loader", {"setting": "value"})
        # Should not raise

    def test_get_hooks(self, registry):
        """Test getting hooks."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        hooks = registry.get_hooks("pre_load")
        assert isinstance(hooks, list)

    def test_execute_hook(self, registry):
        """Test executing a hook."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        results = registry.execute_hook("post_load", "core", "Content")
        assert isinstance(results, list)

    def test_execute_hook_chain(self, registry):
        """Test executing a hook chain."""
        plugin = SampleLoaderPlugin()
        registry.register(plugin)

        result = registry.execute_hook_chain("post_load", "Initial", "core")
        assert isinstance(result, str)

    def test_clear(self, registry):
        """Test clearing all plugins."""
        registry.register(SampleLoaderPlugin())
        registry.register(SampleAnalyzerPlugin())
        registry.clear()

        assert len(registry.list_plugins()) == 0

    def test_get_stats(self, registry):
        """Test getting registry statistics."""
        registry.register(SampleLoaderPlugin())

        stats = registry.get_stats()
        assert isinstance(stats, dict)
        assert "total_plugins" in stats


class TestRegistryHelperFunctions:
    """Tests for registry helper functions."""

    def test_get_plugin_registry(self):
        """Test get_plugin_registry function."""
        registry = get_plugin_registry()
        assert isinstance(registry, PluginRegistry)

    def test_register_plugin_function(self):
        """Test register_plugin helper function."""
        registry = get_plugin_registry()
        registry.clear()
        
        plugin = SampleLoaderPlugin()
        register_plugin(plugin)
        
        plugins = registry.list_plugins()
        plugin_names = [p.name for p in plugins]
        assert "sample-loader" in plugin_names

    def test_get_hooks_function(self):
        """Test get_hooks helper function."""
        registry = get_plugin_registry()
        registry.clear()
        registry.register(SampleLoaderPlugin())

        hooks = get_hooks("pre_load")
        assert isinstance(hooks, list)
