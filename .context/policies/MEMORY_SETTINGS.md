# Memory and Persistence Configuration

> Configuration reference for caching, memory management, and data persistence

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Cache Configuration](#2-cache-configuration)
- [3. Memory Management](#3-memory-management)
- [4. Persistence](#4-persistence)
- [5. Session State](#5-session-state)
- [6. Performance Tuning](#6-performance-tuning)

---

## 1. Overview

### 1.1 Memory Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Memory Layer                             │
├─────────────────┬─────────────────┬─────────────────────────┤
│   L1 Cache      │   L2 Cache      │    Persistence          │
│   (In-Memory)   │   (File/Redis)  │    (Disk/DB)            │
└────────┬────────┴────────┬────────┴────────────┬────────────┘
         │                 │                     │
         ▼                 ▼                     ▼
    Hot Data          Warm Data             Cold Data
    (< 100ms)         (< 500ms)             (< 2s)
```

### 1.2 Storage Hierarchy

| Layer           | Storage    | TTL       | Use Case            |
|:----------------|:-----------|:----------|:--------------------|
| **L1**          | In-memory  | Minutes   | Frequently accessed |
| **L2**          | File/Redis | Hours     | Recently accessed   |
| **Persistence** | Disk/DB    | Permanent | Historical data     |

---

## 2. Cache Configuration

### 2.1 Global Cache Settings

```yaml
# config/sage.yaml
memory:
  cache:
    # Enable/disable caching
    enabled: true

    # Default cache backend
    backend: memory         # memory | file | redis

    # Global TTL (seconds)
    default_ttl: 3600

    # Cache size limits
    max_items: 10000
    max_memory: 100MB

    # Eviction policy
    eviction: lru           # lru | lfu | fifo | ttl
```

### 2.2 Multi-Level Cache

```yaml
memory:
  cache:
    levels:
      # L1: In-memory cache
      l1:
        enabled: true
        backend: memory
        max_items: 1000
        max_memory: 50MB
        ttl: 300              # 5 minutes

      # L2: File-based cache
      l2:
        enabled: true
        backend: file
        path: .cache/l2/
        max_size: 500MB
        ttl: 3600             # 1 hour

      # L3: Redis cache (optional)
      l3:
        enabled: false
        backend: redis
        url: redis://localhost:6379/0
        ttl: 86400            # 24 hours
```

### 2.3 Cache Key Configuration

```yaml
memory:
  cache:
    keys:
      # Key generation
      hash_algorithm: xxhash   # xxhash | md5 | sha256
      include_version: true

      # Namespacing
      namespace: sage
      separator: ":"

      # Key patterns
      patterns:
        content: "{namespace}:content:{layer}:{path}"
        search: "{namespace}:search:{query_hash}"
        metadata: "{namespace}:meta:{file_hash}"
```

### 2.4 Cache Backends

#### Memory Backend

```yaml
memory:
  cache:
    backends:
      memory:
        implementation: dict    # dict | lru_cache
        thread_safe: true
        copy_on_read: false
```

#### File Backend

```yaml
memory:
  cache:
    backends:
      file:
        path: .cache/
        format: json           # json | pickle | msgpack
        compression: gzip      # none | gzip | lz4
        sync_writes: false
```

#### Redis Backend

```yaml
memory:
  cache:
    backends:
      redis:
        url: redis://localhost:6379/0
        password: ${REDIS_PASSWORD}
        pool_size: 10
        timeout: 5000
        retry:
          attempts: 3
          delay: 100
```

---

## 3. Memory Management

### 3.1 Memory Limits

```yaml
memory:
  limits:
    # Total memory budget
    max_total: 500MB

    # Per-component limits
    components:
      cache: 100MB
      content: 200MB
      search_index: 100MB
      session: 50MB

    # Warning thresholds
    warning_threshold: 80%    # Warn at 80% usage
    critical_threshold: 95%   # Take action at 95%
```

### 3.2 Memory Monitoring

```yaml
memory:
  monitoring:
    enabled: true
    interval: 60              # Check every 60 seconds

    # Metrics to collect
    metrics:
      - total_usage
      - component_usage
      - cache_hit_rate
      - eviction_count

    # Alerts
    alerts:
      high_memory:
        threshold: 80%
        action: warn
      critical_memory:
        threshold: 95%
        action: evict
```

### 3.3 Garbage Collection

```yaml
memory:
  gc:
    # Automatic cleanup
    auto_cleanup: true
    cleanup_interval: 300     # Every 5 minutes

    # Cleanup strategies
    strategies:
      - expired_entries
      - least_recently_used
      - oversized_entries

    # Cleanup thresholds
    trigger_threshold: 70%    # Start cleanup at 70%
    target_threshold: 50%     # Cleanup until 50%
```

---

## 4. Persistence

### 4.1 Persistence Configuration

```yaml
memory:
  persistence:
    # Enable persistence
    enabled: true

    # Storage path
    path: .data/

    # What to persist
    targets:
      - cache_state
      - search_index
      - session_state
      - metrics

    # Persistence mode
    mode: async              # sync | async | scheduled
```

### 4.2 Snapshot Configuration

```yaml
memory:
  persistence:
    snapshots:
      enabled: true

      # Snapshot schedule
      schedule:
        interval: 3600        # Every hour
        on_shutdown: true
        on_change_count: 1000 # After 1000 changes

      # Snapshot storage
      path: .data/snapshots/
      format: msgpack
      compression: lz4

      # Retention
      max_snapshots: 24       # Keep last 24
      retention_days: 7
```

### 4.3 Recovery Configuration

```yaml
memory:
  persistence:
    recovery:
      # Auto-recovery on startup
      auto_recover: true

      # Recovery source priority
      sources:
        - latest_snapshot
        - backup
        - rebuild

      # Recovery options
      options:
        validate_integrity: true
        skip_corrupted: true
        log_recovery: true
```

---

## 5. Session State

### 5.1 Session Configuration

```yaml
memory:
  session:
    # Session storage
    storage: memory          # memory | file | redis

    # Session TTL
    ttl: 3600                # 1 hour

    # Maximum sessions
    max_sessions: 100

    # Session data
    include:
      - context
      - history
      - preferences

    # Auto-save
    auto_save:
      enabled: true
      interval: 60           # Every minute
      on_change: true
```

### 5.2 Context Preservation

```yaml
memory:
  session:
    context:
      # What to preserve
      preserve:
        - current_layer
        - search_history
        - recent_files
        - user_preferences

      # Context limits
      max_history: 100
      max_recent_files: 50

      # Expiration
      history_ttl: 86400     # 24 hours
```

### 5.3 Session Persistence

```yaml
memory:
  session:
    persistence:
      enabled: true
      path: .history/current/
      format: yaml

      # What to persist
      on_exit:
        - active_sessions
        - context_state

      # Recovery
      restore_on_start: true
```

---

## 6. Performance Tuning

### 6.1 Cache Optimization

```yaml
memory:
  performance:
    cache:
      # Preloading
      preload:
        enabled: true
        layers:
          - core
          - guidelines

      # Prefetching
      prefetch:
        enabled: true
        depth: 2              # Prefetch related content

      # Warming
      warm_cache_on_start: true
      warm_cache_timeout: 5000
```

### 6.2 Memory Optimization

```yaml
memory:
  performance:
    optimization:
      # Content optimization
      lazy_loading: true
      streaming: true
      chunk_size: 10000       # bytes

      # Compression
      compress_cached: true
      compression_threshold: 1000  # bytes

      # Deduplication
      deduplicate: true
```

### 6.3 Timeout Configuration

Reference to timeout hierarchy:

| Operation        | Timeout | Related Setting                       |
|:-----------------|:--------|:--------------------------------------|
| L1 cache lookup  | 100ms   | `memory.cache.levels.l1.timeout`      |
| L2 cache lookup  | 500ms   | `memory.cache.levels.l2.timeout`      |
| Persistence read | 2000ms  | `memory.persistence.timeout`          |
| Full recovery    | 10000ms | `memory.persistence.recovery.timeout` |

---

## Quick Reference

### Environment Variables

```bash
# Cache settings
export SAGE_CACHE_ENABLED=true
export SAGE_CACHE_BACKEND=memory
export SAGE_CACHE_TTL=3600
export SAGE_CACHE_MAX_MEMORY=100MB

# Redis settings
export SAGE_REDIS_URL=redis://localhost:6379/0
export SAGE_REDIS_PASSWORD=secret

# Persistence
export SAGE_PERSISTENCE_ENABLED=true
export SAGE_PERSISTENCE_PATH=.data/

# Memory limits
export SAGE_MEMORY_MAX_TOTAL=500MB
```

### Cache Commands

```bash
# Cache operations
sage cache stats
sage cache clear
sage cache clear --layer core
sage cache warm

# Memory status
sage memory status
sage memory gc

# Persistence
sage snapshot create
sage snapshot list
sage snapshot restore <id>
```

### Configuration Validation

```bash
# Validate memory configuration
sage config --validate --section memory

# Show memory configuration
sage config --show --section memory.cache
```

---

## Related

- `.context/policies/timeout_hierarchy.md` — Timeout configuration
- `.context/policies/service_settings.md` — Service configuration
- `.context/policies/runtime_settings.md` — Runtime settings
- `.context/decisions/ADR_0003_TIMEOUT_HIERARCHY.md` — Timeout ADR

---

*AI Collaboration Knowledge Base*
