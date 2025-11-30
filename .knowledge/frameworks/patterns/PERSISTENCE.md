# Data Persistence Patterns

> Universal patterns for data lifecycle, retention, and cleanup

---

## Table of Contents

- [1. Data Lifecycle](#1-data-lifecycle)
- [2. Retention Strategies](#2-retention-strategies)
- [3. Priority Levels](#3-priority-levels)
- [4. Cleanup Patterns](#4-cleanup-patterns)
- [5. Implementation](#5-implementation)
- [6. Best Practices](#6-best-practices)

---

## 1. Data Lifecycle

| Phase       | Description       | Actions                  |
|-------------|-------------------|--------------------------|
| **Create**  | Initial storage   | Validate, store, index   |
| **Read**    | Data access       | Cache, query, return     |
| **Update**  | Modification      | Validate, version, store |
| **Archive** | Long-term storage | Compress, move, index    |
| **Delete**  | Removal           | Verify, remove, cleanup  |

---

## 2. Retention Strategies

### 2.1 Time-Based Retention

| Strategy       | Description       | Use Case      |
|----------------|-------------------|---------------|
| TTL            | Fixed lifetime    | Cache entries |
| Rolling window | Keep last N days  | Logs          |
| Tiered         | Hot → warm → cold | Analytics     |

### 2.2 Count-Based Retention

| Strategy       | Description           | Use Case |
|----------------|-----------------------|----------|
| Max entries    | Keep last N items     | History  |
| Max size       | Keep until size limit | Cache    |
| Priority-based | Keep high priority    | Memory   |

---

## 3. Priority Levels

| Priority  | Value | Retention          |
|-----------|-------|--------------------|
| EPHEMERAL | 10    | Discard first      |
| LOW       | 30    | Short retention    |
| NORMAL    | 50    | Standard retention |
| HIGH      | 70    | Extended retention |
| CRITICAL  | 90    | Long retention     |
| PERMANENT | 100   | Never discard      |

---

## 4. Cleanup Patterns

### 4.1 Cleanup Triggers

| Trigger     | When               | Action             |
|-------------|--------------------|--------------------|
| Time-based  | Scheduled          | Background cleanup |
| Threshold   | Limit reached      | Immediate cleanup  |
| On-demand   | Manual request     | Targeted cleanup   |
| Event-based | On specific events | Contextual cleanup |

### 4.2 Cleanup Strategies

| Strategy | Description           |
|----------|-----------------------|
| LRU      | Least recently used   |
| LFU      | Least frequently used |
| FIFO     | First in, first out   |
| Priority | Lowest priority first |

---

## 5. Caching Patterns

### 5.1 Cache Strategies

| Pattern       | Description        | Use Case           |
|---------------|--------------------|--------------------|
| Read-through  | Load on miss       | General caching    |
| Write-through | Write to both      | Consistency        |
| Write-behind  | Async write        | Performance        |
| Refresh-ahead | Preemptive refresh | Predictable access |

### 5.2 Cache Invalidation

| Strategy      | When                  |
|---------------|-----------------------|
| TTL expiry    | After fixed time      |
| Event-based   | On data change        |
| Manual        | Explicit invalidation |
| Version-based | On version mismatch   |

---

## 6. Implementation Example

```python
@dataclass
class RetentionPolicy:
    max_entries: int = 1000
    max_age_days: int = 30
    min_priority: int = 30  # LOW

def cleanup(store: DataStore, policy: RetentionPolicy):
    # Remove by age
    cutoff = datetime.now() - timedelta(days=policy.max_age_days)
    store.delete_before(cutoff)

    # Remove by priority if over limit
    if store.count() > policy.max_entries:
        store.delete_lowest_priority(
            count=store.count() - policy.max_entries,
            below_priority=policy.min_priority
        )
```
---

## Related

- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Timeout handling
- `.knowledge/practices/engineering/PATTERNS.md` — Engineering patterns

---

*AI Collaboration Knowledge Base*
