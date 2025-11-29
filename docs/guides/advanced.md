# Advanced Usage Guide

> Deep dive into SAGE Knowledge Base advanced features and customization

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

### 1.1 Configuration Files

SAGE uses a modular configuration system:

```
config/
├── sage.yaml           # Main configuration
├── core/               # Core layer configs
│   ├── di.yaml         # Dependency injection
│   ├── logging.yaml    # Logging settings
│   ├── memory.yaml     # Memory/persistence
│   ├── security.yaml   # Security settings
│   └── timeout.yaml    # Timeout levels
├── services/           # Service configs
│   ├── api.yaml        # REST API
│   ├── cli.yaml        # CLI settings
│   └── mcp.yaml        # MCP server
├── knowledge/          # Knowledge configs
│   ├── content.yaml    # Content paths
│   ├── loading.yaml    # Loading strategies
│   ├── triggers.yaml   # Auto-load triggers
│   └── token_budget.yaml
└── capabilities/       # Capability configs
    ├── autonomy.yaml
    ├── plugins.yaml
    └── quality.yaml
```

### 1.2 Environment Overrides

Override any config value via environment variables:

```bash
# Pattern: SAGE_<SECTION>_<KEY>=value
export SAGE_TIMEOUT_CACHE_LOOKUP=200ms
export SAGE_LOGGING_LEVEL=DEBUG
export SAGE_MCP_HOST=0.0.0.0
export SAGE_MCP_PORT=8080
```

### 1.3 Custom Configuration

Create a custom config file:

```yaml
# my-config.yaml
extends: config/sage.yaml

timeout:
  operations:
    cache_lookup: 200ms  # Override default
    
logging:
  level: DEBUG
  format: json
```

Load with:

```bash
sage --config my-config.yaml get core
```

---

## 2. CLI Advanced

### 2.1 Output Formats

```bash
# JSON output for scripting
sage get core --format json | jq '.content'

# Markdown output
sage get core --format markdown

# Plain text (default)
sage get core --format text

# Compact mode (minimal output)
sage get core --compact
```

### 2.2 Filtering and Selection

```bash
# Get specific layer
sage get --layer frameworks

# Get with token budget
sage get core --budget 500

# Search with filters
sage search "timeout" --layer core --max-results 10

# Search with context
sage search "pattern" --context 3
```

### 2.3 Batch Operations

```bash
# Load multiple layers
sage get core guidelines frameworks

# Export knowledge to file
sage export --output knowledge.md --layers core,guidelines

# Validate all content
sage validate --all
```

### 2.4 Shell Completion

```bash
# Bash
sage --install-completion bash

# Zsh
sage --install-completion zsh

# Fish
sage --install-completion fish

# PowerShell
sage --install-completion powershell
```

---

## 3. MCP Integration

### 3.1 Server Configuration

```yaml
# config/services/mcp.yaml
mcp:
  host: localhost
  port: 3000
  transport: stdio  # or sse, websocket
  
  tools:
    - get_knowledge
    - search_knowledge
    - kb_info
    - get_framework
    - analyze_code
    - check_quality
    
  resources:
    expose_content: true
    max_resource_size: 100000
```

### 3.2 Multi-Client Setup

```bash
# Start MCP server for multiple clients
sage serve --transport sse --port 3000

# Or via stdio for single client
sage serve --transport stdio
```

### 3.3 Custom Tools

Register custom MCP tools:

```python
from sage.services.mcp import MCPServer

server = MCPServer()

@server.tool()
async def my_custom_tool(query: str) -> str:
    """Custom tool description."""
    # Implementation
    return result

# Or via configuration
# config/services/mcp.yaml
mcp:
  custom_tools:
    - module: mypackage.tools
      function: my_custom_tool
```

### 3.4 Client Configuration Examples

