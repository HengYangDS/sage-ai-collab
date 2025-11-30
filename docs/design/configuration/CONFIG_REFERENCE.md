# Configuration Reference

> Complete reference for all SAGE configuration options

---

## 1. Overview

This document provides a comprehensive reference for all configuration options available in SAGE.

---

## 2. Knowledge Configuration

### 2.1 sage.knowledge

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `layers` | list | See below | Knowledge layer paths |
| `token_budget` | int | 6000 | Total token budget |
| `default_layer` | int | 1 | Default layer to query |
| `cache_enabled` | bool | true | Enable content caching |

```yaml
sage:
  knowledge:
    layers:
      - .knowledge
      - .context
      - .junie
      - docs
    token_budget: 6000
    default_layer: 1
    cache_enabled: true
```

---

## 3. Timeout Configuration

### 3.1 sage.timeout

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `default_ms` | int | 5000 | Default timeout |
| `max_ms` | int | 30000 | Maximum allowed timeout |
| `warning_threshold` | float | 0.8 | Warn at this % of timeout |
| `circuit_breaker` | object | — | Circuit breaker settings |

```yaml
sage:
  timeout:
    default_ms: 5000
    max_ms: 30000
    warning_threshold: 0.8
    circuit_breaker:
      enabled: true
      failure_threshold: 5
      reset_timeout_ms: 60000
```

---

## 4. Services Configuration

### 4.1 sage.services.cli

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `format` | string | rich | Output format (rich/json/md) |
| `color` | bool | true | Enable colors |
| `pager` | bool | true | Use pager for long output |

```yaml
sage:
  services:
    cli:
      format: rich
      color: true
      pager: true
```

### 4.2 sage.services.mcp

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `transport` | string | stdio | Transport (stdio/sse) |
| `timeout_ms` | int | 5000 | Tool timeout |
| `max_results` | int | 100 | Max search results |

```yaml
sage:
  services:
    mcp:
      transport: stdio
      timeout_ms: 5000
      max_results: 100
```

### 4.3 sage.services.api

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `host` | string | 0.0.0.0 | Bind host |
| `port` | int | 8080 | Bind port |
| `workers` | int | 1 | Worker processes |
| `cors_origins` | list | [] | Allowed CORS origins |

```yaml
sage:
  services:
    api:
      host: "0.0.0.0"
      port: 8080
      workers: 4
      cors_origins:
        - "http://localhost:3000"
```

---

## 5. Plugin Configuration

### 5.1 sage.plugins

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | bool | true | Enable plugin system |
| `paths` | list | [] | Additional plugin paths |
| `auto_discover` | bool | true | Auto-discover plugins |

```yaml
sage:
  plugins:
    enabled: true
    paths:
      - ./plugins
      - ~/.sage/plugins
    auto_discover: true
    disabled:
      - plugin_name
```

---

## 6. Logging Configuration

### 6.1 sage.logging

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `level` | string | info | Log level |
| `format` | string | text | Format (text/json) |
| `file` | string | null | Log file path |

```yaml
sage:
  logging:
    level: info
    format: text
    file: ~/.sage/logs/sage.log
    rotation:
      max_size_mb: 10
      backup_count: 5
```

---

## 7. Session Configuration

### 7.1 sage.session

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `idle_timeout_min` | int | 30 | Idle timeout minutes |
| `max_duration_hours` | int | 8 | Max session hours |
| `resume_enabled` | bool | true | Enable session resume |

```yaml
sage:
  session:
    idle_timeout_min: 30
    max_duration_hours: 8
    resume_enabled: true
    max_per_user: 3
```

---

## 8. Persistence Configuration

### 8.1 sage.persistence

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `store` | string | sqlite | Storage backend |
| `path` | string | ~/.sage | Data directory |

```yaml
sage:
  persistence:
    store: sqlite
    path: ~/.sage/data
    sqlite:
      database: sage.db
    backup:
      enabled: true
      interval: daily
```

---

## 9. Capabilities Configuration

### 9.1 sage.capabilities

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | list | all | Enabled capability families |

```yaml
sage:
  capabilities:
    enabled:
      - analyzers
      - checkers
      - monitors
    analyzers:
      content_parser:
        max_depth: 6
    checkers:
      link_checker:
        timeout_ms: 3000
```

---

## 10. Scenarios Configuration

### 10.1 sage.scenarios

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `default` | string | null | Default scenario |
| `paths` | list | [] | Scenario definition paths |

```yaml
sage:
  scenarios:
    default: python_backend
    paths:
      - .knowledge/scenarios
    python_backend:
      preload:
        - .knowledge/guidelines/PYTHON.md
      token_budget: 2000
```

---

## 11. Environment Variables

| Variable | Config Path | Example |
|----------|-------------|---------|
| `SAGE_ENV` | — | production |
| `SAGE_TIMEOUT_DEFAULT_MS` | timeout.default_ms | 10000 |
| `SAGE_SERVICES_API_PORT` | services.api.port | 8080 |
| `SAGE_LOGGING_LEVEL` | logging.level | debug |
| `SAGE_KNOWLEDGE_TOKEN_BUDGET` | knowledge.token_budget | 8000 |

---

## 12. Quick Reference

```yaml
# Minimal configuration
sage:
  knowledge:
    token_budget: 6000
  timeout:
    default_ms: 5000
  services:
    cli:
      format: rich

# Production configuration
sage:
  timeout:
    default_ms: 10000
  services:
    api:
      port: 443
      workers: 4
  logging:
    level: warning
```

---

## Related

- `CONFIG_HIERARCHY.md` — Configuration levels
- `YAML_DSL.md` — Configuration DSL
- `../core_engine/BOOTSTRAP.md` — Startup configuration

---

*Part of SAGE Knowledge Base*
