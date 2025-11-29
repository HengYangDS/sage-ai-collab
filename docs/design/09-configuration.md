# Configuration Design

> Modular configuration system with smart loading and graceful degradation

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Configuration Priority](#2-configuration-priority)
- [3. Configuration Files](#3-configuration-files)
- [4. Configuration Sections](#4-configuration-sections)
- [5. Fallback Content](#5-fallback-content)
- [6. Configuration Loading](#6-configuration-loading)
- [7. Best Practices](#7-best-practices)

---

## 1. Overview

SAGE uses a modular configuration system where settings are organized into focused YAML files in the `config/`
directory, with `sage.yaml` serving as the main entry point.

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

## 2. Configuration Priority

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

## 3. Configuration Files

### Main Entry Point

| File        | Purpose                                     |
|-------------|---------------------------------------------|
| `sage.yaml` | Main configuration, metadata, includes list |

### Modular Config Files

| File                                 | Purpose                             | Key Settings                           |
|--------------------------------------|-------------------------------------|----------------------------------------|
| `config/core/timeout.yaml`           | Timeout hierarchy & circuit breaker | operations, circuit_breaker, fallback  |
| `config/knowledge/loading.yaml`      | Smart loading configuration         | always, max_tokens, default_layers     |
| `config/knowledge/triggers.yaml`     | Keyword-triggered content loading   | 9 triggers with bilingual keywords     |
| `config/capabilities/plugins.yaml`   | Plugin configuration                | bundled plugins, cache settings        |
| `config/capabilities/features.yaml`  | Feature flags                       | optimization features, service toggles |
| `config/core/di.yaml`                | Dependency injection                | service registration, lifetimes        |
| `config/core/memory.yaml`            | Memory persistence                  | store backend, session settings        |
| `config/core/logging.yaml`           | Logging configuration               | level, format, timestamps              |
| `config/capabilities/quality.yaml`   | Quality thresholds                  | coverage, complexity, line limits      |
| `config/knowledge/token_budget.yaml` | Token management                    | max_tokens, thresholds, auto_actions   |
| `config/knowledge/guidelines.yaml`   | Guideline section mapping           | 34 aliases to guideline files          |
| `config/services/api.yaml`           | HTTP API service                    | cors, rate_limit, docs                 |

### Data Files

| File                               | Purpose                                   |
|------------------------------------|-------------------------------------------|
| `src/sage/data/fallback_core.yaml` | Fallback content for graceful degradation |

---

## 4. Configuration Sections

### 1. Timeout Configuration (`config/core/timeout.yaml`)

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

### 2. Triggers Configuration (`config/knowledge/triggers.yaml`)

```yaml
triggers:
  code:
    keywords:
      - code, implement, fix, refactor, debug, bug, function, class, method
      - 代码, 实现, 修复, 重构, 调试, 缺陷, 函数, 类, 方法
    load:
      - .knowledge/guidelines/code_style.md
      - .knowledge/guidelines/python.md
    timeout_ms: 2000
    priority: 1

  # Additional triggers: architecture, testing, ai_collaboration,
  # timeout, expert, analyze, documentation, python
```

### 3. Features Configuration (`config/capabilities/features.yaml`)

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
  context_pruning: false               # Auto-remove irrelevant sections (M2+)
```

### 4. DI Container Configuration (`config/core/di.yaml`)

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

    # M2 Placeholders: KnowledgeProtocol, OutputProtocol, RefineProtocol
```

### 5. API Service Configuration (`config/services/api.yaml`)

```yaml
services:
  api:
    enabled: false
    host: "0.0.0.0"
    port: 8080
    cors:
      enabled: true
      origins: [ "*" ]
    docs:
      enabled: true
      path: /docs
    rate_limit:
      enabled: false
      requests_per_minute: 60
```

### 6. Plugins Configuration (`config/capabilities/plugins.yaml`)

```yaml
plugins:
  loader:
    cache_enabled: true                # Master toggle for content caching
    cache_ttl: 300                     # Default TTL (5 minutes)

  bundled:
    content_cache:
      enabled: true
      max_entries: 1000
      max_size_bytes: 52428800         # 50MB
      ttl_seconds: 3600                # 1 hour

    semantic_search:
      enabled: true
      min_term_length: 2
      max_results: 20
      score_threshold: 0.1
```

### 7. Memory Configuration (`config/core/memory.yaml`)

```yaml
memory:
  store:
    backend: file                      # file | redis | sqlite
    path: .history/memory              # Storage location

  session:
    auto_checkpoint: true              # Auto-checkpoint on critical events
    checkpoint_interval: 300           # Every 5 minutes (seconds)
    max_history: 100                   # Max conversation entries
```

### 8. Token Budget Configuration (`config/knowledge/token_budget.yaml`)

```yaml
token_budget:
  max_tokens: 128000                   # Model context window
  reserved_tokens: 4000                # Reserved for response generation

  thresholds:
    warning: 0.70                      # 70% - CAUTION level
    caution: 0.80                      # 80% - WARNING level
    critical: 0.90                     # 90% - CRITICAL level
    overflow: 0.95                     # 95% - OVERFLOW level

  auto_actions:
    summarize: true                    # Auto-summarize at CRITICAL
    prune: true                        # Auto-prune at OVERFLOW
```

### 9. Loading Configuration (`config/knowledge/loading.yaml`)

```yaml
loading:
  max_tokens: 4000                     # Maximum tokens to load
  default_layers:
    - core                             # Always start with core

  always: # Always pre-cached
    - index.md
    - .knowledge/core/principles.md
    - .knowledge/core/quick_reference.md
```

### 10. Quality Configuration (`config/capabilities/quality.yaml`)

```yaml
quality:
  # Code quality thresholds
  min_test_coverage: 95
  max_function_lines: 50
  max_file_lines: 500
  max_complexity: 10

  # Code style thresholds
  max_line_length: 88
  min_type_hint_coverage: 50

  # Documentation thresholds
  max_doc_line_length: 120
```

### 11. Logging Configuration (`config/core/logging.yaml`)

```yaml
logging:
  level: INFO                          # DEBUG | INFO | WARNING | ERROR
  format: structured                   # structured | plain
  include_timestamps: true
```

### 12. Guidelines Configuration (`config/knowledge/guidelines.yaml`)

```yaml
guidelines:
  sections:
    # Maps aliases to guideline files in .knowledge/guidelines/
    quick_start: quick_start
    overview: quick_start
    planning: planning_design
    code_style: code_style
    code: code_style
    engineering: engineering
    documentation: documentation
    python: python
    ai_collaboration: ai_collaboration
    cognitive: cognitive
    quality: quality
    success: success
    # ... 34 total aliases
```

---

## 5. Fallback Content

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

## 6. Configuration Loading

### Python API

```python
from sage.core.config import load_config, get_config

# Load raw configuration dictionary
config_dict = load_config()

# Get typed configuration object
config = get_config()
print(config.timeouts.t1_instant)  # 100
print(config.logging.level)  # "INFO"
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

## 7. Best Practices

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

## Related

- `04-timeout-loading.md` — Timeout hierarchy details
- `05-plugin-memory.md` — Plugin configuration
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Timeout framework reference
- `.knowledge/core/defaults.md` — Default behavior documentation

---

*Part of SAGE Knowledge Base*
