---
title: SAGE Knowledge Base - Configuration Design
version: 0.1.0
date: 2025-11-29
status: production-ready
---

# Configuration Design

> **Modular configuration system with smart loading and graceful degradation**

## Overview

SAGE uses a modular configuration system where settings are organized into focused YAML files in the `config/` directory, with `sage.yaml` serving as the main entry point.

### Design Philosophy

```yaml
configuration:
  philosophy: "Modular, overridable, fail-safe"
  
  principles:
    - name: "Single Source of Truth"
      description: "Each setting defined in exactly one place"
    - name: "Sensible Defaults"
      description: "Works out of the box without configuration"
    - name: "Progressive Override"
      description: "Environment > sage.yaml > config/*.yaml > defaults"
    - name: "Fail-Safe Loading"
      description: "Missing configs use defaults, never crash"
```

---

## Configuration Priority

Configuration values are resolved in the following order (highest priority first):

```
┌─────────────────────────────────────────────────────────┐
│ 1. Environment Variables (SAGE_*)                       │ ← Highest
├─────────────────────────────────────────────────────────┤
│ 2. Main Config (sage.yaml)                              │
├─────────────────────────────────────────────────────────┤
│ 3. Included Configs (config/*.yaml via includes)        │
├─────────────────────────────────────────────────────────┤
│ 4. Config Directory (config/*.yaml auto-discovery)      │
├─────────────────────────────────────────────────────────┤
│ 5. Default Values (hardcoded in config.py)              │ ← Lowest
└─────────────────────────────────────────────────────────┘
```

### Environment Variable Format

```bash
# Pattern: SAGE_<SECTION>__<KEY>=<VALUE>
SAGE_LOGGING__LEVEL=DEBUG
SAGE_CACHE__ENABLED=false
SAGE_TIMEOUTS__T1_INSTANT=200
```

---

## Configuration Files

### Main Entry Point

| File | Purpose |
|------|---------|
| `sage.yaml` | Main configuration, metadata, includes list |

### Modular Config Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `config/timeout.yaml` | Timeout hierarchy & circuit breaker | operations, circuit_breaker, fallback |
| `config/loading.yaml` | Smart loading configuration | always, max_tokens, default_layers |
| `config/triggers.yaml` | Keyword-triggered content loading | 9 triggers with bilingual keywords |
| `config/plugins.yaml` | Plugin configuration | bundled plugins, cache settings |
| `config/features.yaml` | Feature flags | optimization features, service toggles |
| `config/di.yaml` | Dependency injection | service registration, lifetimes |
| `config/memory.yaml` | Memory persistence | store backend, session settings |
| `config/logging.yaml` | Logging configuration | level, format, timestamps |
| `config/quality.yaml` | Quality thresholds | coverage, complexity, line limits |
| `config/token_budget.yaml` | Token management | max_tokens, thresholds, auto_actions |
| `config/guidelines.yaml` | Guideline section mapping | 34 aliases to guideline files |
| `config/api.yaml` | HTTP API service | cors, rate_limit, docs |

### Data Files

| File | Purpose |
|------|---------|
| `src/sage/data/fallback_core.yaml` | Fallback content for graceful degradation |

---

## Configuration Sections

### 1. Timeout Configuration (`config/timeout.yaml`)

```yaml
timeout:
  global_max: 10s                      # T5: Absolute maximum
  default: 5s                          # T4: Default for most operations

  operations:
    cache_lookup: 100ms                # T1 - Cache hits
    file_read: 500ms                   # T2 - Single file operations
    layer_load: 2s                     # T3 - Layer/directory loading
    full_load: 5s                      # T4 - Complete KB load
    analysis: 10s                      # T5 - Complex analysis
    mcp_call: 10s                      # MCP tool timeout
    search: 3s                         # Search operations

  circuit_breaker:
    enabled: true
    failure_threshold: 3               # Open after 3 consecutive failures
    reset_timeout: 30s                 # Try again after 30 seconds
    half_open_requests: 1              # Test requests in half-open state

  fallback:
    strategy: graceful                 # graceful | strict | none
    cache_stale_ms: 60000              # Use stale cache up to 60 seconds
    timeout_short:
      action: return_partial
    timeout_long:
      action: return_core
    file_not_found:
      action: return_error
    parse_error:
      action: return_raw
    network_error:
      action: use_cache
```

