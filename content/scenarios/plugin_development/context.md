# Plugin Development Scenario

> Context and guidelines for developing SAGE plugins

---

## Scenario Overview

| Aspect | Description |
|--------|-------------|
| **Domain** | SAGE plugin system development |
| **Task Types** | Plugin creation, hook implementation, testing |
| **Autonomy Level** | L3 (Medium) for new plugins, L4 for updates |
| **Key Concerns** | Interface compliance, performance, isolation |

---

## Common Tasks

### Plugin Creation

- Setting up plugin structure
- Implementing plugin interface
- Defining plugin configuration
- Registering hooks

### Hook Implementation

- Understanding hook lifecycle
- Implementing hook handlers
- Managing hook priorities
- Handling async operations

### Testing & Debugging

- Unit testing plugins
- Integration testing
- Performance profiling
- Debug logging

---

## Plugin Architecture

### Extension Points

SAGE provides 7 extension points for plugins:

```
┌─────────────────────────────────────────────────────────────┐
│                    Plugin Extension Points                   │
├──────────────┬──────────────┬──────────────┬───────────────┤
│  before_load │  after_load  │  transform   │  on_error     │
├──────────────┼──────────────┼──────────────┼───────────────┤
│  on_search   │  on_cache    │  on_event    │               │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

### Hook Lifecycle

```
Request → before_load → load → transform → after_load → Response
              ↓                    ↓            ↓
           on_cache            on_event     on_error
```

---

## Plugin Structure

### Directory Layout

```
plugins/
└── my_plugin/
    ├── __init__.py        # Package initialization
    ├── plugin.py          # Main plugin class
    ├── config.yaml        # Plugin configuration
    ├── hooks/             # Hook implementations
    │   ├── __init__.py
    │   ├── load_hooks.py
    │   └── transform_hooks.py
    └── tests/             # Plugin tests
        ├── __init__.py
        └── test_plugin.py
```

### Plugin Class

```python
# plugins/my_plugin/plugin.py
from sage.plugins import PluginBase, hook, PluginConfig

class MyPlugin(PluginBase):
    """Custom plugin for SAGE."""
    
    name = "my_plugin"
    version = "1.0.0"
    description = "My custom SAGE plugin"
    
    def __init__(self, config: PluginConfig):
        super().__init__(config)
        self.custom_setting = config.get("custom_setting", "default")
    
    async def initialize(self) -> None:
        """Called when plugin is loaded."""
        self.logger.info(f"Initializing {self.name}")
        # Setup resources, connections, etc.
    
    async def shutdown(self) -> None:
        """Called when plugin is unloaded."""
        self.logger.info(f"Shutting down {self.name}")
        # Cleanup resources
```

### Hook Decorators

```python
from sage.plugins import hook

class MyPlugin(PluginBase):
    
    @hook("before_load", priority=100)
    async def before_load(self, layer: str, **kwargs) -> dict:
        """Called before knowledge loading."""
        self.logger.debug(f"Before loading: {layer}")
        return {"layer": layer, **kwargs}
    
    @hook("after_load", priority=100)
    async def after_load(self, result: LoadResult, **kwargs) -> LoadResult:
        """Called after knowledge loading."""
        self.logger.debug(f"Loaded {result.metadata.files_loaded} files")
        return result
    
    @hook("transform_content", priority=50)
    async def transform(self, content: str, **kwargs) -> str:
        """Transform loaded content."""
        return self.add_header(content)
    
    @hook("on_error")
    async def handle_error(self, error: Exception, **kwargs) -> None:
        """Called when an error occurs."""
        self.logger.error(f"Error: {error}")
```

---

## Configuration

### Plugin Config File

```yaml
# plugins/my_plugin/config.yaml
my_plugin:
  enabled: true
  priority: 100
  
  settings:
    custom_setting: "value"
    feature_flag: true
    
  hooks:
    before_load:
      enabled: true
      priority: 100
    transform_content:
      enabled: true
      priority: 50
```

### Global Plugin Config

```yaml
# config/capabilities/plugins.yaml
plugins:
  enabled: true
  
  load_paths:
    - plugins/
    - ~/.sage/plugins/
  
  enabled_plugins:
    - my_plugin
    - cache_plugin
    
  disabled_plugins:
    - experimental_plugin
  
  bundled:
    cache:
      enabled: true
    semantic_search:
      enabled: false
```

---

## Hook Reference

### before_load

Called before knowledge loading begins.

```python
@hook("before_load")
async def before_load(
    self,
    layer: str,
    topic: str | None,
    timeout_ms: int,
    **kwargs
) -> dict:
    """
    Modify or validate load parameters.
    
    Returns:
        Modified kwargs dict
    """
    return {"layer": layer, "topic": topic, "timeout_ms": timeout_ms}
