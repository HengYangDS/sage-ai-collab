# Advanced Usage Guide

> Deep dive into SAGE Knowledge Base advanced features

---

## Table of Contents

[1. Configuration](#1-configuration) · [2. CLI Customization](#2-cli-customization) · [3. MCP Advanced](#3-mcp-advanced) · [4. Python Advanced](#4-python-advanced) · [5. Plugin Development](#5-plugin-development) · [6. Custom Knowledge](#6-custom-knowledge)

---

## 1. Configuration

### Configuration Structure

SAGE uses a modular configuration system:

```
config/
├── sage.yaml              # Main entry point
├── core/                  # Core infrastructure
│   ├── timeout.yaml       # Timeout hierarchy
│   ├── logging.yaml       # Logging settings
│   ├── memory.yaml        # Memory/cache settings
│   └── di.yaml            # Dependency injection
├── services/              # Service layer
│   ├── cli.yaml           # CLI settings
│   ├── mcp.yaml           # MCP server settings
│   └── api.yaml           # REST API settings
├── knowledge/             # Knowledge management
│   ├── content.yaml       # Content structure
│   ├── loading.yaml       # Loading strategies
│   └── search.yaml        # Search settings
└── capabilities/          # Features
    ├── features.yaml      # Feature flags
    ├── plugins.yaml       # Plugin settings
    └── autonomy.yaml      # Autonomy levels
```

### Timeout Configuration

Customize the 5-level timeout hierarchy in `config/core/timeout.yaml`:

```yaml
timeout:
  levels:
    t1: 100      # Cache lookup
    t2: 500      # Single file
    t3: 2000     # Layer load (default)
    t4: 5000     # Full KB load
    t5: 10000    # Complex analysis

  strategies:
    graceful_degradation: true
    partial_results: true
    fallback_content: true
```

### Logging Configuration

Configure structured logging in `config/core/logging.yaml`:

```yaml
logging:
  level: INFO
  format: json
  
  handlers:
    console:
      enabled: true
      level: INFO
    file:
      enabled: true
      path: .logs/sage.log
      rotation: daily
      retention: 7
```

### Environment Variables

Override configuration via environment:

| Variable | Config Path | Example |
|----------|-------------|---------|
| `SAGE_TIMEOUT_T3` | `timeout.levels.t3` | `3000` |
| `SAGE_MCP_PORT` | `mcp.port` | `9000` |
| `SAGE_LOG_LEVEL` | `logging.level` | `DEBUG` |
| `SAGE_CACHE_ENABLED` | `memory.cache.enabled` | `false` |

---

## 2. CLI Customization

### Output Formats

```bash
# Rich formatted output (default)
sage get core --format rich

# Plain text output
sage get core --format plain

# JSON output for scripting
sage get core --format json | jq '.content'
```

### Custom Timeouts

```bash
# Quick response (may be partial)
sage get core --timeout 500

# Ensure complete response
sage get all --timeout 10000
```

### Verbose Mode

```bash
# Show detailed information
sage get core --verbose

# Debug mode
sage search "pattern" -v -v
```

### Configuration Override

```bash
# Use custom config file
sage --config /path/to/custom.yaml get core

# Override specific settings
SAGE_TIMEOUT_T3=5000 sage get all
```

### Shell Completion

```bash
# Generate completion script (bash)
sage --install-completion bash

# Generate completion script (zsh)
sage --install-completion zsh

# Generate completion script (fish)
sage --install-completion fish
```

---

## 3. MCP Advanced

### Server Configuration

Advanced MCP settings in `config/services/mcp.yaml`:

```yaml
mcp:
  host: localhost
  port: 8000
  
  # Connection limits
  max_connections: 10
  connection_timeout: 30000
  
  # Capabilities
  capabilities:
    - knowledge_retrieval
    - search
    - context_management
    - task_optimization
  
  # Resource caching
  resource_cache:
    enabled: true
    ttl: 300  # seconds
```

### Custom Tools

Register custom MCP tools:

```python
from sage.services.mcp_server import mcp_server

@mcp_server.tool()
async def custom_analysis(content: str, analysis_type: str) -> dict:
    """Perform custom analysis on content."""
    # Your implementation
    return {"result": "..."}
```

### Resource Templates

Define custom resource templates:

```python
from sage.services.mcp_server import mcp_server

@mcp_server.resource("analysis://{topic}")
async def analysis_resource(topic: str) -> str:
    """Provide analysis for a topic."""
    # Load and analyze content
    return analysis_result
```

### Error Handling

Configure error responses:

```yaml
mcp:
  error_handling:
    include_stack_trace: false
    include_fallback: true
    log_errors: true
```

---

## 4. Python Advanced

### Custom Configuration

```python
from sage.core.config import SAGEConfig

config = SAGEConfig(
    knowledge_base_path="/custom/path",
    timeout_t3=3000,
    cache_enabled=True,
    cache_ttl=600
)

loader = KnowledgeLoader(config=config)
```

### Task-Based Loading

Load knowledge optimized for specific tasks:

```python
from sage.core.loader import KnowledgeLoader
from sage.domain.knowledge import TaskType

loader = KnowledgeLoader()

# Load for coding task
coding_context = await loader.load_for_task(
    task_type=TaskType.CODING,
    token_budget=4000,
    language="python"
)

# Load for debugging
debug_context = await loader.load_for_task(
    task_type=TaskType.DEBUGGING,
    token_budget=6000,
    include_patterns=True
)
```

### Event Handling

Subscribe to system events:

```python
from sage.core.events import EventBus, Event

bus = EventBus()

@bus.subscribe("knowledge.loaded")
async def on_knowledge_loaded(event: Event):
    print(f"Layer: {event.data['layer']}")
    print(f"Time: {event.data['load_time_ms']}ms")

@bus.subscribe("cache.hit")
async def on_cache_hit(event: Event):
    print(f"Cache hit: {event.data['key']}")

@bus.subscribe("timeout.warning")
async def on_timeout_warning(event: Event):
    print(f"Approaching timeout: {event.data['remaining_ms']}ms")
```

### Custom Loaders

Create specialized loaders:

```python
from sage.core.loader import KnowledgeLoader
from sage.interfaces import LoaderProtocol

class CustomLoader(LoaderProtocol):
    async def load(self, layer: str, **kwargs) -> LoadResult:
        # Custom loading logic
        content = await self.custom_fetch(layer)
        return LoadResult(
            content=content,
            metadata=LoadMetadata(layer=layer, ...),
            complete=True
        )
```

### Timeout Context

Fine-grained timeout control:

```python
from sage.core.timeout import timeout_context, TimeoutLevel

async def complex_operation():
    async with timeout_context(TimeoutLevel.T4) as ctx:
        # Phase 1: Core loading
        core = await load_core()
        
        if ctx.remaining_ms < 2000:
            return core  # Return partial
        
        # Phase 2: Extended loading
        extended = await load_extended()
        
        return merge(core, extended)
```

---

## 5. Plugin Development

### Plugin Structure

```
plugins/
└── my_plugin/
    ├── __init__.py
    ├── plugin.py
    └── config.yaml
```

### Plugin Interface

```python
# plugins/my_plugin/plugin.py
from sage.plugins import PluginBase, hook

class MyPlugin(PluginBase):
    name = "my_plugin"
    version = "1.0.0"
    
    @hook("before_load")
    async def before_load(self, layer: str, **kwargs):
        """Called before knowledge loading."""
        self.logger.info(f"Loading {layer}")
    
    @hook("after_load")
    async def after_load(self, result: LoadResult, **kwargs):
        """Called after knowledge loading."""
        self.logger.info(f"Loaded {result.metadata.files_loaded} files")
    
    @hook("transform_content")
    async def transform(self, content: str, **kwargs) -> str:
        """Transform loaded content."""
        return self.add_custom_header(content)
```

### Plugin Configuration

```yaml
# plugins/my_plugin/config.yaml
my_plugin:
  enabled: true
  priority: 100
  settings:
    custom_header: "# My Custom Header"
```

### Registering Plugins

```yaml
# config/capabilities/plugins.yaml
plugins:
  load_path:
    - plugins/
    - ~/.sage/plugins/
  
  enabled:
    - my_plugin
    - another_plugin
  
  disabled:
    - experimental_plugin
```

---

## 6. Custom Knowledge

### Adding Knowledge Content

Add custom content to the knowledge base:

```
content/
└── custom/
    ├── index.md
    └── my_guide.md
```

### Content Format

Follow the standard format:

```markdown
# Title

> Brief description

---

## Table of Contents

[1. Section](#1-section) · [2. Another](#2-another)

---

## 1. Section

Content here...

---

## Related

- `other/file.md` — Description

---

*Footer*
```

### Knowledge Layers

Register custom layer in `config/knowledge/content.yaml`:

```yaml
content:
  layers:
    core:
      path: content/core
      priority: 1
    custom:
      path: content/custom
      priority: 5
```

### Context Triggers

Add triggers for your content in `config/knowledge/triggers.yaml`:

```yaml
triggers:
  keywords:
    my_topic:
      - "custom keyword"
      - "my feature"
    
  patterns:
    my_pattern:
      regex: "custom-\\d+"
      layer: custom
```

---

## 7. Performance Tuning

### Cache Optimization

```yaml
# config/core/memory.yaml
memory:
  cache:
    enabled: true
    max_size: 100  # MB
    ttl: 300       # seconds
    strategy: lru
    
  preload:
    enabled: true
    layers:
      - core
      - guidelines
```

### Parallel Loading

```yaml
# config/knowledge/loading.yaml
loading:
  parallel:
    enabled: true
    max_concurrent: 4
    
  smart_loading:
    enabled: true
    task_priority: true
```

### Token Budget

Configure token limits:

```yaml
# config/knowledge/token_budget.yaml
token_budget:
  default: 4000
  
  by_task:
    coding: 4000
    debugging: 6000
    reviewing: 5000
    planning: 3000
    
  by_layer:
    core: 1000
    guidelines: 1500
    frameworks: 1000
    practices: 500
```

---

## 8. Troubleshooting

### Debug Mode

Enable debug logging:

```bash
SAGE_LOG_LEVEL=DEBUG sage get core
```

### Performance Profiling

```python
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = await loader.load("all", profile=True)

print(result.metadata.profile)
# {
#   "total_ms": 2500,
#   "file_read_ms": 1200,
#   "parse_ms": 800,
#   "transform_ms": 500
# }
```

### Cache Inspection

```bash
# Show cache status
sage info --json | jq '.cache'

# Clear cache
sage cache clear

# Warm cache
sage cache warm --layers core,guidelines
```

---

## Related

- [Quick Start](quickstart.md) — Getting started guide
- [API Reference](../api/index.md) — API documentation
- [Design Documents](../design/) — Architecture details
- `config/` — Configuration files

---

*SAGE Knowledge Base - Advanced Usage Guide*