**Claude Desktop (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "sage": {
      "command": "sage",
      "args": ["serve"],
      "env": {
        "SAGE_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Cursor (`.cursor/mcp.json`):**

```json
{
  "servers": {
    "sage": {
      "command": "sage",
      "args": ["serve", "--transport", "stdio"]
    }
  }
}
```

---

## 4. Python API

### 4.1 Async Patterns

```python
import asyncio
from sage.core.loader import KnowledgeLoader
from sage.core.timeout import TimeoutManager

async def load_with_custom_timeout():
    loader = KnowledgeLoader()
    timeout_mgr = TimeoutManager()
    
    # Load with specific timeout level
    async with timeout_mgr.timeout(level="T3"):  # 2s
        result = await loader.load_layer("frameworks")
    
    return result

# Run async
result = asyncio.run(load_with_custom_timeout())
```

### 4.2 Batch Loading

```python
from sage.core.loader import KnowledgeLoader

async def batch_load():
    loader = KnowledgeLoader()
    
    # Load multiple layers concurrently
    layers = ["core", "guidelines", "frameworks"]
    results = await loader.load_batch(layers, timeout_ms=5000)
    
    # Process results
    for layer, content in results.items():
        print(f"{layer}: {len(content)} chars")

asyncio.run(batch_load())
```

### 4.3 Custom Loader

```python
from sage.core.protocols import LoaderProtocol
from sage.core.di import Container

class CustomLoader(LoaderProtocol):
    """Custom knowledge loader."""
    
    async def load(self, path: str, timeout_ms: int = 2000) -> str:
        # Custom loading logic
        pass
    
    async def search(self, query: str, **kwargs) -> list:
        # Custom search logic
        pass

# Register with DI container
container = Container()
container.register(LoaderProtocol, CustomLoader, lifetime="singleton")
```

### 4.4 Event Handling

```python
from sage.core.events import EventBus

bus = EventBus()

# Subscribe to events
@bus.subscribe("knowledge.loaded")
async def on_knowledge_loaded(event):
    print(f"Loaded: {event.layer} in {event.duration_ms}ms")

@bus.subscribe("timeout.triggered")
async def on_timeout(event):
    print(f"Timeout at level {event.level}: {event.operation}")

# Events are automatically published by core components
```

---

## 5. Plugin Development

### 5.1 Plugin Structure

```
my_plugin/
├── __init__.py
├── plugin.py          # Main plugin class
├── tools.py           # MCP tools (optional)
├── analyzers.py       # Analyzers (optional)
└── config.yaml        # Plugin config
```

### 5.2 Basic Plugin

```python
# my_plugin/plugin.py
from sage.plugins import PluginBase, hookimpl

class MyPlugin(PluginBase):
    """My custom plugin."""
    
    name = "my-plugin"
    version = "1.0.0"
    
    @hookimpl
    def on_load(self, context):
        """Called when plugin is loaded."""
        self.logger.info("Plugin loaded!")
    
    @hookimpl
    def on_knowledge_request(self, layer: str, query: str):
        """Hook into knowledge requests."""
        # Modify or extend behavior
        pass
    
    @hookimpl
    def register_tools(self, registry):
        """Register custom MCP tools."""
        registry.add_tool(self.my_tool)
    
    async def my_tool(self, param: str) -> str:
        """Custom tool implementation."""
        return f"Result: {param}"
```

### 5.3 Plugin Configuration

```yaml
# my_plugin/config.yaml
plugin:
  name: my-plugin
  enabled: true
  
  settings:
    custom_option: value
    
  hooks:
    - on_load
    - on_knowledge_request
    - register_tools
```

### 5.4 Installing Plugins

```bash
# Install from directory
sage plugin install ./my_plugin

# Install from package
pip install sage-plugin-myplugin

# Enable/disable
sage plugin enable my-plugin
sage plugin disable my-plugin

# List plugins
sage plugin list
```

---

## 6. Performance Tuning

### 6.1 Timeout Optimization

```yaml
# config/core/timeout.yaml
timeout:
  operations:
    # Adjust based on your environment
    cache_lookup: 50ms    # Reduce for fast storage
    file_read: 300ms      # Reduce for SSD
    layer_load: 1500ms    # Adjust for content size
    full_load: 4000ms     # Total budget
    analysis: 8000ms      # Complex operations
    
  circuit_breaker:
    failure_threshold: 3
    recovery_time: 30s
    half_open_requests: 1
```

### 6.2 Caching Strategy

```yaml
# config/core/memory.yaml
memory:
  cache:
    enabled: true
    max_size: 100MB
    ttl: 3600s           # 1 hour
    strategy: lru        # lru, lfu, fifo
    
  persistence:
    enabled: true
    path: .cache/sage
    sync_interval: 60s
```

### 6.3 Token Budget Management

```yaml
# config/knowledge/token_budget.yaml
token_budget:
  default: 4000
  
  # Per-layer budgets
  layers:
    core: 500
    guidelines: 1000
    frameworks: 1500
    practices: 1000
    
  # Compression settings
  compression:
    enabled: true
    threshold: 0.8       # Compress when >80% budget
    strategy: summarize  # summarize, truncate, prioritize
```

### 6.4 Logging for Performance Analysis

```yaml
# config/core/logging.yaml
logging:
  level: INFO
  
  # Enable performance logging
  performance:
    enabled: true
    slow_threshold: 500ms
    
  handlers:
    - type: file
      path: .logs/performance.log
      format: json
      filter: performance
```

### 6.5 Profiling

```bash
# Run with profiling
sage --profile get core

# Generate performance report
sage diagnose --performance

# Benchmark operations
sage benchmark --iterations 100
```

---

## Related

- [Quick Start](quickstart.md) — Basic setup and usage
- [Troubleshooting](troubleshooting.md) — Common issues and solutions
- `docs/api/` — API reference
- `docs/design/` — Architecture documentation
- `.knowledge/practices/engineering/` — Engineering best practices

---

*SAGE Knowledge Base - Advanced Usage Guide*
