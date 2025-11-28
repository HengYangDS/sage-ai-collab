"""
Plugin System - Extensible plugin architecture for AI Collaboration KB.

This package provides:
- PluginBase: Base class for all plugins
- LoaderPlugin: Plugin for customizing knowledge loading
- AnalyzerPlugin: Plugin for custom content analysis
- FormatterPlugin: Plugin for output formatting
- SearchPlugin: Plugin for customizing search behavior
- PluginRegistry: Central plugin management with hot-reload support

Extension Points (8 hooks):
- pre_load: Before loading content
- post_load: After loading content
- on_timeout: On timeout event
- pre_search: Before search
- post_search: After search
- pre_format: Before output formatting
- post_format: After output formatting
- analyze: Custom content analysis

Example:
    from ai_collab_kb.plugins import PluginBase, PluginMetadata, get_plugin_registry

    class MyPlugin(PluginBase):
        @property
        def metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="my-plugin",
                version="1.0.0",
                hooks=["post_load"],
            )

        def post_load(self, layer: str, content: str) -> str:
            return content.upper()

    # Register the plugin
    registry = get_plugin_registry()
    registry.register(MyPlugin())

Author: AI Collaboration KB Team
Version: 2.0.0
"""

from .base import (
    AVAILABLE_HOOKS,
    HOOK_TYPES,
    AnalyzerPlugin,
    FormatterPlugin,
    LoaderPlugin,
    PluginBase,
    PluginMetadata,
    SearchPlugin,
)
from .registry import (
    PluginRegistry,
    get_hooks,
    get_plugin_registry,
    register_plugin,
)

__all__ = [
    # Metadata
    "PluginMetadata",
    # Base classes
    "PluginBase",
    "LoaderPlugin",
    "AnalyzerPlugin",
    "FormatterPlugin",
    "SearchPlugin",
    # Registry
    "PluginRegistry",
    "get_plugin_registry",
    "register_plugin",
    "get_hooks",
    # Constants
    "HOOK_TYPES",
    "AVAILABLE_HOOKS",
]