### 2. Triggers Configuration (`config/triggers.yaml`)

```yaml
triggers:
  code:
    keywords:
      - code, implement, fix, refactor, debug, bug, function, class, method
      - 代码, 实现, 修复, 重构, 调试, 缺陷, 函数, 类, 方法
    load:
      - content/guidelines/code_style.md
      - content/guidelines/python.md
    timeout_ms: 2000
    priority: 1

  # Additional triggers: architecture, testing, ai_collaboration,
  # timeout, expert, analyze, documentation, python
```

### 3. Features Configuration (`config/features.yaml`)

```yaml
features:
  # Core Features
  event_driven_plugins: true           # Event-driven plugin architecture
  memory_persistence: true             # Cross-session memory persistence
  api_service: false                   # HTTP REST API service

  # Loading Optimization Features
  differential_loading: false          # Load only changed content
  compressed_loading: false            # Compressed/summarized content
  client_cache: true                   # Client-side caching
  lazy_expansion: true                 # Headers-only with expand-on-demand
  context_pruning: false               # Auto-remove irrelevant sections (v1.1+)
```

### 4. DI Container Configuration (`config/di.yaml`)

```yaml
di:
  auto_wire: true

  services:
    EventBus:
      lifetime: singleton
      implementation: AsyncEventBus

    SourceProtocol:
      lifetime: singleton
      implementation: TimeoutLoader
      config_key: plugins.loader

    MemoryStore:
      lifetime: singleton
      implementation: MemoryStore

    TokenBudget:
      lifetime: singleton
      implementation: TokenBudget

    # v1.1 Placeholders: KnowledgeProtocol, OutputProtocol, RefineProtocol
```

### 5. API Service Configuration (`config/api.yaml`)

```yaml
services:
  api:
    enabled: false
    host: "0.0.0.0"
    port: 8080
    cors:
      enabled: true
      origins: ["*"]
    docs:
      enabled: true
      path: /docs
    rate_limit:
      enabled: false
      requests_per_minute: 60
```

---

## Fallback Content (`src/sage/data/fallback_core.yaml`)

Emergency fallback content loaded when all else fails:

```yaml
fallback:
  core_principles: |
    # Core Principles (Fallback)
    ## Xin-Da-Ya (信达雅) Design Philosophy
    - **Xin (信)**: Faithfulness - accurate, reliable, testable
    - **Da (达)**: Clarity - clear, maintainable, structured
    - **Ya (雅)**: Elegance - refined, balanced, sustainable
    ...

  minimal_emergency: |
    Be accurate. Be clear. Be elegant.

  quick_reference: |
    **Philosophy**: 信达雅 - Faithful, Clear, Elegant
    **5 Questions**: Assumptions? Risks? Simpler? Maintainable? Big picture?
```

---

## Configuration Loading

### Python API

```python
from sage.core.config import load_config, get_config

# Load raw configuration dictionary
config_dict = load_config()

# Get typed configuration object
config = get_config()
print(config.timeouts.t1_instant)  # 100
print(config.logging.level)        # "INFO"
```

### Configuration Dataclasses

```python
@dataclass
class SAGEConfig:
    version: str
    knowledge_base: KnowledgeBaseConfig
    timeouts: TimeoutConfig
    cache: CacheConfig
    logging: LoggingConfig
    plugins: PluginConfig
    memory: MemoryConfig
    mcp: MCPConfig
    loading: dict[str, Any]
```

---

## Best Practices

### Do

- ✅ Use environment variables for deployment-specific settings
- ✅ Keep sensitive values out of config files
- ✅ Use modular config files for separation of concerns
- ✅ Provide sensible defaults for all settings
- ✅ Document configuration options with comments

### Don't

- ❌ Hardcode values that should be configurable
- ❌ Create circular dependencies between config files
- ❌ Override defaults without clear reason
- ❌ Put secrets in version-controlled config files

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `docs/design/04-timeout-loading.md` | Timeout hierarchy details |
| `docs/design/05-plugin-memory.md` | Plugin configuration |
| `content/frameworks/timeout/hierarchy.md` | Timeout framework reference |
| `content/core/defaults.md` | Default behavior documentation |

---

*Part of SAGE Knowledge Base v0.1.0 - Configuration Design*
