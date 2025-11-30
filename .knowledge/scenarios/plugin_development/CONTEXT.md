# Plugin Development Scenario Context

> Pre-configured context for SAGE plugin development

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)

- [2. Relevant Knowledge](#2-relevant-knowledge)

- [3. Project Structure](#3-project-structure)

- [4. Plugin Architecture](#4-plugin-architecture)

- [5. Implementation Patterns](#5-implementation-patterns)

- [6. Common Tasks](#6-common-tasks)

- [7. Autonomy Calibration](#7-autonomy-calibration)

- [8. Quick Commands](#8-quick-commands)

---

## 1. Scenario Profile

```yaml

scenario: plugin_development

languages: [ python ]

tools: [ pytest, mypy, ruff ]

focus: [ extensibility, hooks, lifecycle, configuration ]

autonomy_default: L3

```
---

## 2. Relevant Knowledge

| Priority      | Files                                                                                                                            |

|---------------|----------------------------------------------------------------------------------------------------------------------------------|

| **Auto-Load** | `core/PRINCIPLES.md` · `docs/api/PLUGIN_QUICK_REF.md` · `.knowledge/practices/engineering/PATTERNS.md`                                      |

| **On-Demand** | `.knowledge/practices/engineering/TESTING_STRATEGY.md` · `.context/decisions/ADR_0008_PLUGIN_SYSTEM.md` · `docs/design/05-plugin-memory.md` |

---

## 3. Project Structure

| Directory                   | Purpose                  |

|-----------------------------|--------------------------|

| `src/sage/plugins/`         | Plugin framework core    |

| `src/sage/plugins/bundled/` | Built-in plugins         |

| `config/capabilities/`      | Plugin configuration     |

| `tests/unit/plugins/`       | Plugin unit tests        |

| `docs/guides/ADVANCED.md`   | Plugin development guide |

---

## 4. Plugin Architecture

### 4.1 Plugin System Overview

```mermaid
flowchart TB
    subgraph Core["SAGE Core"]
        PM["Plugin Manager"]
        HR["Hook Registry"]
        PC["Plugin Config"]
    end
    
    subgraph Interface["Plugin Interface"]
        subgraph Bundled["Bundled Plugins"]
            A["Plugin A"]
            B["Plugin B"]
            C["Plugin C"]
            D["Plugin D"]
        end
    end
    
    EP["External Plugins"]
    
    Core --> Interface
    Interface --> EP
```
### 4.2 Core Components

| Component         | Purpose                     | Location                           |

|-------------------|-----------------------------|------------------------------------|

| **PluginBase**    | Base class for all plugins  | `src/sage/plugins/base.py`         |

| **PluginManager** | Plugin lifecycle management | `src/sage/plugins/manager.py`      |

| **HookRegistry**  | Hook point registration     | `src/sage/plugins/hooks.py`        |

| **PluginConfig**  | Plugin configuration        | `config/capabilities/plugins.yaml` |

### 4.3 Plugin Lifecycle

```mermaid
flowchart LR
    D["Discover"] --> V["Validate"] --> R["Register"] --> E["Enable"]
    E --> A["Active"]
    A --> Di["Disable"] --> U["Unload"]
```
| Phase        | Description            | Hook          |

|--------------|------------------------|---------------|

| **Discover** | Find available plugins | -             |

| **Validate** | Check compatibility    | `on_validate` |

| **Register** | Add to plugin registry | `on_register` |

| **Enable**   | Activate plugin        | `on_enable`   |

| **Active**   | Plugin running         | Various hooks |

| **Disable**  | Deactivate plugin      | `on_disable`  |

| **Unload**   | Remove from memory     | `on_unload`   |

---

## 5. Implementation Patterns

### 5.1 Basic Plugin Structure

```python

from sage.plugins import PluginBase, hook

class MyPlugin(PluginBase):

    """My custom SAGE plugin.

    

    This plugin demonstrates the basic structure and

    available hook points.

    """

    # Plugin metadata

    name = "my-plugin"

    version = "1.0.0"

    description = "A sample SAGE plugin"

    author = "Your Name"

    # Dependencies (optional)

    dependencies = ["other-plugin>=1.0"]

    def __init__(self, config: dict | None = None):

        """Initialize plugin with optional config."""

        super().__init__(config)

        self._initialized = False

    # Lifecycle hooks

    async def on_enable(self) -> None:

        """Called when plugin is enabled."""

        self._initialized = True

        self.logger.info(f"{self.name} enabled")

    async def on_disable(self) -> None:

        """Called when plugin is disabled."""

        self._initialized = False

        self.logger.info(f"{self.name} disabled")

```
### 5.2 Hook Implementation

```python

from sage.plugins import PluginBase, hook

class ContentPlugin(PluginBase):

    """Plugin that processes content."""

    name = "content-processor"

    version = "1.0.0"

    @hook("before_load")

    async def before_load(self, path: str) -> str:

        """Modify path before content loading.

        

        Args:

            path: Original content path

            

        Returns:

            Modified path (or original if unchanged)

        """

        # Example: Redirect old paths

        if path.startswith("legacy/"):

            return path.replace("legacy/", ".knowledge/")

        return path

    @hook("after_load")

    async def after_load(self, content: str, path: str) -> str:

        """Process content after loading.

        

        Args:

            content: Loaded content

            path: Content path

            

        Returns:

            Processed content

        """

        # Example: Add metadata header

        header = f"<!-- Source: {path} -->\n"

        return header + content

    @hook("on_search")

    async def on_search(self, query: str, results: list) -> list:

        """Filter or reorder search results.

        

        Args:

            query: Search query

            results: Current results

            

        Returns:

            Modified results

        """

        # Example: Boost certain results

        return sorted(results, key=lambda r: r.relevance, reverse=True)

```
### 5.3 Available Hook Points

| Hook               | Trigger             | Parameters                        | Returns |

|--------------------|---------------------|-----------------------------------|---------|

| `before_load`      | Before content load | `path: str`                       | `str`   |

| `after_load`       | After content load  | `content: str, path: str`         | `str`   |

| `on_search`        | During search       | `query: str, results: list`       | `list`  |

| `on_error`         | On error occurrence | `error: Exception, context: dict` | `None`  |

| `on_config_change` | Config updated      | `key: str, value: Any`            | `None`  |

| `before_serve`     | Before MCP serve    | `server: FastMCP`                 | `None`  |

| `after_serve`      | After MCP stop      | `server: FastMCP`                 | `None`  |

### 5.4 Plugin Configuration

```yaml

# config/capabilities/plugins.yaml

plugins:

  # Built-in plugins

  bundled:

    - name: cache-plugin

      enabled: true

      config:

        ttl: 3600

        max_size: 100MB

    - name: metrics-plugin

      enabled: true

      config:

        export_prometheus: true

  # External plugins

  external:

    - name: my-plugin

      path: ~/.sage/plugins/my_plugin.py

      enabled: true

      config:

        custom_option: value

  # Discovery paths

  discovery:

    - ~/.sage/plugins/

    - ./plugins/

```
### 5.5 Plugin with Configuration

```python

from sage.plugins import PluginBase, hook

from pydantic import BaseModel

class MyPluginConfig(BaseModel):

    """Configuration schema for MyPlugin."""

    option_a: str = "default"

    option_b: int = 10

    enabled_features: list[str] = []

class MyPlugin(PluginBase):

    """Plugin with typed configuration."""

    name = "configurable-plugin"

    version = "1.0.0"

    config_schema = MyPluginConfig

    def __init__(self, config: dict | None = None):

        super().__init__(config)

        # Config is validated and typed

        self.settings = MyPluginConfig(**(config or {}))

    @hook("after_load")

    async def after_load(self, content: str, path: str) -> str:

        if "feature_x" in self.settings.enabled_features:

            return self._process_feature_x(content)

        return content

```
### 5.6 Testing Plugins

```python

import pytest

from sage.plugins import PluginManager

from my_plugin import MyPlugin

@pytest.fixture

def plugin_manager():

    """Create plugin manager for testing."""

    return PluginManager()

@pytest.fixture

def my_plugin():

    """Create plugin instance."""

    return MyPlugin(config={"option_a": "test"})

class TestMyPlugin:

    """Tests for MyPlugin."""

    async def test_plugin_enables(self, my_plugin):

        """Plugin should enable successfully."""

        await my_plugin.on_enable()

        assert my_plugin._initialized

    async def test_before_load_hook(self, my_plugin):

        """Hook should modify legacy paths."""

        result = await my_plugin.before_load("legacy/old.md")

        assert result == ".knowledge/old.md"

    async def test_after_load_hook(self, my_plugin):

        """Hook should add metadata header."""

        result = await my_plugin.after_load("content", "test.md")

        assert "<!-- Source: test.md -->" in result

    async def test_plugin_integration(self, plugin_manager, my_plugin):

        """Plugin should integrate with manager."""

        await plugin_manager.register(my_plugin)

        await plugin_manager.enable("my-plugin")

        assert plugin_manager.is_enabled("my-plugin")

```
---

## 6. Common Tasks

| Task                 | Steps                                                     |

|----------------------|-----------------------------------------------------------|

| **Create plugin**    | Extend PluginBase → Add metadata → Implement hooks → Test |

| **Add hook point**   | Define in registry → Document → Implement in core         |

| **Configure plugin** | Define schema → Add to config → Validate on load          |

| **Test plugin**      | Unit tests → Integration tests → Manual testing           |

| **Package plugin**   | Add setup.py → Document → Publish to PyPI                 |

| **Debug plugin**     | Enable debug logging → Use breakpoints → Check hook calls |

### 6.1 Creating a New Plugin

```bash

# 1. Create plugin file

mkdir -p src/sage/plugins/bundled/my_plugin

touch src/sage/plugins/bundled/my_plugin/__init__.py

# 2. Implement plugin (see patterns above)

# 3. Add configuration

# Edit config/capabilities/plugins.yaml

# 4. Create tests

touch tests/unit/plugins/test_my_plugin.py

# 5. Run tests

pytest tests/unit/plugins/test_my_plugin.py -v

```
### 6.2 Debugging Plugins

```python

import logging

# Enable debug logging for plugins

logging.getLogger("sage.plugins").setLevel(logging.DEBUG)

# In your plugin

class MyPlugin(PluginBase):

    @hook("before_load")

    async def before_load(self, path: str) -> str:

        self.logger.debug(f"Processing path: {path}")

        # ... implementation

```
---

## 7. Autonomy Calibration

| Task Type                   | Level | Notes               |

|-----------------------------|-------|---------------------|

| Fix plugin documentation    | L5    | Low risk            |

| Add hook to existing plugin | L4    | Follow patterns     |

| Create new bundled plugin   | L3    | Needs review        |

| Add new hook point          | L2    | Affects all plugins |

| Change plugin API           | L1-L2 | Breaking change     |

| Modify lifecycle            | L1    | Core architecture   |

---

## 8. Quick Commands

| Category   | Commands                                                     |

|------------|--------------------------------------------------------------|

| **Test**   | `pytest tests/unit/plugins/ -v`                              |

| **Lint**   | `ruff check src/sage/plugins/`                               |

| **Type**   | `mypy src/sage/plugins/`                                     |

| **List**   | `sage plugins list` · `sage plugins info <name>`             |

| **Enable** | `sage plugins enable <name>` · `sage plugins disable <name>` |

---

## Best Practices

### Plugin Design

| Practice                     | Description                     |

|------------------------------|---------------------------------|

| **Single Purpose**           | Each plugin does one thing well |

| **Minimal Dependencies**     | Reduce external requirements    |

| **Graceful Degradation**     | Handle errors without crashing  |

| **Configuration Validation** | Use Pydantic for config schemas |

| **Comprehensive Testing**    | Unit + integration tests        |

### Performance

| Aspect               | Guideline                     |

|----------------------|-------------------------------|

| **Hook Execution**   | Keep hooks fast (< 100ms)     |

| **Memory Usage**     | Clean up resources on disable |

| **Async Operations** | Use async for IO operations   |

| **Caching**          | Cache expensive computations  |

### Security

| Check                | Description                 |

|----------------------|-----------------------------|

| **Input Validation** | Validate all external input |

| **Path Traversal**   | Prevent path manipulation   |

| **Code Injection**   | Sanitize dynamic code       |

| **Permissions**      | Follow least privilege      |

---

## Related

- `docs/design/05-plugin-memory.md` — Plugin system design

- `.context/decisions/ADR_0008_PLUGIN_SYSTEM.md` — Architecture decision

- `.knowledge/practices/engineering/PATTERNS.md` — Design patterns

- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing guide

---

*AI Collaboration Knowledge Base*

