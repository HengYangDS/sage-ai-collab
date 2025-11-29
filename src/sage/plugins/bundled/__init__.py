"""SAGE Bundled Plugins.

This package contains bundled plugin implementations that are
distributed with the SAGE Knowledge Base system.

Bundled plugins provide common functionality:
- ContentCachePlugin: LRU caching for knowledge content
- SemanticSearchPlugin: Semantic search capabilities

These plugins are optional and can be enabled/disabled via sage.yaml.

Version: 0.1.0

Example:
    >>> from sage.plugins.bundled import ContentCachePlugin, SemanticSearchPlugin
    >>> from sage.plugins.registry import PluginRegistry
    >>>
    >>> registry = PluginRegistry()
    >>> registry.register(ContentCachePlugin())
    >>> registry.register(SemanticSearchPlugin())
"""

from __future__ import annotations

from .cache_plugin import ContentCachePlugin
from .semantic_search import SemanticSearchPlugin

__all__ = [
    "ContentCachePlugin",
    "SemanticSearchPlugin",
]
