"""
Plugin Registry - Central plugin management with hot-reload support.

This module provides:
- PluginRegistry: Singleton registry for all plugins
- Plugin discovery from directories
- Hot-reload support
- Hook execution pipeline

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import importlib.util
import logging
from pathlib import Path
from threading import Lock
from typing import Any, Optional

from .base import (
    AVAILABLE_HOOKS,
    AnalyzerPlugin,
    FormatterPlugin,
    LoaderPlugin,
    PluginBase,
    PluginMetadata,
    SearchPlugin,
)

logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    Central plugin registry with hot-reload support.

    Features:
    - Singleton pattern for global access
    - Plugin registration and unregistration
    - Hook-based plugin organization
    - Priority-based execution order
    - Hot-reload from directories
    - Thread-safe operations

    Example:
        registry = PluginRegistry()
        registry.register(MyPlugin())

        # Execute hooks
        for plugin in registry.get_hooks("post_load"):
            content = plugin.post_load(layer, content)
    """

    _instance: Optional["PluginRegistry"] = None
    _lock = Lock()

    def __new__(cls) -> "PluginRegistry":
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the registry (only once due to singleton)."""
        if self._initialized:
            return

        self._plugins: dict[str, PluginBase] = {}
        self._hooks: dict[str, list[PluginBase]] = {
            hook: [] for hook in AVAILABLE_HOOKS
        }
        self._loaded_modules: dict[str, Any] = {}
        self._initialized = True

        logger.debug("PluginRegistry initialized")

    def register(self, plugin: PluginBase) -> bool:
        """
        Register a plugin.

        Args:
            plugin: Plugin instance to register

        Returns:
            True if registered successfully, False if already exists
        """
        meta = plugin.metadata

        if meta.name in self._plugins:
            logger.warning(f"Plugin already registered: {meta.name}")
            return False

        # Store plugin
        self._plugins[meta.name] = plugin

        # Register hooks
        for hook in meta.hooks:
            if hook in self._hooks:
                self._hooks[hook].append(plugin)
                # Sort by priority (lower = higher priority)
                self._hooks[hook].sort(key=lambda p: p.metadata.priority)
            else:
                logger.warning(f"Unknown hook '{hook}' in plugin {meta.name}")

        # Call lifecycle hook
        plugin.on_load({"registry": self})

        logger.info(f"Registered plugin: {meta.name} v{meta.version}")
        return True

    def unregister(self, name: str) -> bool:
        """
        Unregister a plugin by name.

        Args:
            name: Plugin name to unregister

        Returns:
            True if unregistered, False if not found
        """
        if name not in self._plugins:
            logger.warning(f"Plugin not found: {name}")
            return False

        plugin = self._plugins[name]

        # Call lifecycle hook
        plugin.on_unload()

        # Remove from hooks
        for hook_list in self._hooks.values():
            hook_list[:] = [p for p in hook_list if p.metadata.name != name]

        # Remove from plugins
        del self._plugins[name]

        logger.info(f"Unregistered plugin: {name}")
        return True

    def get_plugin(self, name: str) -> PluginBase | None:
        """Get a plugin by name."""
        return self._plugins.get(name)

    def get_hooks(self, hook_name: str) -> list[PluginBase]:
        """
        Get all plugins registered for a specific hook.

        Args:
            hook_name: Name of the hook

        Returns:
            List of plugins sorted by priority
        """
        return [p for p in self._hooks.get(hook_name, []) if p.metadata.enabled]

    def list_plugins(self) -> list[PluginMetadata]:
        """List all registered plugins."""
        return [p.metadata for p in self._plugins.values()]

    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin."""
        plugin = self._plugins.get(name)
        if plugin:
            plugin.metadata.enabled = True
            plugin.on_enable()
            logger.info(f"Enabled plugin: {name}")
            return True
        return False

    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin."""
        plugin = self._plugins.get(name)
        if plugin:
            plugin.metadata.enabled = False
            plugin.on_disable()
            logger.info(f"Disabled plugin: {name}")
            return True
        return False

    def configure_plugin(self, name: str, config: dict[str, Any]) -> bool:
        """Configure a plugin with custom settings."""
        plugin = self._plugins.get(name)
        if plugin:
            plugin.configure(config)
            logger.info(f"Configured plugin: {name}")
            return True
        return False

    def load_from_directory(self, path: Path) -> int:
        """
        Load all plugins from a directory.

        Args:
            path: Directory containing plugin Python files

        Returns:
            Number of plugins loaded
        """
        if not path.exists() or not path.is_dir():
            logger.warning(f"Plugin directory not found: {path}")
            return 0

        count = 0

        for py_file in path.glob("*.py"):
            # Skip private files
            if py_file.name.startswith("_"):
                continue

            try:
                loaded = self._load_plugin_file(py_file)
                count += loaded
            except Exception as e:
                logger.error(f"Failed to load plugin from {py_file}: {e}")

        logger.info(f"Loaded {count} plugins from {path}")
        return count

    def _load_plugin_file(self, path: Path) -> int:
        """
        Load plugins from a single Python file.

        Args:
            path: Path to Python file

        Returns:
            Number of plugins loaded from file
        """
        module_name = f"aikb_plugin_{path.stem}"

        # Load module
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            logger.warning(f"Cannot load module spec from {path}")
            return 0

        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(f"Error executing module {path}: {e}")
            return 0

        self._loaded_modules[module_name] = module

        # Find and register plugin classes
        count = 0
        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # Check if it's a plugin class (not base classes)
            if (
                isinstance(attr, type)
                and issubclass(attr, PluginBase)
                and attr
                not in (
                    PluginBase,
                    LoaderPlugin,
                    AnalyzerPlugin,
                    FormatterPlugin,
                    SearchPlugin,
                )
            ):
                try:
                    plugin = attr()
                    if self.register(plugin):
                        count += 1
                except Exception as e:
                    logger.error(f"Error instantiating plugin {attr_name}: {e}")

        return count

    def reload_plugin(self, name: str) -> bool:
        """
        Reload a plugin (hot-reload).

        Args:
            name: Plugin name to reload

        Returns:
            True if reloaded successfully
        """
        plugin = self._plugins.get(name)
        if not plugin:
            logger.warning(f"Plugin not found for reload: {name}")
            return False

        # Find the module
        module_name = None
        for mod_name, module in self._loaded_modules.items():
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and isinstance(plugin, attr):
                    module_name = mod_name
                    break
            if module_name:
                break

        if not module_name:
            logger.warning(f"Cannot find module for plugin: {name}")
            return False

        # Unregister old plugin
        self.unregister(name)

        # Reload module
        module = self._loaded_modules[module_name]
        try:
            importlib.reload(module)
            self._loaded_modules[module_name] = module
        except Exception as e:
            logger.error(f"Error reloading module: {e}")
            return False

        # Re-register plugin
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, PluginBase)
                and attr
                not in (
                    PluginBase,
                    LoaderPlugin,
                    AnalyzerPlugin,
                    FormatterPlugin,
                    SearchPlugin,
                )
            ):
                try:
                    new_plugin = attr()
                    if new_plugin.metadata.name == name:
                        self.register(new_plugin)
                        logger.info(f"Reloaded plugin: {name}")
                        return True
                except Exception as e:
                    logger.error(f"Error re-instantiating plugin: {e}")

        return False

    def execute_hook(self, hook_name: str, *args, **kwargs) -> list[Any]:
        """
        Execute all plugins for a hook.

        Args:
            hook_name: Hook to execute
            *args: Positional arguments for hook method
            **kwargs: Keyword arguments for hook method

        Returns:
            List of results from each plugin
        """
        results = []

        for plugin in self.get_hooks(hook_name):
            try:
                method = getattr(plugin, hook_name, None)
                if method and callable(method):
                    result = method(*args, **kwargs)
                    results.append(result)
            except Exception as e:
                logger.error(
                    f"Error executing hook {hook_name} in {plugin.metadata.name}: {e}"
                )

        return results

    def execute_hook_chain(
        self, hook_name: str, initial_value: Any, *args, **kwargs
    ) -> Any:
        """
        Execute hooks in a chain, passing result from one to the next.

        Args:
            hook_name: Hook to execute
            initial_value: Initial value to pass to first plugin
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            Final value after all plugins have processed
        """
        value = initial_value

        for plugin in self.get_hooks(hook_name):
            try:
                method = getattr(plugin, hook_name, None)
                if method and callable(method):
                    value = method(value, *args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Error in hook chain {hook_name} at {plugin.metadata.name}: {e}"
                )

        return value

    def clear(self) -> None:
        """Clear all registered plugins."""
        for name in list(self._plugins.keys()):
            self.unregister(name)

        self._loaded_modules.clear()
        logger.info("Plugin registry cleared")

    def get_stats(self) -> dict[str, Any]:
        """Get registry statistics."""
        return {
            "total_plugins": len(self._plugins),
            "enabled_plugins": sum(
                1 for p in self._plugins.values() if p.metadata.enabled
            ),
            "hooks": {
                hook: len([p for p in plugins if p.metadata.enabled])
                for hook, plugins in self._hooks.items()
            },
            "loaded_modules": len(self._loaded_modules),
        }


# Global registry instance
_registry: PluginRegistry | None = None


def get_plugin_registry() -> PluginRegistry:
    """Get the global plugin registry singleton."""
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


def register_plugin(plugin: PluginBase) -> bool:
    """Convenience function to register a plugin."""
    return get_plugin_registry().register(plugin)


def get_hooks(hook_name: str) -> list[PluginBase]:
    """Convenience function to get plugins for a hook."""
    return get_plugin_registry().get_hooks(hook_name)
