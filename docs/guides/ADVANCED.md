
# Advanced Usage Guide

> Deep dive into SAGE Knowledge Base advanced features

---

## Table of Contents

- [1. Configuration](#1-configuration)
- [2. CLI Advanced](#2-cli-advanced)
- [3. MCP Integration](#3-mcp-integration)
- [4. Python API](#4-python-api)
- [5. Plugin Development](#5-plugin-development)
- [6. Performance Tuning](#6-performance-tuning)

---

## 1. Configuration

### 1.1 Configuration Structure

```
config/
├── sage.yaml           # Main configuration
├── core/               # Core: di, logging, memory, timeout
├── services/           # Services: api, cli, mcp
├── knowledge/          # Knowledge: content, loading, triggers
└── capabilities/       # Capabilities: autonomy, plugins, quality
```

### 1.2 Environment Overrides

| Pattern | Example |
|---------|---------|
| `SAGE_<SECTION>_<KEY>` | `SAGE_TIMEOUT_CACHE_LOOKUP=200ms` |
| Logging level | `SAGE_LOGGING_LEVEL=DEBUG` |
| MCP host/port | `SAGE_MCP_HOST=0.0.0.0` |

### 1.3 Custom Configuration

```yaml
# my-config.yaml
extends: config/sage.yaml
timeout:
  operations:
    cache_lookup: 200ms
logging:
  level: DEBUG
```

Load: `sage --config my-config.yaml get core`

---

## 2. CLI Advanced

### 2.1 Output Formats

| Format | Command | Use Case |
|--------|---------|----------|
| JSON | `sage get core --format json` | Scripting |
| Markdown | `sage get core --format markdown` | Documentation |
| Compact | `sage get core --compact` | Minimal output |

### 2.2 Filtering and Selection

```bash
sage get core --topics "principles,defaults"  # Select topics
sage search "timeout" --layer frameworks      # Layer filter
sage get guidelines --exclude "python"        # Exclude topics
```

### 2.3 Batch Operations

```bash
sage get core guidelines frameworks --merge   # Load multiple
sage search "pattern" --output results.json   # Save results
```

### 2.4 Debug Mode

```bash
sage --debug get core              # Verbose logging
sage --trace search "query"        # Trace execution
sage get core --timing             # Show timing info
```

---

## 3. MCP Integration

### 3.1 Server Configuration

```yaml
# config/services/mcp.yaml
mcp:
  host: localhost
  port: 8080
  transport: stdio  # or: sse, websocket
  timeout_ms: 5000
```

### 3.2 Claude Desktop Integration

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": ["serve", "--transport", "stdio"]
    }
  }
}
```

### 3.3 Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `sage_get_knowledge` | Load knowledge | `layer`, `timeout_ms` |
| `sage_search` | Search KB | `query`, `limit`, `layer` |
| `sage_get_context` | Task context | `task_type`, `token_budget` |
| `sage_info` | System info | (none) |

### 3.4 Custom Tools

```python
from sage.services.mcp_server import mcp

@mcp.tool()
async def my_custom_tool(param: str) -> dict:
    """Custom tool description."""
    return {"result": process(param)}
```

---

## 4. Python API

### 4.1 Basic Usage

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = await loader.load("core", timeout_ms=2000)
print(result.content, result.metadata)
```

### 4.2 Search API

```python
from sage.core.search import KnowledgeSearcher

searcher = KnowledgeSearcher()
results = await searcher.search("timeout", limit=5)
for hit in results:
    print(f"{hit.path}: {hit.score}")
```

### 4.3 Event System

```python
from sage.core.events import EventBus, Event

bus = EventBus()

@bus.subscribe("knowledge.loaded")
async def on_load(event: Event):
    print(f"Loaded: {event.data}")

await bus.publish(Event(type="knowledge.loaded", data={"layer": "core"}))
```

### 4.4 Context Manager

```python
from sage.core.timeout import timeout_context, TimeoutLevel

async with timeout_context(TimeoutLevel.T3) as ctx:
    result = await long_operation()
    if ctx.remaining_ms < 100:
        return partial_result
```

---

## 5. Plugin Development

### 5.1 Plugin Structure

```
my_plugin/
├── __init__.py      # Plugin entry point
├── plugin.yaml      # Plugin metadata
└── handlers.py      # Event handlers
```

### 5.2 Basic Plugin

```python
# my_plugin/__init__.py
from sage.plugins import Plugin, hook

class MyPlugin(Plugin):
    name = "my-plugin"
    version = "1.0.0"
    
    @hook("knowledge.pre_load")
    async def on_pre_load(self, event):
        # Modify or observe loading
        pass
```

### 5.3 Plugin Configuration

```yaml
# plugin.yaml
name: my-plugin
version: 1.0.0
description: My custom plugin
hooks:
  - knowledge.pre_load
  - knowledge.post_load
settings:
  enabled: true
  custom_option: value
```

### 5.4 Available Hooks

| Hook | Timing | Use Case |
|------|--------|----------|
| `knowledge.pre_load` | Before load | Validation, caching |
| `knowledge.post_load` | After load | Transformation |
| `search.pre_search` | Before search | Query modification |
| `search.post_search` | After search | Result filtering |

---

## 6. Performance Tuning

### 6.1 Timeout Configuration

| Level | Default | Use Case |
|-------|---------|----------|
| T1 | 100ms | Cache lookup |
| T2 | 500ms | Single file |
| T3 | 2s | Layer load |
| T4 | 5s | Full KB |
| T5 | 10s | Complex analysis |

### 6.2 Caching Strategy

```yaml
cache:
  enabled: true
  backend: memory  # or: redis, file
  ttl: 300         # seconds
  max_size: 1000   # entries
```

### 6.3 Memory Management

| Setting | Default | Description |
|---------|---------|-------------|
| `memory.max_tokens` | 4000 | Token budget |
| `memory.auto_prune` | true | Auto cleanup |
| `memory.warning_threshold` | 0.8 | 80% warning |

### 6.4 Loading Optimization

```yaml
loading:
  smart_loading: true       # Keyword triggers
  lazy: true                # Load on demand
  preload: ["core"]         # Always preload
  max_files_per_layer: 50   # Limit per layer
```

### 6.5 Monitoring

```bash
sage info --metrics                    # Show metrics
sage get core --timing                 # Load timing
SAGE_LOGGING_LEVEL=DEBUG sage serve    # Debug logs
```

---

## Related

- `docs/guides/quickstart.md` — Quick start guide
- `docs/guides/configuration.md` — Configuration reference
- `docs/guides/plugin_development.md` — Full plugin guide
- `docs/api/python.md` — Python API reference

---

*AI Collaboration Knowledge Base*
