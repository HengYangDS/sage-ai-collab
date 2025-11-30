---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---
# SAGE Runtime Settings

> Runtime configuration, logging, and environment settings

---

## Table of Contents

- [1. Environment Variables](#1-environment-variables)
- [2. Logging Configuration](#2-logging-configuration)
- [3. Service Settings](#3-service-settings)
- [4. Feature Flags](#4-feature-flags)
- [5. Debug Settings](#5-debug-settings)

---

## 1. Environment Variables

### 1.1 Core Environment Variables

| Variable           | Default       | Description                          |
|:-------------------|:--------------|:-------------------------------------|
| `SAGE_CONFIG_PATH` | `./sage.yaml` | Path to main config file             |
| `SAGE_ENV`         | `production`  | Environment (development/production) |
| `SAGE_DEBUG`       | `false`       | Enable debug mode                    |
| `SAGE_LOG_LEVEL`   | `INFO`        | Logging level                        |

### 1.2 Override Pattern

Environment variables use double underscore (`__`) for nested keys:

```bash
# Pattern: SAGE__SECTION__KEY=value

# Override timeout.cache_lookup
export SAGE__TIMEOUT__CACHE_LOOKUP=200

# Override logging.level
export SAGE__LOGGING__LEVEL=DEBUG

# Override knowledge.base_path
export SAGE__KNOWLEDGE__BASE_PATH=/custom/path
```

### 1.3 Boolean Values

```bash
# True values: true, 1, yes, on
export SAGE__FEATURES__ENABLE_CACHING=true

# False values: false, 0, no, off
export SAGE__FEATURES__ENABLE_METRICS=false
```

### 1.4 List Values

```bash
# Comma-separated for simple lists
export SAGE__LOADING__HYBRID__EAGER_LAYERS=core,frameworks
```

---

## 2. Logging Configuration

### 2.1 Logging Levels

| Level      | Value | Use Case                        |
|:-----------|:------|:--------------------------------|
| `DEBUG`    | 10    | Detailed debugging information  |
| `INFO`     | 20    | General operational information |
| `WARNING`  | 30    | Warning messages                |
| `ERROR`    | 40    | Error conditions                |
| `CRITICAL` | 50    | Critical failures               |

### 2.2 Logging Configuration

```yaml
# sage.yaml
logging:
  level: INFO
  format: json              # json | text | rich
  output: stderr            # stderr | stdout | file
  
  # File output settings
  file:
    path: .logs/sage.log
    max_size_mb: 10
    backup_count: 5
    rotation: daily         # daily | size | none
  
  # Structured logging fields
  include:
    timestamp: true
    level: true
    logger: true
    request_id: true
  
  # Module-specific levels
  modules:
    sage.core: DEBUG
    sage.services: INFO
    sage.capabilities: INFO
```

### 2.3 Log Format Examples

**JSON Format** (default for production):

```json
{
  "timestamp": "2025-11-29T10:30:00.123Z",
  "level": "INFO",
  "logger": "sage.core.loader",
  "message": "Knowledge loaded",
  "layer": "core",
  "count": 42,
  "duration_ms": 150
}
```

**Text Format** (development):

```
2025-11-29 10:30:00.123 INFO  [sage.core.loader] Knowledge loaded layer=core count=42 duration_ms=150
```

**Rich Format** (CLI development):

```
10:30:00 │ INFO  │ Knowledge loaded                    │ layer=core count=42
```

### 2.4 Environment Override

```bash
# Set log level
export SAGE__LOGGING__LEVEL=DEBUG

# Set format
export SAGE__LOGGING__FORMAT=text

# Enable file logging
export SAGE__LOGGING__OUTPUT=file
export SAGE__LOGGING__FILE__PATH=/var/log/sage.log
```

---

## 3. Service Settings

### 3.1 CLI Service

```yaml
# config/services/cli.yaml
cli:
  colors: auto              # auto | always | never
  progress_bar: true
  table_format: rich        # rich | simple | markdown
  pager: auto               # auto | always | never
  
  # Output settings
  output:
    default_format: text    # text | json | yaml
    max_width: 120
    truncate_long: true
```

### 3.2 MCP Service

```yaml
# config/services/mcp.yaml
mcp:
  server:
    name: sage-kb
    version: "0.1.0"
  
  # Tool settings
  tools:
    enabled:
      - get_knowledge
      - search_knowledge
      - kb_info
      - get_framework
    
    # Rate limiting
    rate_limit:
      requests_per_minute: 60
      burst: 10
  
  # Response settings
  response:
    max_tokens: 4000
    include_sources: true
```

### 3.3 API Service

```yaml
# config/services/api.yaml
api:
  host: 0.0.0.0
  port: 8000
  
  # CORS settings
  cors:
    enabled: true
    origins:
      - "*"
    methods:
      - GET
      - POST
    headers:
      - "*"
  
  # Rate limiting
  rate_limit:
    enabled: true
    requests_per_minute: 100
  
  # Response settings
  response:
    pretty_json: false
    include_timing: true
```

### 3.4 Service Environment Variables

```bash
# CLI
export SAGE__CLI__COLORS=never

# MCP
export SAGE__MCP__SERVER__NAME=custom-kb

# API
export SAGE__API__PORT=9000
export SAGE__API__HOST=127.0.0.1
```

---

## 4. Feature Flags

### 4.1 Feature Configuration

```yaml
# sage.yaml
features:
  # Caching
  enable_caching: true
  cache_warming: false
  
  # Metrics and monitoring
  enable_metrics: true
  enable_tracing: false
  
  # Experimental features
  experimental:
    smart_loading: true
    ai_suggestions: false
    
  # Development features
  development:
    hot_reload: false
    mock_services: false
```

### 4.2 Feature Flag Usage

```python
from sage.core.config import get_config

config = get_config()

if config.features.enable_caching:
    result = await cache.get(key)
    if result is None:
        result = await compute(key)
        await cache.set(key, result)
else:
    result = await compute(key)
```

### 4.3 Environment Override

```bash
# Disable caching
export SAGE__FEATURES__ENABLE_CACHING=false

# Enable experimental feature
export SAGE__FEATURES__EXPERIMENTAL__AI_SUGGESTIONS=true
```

---

## 5. Debug Settings

### 5.1 Debug Configuration

```yaml
# sage.yaml
debug:
  enabled: false
  
  # Verbose output
  verbose:
    config_loading: false
    event_bus: false
    di_container: false
    timeout_manager: false
  
  # Profiling
  profiling:
    enabled: false
    output: .outputs/profile.json
  
  # Request tracing
  tracing:
    enabled: false
    sample_rate: 0.1        # 10% of requests
```

### 5.2 Development Mode

```yaml
# sage.yaml (development)
debug:
  enabled: true
  
  # Auto-reload on file changes
  hot_reload:
    enabled: true
    watch_paths:
      - .knowledge/
      - config/
    debounce_ms: 500
  
  # Mock external services
  mocks:
    enabled: false
    services:
      - external_api
```

### 5.3 Debug Environment Variables

```bash
# Enable full debug mode
export SAGE_DEBUG=true
export SAGE__DEBUG__ENABLED=true

# Enable specific verbose logging
export SAGE__DEBUG__VERBOSE__EVENT_BUS=true

# Enable profiling
export SAGE__DEBUG__PROFILING__ENABLED=true
```

---

## 6. Performance Tuning

### 6.1 Memory Settings

```yaml
# sage.yaml
performance:
  memory:
    max_heap_mb: 512
    gc_threshold: 0.8       # Trigger GC at 80% usage
    
  # Connection pools
  pools:
    default_size: 10
    max_size: 50
    timeout_ms: 5000
```

### 6.2 Concurrency Settings

```yaml
# sage.yaml
performance:
  concurrency:
    max_workers: 4
    thread_pool_size: 10
    async_pool_size: 100
```

### 6.3 Environment Override

```bash
# Memory settings
export SAGE__PERFORMANCE__MEMORY__MAX_HEAP_MB=1024

# Concurrency
export SAGE__PERFORMANCE__CONCURRENCY__MAX_WORKERS=8
```

---

## 7. Quick Reference

### 7.1 Essential Environment Variables

```bash
# Core settings
export SAGE_ENV=development
export SAGE_DEBUG=true
export SAGE_LOG_LEVEL=DEBUG
export SAGE_CONFIG_PATH=./sage.yaml

# Override specific settings
export SAGE__TIMEOUT__CACHE_LOOKUP=200
export SAGE__FEATURES__ENABLE_CACHING=true
export SAGE__LOGGING__FORMAT=text
```

### 7.2 Production Recommendations

```yaml
# sage.yaml (production)
logging:
  level: INFO
  format: json
  output: file

features:
  enable_caching: true
  enable_metrics: true

debug:
  enabled: false

performance:
  concurrency:
    max_workers: 8
```

### 7.3 Development Recommendations

```yaml
# sage.yaml (development)
logging:
  level: DEBUG
  format: rich
  output: stderr

features:
  enable_caching: false

debug:
  enabled: true
  hot_reload:
    enabled: true
```

---

## Related

- `.context/policies/timeout_hierarchy.md` — Timeout configuration
- `.context/policies/loading_configurations.md` — Loading configuration
- `.context/decisions/ADR-0007-configuration.md` — Configuration design decision
- `docs/design/09-configuration.md` — Full configuration design

---

*Part of SAGE Knowledge Base - Project Configuration*
