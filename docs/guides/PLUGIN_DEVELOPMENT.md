
# Plugin Development Guide

> How to create and publish plugins for SAGE Knowledge Base

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Getting Started](#2-getting-started)
- [3. Plugin Structure](#3-plugin-structure)
- [4. Hook System](#4-hook-system)
- [5. Publishing](#5-publishing)

---

## 1. Overview

### Plugin Capabilities

SAGE plugins can:

- Add custom MCP tools
- Extend knowledge loading
- Implement custom analyzers
- Add CLI commands
- Hook into core events

### Plugin Types

| Type          | Purpose                   | Example                 |
|---------------|---------------------------|-------------------------|
| **Tool**      | Add MCP tools             | Custom search, analysis |
| **Loader**    | Extend content loading    | Custom file formats     |
| **Analyzer**  | Add analysis capabilities | Code quality checks     |
| **Formatter** | Custom output formats     | Export to PDF           |

---

## 2. Getting Started

### Quick Start

```bash
# Create plugin directory
mkdir sage-plugin-myplugin
cd sage-plugin-myplugin

# Initialize structure
mkdir -p src/sage_myplugin
touch src/sage_myplugin/__init__.py
touch src/sage_myplugin/plugin.py
touch pyproject.toml
```

### Minimal Plugin

```python
# src/sage_myplugin/plugin.py
from sage.plugins import PluginBase, hookimpl

class MyPlugin(PluginBase):
    """My custom SAGE plugin."""
    
    name = "my-plugin"
    version = "1.0.0"
    description = "A custom SAGE plugin"
    
    @hookimpl
    def on_load(self, context):
        """Called when plugin loads."""
        self.logger.info(f"{self.name} loaded!")
    
    @hookimpl
    def register_tools(self, registry):
        """Register MCP tools."""
        registry.add_tool(self.my_tool)
    
    async def my_tool(self, query: str) -> str:
        """My custom tool.
        
        Args:
            query: The search query
            
        Returns:
            Tool result
        """
        return f"Result for: {query}"
```

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "sage-plugin-myplugin"
version = "1.0.0"
description = "My SAGE plugin"
requires-python = ">=3.12"
dependencies = ["sage-kb>=0.1.0"]

[project.entry-points."sage.plugins"]
my-plugin = "sage_myplugin.plugin:MyPlugin"
```

---

## 3. Plugin Structure

### Recommended Layout

```
sage-plugin-myplugin/
├── src/
│   └── sage_myplugin/
│       ├── __init__.py
│       ├── plugin.py      # Main plugin class
│       ├── tools.py       # MCP tools
│       ├── analyzers.py   # Analyzers (optional)
│       └── config.yaml    # Plugin config
├── tests/
│   └── test_plugin.py
├── pyproject.toml
├── README.md
└── LICENSE
```

### Configuration

```yaml
# src/sage_myplugin/config.yaml
plugin:
  name: my-plugin
  enabled: true
  
settings:
  api_endpoint: "https://api.example.com"
  timeout_ms: 5000
  
hooks:
  - on_load
  - register_tools
  - on_knowledge_request
```

### Loading Configuration

```python
from pathlib import Path
import yaml

class MyPlugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        config_path = Path(__file__).parent / "config.yaml"
        if config_path.exists():
            return yaml.safe_load(config_path.read_text())
        return {}
```

---

## 4. Hook System

### Available Hooks

| Hook                   | When Called           | Parameters         |
|------------------------|-----------------------|--------------------|
| `on_load`              | Plugin initialization | `context`          |
| `on_unload`            | Plugin shutdown       | `context`          |
| `register_tools`       | Tool registration     | `registry`         |
| `on_knowledge_request` | Before loading        | `layer`, `query`   |
| `on_knowledge_loaded`  | After loading         | `layer`, `content` |
| `on_search`            | Before search         | `query`, `options` |
| `on_error`             | On any error          | `error`, `context` |

### Hook Implementation

```python
from sage.plugins import PluginBase, hookimpl

class MyPlugin(PluginBase):
    
    @hookimpl
    def on_load(self, context):
        """Initialize plugin resources."""
        self.client = self._create_client()
        self.logger.info("Plugin initialized")
    
    @hookimpl
    def on_unload(self, context):
        """Cleanup plugin resources."""
        if self.client:
            self.client.close()
    
    @hookimpl
    def on_knowledge_request(self, layer: str, query: str):
        """Intercept knowledge requests."""
        # Return None to let default handling proceed
        # Return content to override
        if layer == "custom":
            return self._load_custom_content(query)
        return None
    
    @hookimpl
    def on_knowledge_loaded(self, layer: str, content: str):
        """Process loaded content."""
        # Modify or enrich content
        if self.config.get("enrich_content"):
            return self._enrich(content)
        return content
```

### Hook Priority

```python
@hookimpl(tryfirst=True)  # Run before other plugins
def on_knowledge_request(self, layer, query):
    ...

@hookimpl(trylast=True)   # Run after other plugins
def on_knowledge_loaded(self, layer, content):
    ...
```

---

## 5. Publishing

### Testing Locally

```bash
# Install in development mode
pip install -e .

# Enable plugin
sage plugin enable my-plugin

# Test
sage plugin list
sage info  # Should show plugin
```

### Publishing to PyPI

```bash
# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### Plugin Guidelines

**Do:**

- ✅ Follow SAGE naming conventions
- ✅ Handle errors gracefully
- ✅ Log important events
- ✅ Document all tools
- ✅ Include tests

**Don't:**

- ❌ Block the event loop
- ❌ Modify core behavior unexpectedly
- ❌ Store sensitive data in logs
- ❌ Create circular dependencies

---

## Quick Reference

### Plugin Commands

```bash
# List plugins
sage plugin list

# Install plugin
pip install sage-plugin-name
sage plugin enable plugin-name

# Disable plugin
sage plugin disable plugin-name

# Plugin info
sage plugin info plugin-name
```

### Debugging

```python
# Enable debug logging
import logging
logging.getLogger("sage.plugins").setLevel(logging.DEBUG)

# In plugin
self.logger.debug("Debug message", extra={"data": data})
```

---

## Related

- [Advanced Usage](advanced.md) — Plugin configuration
- `docs/design/05-plugin-memory.md` — Plugin architecture
- `.context/decisions/ADR_0008_PLUGIN_SYSTEM.md` — Plugin design decisions

---

*AI Collaboration Knowledge Base*
