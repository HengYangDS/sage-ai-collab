# SAGE Loading Configurations

> Knowledge Base loading strategies and layer configuration

---

## Table of Contents

- [1. Loading Strategies](#1-loading-strategies)
- [2. Layer Configuration](#2-layer-configuration)
- [3. Trigger Conditions](#3-trigger-conditions)
- [4. Smart Loading](#4-smart-loading)
- [5. Configuration Reference](#5-configuration-reference)

---

## 1. Loading Strategies

### 1.1 Strategy Overview

| Strategy      | Description                 | Use Case                     |
|:--------------|:----------------------------|:-----------------------------|
| **eager**     | Load all content at startup | Small KB, fast access needed |
| **lazy**      | Load on first access        | Large KB, memory constrained |
| **on-demand** | Load specific items only    | Very large KB, selective use |
| **hybrid**    | Core eager, rest lazy       | Balanced approach (default)  |

### 1.2 Strategy Selection

```yaml
# sage.yaml
loading:
  strategy: hybrid    # eager | lazy | on-demand | hybrid
  
  # Hybrid strategy configuration
  hybrid:
    eager_layers:
      - core
    lazy_layers:
      - frameworks
      - practices
      - scenarios
```

### 1.3 Strategy Comparison

| Aspect       | Eager | Lazy   | On-Demand | Hybrid |
|:-------------|:------|:-------|:----------|:-------|
| Startup time | Slow  | Fast   | Fast      | Medium |
| First access | Fast  | Slow   | Slow      | Mixed  |
| Memory usage | High  | Low    | Lowest    | Medium |
| Complexity   | Low   | Medium | High      | Medium |

---

## 2. Layer Configuration

### 2.1 Knowledge Layers

SAGE organizes knowledge into hierarchical layers:

```
┌─────────────────────────────────────────────────────────┐
│                     core (Priority 1)                   │
│              Fundamental principles                     │
├─────────────────────────────────────────────────────────┤
│                  frameworks (Priority 2)                │
│            Conceptual frameworks & patterns             │
├─────────────────────────────────────────────────────────┤
│                  practices (Priority 3)                 │
│              Best practices & guidelines                │
├─────────────────────────────────────────────────────────┤
│                  scenarios (Priority 4)                 │
│             Domain-specific scenarios                   │
├─────────────────────────────────────────────────────────┤
│                  templates (Priority 5)                 │
│              Document templates                         │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Layer Configuration

```yaml
# sage.yaml
knowledge:
  base_path: .knowledge/
  
  layers:
    - name: core
      path: core/
      priority: 1
      load_strategy: eager
      cache_ttl: 3600        # 1 hour
      
    - name: frameworks
      path: frameworks/
      priority: 2
      load_strategy: lazy
      subdirectories:
        - autonomy
        - cognitive
        - design
        - patterns
        - resilience
      
    - name: practices
      path: practices/
      priority: 3
      load_strategy: lazy
      subdirectories:
        - ai_collaboration
        - decisions
        - documentation
        - engineering
      
    - name: scenarios
      path: scenarios/
      priority: 4
      load_strategy: on-demand
      
    - name: templates
      path: templates/
      priority: 5
      load_strategy: on-demand
```

### 2.3 Priority Rules

1. Lower priority number = higher importance
2. Higher priority layers loaded first in hybrid mode
3. Fallback uses highest priority available content
4. Search results ordered by priority

---

## 3. Trigger Conditions

### 3.1 Load Triggers

| Trigger        | Description               | Example            |
|:---------------|:--------------------------|:-------------------|
| `startup`      | Load at application start | Core layer         |
| `first_access` | Load on first request     | Lazy layers        |
| `explicit`     | Load only when requested  | On-demand          |
| `scheduled`    | Load at specific times    | Background refresh |

### 3.2 Trigger Configuration

```yaml
# sage.yaml
loading:
  triggers:
    startup:
      layers:
        - core
      timeout: 5s
    
    first_access:
      layers:
        - frameworks
        - practices
      preload_related: true
    
    scheduled:
      enabled: false
      interval: 3600        # 1 hour
      layers:
        - core
```

### 3.3 Context-Based Loading

```yaml
# sage.yaml
loading:
  context_triggers:
    # Load Python scenarios when Python detected
    python_detected:
      condition: "file_extension == '.py'"
      layers:
        - scenarios/python_backend
    
    # Load decision content when ADR mentioned
    adr_mentioned:
      condition: "'ADR' in query"
      layers:
        - practices/decisions
```

---

## 4. Smart Loading

### 4.1 Intelligent Preloading

```yaml
# sage.yaml
loading:
  smart:
    enabled: true
    
    # Preload related content
    preload_related: true
    preload_depth: 1          # How many levels of related content
    
    # Usage-based optimization
    track_usage: true
    popular_threshold: 10     # Access count to mark as popular
    preload_popular: true
```

### 4.2 Cache Configuration

```yaml
# sage.yaml
cache:
  enabled: true
  backend: memory            # memory | file | redis
  
  ttl:
    default: 1800            # 30 minutes
    core: 3600               # 1 hour for core
    hot: 300                 # 5 minutes for frequently accessed
  
  size:
    max_items: 1000
    max_memory_mb: 100
  
  invalidation:
    on_file_change: true
    check_interval: 60       # seconds
```

### 4.3 Preloading Patterns

```yaml
# sage.yaml
loading:
  preload:
    # Preload based on current context
    context_aware:
      enabled: true
      max_items: 10
    
    # Preload frequently used together
    co_occurrence:
      enabled: true
      min_correlation: 0.5
    
    # Preload based on navigation patterns
    navigation:
      enabled: true
      predict_depth: 2
```

---

## 5. Configuration Reference

### 5.1 Full Loading Configuration

```yaml
# sage.yaml - Complete loading configuration
loading:
  # Main strategy
  strategy: hybrid
  
  # Hybrid mode settings
  hybrid:
    eager_layers:
      - core
    lazy_layers:
      - frameworks
      - practices
    on_demand_layers:
      - scenarios
      - templates
  
  # Timeout settings (defer to timeout_hierarchy.md)
  timeouts:
    layer_load: 2s           # T3
    full_load: 5s            # T4
  
  # Fallback behavior
  fallback:
    on_timeout: partial      # partial | core_only | error
    on_error: skip           # skip | retry | error
    max_retries: 2
  
  # Performance tuning
  performance:
    parallel_loads: 4        # Concurrent layer loads
    batch_size: 50           # Files per batch
    memory_limit_mb: 200     # Max memory for loading

# Knowledge layers
knowledge:
  base_path: .knowledge/
  index_file: index.md
  
  layers:
    - name: core
      path: core/
      priority: 1
      load_strategy: eager
    
    - name: frameworks
      path: frameworks/
      priority: 2
      load_strategy: lazy
    
    - name: practices
      path: practices/
      priority: 3
      load_strategy: lazy
    
    - name: scenarios
      path: scenarios/
      priority: 4
      load_strategy: on-demand
    
    - name: templates
      path: templates/
      priority: 5
      load_strategy: on-demand

# Cache settings
cache:
  enabled: true
  backend: memory
  ttl:
    default: 1800
  size:
    max_items: 1000
```

### 5.2 Environment Variable Overrides

```bash
# Override loading strategy
export SAGE__LOADING__STRATEGY=eager

# Override cache TTL
export SAGE__CACHE__TTL__DEFAULT=3600

# Disable cache
export SAGE__CACHE__ENABLED=false
```

### 5.3 Default Values

| Setting                       | Default   | Description          |
|:------------------------------|:----------|:---------------------|
| `loading.strategy`            | `hybrid`  | Loading strategy     |
| `loading.timeouts.layer_load` | `2s`      | Layer load timeout   |
| `loading.fallback.on_timeout` | `partial` | Timeout behavior     |
| `cache.enabled`               | `true`    | Enable caching       |
| `cache.ttl.default`           | `1800`    | Default TTL (30 min) |

---

## Related

- `.context/policies/timeout_hierarchy.md` — Timeout configuration
- `.context/policies/runtime_settings.md` — Runtime settings
- `.context/decisions/ADR_0003_TIMEOUT_HIERARCHY.md` — Timeout design decision
- `docs/design/04-timeout-loading.md` — Full loading design

---

*AI Collaboration Knowledge Base*
