"""Content Caching Plugin for SAGE Knowledge Base.

This plugin provides LRU caching for knowledge content to improve
performance by avoiding repeated file system reads.

Version: 0.1.0
"""

from __future__ import annotations

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from sage.plugins.base import CachePlugin, LoaderPlugin, PluginMetadata

if TYPE_CHECKING:
    pass

__all__ = ["ContentCachePlugin", "CacheEntry", "CacheStats"]


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""

    key: str
    value: str
    size_bytes: int
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0

    def touch(self) -> None:
        """Update access metadata."""
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class CacheStats:
    """Cache statistics for monitoring."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size_bytes: int = 0
    entry_count: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "hit_rate": round(self.hit_rate, 4),
            "total_size_bytes": self.total_size_bytes,
            "entry_count": self.entry_count,
        }


class ContentCachePlugin(CachePlugin, LoaderPlugin):
    """LRU cache plugin for knowledge content.

    Provides in-memory caching with:
    - Configurable max size (entries and bytes)
    - LRU eviction policy
    - TTL support
    - Cache statistics

    Configuration options (via sage.yaml):
        max_entries: Maximum number of cache entries (default: 1000)
        max_size_bytes: Maximum total cache size in bytes (default: 50MB)
        ttl_seconds: Time-to-live for entries (default: 3600)
        enabled: Whether caching is enabled (default: True)

    Example:
        >>> plugin = ContentCachePlugin(max_entries=500, ttl_seconds=1800)
        >>> registry.register(plugin)
    """

    def __init__(
        self,
        max_entries: int = 1000,
        max_size_bytes: int = 50 * 1024 * 1024,  # 50MB
        ttl_seconds: int = 3600,
    ) -> None:
        """Initialize the cache plugin.

        Args:
            max_entries: Maximum number of entries to cache.
            max_size_bytes: Maximum total cache size in bytes.
            ttl_seconds: Time-to-live for cache entries.
        """
        self._metadata = PluginMetadata(
            name="content_cache",
            version="0.1.0",
            description="LRU content caching for improved performance",
            author="SAGE Team",
            hooks=["on_cache_hit", "on_cache_miss", "post_load"],
        )

        self.max_entries = max_entries
        self.max_size_bytes = max_size_bytes
        self.ttl_seconds = ttl_seconds

        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats()
        self._enabled = True

    @property
    def metadata(self) -> PluginMetadata:
        """Get plugin metadata."""
        return self._metadata

    def configure(self, config: dict[str, Any]) -> None:
        """Configure the plugin from settings.

        Args:
            config: Configuration dictionary.
        """
        self.max_entries = config.get("max_entries", self.max_entries)
        self.max_size_bytes = config.get("max_size_bytes", self.max_size_bytes)
        self.ttl_seconds = config.get("ttl_seconds", self.ttl_seconds)
        self._enabled = config.get("enabled", True)

    def on_load(self, context: dict[str, Any]) -> None:
        """Handle plugin load event."""
        self._cache.clear()
        self._stats = CacheStats()

    def on_unload(self) -> None:
        """Handle plugin unload event."""
        self._cache.clear()

    def on_enable(self) -> None:
        """Handle plugin enable event."""
        self._enabled = True

    def on_disable(self) -> None:
        """Handle plugin disable event."""
        self._enabled = False

    # CachePlugin hooks

    def on_cache_hit(
        self,
        key: str,
        value: Any,
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Handle cache hit event.

        Args:
            key: The cache key that was hit.
            value: The cached value.
            context: Additional context.

        Returns:
            Optional modified context.
        """
        self._stats.hits += 1
        return {"cached": True, "key": key}

    def on_cache_miss(
        self,
        key: str,
        context: dict[str, Any],
    ) -> None:
        """Handle cache miss event.

        Args:
            key: The cache key that was missed.
            context: Additional context.
        """
        self._stats.misses += 1

    # LoaderPlugin hooks

    def post_load(self, layer: str, content: str) -> str:
        """Cache content after loading.

        Args:
            layer: The layer being loaded.
            content: The loaded content.

        Returns:
            The content (unchanged).
        """
        if self._enabled:
            key = self._make_key(layer, content)
            self._set(key, content)
        return content

    # Cache operations

    def get(self, key: str) -> str | None:
        """Get a value from the cache.

        Args:
            key: The cache key.

        Returns:
            The cached value or None if not found.
        """
        if not self._enabled:
            return None

        entry = self._cache.get(key)
        if entry is None:
            self._stats.misses += 1
            return None

        # Check TTL
        if time.time() - entry.created_at > self.ttl_seconds:
            self._evict(key)
            self._stats.misses += 1
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        entry.touch()
        self._stats.hits += 1
        return entry.value

    def _set(self, key: str, value: str) -> None:
        """Set a value in the cache.

        Args:
            key: The cache key.
            value: The value to cache.
        """
        size_bytes = len(value.encode("utf-8"))

        # Check if entry already exists
        if key in self._cache:
            old_entry = self._cache[key]
            self._stats.total_size_bytes -= old_entry.size_bytes
            del self._cache[key]
            self._stats.entry_count -= 1

        # Evict entries if needed
        self._evict_if_needed(size_bytes)

        # Add new entry
        entry = CacheEntry(key=key, value=value, size_bytes=size_bytes)
        self._cache[key] = entry
        self._stats.total_size_bytes += size_bytes
        self._stats.entry_count += 1

    def _evict_if_needed(self, new_size: int) -> None:
        """Evict entries if cache is full.

        Args:
            new_size: Size of new entry to add.
        """
        # Evict by entry count
        while len(self._cache) >= self.max_entries:
            self._evict_oldest()

        # Evict by size
        while (
            self._stats.total_size_bytes + new_size > self.max_size_bytes
            and self._cache
        ):
            self._evict_oldest()

    def _evict_oldest(self) -> None:
        """Evict the oldest (least recently used) entry."""
        if self._cache:
            key, entry = self._cache.popitem(last=False)
            self._stats.total_size_bytes -= entry.size_bytes
            self._stats.entry_count -= 1
            self._stats.evictions += 1

    def _evict(self, key: str) -> None:
        """Evict a specific entry.

        Args:
            key: The cache key to evict.
        """
        if key in self._cache:
            entry = self._cache.pop(key)
            self._stats.total_size_bytes -= entry.size_bytes
            self._stats.entry_count -= 1
            self._stats.evictions += 1

    def _make_key(self, layer: str, content: str) -> str:
        """Generate a cache key.

        Args:
            layer: The layer name.
            content: The content to hash.

        Returns:
            A unique cache key.
        """
        content_hash = hashlib.md5(content.encode(), usedforsecurity=False).hexdigest()
        return f"{layer}:{content_hash[:16]}"

    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._stats = CacheStats()

    def get_stats(self) -> CacheStats:
        """Get cache statistics.

        Returns:
            Current cache statistics.
        """
        return self._stats

    def get_keys(self) -> list[str]:
        """Get all cache keys.

        Returns:
            List of cache keys.
        """
        return list(self._cache.keys())
