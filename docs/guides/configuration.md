---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~800
---

# Configuration Guide

> Complete reference for SAGE Knowledge Base configuration options

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Configuration Files](#2-configuration-files)
- [3. Core Settings](#3-core-settings)
- [4. Knowledge Settings](#4-knowledge-settings)
- [5. Environment Variables](#5-environment-variables)
- [6. Quick Reference](#6-quick-reference)

---

## 1. Overview

### 1.1 Configuration Philosophy

| Principle      | Description                          |
|----------------|--------------------------------------|
| **Modular**    | Split by concern into separate files |
| **Layered**    | Defaults → File → Environment        |
| **Validated**  | Schema-based validation              |
| **Documented** | Self-documenting with comments       |

### 1.2 Configuration Hierarchy

```
Priority (highest to lowest):
1. Environment variables (SAGE_*)
2. config/*.yaml files
3. Built-in defaults
```

### 1.3 Detailed Documentation

| Document                          | Content                              |
|-----------------------------------|--------------------------------------|
| `docs/design/01b-configuration.md`| Configuration design and YAML DSL    |
| `docs/design/04-timeout-loading.md`| Timeout configuration details       |
| `docs/design/09-configuration.md` | Full configuration reference         |

---

## 2. Configuration Files

### 2.1 Directory Structure

```
config/
├── sage.yaml              # Main config (optional override)
├── core/                  # Core system settings
│   ├── timeout.yaml       # Timeout configuration
│   ├── logging.yaml       # Logging configuration
│   └── di.yaml            # Dependency injection
├── knowledge/             # Knowledge base settings
│   ├── loading.yaml       # Loading configuration
│   ├── triggers.yaml      # Auto-load triggers
│   └── token_budget.yaml  # Token limits
├── services/              # Service configurations
│   ├── cli.yaml           # CLI settings
│   ├── mcp.yaml           # MCP server settings
│   └── api.yaml           # API settings
└── environments/          # Environment-specific
    ├── development.yaml
    ├── testing.yaml
    └── production.yaml
```

### 2.2 Main Configuration (sage.yaml)

```yaml
# sage.yaml - Main configuration file
project:
  name: "my-project"
  version: "1.0.0"

# Include other configs (optional)
includes:
  - core/timeout.yaml
  - knowledge/loading.yaml

# Override specific values
timeout:
  default_ms: 5000

knowledge:
  content_path: "./.knowledge"
```

---

## 3. Core Settings

### 3.1 Timeout Configuration

```yaml
# config/core/timeout.yaml
timeout:
  global_max: 10s
  default: 5s
  
  operations:
    cache_lookup: 100ms    # T1
    file_read: 500ms       # T2
    layer_load: 2s         # T3
    full_load: 5s          # T4
    analysis: 10s          # T5
```

### 3.2 Logging Configuration

```yaml
# config/core/logging.yaml
logging:
  level: INFO              # DEBUG, INFO, WARNING, ERROR
  format: console          # console or json
  output:
    - console
    - file: .logs/sage.log
```

### 3.3 Circuit Breaker

```yaml
# config/core/timeout.yaml
circuit_breaker:
  enabled: true
  failure_threshold: 3
  reset_timeout: 30s
  half_open_requests: 1
```

---

## 4. Knowledge Settings

### 4.1 Loading Configuration

```yaml
# config/knowledge/loading.yaml
loading:
  always:                  # Always loaded (pre-cached)
    - index.md
    - .knowledge/core/principles.md
    - .knowledge/core/quick_reference.md
  
  max_tokens: 8000
  cache_enabled: true
  cache_ttl: 300s
```

### 4.2 Smart Loading Triggers

```yaml
# config/knowledge/triggers.yaml
triggers:
  code:
    keywords: [code, implement, fix, refactor, debug]
    load:
      - .knowledge/guidelines/code_style.md
      - .knowledge/guidelines/python.md
    timeout_ms: 2000
    priority: 1

  architecture:
    keywords: [architecture, design, system, pattern]
    load:
      - .knowledge/guidelines/planning_design.md
      - .knowledge/frameworks/decision/
    timeout_ms: 3000
    priority: 2
```

### 4.3 Token Budget

```yaml
# config/knowledge/token_budget.yaml
token_budget:
  total: 8000
  allocation:
    core: 500              # Always loaded
    guidelines: 1200       # On-demand
    frameworks: 2000       # On-demand
    practices: 1500        # On-demand
    context: 1000          # Conversation
    memory: 500            # Cross-task
```

---

## 5. Environment Variables

### 5.1 Common Variables

| Variable                    | Description              | Default            |
|-----------------------------|--------------------------|--------------------|
| `SAGE_CONFIG`               | Config file path         | `config/sage.yaml` |
| `SAGE_LOG_LEVEL`            | Logging level            | `INFO`             |
| `SAGE_LOG_FORMAT`           | Log format               | `console`          |
| `SAGE_TIMEOUT_DEFAULT_MS`   | Default timeout          | `5000`             |
| `SAGE_LOADING_MAX_TOKENS`   | Max tokens to load       | `8000`             |
| `SAGE_CACHE_ENABLED`        | Enable caching           | `true`             |

### 5.2 Override Examples

```bash
# Override timeout settings
export SAGE_TIMEOUT_DEFAULT_MS=8000
export SAGE_TIMEOUT_GLOBAL_MAX_MS=15000

# Override logging
export SAGE_LOG_LEVEL=DEBUG
export SAGE_LOG_FORMAT=json

# Override loading behavior
export SAGE_LOADING_MAX_TOKENS=10000
export SAGE_CACHE_ENABLED=false
```

---

## 6. Quick Reference

### 6.1 Timeout Levels

| Level | Default | Config Key           | Use Case               |
|-------|---------|----------------------|------------------------|
| T1    | 100ms   | `timeout.operations.cache_lookup` | Cache lookup  |
| T2    | 500ms   | `timeout.operations.file_read`    | Single file   |
| T3    | 2s      | `timeout.operations.layer_load`   | Layer load    |
| T4    | 5s      | `timeout.operations.full_load`    | Full KB       |
| T5    | 10s     | `timeout.operations.analysis`     | Analysis      |

### 6.2 Layer Token Budgets

| Layer      | Default Budget | Config Key                    |
|------------|----------------|-------------------------------|
| core       | 500            | `token_budget.allocation.core`|
| guidelines | 1200           | `token_budget.allocation.guidelines` |
| frameworks | 2000           | `token_budget.allocation.frameworks` |
| practices  | 1500           | `token_budget.allocation.practices`  |

### 6.3 Common Configuration Tasks

| Task                      | Configuration                           |
|---------------------------|-----------------------------------------|
| Increase timeout          | `timeout.default: 8s`                   |
| Enable debug logging      | `logging.level: DEBUG`                  |
| Disable cache             | `loading.cache_enabled: false`          |
| Add custom trigger        | Add entry to `triggers` section         |
| Change token budget       | Modify `token_budget.allocation`        |

---

## Related

- `docs/design/01b-configuration.md` — Configuration design
- `docs/design/04-timeout-loading.md` — Timeout patterns
- `docs/design/09-configuration.md` — Full configuration reference
- `docs/guides/quickstart.md` — Getting started guide
- `config/sage.yaml` — Main configuration file

---

*Part of SAGE Knowledge Base*
