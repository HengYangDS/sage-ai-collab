---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~800
---

# Configuration Design

> Modular configuration system with smart loading and graceful degradation

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Configuration Priority](#2-configuration-priority)
- [3. Configuration Files](#3-configuration-files)
- [4. Key Configuration Sections](#4-key-configuration-sections)
- [5. Configuration Loading](#5-configuration-loading)
- [6. Best Practices](#6-best-practices)

---

## 1. Overview

SAGE uses a modular configuration system with `sage.yaml` as the main entry point.

### Design Principles

| Principle | Description |
|-----------|-------------|
| Single Source of Truth | Each setting defined in exactly one place |
| Sensible Defaults | Works out of the box without configuration |
| Progressive Override | Environment > sage.yaml > config/*.yaml > defaults |
| Fail-Safe Loading | Missing configs use defaults, never crash |

---

## 2. Configuration Priority

```
┌─────────────────────────────────────────────────────────┐
│ 1. Environment Variables (SAGE_*)                       │ ← Highest
├─────────────────────────────────────────────────────────┤
│ 2. Main Config (sage.yaml)                              │
├─────────────────────────────────────────────────────────┤
│ 3. Included Configs (config/*.yaml via includes)        │
├─────────────────────────────────────────────────────────┤
│ 4. Default Values (hardcoded in config.py)              │ ← Lowest
└─────────────────────────────────────────────────────────┘
```

### Environment Variable Format

| Pattern | Example |
|---------|---------|
| `SAGE_<SECTION>__<KEY>` | `SAGE_LOGGING__LEVEL=DEBUG` |
| Cache settings | `SAGE_CACHE__ENABLED=false` |
| Timeout settings | `SAGE_TIMEOUTS__T1_INSTANT=200` |

---

## 3. Configuration Files

### Directory Structure

```
config/
├── sage.yaml              # Main entry point
├── core/                  # Core system configs
│   ├── timeout.yaml       # Timeout hierarchy
│   ├── di.yaml            # Dependency injection
│   ├── memory.yaml        # Memory persistence
│   └── logging.yaml       # Logging settings
├── knowledge/             # Knowledge loading
│   ├── loading.yaml       # Smart loading
│   ├── triggers.yaml      # Keyword triggers
│   └── token_budget.yaml  # Token management
├── capabilities/          # Capability configs
│   ├── plugins.yaml       # Plugin settings
│   ├── features.yaml      # Feature flags
│   └── quality.yaml       # Quality thresholds
└── services/              # Service configs
    ├── api.yaml           # HTTP API
    ├── cli.yaml           # CLI settings
    └── mcp.yaml           # MCP server
```

### File Purposes

| File | Purpose | Key Settings |
|------|---------|--------------|
| `core/timeout.yaml` | Timeout hierarchy | T1-T5 levels, circuit breaker |
| `knowledge/loading.yaml` | Smart loading | always load, max_tokens |
| `knowledge/triggers.yaml` | Auto-load triggers | 9 keyword triggers |
| `capabilities/features.yaml` | Feature flags | optimization toggles |
| `services/mcp.yaml` | MCP server | host, port, timeout |

---

## 4. Key Configuration Sections

### 4.1 Timeout Configuration

| Level | Name | Default | Use Case |
|-------|------|---------|----------|
| T1 | Instant | 100ms | Cache lookup |
| T2 | Fast | 500ms | Single file |
| T3 | Standard | 2000ms | Layer load |
| T4 | Extended | 5000ms | Full KB |
| T5 | Maximum | 10000ms | Complex analysis |

### 4.2 Smart Loading Triggers

| Trigger | Keywords | Loaded Content |
|---------|----------|----------------|
| code | code, implement, fix, 代码 | code_style.md |
| architecture | architecture, design, 架构 | planning.md |
| testing | test, coverage, 测试 | engineering.md |
| documentation | doc, guide, 文档 | documentation.md |
| python | python, pip, 蟒蛇 | python.md |

### 4.3 Token Budget

| Setting | Default | Description |
|---------|---------|-------------|
| `max_tokens` | 4000 | Maximum tokens per request |
| `warning_threshold` | 0.7 | Warn at 70% usage |
| `critical_threshold` | 0.9 | Critical at 90% |
| `overflow_action` | prune | Action when exceeded |

### 4.4 Circuit Breaker

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | true | Enable circuit breaker |
| `failure_threshold` | 3 | Open after N failures |
| `reset_timeout_ms` | 30000 | Reset after 30s |
| `half_open_requests` | 1 | Test requests |

### 4.5 Feature Flags

| Feature | Default | Description |
|---------|---------|-------------|
| `smart_loading` | true | Keyword-triggered loading |
| `caching` | true | Response caching |
| `metrics` | true | Performance metrics |
| `plugins` | true | Plugin system |

---

## 5. Configuration Loading

### 5.1 Load Order

```python
# 1. Load defaults (hardcoded)
config = DEFAULT_CONFIG.copy()

# 2. Load config/*.yaml files
for file in config_dir.glob("**/*.yaml"):
    config.merge(load_yaml(file))

# 3. Load sage.yaml (main)
config.merge(load_yaml("sage.yaml"))

# 4. Apply environment overrides
config.apply_env_overrides()
```

### 5.2 Fallback Behavior

| Scenario | Action |
|----------|--------|
| Config file missing | Use defaults |
| Parse error | Log warning, use defaults |
| Invalid value | Log warning, use default for that key |
| Environment override | Always takes precedence |

### 5.3 Validation

```bash
sage config validate              # Validate all configs
sage config show                  # Show merged config
sage config show --section timeout  # Show specific section
```

---

## 6. Best Practices

### 6.1 Configuration Guidelines

| Practice | Description |
|----------|-------------|
| Use includes | Keep sage.yaml small, delegate to config/ |
| Environment for secrets | Never commit secrets in YAML |
| Document overrides | Comment non-default values |
| Test changes | Validate before deploying |

### 6.2 Common Overrides

```yaml
# sage.yaml - Common customizations
logging:
  level: DEBUG  # Override for development

timeout:
  operations:
    t3_standard: 3000  # Increase for slow systems

cache:
  enabled: false  # Disable for debugging
```

### 6.3 Environment-Specific

| Environment | Recommended Settings |
|-------------|---------------------|
| Development | `SAGE_LOGGING__LEVEL=DEBUG` |
| Testing | `SAGE_CACHE__ENABLED=false` |
| Production | Default values (optimized) |

---

## Related

- `docs/design/01b-configuration.md` — Configuration hierarchy details
- `docs/design/04-timeout-loading.md` — Timeout design
- `docs/guides/configuration.md` — Configuration user guide
- `config/sage.yaml` — Main configuration file

---

*Part of SAGE Knowledge Base*
