"""
Knowledge Loader - Production-grade knowledge loading with timeout protection.

This module provides:
- Layer-based progressive loading (L0-L4)
- Smart trigger-based loading
- Timeout protection at all levels
- Caching and fallback strategies
- Differential and compressed loading

Author: SAGE AI Collab Team
Version: 0.1.0
"""

import asyncio
import importlib.util

# Add a project root to a path for imports
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any

_project_root = Path(
    __file__
).parent.parent.parent.parent  # core -> sage -> src -> project_root
_tools_path = _project_root / "tools"

# Add paths if not present
for p in [str(_project_root), str(_tools_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)


# Load timeout_manager module directly from a file
def _load_timeout_manager() -> ModuleType:
    """Load timeout_manager module from 05_tools directory."""
    module_path = _tools_path / "timeout_manager.py"
    spec = importlib.util.spec_from_file_location("timeout_manager", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_tm = _load_timeout_manager()
TimeoutManager = _tm.TimeoutManager
TimeoutLevel = _tm.TimeoutLevel
TimeoutConfig = _tm.TimeoutConfig
TimeoutResult = _tm.TimeoutResult
get_timeout_manager = _tm.get_timeout_manager
EMBEDDED_CORE = _tm.EMBEDDED_CORE

# Structured logging
# Event system for async decoupling
from sage.core.events import EventType, LoadEvent, SearchEvent, get_event_bus
from sage.core.logging import get_logger

logger = get_logger(__name__)


# =============================================================================
# Configuration Loading
# =============================================================================

_config_cache: dict[str, Any] | None = None


def _load_config() -> dict[str, Any]:
    """Load configuration using the unified config system.

    This function uses the config module's load_config() which supports:
    - Modular config files in config/ directory
    - Main sage.yaml configuration
    - Includes from sage.yaml
    - Environment variable overrides

    Returns:
        Merged configuration dictionary from all sources.
    """
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    try:
        # Import here to avoid circular imports
        from sage.core.config import load_config as load_unified_config

        _config_cache = load_unified_config()
    except Exception as e:
        logger.warning("config_load_failed", error=str(e))
        _config_cache = {}

    return _config_cache


def _get_triggers_from_config() -> list["LoadingTrigger"]:
    """
    Load triggers from the sage.yaml configuration.

    Returns:
        List of LoadingTrigger objects parsed from config, or empty list if not found.
    """
    config = _load_config()
    triggers_config = config.get("triggers", {})

    if not triggers_config:
        return []

    triggers: list[LoadingTrigger] = []
    for name, trigger_data in triggers_config.items():
        if not isinstance(trigger_data, dict):
            continue

        keywords = trigger_data.get("keywords", [])
        files = trigger_data.get("load", [])  # Config uses "load", code uses "files"
        timeout_ms = trigger_data.get("timeout_ms", 2000)

        if keywords and files:
            triggers.append(
                LoadingTrigger(
                    name=name,
                    keywords=keywords,
                    files=files,
                    timeout_ms=timeout_ms,
                )
            )

    # Sort by priority if available (lower = higher priority)
    triggers.sort(key=lambda t: triggers_config.get(t.name, {}).get("priority", 999))

    return triggers


def _get_always_load_from_config() -> list[str]:
    """
    Load always-load files from sage.yaml configuration.

    Returns:
        List of file paths that should always be loaded, or empty list if not found.
    """
    config = _load_config()
    loading_config = config.get("loading", {})
    always_load: list[str] = loading_config.get("always", [])
    return always_load


def _parse_timeout_str(timeout_str: str | int) -> int:
    """
    Parse timeout string (e.g., '5s', '500ms', '2s') to milliseconds.

    Args:
        timeout_str: Timeout value as string (e.g., '5s', '500ms') or int (ms).

    Returns:
        Timeout in milliseconds.
    """
    if isinstance(timeout_str, int):
        return timeout_str

    timeout_str = str(timeout_str).strip().lower()

    if timeout_str.endswith("ms"):
        return int(timeout_str[:-2])
    elif timeout_str.endswith("s"):
        return int(float(timeout_str[:-1]) * 1000)
    else:
        # Assume milliseconds if no unit
        return int(timeout_str)


def _get_timeout_from_config(operation: str, default_ms: int) -> int:
    """
    Get timeout value for a specific operation from the sage.yaml configuration.

    Args:
        operation: Operation name (e.g., 'full_load', 'layer_load', 'file_read').
        default_ms: Default timeout in milliseconds if not found in config.

    Returns:
        Timeout in milliseconds.
    """
    config = _load_config()
    timeout_config = config.get("timeout", {})
    operations = timeout_config.get("operations", {})

    if operation in operations:
        return _parse_timeout_str(operations[operation])

    # Fallback to default timeout from config
    if "default" in timeout_config:
        return _parse_timeout_str(timeout_config["default"])

    return default_ms


class Layer(Enum):
    """Knowledge layer hierarchy."""

    L0_INDEX = 0  # Navigation index (~100 tokens)
    L1_CORE = 1  # Core principles (~500 tokens)
    L2_GUIDELINES = 2  # Engineering guidelines (~100-200/chapter)
    L3_FRAMEWORKS = 3  # Deep frameworks (~300-500/doc)
    L4_PRACTICES = 4  # Best practices (~200-400/doc)


@dataclass
class LoadResult:
    """Result of a knowledge load operation."""

    content: str
    layers_loaded: list[Layer] = field(default_factory=list)
    files_loaded: list[str] = field(default_factory=list)
    tokens_estimate: int = 0
    duration_ms: int = 0
    complete: bool = True
    status: str = "success"  # success, partial, fallback, error
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "content": self.content,
            "layers_loaded": [l.name for l in self.layers_loaded],
            "files_loaded": self.files_loaded,
            "tokens_estimate": self.tokens_estimate,
            "duration_ms": self.duration_ms,
            "complete": self.complete,
            "status": self.status,
            "errors": self.errors,
        }


@dataclass
class LoadingTrigger:
    """Smart loading trigger configuration."""

    name: str
    keywords: list[str]
    files: list[str]
    timeout_ms: int = 2000


class KnowledgeLoader:
    """
    Production-grade knowledge loader with timeout protection.

    Features:
    - Progressive layer loading (L0-L4)
    - Smart keyword-triggered loading
    - Timeout protection at all levels
    - In-memory caching
    - Graceful degradation
    - Differential loading support
    """

    def __init__(
        self,
        kb_path: Path | None = None,
        timeout_manager: Any | None = None,  # TimeoutManager instance
        triggers: list[LoadingTrigger] | None = None,
        always_load: list[str] | None = None,
    ):
        """
        Initialize the knowledge loader.

        Args:
            kb_path: Path to knowledge base root (default: project root)
            timeout_manager: Custom timeout manager (default: global singleton)
            triggers: Custom loading triggers (default: from sage.yaml config)
            always_load: Files to always load (default: from sage.yaml config)
        """
        self.kb_path = kb_path or Path(__file__).parent.parent.parent.parent
        self.timeout_manager = timeout_manager or get_timeout_manager()

        # Load triggers: explicit param > config (no hardcoded fallback)
        if triggers is not None:
            self.triggers = triggers
        else:
            self.triggers = _get_triggers_from_config()

        # Load always_load: explicit param > config (no hardcoded fallback)
        if always_load is not None:
            self._always_load = always_load
        else:
            self._always_load = _get_always_load_from_config()

        # Caches
        self._cache: dict[str, str] = {}
        self._cache_hashes: dict[str, str] = {}
        self._last_load: dict[str, str] = {}

        # Event bus for async event publishing
        self._event_bus = get_event_bus()

    async def _publish_event(self, event: LoadEvent | SearchEvent) -> None:
        """Publish an event to the event bus (fire-and-forget).

        This method publishes events without blocking the main operation.
        Errors in event handlers are logged but don't affect the loader.
        """
        try:
            await self._event_bus.publish(event)
        except Exception as e:
            logger.warning(
                "event_publish_failed", error=str(e), event_type=str(event.event_type)
            )

    async def load(
        self,
        layer: Layer | None = None,
        task: str = "",
        files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> LoadResult:
        """
        Load knowledge with smart selection and timeout protection.

        Args:
            layer: Specific layer to load (None = auto select based on a task)
            task: Task description for smart loading
            files: Specific files to load (overrides layer/task)
            timeout_ms: Override timeout in milliseconds

        Returns:
            LoadResult with content and metadata
        """
        start_time = time.monotonic()
        timeout_ms = timeout_ms or _get_timeout_from_config("full_load", 5000)

        logger.debug(
            "load_started",
            layer=layer.name if layer else None,
            task=task or None,
            files_specified=len(files) if files else 0,
            timeout_ms=timeout_ms,
        )

        # Publish LOADER_START event
        await self._publish_event(
            LoadEvent(
                event_type=EventType.LOADER_START,
                source="KnowledgeLoader",
                layer=layer.name if layer else "auto",
                file_count=len(files) if files else 0,
            )
        )

        # Determine files to load
        if files:
            files_to_load = files
        elif task:
            files_to_load = self._get_files_for_task(task)
        elif layer is not None:
            files_to_load = self._get_files_for_layer(layer)
        else:
            files_to_load = self._always_load.copy()

        # Always include core files
        for core_file in self._always_load:
            if core_file not in files_to_load:
                files_to_load.insert(0, core_file)

        # Load files with timeout
        result = await self._load_files_with_timeout(files_to_load, timeout_ms)

        result.duration_ms = int((time.monotonic() - start_time) * 1000)

        logger.info(
            "load_completed",
            status=result.status,
            files_loaded=len(result.files_loaded),
            tokens_estimate=result.tokens_estimate,
            duration_ms=result.duration_ms,
        )

        # Publish LOADER_COMPLETE event
        await self._publish_event(
            LoadEvent(
                event_type=EventType.LOADER_COMPLETE,
                source="KnowledgeLoader",
                layer=layer.name if layer else "auto",
                file_count=len(result.files_loaded),
                duration_ms=float(result.duration_ms),
            )
        )

        return result

    async def load_core(self, timeout_ms: int | None = None) -> LoadResult:
        """Load core principles only (L0 + L1)."""
        timeout_ms = timeout_ms or _get_timeout_from_config("layer_load", 2000)
        return await self.load(
            files=self._always_load,
            timeout_ms=timeout_ms,
        )

    async def load_for_task(
        self,
        task: str,
        timeout_ms: int | None = None,
    ) -> LoadResult:
        """Load knowledge relevant to a specific task."""
        timeout_ms = timeout_ms or _get_timeout_from_config("full_load", 5000)
        return await self.load(task=task, timeout_ms=timeout_ms)

    async def load_guidelines(
        self,
        chapter: str,
        timeout_ms: int | None = None,
    ) -> LoadResult:
        """Load a specific guidelines chapter."""
        timeout_ms = timeout_ms or _get_timeout_from_config("layer_load", 2000)
        file_path = f".knowledge/guidelines/{chapter}.md"
        if not chapter.endswith(".md"):
            # Try to find a matching file
            guidelines_dir = self.kb_path / "knowledge" / "guidelines"
            if guidelines_dir.exists():
                for f in guidelines_dir.glob("*.md"):
                    if chapter.lower() in f.stem.lower():
                        file_path = f".knowledge/guidelines/{f.name}"
                        break

        return await self.load(files=[file_path], timeout_ms=timeout_ms)

    async def load_framework(
        self,
        name: str,
        timeout_ms: int | None = None,
    ) -> LoadResult:
        """Load a specific framework."""
        timeout_ms = timeout_ms or _get_timeout_from_config("full_load", 5000)
        framework_dir = self.kb_path / "knowledge" / "frameworks" / name
        files = []

        if framework_dir.exists():
            files = [
                f".knowledge/frameworks/{name}/{f.name}"
                for f in framework_dir.glob("*.md")
            ]
        else:
            # Try to find in subdirectories
            for subdir in (self.kb_path / "knowledge" / "frameworks").glob("*"):
                if subdir.is_dir():
                    for f in subdir.glob(f"*{name}*.md"):
                        files.append(f".knowledge/frameworks/{subdir.name}/{f.name}")

        if not files:
            return LoadResult(
                content=f"Framework '{name}' not found.",
                status="error",
                errors=[f"Framework not found: {name}"],
            )

        return await self.load(files=files, timeout_ms=timeout_ms)

    async def search(
        self,
        query: str,
        max_results: int = 5,
        timeout_ms: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search knowledge base for matching content.

        Args:
            query: Search query
            max_results: Maximum results to return
            timeout_ms: Search timeout

        Returns:
            List of search results with a path, score, and preview
        """
        timeout_ms = timeout_ms or _get_timeout_from_config("search", 3000)
        start_time = time.monotonic()
        results = []
        query_lower = query.lower()

        logger.debug(
            "search_started",
            query=query,
            max_results=max_results,
            timeout_ms=timeout_ms,
        )

        # Publish SEARCH_START event
        await self._publish_event(
            SearchEvent(
                event_type=EventType.SEARCH_START,
                source="KnowledgeLoader",
                query=query,
            )
        )

        try:

            async def do_search():  # type: ignore[no-untyped-def]
                for md_file in self.kb_path.rglob("*.md"):
                    # Skip archive
                    if ".knowledge/archive" in str(md_file).replace("\\", "/"):
                        continue

                    try:
                        content = md_file.read_text(encoding="utf-8")
                        content_lower = content.lower()

                        # Calculate simple relevance score
                        score = 0
                        if query_lower in content_lower:
                            score = content_lower.count(query_lower)
                            # Boost for matches in headers
                            for line in content.split("\n"):
                                if line.startswith("#") and query_lower in line.lower():
                                    score += 5

                        if score > 0:
                            # Get preview
                            preview = self._get_preview(content, query_lower)
                            rel_path = md_file.relative_to(self.kb_path)
                            results.append(
                                {
                                    "path": str(rel_path),
                                    "score": score,
                                    "preview": preview,
                                }
                            )
                    except Exception as _:
                        logger.warning(
                            "file_read_error", file=str(md_file), error=str(_)
                        )

                # Sort by score descending
                results.sort(key=lambda x: x["score"], reverse=True)
                return results[:max_results]

            timeout_result = await self.timeout_manager.execute_with_timeout(
                do_search(),
                TimeoutLevel.T3_LAYER,
                timeout_ms=timeout_ms,
            )

            duration_ms = int((time.monotonic() - start_time) * 1000)

            if timeout_result.success:
                final_results = timeout_result.value or []
                logger.info(
                    "search_completed",
                    query=query,
                    results_count=len(final_results),
                    duration_ms=duration_ms,
                )
                # Publish SEARCH_COMPLETE event
                await self._publish_event(
                    SearchEvent(
                        event_type=EventType.SEARCH_COMPLETE,
                        source="KnowledgeLoader",
                        query=query,
                        results_count=len(final_results),
                        duration_ms=float(duration_ms),
                    )
                )
                return final_results
            else:
                logger.warning(
                    "search_timeout",
                    query=query,
                    partial_results=len(results),
                    error=str(timeout_result.error),
                )
                return results[:max_results] if results else []

        except Exception as e:
            logger.error("search_error", query=query, error=str(e))
            return []

    def _get_files_for_task(self, task: str) -> list[str]:
        """Determine files to load based on the task description."""
        task_lower = task.lower()
        files: set[str] = set()

        for trigger in self.triggers:
            for keyword in trigger.keywords:
                if keyword in task_lower:
                    files.update(trigger.files)
                    break

        return list(files) if files else self._always_load.copy()

    def _get_files_for_layer(self, layer: Layer) -> list[str]:
        """Get files for a specific layer."""
        layer_dirs = {
            Layer.L0_INDEX: ["index.md"],
            Layer.L1_CORE: [".knowledge/core"],
            Layer.L2_GUIDELINES: [".knowledge/guidelines"],
            Layer.L3_FRAMEWORKS: [".knowledge/frameworks"],
            Layer.L4_PRACTICES: [".knowledge/practices"],
        }

        files = []
        paths = layer_dirs.get(layer, [])

        for path_str in paths:
            path = self.kb_path / path_str
            if path.is_file():
                files.append(path_str)
            elif path.is_dir():
                files.extend(
                    [str(f.relative_to(self.kb_path)) for f in path.glob("*.md")]
                )

        return files

    async def _load_files_with_timeout(
        self,
        files: list[str],
        total_timeout_ms: int,
    ) -> LoadResult:
        """Load multiple files with timeout protection."""
        start_time = time.monotonic()
        contents = []
        loaded_files = []
        errors = []
        layers_loaded: set[Layer] = set()

        for file_path in files:
            # Check remaining time
            elapsed = (time.monotonic() - start_time) * 1000
            remaining = total_timeout_ms - elapsed

            if remaining <= 0:
                errors.append(f"Timeout before loading: {file_path}")
                break

            # Try cache first
            if file_path in self._cache:
                contents.append(self._cache[file_path])
                loaded_files.append(file_path)
                layers_loaded.add(self._get_layer_for_file(file_path))
                continue

            # Load file with timeout
            file_timeout = min(remaining, 500)  # Max 500ms per file

            try:
                result = await self.timeout_manager.execute_with_timeout(
                    self._read_file(file_path),
                    TimeoutLevel.T2_FILE,
                    timeout_ms=int(file_timeout),
                )

                if result.success and result.value:
                    content = result.value
                    contents.append(content)
                    loaded_files.append(file_path)
                    layers_loaded.add(self._get_layer_for_file(file_path))

                    # Update cache
                    self._cache[file_path] = content
                else:
                    errors.append(f"Failed to load {file_path}: {result.error}")

            except Exception as e:
                errors.append(f"Error loading {file_path}: {e}")

        # Build result
        if contents:
            combined_content = "\n\n---\n\n".join(contents)
            status = "success" if not errors else "partial"
        else:
            # Use fallback
            combined_content = EMBEDDED_CORE
            status = "fallback"
            layers_loaded.add(Layer.L1_CORE)

        return LoadResult(
            content=combined_content,
            layers_loaded=list(layers_loaded),
            files_loaded=loaded_files,
            tokens_estimate=len(combined_content) // 4,
            complete=len(errors) == 0,
            status=status,
            errors=errors,
        )

    async def _read_file(self, file_path: str) -> str:
        """Read a file asynchronously."""
        full_path = self.kb_path / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use asyncio to read a file
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(
            None, lambda: full_path.read_text(encoding="utf-8")
        )
        return content

    @staticmethod
    def _get_layer_for_file(file_path: str) -> Layer:
        """Determine a layer for a file path."""
        if file_path == "index.md":
            return Layer.L0_INDEX
        elif ".knowledge/core" in file_path or file_path.startswith(".knowledge/core"):
            return Layer.L1_CORE
        elif ".knowledge/guidelines" in file_path or file_path.startswith(
            ".knowledge/guidelines"
        ):
            return Layer.L2_GUIDELINES
        elif ".knowledge/frameworks" in file_path or file_path.startswith(
            ".knowledge/frameworks"
        ):
            return Layer.L3_FRAMEWORKS
        elif ".knowledge/practices" in file_path or file_path.startswith(
            ".knowledge/practices"
        ):
            return Layer.L4_PRACTICES
        else:
            return Layer.L1_CORE

    @staticmethod
    def _get_preview(content: str, query: str, max_len: int = 100) -> str:
        """Get a preview snippet containing the query."""
        content_lower = content.lower()
        idx = content_lower.find(query)

        if idx == -1:
            return content[:max_len] + "..."

        start = max(0, idx - 30)
        end = min(len(content), idx + len(query) + 70)

        preview = content[start:end]
        if start > 0:
            preview = "..." + preview
        if end < len(content):
            preview = preview + "..."

        return preview.replace("\n", " ")

    def clear_cache(self) -> None:
        """Clear all caches."""
        self._cache.clear()
        self._cache_hashes.clear()
        self._last_load.clear()

    def get_cache_stats(self) -> dict[str, int]:
        """Get cache statistics."""
        return {
            "cached_files": len(self._cache),
            "total_size": sum(len(v) for v in self._cache.values()),
        }


# Convenience functions
async def load_knowledge(
    task: str = "",
    timeout_ms: int | None = None,
) -> LoadResult:
    """Quick function to load knowledge for a task."""
    loader = KnowledgeLoader()
    timeout_ms = timeout_ms or _get_timeout_from_config("full_load", 5000)
    return await loader.load(task=task, timeout_ms=timeout_ms)


async def load_core(timeout_ms: int | None = None) -> LoadResult:
    """Quick function to load core principles."""
    loader = KnowledgeLoader()
    timeout_ms = timeout_ms or _get_timeout_from_config("layer_load", 2000)
    return await loader.load_core(timeout_ms=timeout_ms)


async def search_knowledge(
    query: str,
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """Quick function to search knowledge base."""
    loader = KnowledgeLoader()
    return await loader.search(query, max_results)