```

### after_load

Called after knowledge loading completes.

```python
@hook("after_load")
async def after_load(
    self,
    result: LoadResult,
    **kwargs
) -> LoadResult:
    """
    Process or modify load results.
    
    Returns:
        Modified LoadResult
    """
    return result
```

### transform_content

Called to transform loaded content.

```python
@hook("transform_content")
async def transform(
    self,
    content: str,
    metadata: LoadMetadata,
    **kwargs
) -> str:
    """
    Transform content before returning.
    
    Returns:
        Transformed content string
    """
    return f"# Header\n\n{content}"
```

### on_error

Called when an error occurs.

```python
@hook("on_error")
async def on_error(
    self,
    error: Exception,
    context: dict,
    **kwargs
) -> None:
    """Handle errors (logging, recovery, etc.)."""
    self.logger.error(f"Error in {context.get('operation')}: {error}")
```

### on_cache

Called for cache operations.

```python
@hook("on_cache")
async def on_cache(
    self,
    operation: str,  # "get", "set", "invalidate"
    key: str,
    value: Any | None,
    **kwargs
) -> Any:
    """Intercept or modify cache operations."""
    if operation == "get":
        return self.custom_cache.get(key)
    return value
```

### on_event

Called when events are published.

```python
@hook("on_event")
async def on_event(
    self,
    event: Event,
    **kwargs
) -> None:
    """React to system events."""
    if event.type == "knowledge.loaded":
        self.metrics.record_load(event.data)
```

---

## Testing

### Unit Tests

```python
# plugins/my_plugin/tests/test_plugin.py
import pytest
from plugins.my_plugin.plugin import MyPlugin
from sage.plugins import PluginConfig

@pytest.fixture
def plugin():
    config = PluginConfig({"custom_setting": "test"})
    return MyPlugin(config)

@pytest.mark.asyncio
async def test_before_load(plugin):
    result = await plugin.before_load(
        layer="core",
        topic=None,
        timeout_ms=2000
    )
    assert result["layer"] == "core"

@pytest.mark.asyncio
async def test_transform(plugin):
    content = "Test content"
    result = await plugin.transform(content)
    assert "Header" in result
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_plugin_integration():
    from sage.core.loader import KnowledgeLoader
    from sage.plugins import PluginManager
    
    # Load plugin
    manager = PluginManager()
    await manager.load_plugin("my_plugin")
    
    # Test with loader
    loader = KnowledgeLoader(plugin_manager=manager)
    result = await loader.load("core")
    
    # Verify plugin effects
    assert "Header" in result.content
```

---

## Best Practices

### Performance

1. **Async operations**: Always use async for I/O
2. **Minimal overhead**: Keep hooks lightweight
3. **Caching**: Cache expensive computations
4. **Lazy loading**: Load resources on demand

### Error Handling

1. **Graceful failures**: Don't crash the system
2. **Logging**: Log errors with context
3. **Fallbacks**: Provide default behavior
4. **Isolation**: Don't affect other plugins

### Configuration

1. **Sensible defaults**: Work without config
2. **Validation**: Validate config values
3. **Documentation**: Document all options
4. **Hot reload**: Support config changes

---

## Debugging

### Debug Logging

```python
class MyPlugin(PluginBase):
    
    @hook("before_load")
    async def before_load(self, **kwargs):
        self.logger.debug(f"before_load called with: {kwargs}")
        return kwargs
```

### Enable Debug Mode

```bash
SAGE_LOG_LEVEL=DEBUG sage get core
```

### Plugin Inspector

```python
from sage.plugins import PluginManager

manager = PluginManager()
await manager.load_all()

# List loaded plugins
for plugin in manager.plugins:
    print(f"{plugin.name} v{plugin.version}")
    print(f"  Hooks: {plugin.registered_hooks}")
```

---

## Token Budget

For plugin development tasks:

| Task | Budget | Layers |
|------|--------|--------|
| New plugin | 4000 | core, practices/engineering, frameworks/patterns |
| Hook implementation | 3000 | core, practices |
| Testing | 3000 | core, practices/engineering |
| Debugging | 2000 | core, practices |

---

## Related Scenarios

- `python_backend/` — Python development context
- `mcp_integration/` — MCP integration context
- `knowledge_management/` — Knowledge management context

---

## Related Content

- `docs/guides/advanced.md#plugin-development` — Plugin development guide
- `config/capabilities/plugins.yaml` — Plugin configuration
- `.context/decisions/ADR-0008-plugin-system.md` — Plugin system ADR
- `docs/design/05-plugin-memory.md` — Plugin architecture design

---

*SAGE Knowledge Base - Plugin Development Scenario*
