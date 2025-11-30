# ADR-0008: Plugin System Design

> Architecture Decision Record for SAGE Knowledge Base

---

## Table of Contents

- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Alternatives Considered](#alternatives-considered)
- [Consequences](#consequences)
- [Implementation](#implementation)
- [Related](#related)

---

## Status

**Accepted** | Date: 2025-11-28

---

## Context

SAGE Knowledge Base requires extensibility through plugins:

1. Third-party capabilities without core modifications
2. Custom analyzers, checkers, and monitors
3. Organization-specific integrations
4. Hot-pluggable functionality
5. Isolated plugin failures

### Requirements

- Discovery and loading at runtime
- Protocol-based plugin contracts
- Configuration-driven plugin enablement
- Graceful handling of plugin failures
- Clear plugin lifecycle management

---

## Decision

Implement a **Protocol-Based Plugin System** with bundled and external plugin support.

### Plugin Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Plugin Manager                        │
│  • Discovery (bundled + external)                       │
│  • Loading and initialization                           │
│  • Lifecycle management                                 │
│  • Dependency resolution                                │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Bundled Plugins │ │ External Plugins│ │  User Plugins   │
│  (src/plugins/  │ │   (pip install) │ │ (~/.sage/plugins)│
│    bundled/)    │ │                 │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Plugin Types

| Type      | Protocol          | Purpose                          |
|:----------|:------------------|:---------------------------------|
| Analyzer  | `AnalyzerPlugin`  | Code/content analysis            |
| Checker   | `CheckerPlugin`   | Validation and health checks     |
| Monitor   | `MonitorPlugin`   | Performance and usage monitoring |
| Source    | `SourcePlugin`    | Custom knowledge sources         |
| Formatter | `FormatterPlugin` | Output formatting                |

---

## Alternatives Considered

### Alternative 1: No Plugin System

All functionality in core.

- **Pros**: Simple, no plugin complexity
- **Cons**: Can't extend without forking, monolithic
- **Rejected**: Extensibility is a core requirement

### Alternative 2: Entry Points Only

Use Python entry points (setuptools).

- **Pros**: Standard mechanism
- **Cons**: Requires package installation, no hot-loading
- **Rejected**: Need simpler plugin deployment

### Alternative 3: Dynamic Module Loading

Load any Python module as plugin.

- **Pros**: Maximum flexibility
- **Cons**: Security concerns, no contract enforcement
- **Rejected**: Need structured plugin contracts

---

## Consequences

### Positive

1. **Extensibility**: Add features without core changes
2. **Isolation**: Plugin failures don't crash system
3. **Flexibility**: Multiple plugin deployment options
4. **Community**: Enable third-party contributions

### Negative

1. **Complexity**: Plugin lifecycle management
2. **Debugging**: Cross-plugin issues harder to trace
3. **Compatibility**: Plugin API versioning needed

### Mitigations

1. **Clear contracts**: Protocol-based interfaces
2. **Logging**: Detailed plugin lifecycle logging
3. **Versioning**: Semantic versioning for plugin API

---

## Implementation

### Plugin Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class PluginProtocol(Protocol):
    """Base protocol for all plugins."""
    
    @property
    def name(self) -> str:
        """Plugin name."""
        ...
    
    @property
    def version(self) -> str:
        """Plugin version."""
        ...
    
    async def initialize(self) -> None:
        """Initialize plugin."""
        ...
    
    async def shutdown(self) -> None:
        """Shutdown plugin."""
        ...
```

### Analyzer Plugin Example

```python
@runtime_checkable
class AnalyzerPlugin(PluginProtocol, Protocol):
    """Protocol for analyzer plugins."""
    
    async def analyze(self, content: str) -> AnalysisResult:
        """Analyze content."""
        ...
    
    def supported_types(self) -> list[str]:
        """Return supported content types."""
        ...
```

### Plugin Implementation

```python
class CustomAnalyzer:
    """Custom analyzer plugin."""
    
    name = "custom-analyzer"
    version = "1.0.0"
    
    async def initialize(self) -> None:
        self._model = await load_model()
    
    async def shutdown(self) -> None:
        await self._model.cleanup()
    
    async def analyze(self, content: str) -> AnalysisResult:
        return await self._model.analyze(content)
    
    def supported_types(self) -> list[str]:
        return ["python", "markdown"]
```

### Plugin Discovery

```python
class PluginManager:
    """Manages plugin lifecycle."""
    
    def __init__(self):
        self._plugins: dict[str, PluginProtocol] = {}
    
    async def discover(self) -> None:
        """Discover plugins from all sources."""
        # 1. Bundled plugins
        await self._discover_bundled()
        
        # 2. External plugins (entry points)
        await self._discover_entry_points()
        
        # 3. User plugins (~/.sage/plugins)
        await self._discover_user_plugins()
    
    async def load(self, name: str) -> PluginProtocol:
        """Load and initialize a plugin."""
        plugin = self._plugins[name]
        await plugin.initialize()
        return plugin
```

### Plugin Configuration

```yaml
# sage.yaml
plugins:
  enabled:
    - custom-analyzer
    - health-checker
  
  disabled:
    - experimental-feature
  
  settings:
    custom-analyzer:
      model: gpt-4
      timeout: 5000
```

### Plugin Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Discover │ →  │  Load    │ →  │Initialize│ →  │  Active  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                                                      │
                                                      ▼
                                              ┌──────────┐
                                              │ Shutdown │
                                              └──────────┘
```

### Plugin Registration with DI

```python
# Register plugin with DI container
async def register_plugin(plugin: PluginProtocol) -> None:
    container = get_container()
    
    if isinstance(plugin, AnalyzerPlugin):
        container.register_instance(
            AnalyzerPlugin,
            plugin
        )
    
    # Emit event for other components
    await bus.publish(Event(
        type="plugin.registered",
        data={"name": plugin.name, "version": plugin.version}
    ))
```

### Error Handling

```python
async def safe_plugin_call(
    plugin: PluginProtocol,
    method: str,
    *args,
    **kwargs
) -> Any:
    """Call plugin method with error isolation."""
    try:
        func = getattr(plugin, method)
        return await func(*args, **kwargs)
    except Exception as e:
        logger.error(
            "Plugin error",
            plugin=plugin.name,
            method=method,
            error=str(e)
        )
        await bus.publish(Event(
            type="plugin.error",
            data={"plugin": plugin.name, "error": str(e)}
        ))
        raise PluginError(f"Plugin {plugin.name} failed: {e}")
```

### Directory Structure

```
src/sage/plugins/
├── __init__.py          # Plugin system exports
├── manager.py           # Plugin manager
├── protocols.py         # Plugin protocols
├── loader.py            # Plugin loading utilities
└── bundled/             # Bundled plugins
    ├── __init__.py
    ├── health_checker.py
    └── code_analyzer.py
```

---

## Related

- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Capabilities layer
- `.context/decisions/ADR_0004_DEPENDENCY_INJECTION.md` — DI integration
- `.context/decisions/ADR_0006_PROTOCOL_FIRST.md` — Protocol contracts
- `docs/design/05-plugin-memory.md` — Full plugin design
- `src/sage/plugins/` — Implementation

---

*AI Collaboration Knowledge Base*
