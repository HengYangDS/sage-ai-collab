---
title: SAGE Knowledge Base - Plugin Architecture & Memory Persistence
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~800
---

# Plugin Architecture & Memory Persistence

> **Extensible plugin system with cross-task memory persistence and session continuity**

---

## Table of Contents

- [1. Document Series](#1-document-series)
- [2. Overview](#2-overview)
- [3. Plugin System Design](#3-plugin-system-design)
- [4. Extension Points](#4-extension-points)
- [5. Plugin Registry](#5-plugin-registry)
- [6. Event-Driven Architecture Summary](#6-event-driven-architecture-summary)
- [7. Memory Persistence Summary](#7-memory-persistence-summary)

---

## 1. Document Series

This document is part of the Plugin & Memory series:

| Document                      | Content                                    |
|-------------------------------|--------------------------------------------|
| **05-PLUGIN-MEMORY.MD** (this)| Overview, plugin system, extension points  |
| `05A-EVENT-PLUGINS.md`        | Event-driven plugin architecture details   |
| `05B-MEMORY-PERSISTENCE.md`   | Cross-task memory persistence details      |

---

## 2. Overview

This document covers:

1. **Plugin System** - Base classes, extension points, and registry
2. **Event-Driven Architecture** - Protocol + EventBus pattern for async decoupling
3. **Memory Persistence** - Cross-task memory with token management
4. **Session Continuity** - Checkpoint/restore and handoff packages

---

## 3. Plugin System Design

### Plugin Base Classes

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class PluginMetadata:
    """Plugin metadata for registration."""
    name: str
    version: str
    author: str
    description: str
    hooks: List[str]
    priority: int = 100  # Lower = higher priority


class PluginBase(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass

    def on_load(self, context: Dict[str, Any]) -> None:
        """Called when plugin is loaded."""
        pass

    def on_unload(self) -> None:
        """Called when plugin is unloaded."""
        pass
```

### Plugin Types

| Plugin Type       | Purpose                    | Key Methods                    |
|-------------------|----------------------------|--------------------------------|
| `LoaderPlugin`    | Knowledge loading          | `pre_load`, `post_load`, `on_timeout` |
| `SearchPlugin`    | Content search             | `pre_search`, `post_search`    |
| `FormatterPlugin` | Output formatting          | `pre_format`, `post_format`    |
| `AnalyzerPlugin`  | Content analysis           | `pre_analyze`, `analyze`, `post_analyze` |
| `LifecyclePlugin` | System lifecycle           | `on_startup`, `on_shutdown`    |

---

## 4. Extension Points

SAGE provides 15 extension hooks:

| Hook            | Plugin Type     | Phase           | Use Case                          |
|-----------------|-----------------|-----------------|-----------------------------------|
| `pre_load`      | LoaderPlugin    | Before loading  | Custom path resolution, caching   |
| `post_load`     | LoaderPlugin    | After loading   | Content transformation, injection |
| `on_timeout`    | LoaderPlugin    | On timeout      | Custom fallback strategies        |
| `pre_search`    | SearchPlugin    | Before search   | Query expansion, synonyms         |
| `post_search`   | SearchPlugin    | After search    | Result ranking, filtering         |
| `pre_format`    | FormatterPlugin | Before output   | Content preprocessing             |
| `post_format`   | FormatterPlugin | After output    | Final transformations             |
| `pre_analyze`   | AnalyzerPlugin  | Before analysis | Content preprocessing             |
| `analyze`       | AnalyzerPlugin  | Analysis        | Custom content analysis           |
| `post_analyze`  | AnalyzerPlugin  | After analysis  | Result post-processing            |
| `on_startup`    | LifecyclePlugin | System start    | Initialization, metrics setup     |
| `on_shutdown`   | LifecyclePlugin | System stop     | Cleanup, final metrics            |
| `on_error`      | ErrorPlugin     | Error occurred  | Error handling, recovery          |
| `on_cache_hit`  | CachePlugin     | Cache hit       | Cache metrics, value modification |
| `on_cache_miss` | CachePlugin     | Cache miss      | Cache metrics, prefetching        |

---

## 5. Plugin Registry

```python
class PluginRegistry:
    """Central plugin registry with hot-reload support."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._plugins: Dict[str, PluginBase] = {}
            cls._instance._hooks: Dict[str, List[PluginBase]] = {}
        return cls._instance

    def register(self, plugin: PluginBase) -> None:
        """Register a plugin."""
        meta = plugin.metadata
        self._plugins[meta.name] = plugin
        for hook in meta.hooks:
            if hook not in self._hooks:
                self._hooks[hook] = []
            self._hooks[hook].append(plugin)
            self._hooks[hook].sort(key=lambda p: p.metadata.priority)

    def get_hooks(self, hook_name: str) -> List[PluginBase]:
        """Get all plugins registered for a hook."""
        return self._hooks.get(hook_name, [])
```

---

## 6. Event-Driven Architecture Summary

> **Detailed Design**: See `05A-EVENT-PLUGINS.md`

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                       EventBus                               │
│  (S.A.G.E. aligned async pub/sub with priority ordering)     │
├─────────────────────────────────────────────────────────────┤
│  publish(event) ──────────────────────► subscribers         │
│  subscribe(type, handler, priority) ◄── plugins             │
│  Channels: source.*/analyze.*/generate.*/evolve.*           │
└─────────────────────────────────────────────────────────────┘
```

### Key Benefits

| Aspect          | ABC Pattern            | Protocol + EventBus           |
|-----------------|------------------------|-------------------------------|
| Coupling        | Tight (inheritance)    | Loose (structural typing)     |
| Async           | Not supported          | Native async/await            |
| Extensibility   | 7 fixed hooks          | Unlimited event types         |
| Error Isolation | One plugin crashes all | Per-handler isolation         |

---

## 7. Memory Persistence Summary

> **Detailed Design**: See `05B-MEMORY-PERSISTENCE.md`

### Memory Components

| Component       | Purpose                    | Persistence        |
|-----------------|----------------------------|--------------------|
| `MemoryStore`   | Key-value storage          | Session-scoped     |
| `TokenBudget`   | Token allocation tracking  | Per-request        |
| `SessionState`  | Session checkpoint/restore | File-based         |
| `HandoffPackage`| Cross-session handoff      | Markdown export    |

### Token Budget Management

| Priority | Category    | Budget | Use Case                    |
|----------|-------------|--------|-----------------------------|
| 1        | Core        | 500    | Always loaded               |
| 2        | Task        | 2000   | Task-specific knowledge     |
| 3        | Context     | 1000   | Conversation context        |
| 4        | Memory      | 500    | Cross-task memory           |
| **Total**|             | 4000   | Default context budget      |

---

## Related

- `docs/design/05A-EVENT-PLUGINS.md` — Event-driven plugin architecture
- `docs/design/05B-MEMORY-PERSISTENCE.md` — Memory persistence design
- `docs/design/02-SAGE-PROTOCOL.md` — SAGE protocol design
- `docs/design/01-ARCHITECTURE.md` — Architecture overview
- `docs/api/PLUGIN_QUICK_REF.md` — Plugin API quick reference

---

*Part of SAGE Knowledge Base*
