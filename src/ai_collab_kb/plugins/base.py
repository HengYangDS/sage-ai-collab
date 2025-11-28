"""
Plugin Base Classes - Interface definitions for the plugin system.

This module provides:
- PluginMetadata: Plugin metadata for registration
- PluginBase: Base class for all plugins
- LoaderPlugin: Plugin for customizing knowledge loading
- AnalyzerPlugin: Plugin for custom analysis
- FormatterPlugin: Plugin for output formatting

Extension Points (7 hooks):
- pre_load: Before loading content
- post_load: After loading content
- on_timeout: On timeout event
- pre_search: Before search
- post_search: After search
- pre_format: Before output formatting
- post_format: After output formatting

Author: AI Collaboration KB Team
Version: 2.0.0
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PluginMetadata:
    """
    Plugin metadata for registration.

    Attributes:
        name: Unique plugin name
        version: Plugin version (semver)
        author: Plugin author
        description: Brief description
        hooks: List of hooks this plugin implements
        priority: Execution priority (lower = higher priority)
        enabled: Whether the plugin is enabled
        config: Plugin-specific configuration
    """

    name: str
    version: str
    author: str = "Unknown"
    description: str = ""
    hooks: list[str] = field(default_factory=list)
    priority: int = 100  # Lower = higher priority
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "hooks": self.hooks,
            "priority": self.priority,
            "enabled": self.enabled,
        }


class PluginBase(ABC):
    """
    Base class for all plugins.

    All plugins must inherit from this class and implement
    the metadata property. Lifecycle hooks are optional.

    Example:
        class MyPlugin(PluginBase):
            @property
            def metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="my-plugin",
                    version="1.0.0",
                    hooks=["post_load"],
                )

            def on_load(self, context):
                print(f"Plugin loaded: {self.metadata.name}")
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata. Must be implemented by subclasses."""
        pass

    def on_load(self, context: dict[str, Any]) -> None:
        """
        Called when plugin is loaded into the registry.

        Args:
            context: Dictionary containing registry and other context info
        """
        logger.debug(f"Plugin loaded: {self.metadata.name}")

    def on_unload(self) -> None:
        """Called when plugin is unloaded from the registry."""
        logger.debug(f"Plugin unloaded: {self.metadata.name}")

    def on_enable(self) -> None:
        """Called when plugin is enabled."""
        pass

    def on_disable(self) -> None:
        """Called when plugin is disabled."""
        pass

    def configure(self, config: dict[str, Any]) -> None:
        """
        Configure the plugin with custom settings.

        Args:
            config: Configuration dictionary
        """
        self.metadata.config.update(config)


class LoaderPlugin(PluginBase):
    """
    Plugin for customizing knowledge loading.

    Hooks:
    - pre_load: Modify path or skip loading
    - post_load: Transform loaded content
    - on_timeout: Provide fallback content

    Example:
        class CachePlugin(LoaderPlugin):
            @property
            def metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="cache-plugin",
                    version="1.0.0",
                    hooks=["pre_load", "post_load"],
                )

            def pre_load(self, layer, path):
                # Return cached content or None to continue
                return self._cache.get(path)

            def post_load(self, layer, content):
                # Cache and return content
                self._cache[layer] = content
                return content
    """

    def pre_load(self, layer: str, path: str) -> str | None:
        """
        Hook before loading content.

        Args:
            layer: Layer name (e.g., "core", "guidelines")
            path: Path to the file being loaded

        Returns:
            Modified path, cached content, or None to continue normal loading
        """
        return None

    def post_load(self, layer: str, content: str) -> str:
        """
        Hook after loading content.

        Args:
            layer: Layer name
            content: Loaded content

        Returns:
            Modified content (or original if unchanged)
        """
        return content

    def on_timeout(self, layer: str, elapsed_ms: int) -> str | None:
        """
        Hook when loading times out.

        Args:
            layer: Layer that timed out
            elapsed_ms: Elapsed time in milliseconds

        Returns:
            Fallback content or None to use default fallback
        """
        return None


class AnalyzerPlugin(PluginBase):
    """
    Plugin for custom content analysis.

    Example:
        class QualityAnalyzer(AnalyzerPlugin):
            @property
            def metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="quality-analyzer",
                    version="1.0.0",
                    hooks=["analyze"],
                )

            def analyze(self, content, context):
                return {
                    "word_count": len(content.split()),
                    "quality_score": self._calculate_score(content),
                }
    """

    @abstractmethod
    def analyze(self, content: str, context: dict[str, Any]) -> dict[str, Any]:
        """
        Perform analysis on content.

        Args:
            content: Content to analyze
            context: Additional context (file path, layer, etc.)

        Returns:
            Analysis results dictionary
        """
        pass


class FormatterPlugin(PluginBase):
    """
    Plugin for output formatting.

    Hooks:
    - pre_format: Preprocess content before formatting
    - post_format: Post-process formatted output

    Example:
        class MarkdownEnhancer(FormatterPlugin):
            @property
            def metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="markdown-enhancer",
                    version="1.0.0",
                    hooks=["pre_format", "post_format"],
                )

            def format(self, content, format_type):
                # Add syntax highlighting hints
                return self._enhance_code_blocks(content)
    """

    def pre_format(self, content: str, format_type: str) -> str:
        """
        Preprocess content before formatting.

        Args:
            content: Content to preprocess
            format_type: Target format (e.g., "markdown", "html")

        Returns:
            Preprocessed content
        """
        return content

    @abstractmethod
    def format(self, content: str, format_type: str) -> str:
        """
        Format content for output.

        Args:
            content: Content to format
            format_type: Target format

        Returns:
            Formatted content
        """
        pass

    def post_format(self, content: str, format_type: str) -> str:
        """
        Post-process formatted output.

        Args:
            content: Formatted content
            format_type: Target format

        Returns:
            Final output
        """
        return content


class SearchPlugin(PluginBase):
    """
    Plugin for customizing search behavior.

    Hooks:
    - pre_search: Modify query or add filters
    - post_search: Rerank or filter results

    Example:
        class SemanticSearch(SearchPlugin):
            @property
            def metadata(self) -> PluginMetadata:
                return PluginMetadata(
                    name="semantic-search",
                    version="1.0.0",
                    hooks=["pre_search", "post_search"],
                )

            def pre_search(self, query, options):
                # Expand query with synonyms
                expanded = self._expand_query(query)
                return expanded, options

            def post_search(self, results, query):
                # Rerank by semantic similarity
                return self._rerank(results, query)
    """

    def pre_search(
        self,
        query: str,
        options: dict[str, Any],
    ) -> tuple[str, dict[str, Any]]:
        """
        Preprocess search query.

        Args:
            query: Search query
            options: Search options (max_results, filters, etc.)

        Returns:
            Tuple of (modified query, modified options)
        """
        return query, options

    def post_search(
        self,
        results: list[dict[str, Any]],
        query: str,
    ) -> list[dict[str, Any]]:
        """
        Post-process search results.

        Args:
            results: Search results
            query: Original query

        Returns:
            Modified results (reranked, filtered, etc.)
        """
        return results


# Hook type definitions
HOOK_TYPES = {
    "pre_load": LoaderPlugin,
    "post_load": LoaderPlugin,
    "on_timeout": LoaderPlugin,
    "pre_search": SearchPlugin,
    "post_search": SearchPlugin,
    "pre_format": FormatterPlugin,
    "post_format": FormatterPlugin,
    "analyze": AnalyzerPlugin,
}

AVAILABLE_HOOKS = list(HOOK_TYPES.keys())
