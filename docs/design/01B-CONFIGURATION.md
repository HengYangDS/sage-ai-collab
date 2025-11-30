---
title: SAGE Knowledge Base - Configuration Design
version: "0.1.0"
last_updated: "2025-11-30"
status: production-ready
tokens: ~1200
---

# Configuration Design

> **Configuration hierarchy, timeout patterns, and YAML DSL**

---

## Table of Contents

- [1. Configuration Hierarchy](#1-configuration-hierarchy)
- [2. Timeout & Reliability](#2-timeout--reliability)
- [3. YAML Configuration DSL](#3-yaml-configuration-dsl)
- [4. DI Container Configuration](#4-di-container-configuration)

---

## 1. Configuration Hierarchy

### 1.1 Priority Order (Highest to Lowest)

```
┌───────────────────────────────────────────────────┐
│ 1. Environment Variables (SAGE_*)                 │ ← Highest
├───────────────────────────────────────────────────┤
│ 2. User Config (~/.config/sage/config.yaml)       │
├───────────────────────────────────────────────────┤
│ 3. Project Config (./sage.yaml)                   │
├───────────────────────────────────────────────────┤
│ 4. Package Defaults (built-in)                    │ ← Lowest
└───────────────────────────────────────────────────┘
```

### 1.2 Environment Variable Examples

```bash
# Override timeout settings
export SAGE_TIMEOUT_GLOBAL_MAX_MS=15000
export SAGE_TIMEOUT_DEFAULT_MS=8000

# Override logging
export SAGE_LOG_LEVEL=DEBUG
export SAGE_LOG_FORMAT=json

# Override loading behavior
export SAGE_LOADING_MAX_TOKENS=8000
export SAGE_LOADING_CACHE_ENABLED=false
```

---

## 2. Timeout & Reliability

> **Detailed Design**: See `docs/design/04-TIMEOUT-LOADING.md`
> **Philosophy**: "No operation should block indefinitely"

### 2.1 Five-Level Timeout Hierarchy

| Level  | Timeout | Scope            | Action on Timeout      | Use Case                     |
|--------|---------|------------------|------------------------|------------------------------|
| **T1** | 100ms   | Cache lookup     | Return cached/fallback | Memory cache, index lookup   |
| **T2** | 500ms   | Single file read | Use partial/fallback   | Individual markdown file     |
| **T3** | 2s      | Layer load       | Load partial + warning | `.knowledge/core/` directory |
| **T4** | 5s      | Full KB load     | Emergency core only    | All layers requested         |
| **T5** | 10s     | Complex analysis | Abort + summary        | Search, graph building       |

### 2.2 Graceful Degradation Strategy

```
Priority Order: Always return something (never empty response)

┌────────────────────────────────────────────────────┐
│ Level 1: Full Load (all requested layers)          │ ← Ideal
├────────────────────────────────────────────────────┤
│ Level 2: Partial Load (core + some requested)      │ ← Acceptable
├────────────────────────────────────────────────────┤
│ Level 3: Minimal Load (core only)                  │ ← Fallback
├────────────────────────────────────────────────────┤
│ Level 4: Emergency (hardcoded principles)          │ ← Last resort
└────────────────────────────────────────────────────┘

Key Principles:
1. Core principles ALWAYS available (pre-cached)
2. Partial results preferred over timeout error
3. Clear indication of incomplete load in response
```

### 2.3 Circuit Breaker Pattern

```yaml
# sage.yaml - Circuit Breaker Configuration
timeout:
  circuit_breaker:
    enabled: true
    failure_threshold: 3      # Open after 3 consecutive failures
    reset_timeout: 30s        # Try again after 30 seconds
    half_open_requests: 1     # Test requests in half-open state
```

**State Transitions:**

| Current State | Event             | Next State | Action                   |
|---------------|-------------------|------------|--------------------------|
| CLOSED        | failure_threshold | OPEN       | Start rejecting requests |
| OPEN          | reset_timeout     | HALF-OPEN  | Allow test request       |
| HALF-OPEN     | test_success      | CLOSED     | Resume normal operation  |
| HALF-OPEN     | test_failure      | OPEN       | Continue rejecting       |

---

## 3. YAML Configuration DSL

> **Central Configuration**: All behavior controlled via `sage.yaml`

### 3.1 Smart Loading Triggers

```yaml
# sage.yaml - Smart Loading with Keyword Triggers
loading:
  always:  # Always loaded (pre-cached)
    - INDEX.md
    - .knowledge/core/PRINCIPLES.md
    - .knowledge/core/QUICK_REFERENCE.md

triggers:
  code:
    keywords: [code, implement, fix, refactor, debug, 代码, 实现, 修复]
    load:
      - .knowledge/guidelines/CODE_STYLE.md
      - .knowledge/guidelines/PYTHON.md
    timeout_ms: 2000
    priority: 1

  architecture:
    keywords: [architecture, design, system, pattern, 架构, 设计, 系统]
    load:
      - .knowledge/guidelines/PLANNING_DESIGN.md
      - .knowledge/frameworks/decision/
    timeout_ms: 3000
    priority: 2

  testing:
    keywords: [test, coverage, unit, integration, 测试, 覆盖率]
    load:
      - .knowledge/guidelines/ENGINEERING.md
    timeout_ms: 2000
    priority: 3
```

### 3.2 Timeout Configuration

```yaml
# sage.yaml - Timeout Configuration
timeout:
  global_max: 10s                      # Absolute maximum
  default: 5s                          # Default if not specified

  operations:
    cache_lookup: 100ms                # T1
    file_read: 500ms                   # T2
    layer_load: 2s                     # T3
    full_load: 5s                      # T4
    analysis: 10s                      # T5

  strategies:
    on_timeout:
      - return_partial                 # Return what we have
      - use_fallback                   # Use cached/default content
      - log_warning                    # Log for monitoring
      - never_hang                     # Guarantee response
```

---

## 4. DI Container Configuration

### 4.1 Service Registration

```yaml
# sage.yaml - Dependency Injection Configuration
di:
  auto_wire: true                      # Auto-resolve from type hints

  services:
    EventBus:
      lifetime: singleton
      implementation: AsyncEventBus

    SourceProtocol:
      lifetime: singleton
      implementation: TimeoutLoader
      config_key: plugins.loader

    AnalyzeProtocol:
      lifetime: transient
      implementation: KnowledgeService

    GenerateProtocol:
      lifetime: scoped
      implementation: MultiChannelOutput
```

### 4.2 Lifetime Types

| Lifetime    | Description                         | Use Case                           |
|-------------|-------------------------------------|------------------------------------|
| `singleton` | One instance for entire application | EventBus, Config, Cache            |
| `transient` | New instance per resolution         | Request handlers, DTOs             |
| `scoped`    | One instance per scope (request)    | Database sessions, request context |

---

## Related

- `docs/design/01-ARCHITECTURE.md` — Main architecture design
- `docs/design/01A-INFRASTRUCTURE.md` — Infrastructure design
- `docs/design/01C-USAGE.md` — Usage patterns
- `docs/design/04-TIMEOUT-LOADING.md` — Detailed timeout design
- `docs/guides/CONFIGURATION.md` — Configuration guide

---

*Part of SAGE Knowledge Base*
