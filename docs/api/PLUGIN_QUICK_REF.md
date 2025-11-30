---
title: Plugin API Reference
type: reference
tags: [plugin, api, hooks]
---

# Plugin API Reference

## Core Classes

### `PluginMetadata`

```python
@dataclass
class PluginMetadata:
    name: str
    version: str
    author: str
    description: str
    hooks: List[str]
    priority: int = 100  # Lower = higher priority
```

### `PluginBase`

```python
class PluginBase(ABC):
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata: pass

    def on_load(self, context: Dict[str, Any]) -> None: pass
    def on_unload(self) -> None: pass
```

### `LoaderPlugin`

```python
class LoaderPlugin(PluginBase):
    def pre_load(self, layer: str, path: str) -> Optional[str]: pass
    def post_load(self, layer: str, content: str) -> str: pass
    def on_timeout(self, layer: str, elapsed_ms: int) -> Optional[str]: pass
```

## Hooks Reference

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
