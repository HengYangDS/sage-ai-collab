# Timeout Hierarchy Framework

> Guarantee response times, prevent hangs, graceful degradation

---

## Table of Contents

[1. Five-Level Hierarchy](#1-five-level-hierarchy) · [2. Timeout Flow](#2-timeout-flow) · [3. Fallback Strategies](#3-fallback-strategies) · [4. Configuration](#4-configuration) · [5. Implementation Guidelines](#5-implementation-guidelines) · [6. Related Patterns](#6-related-patterns)

---

## 1. Five-Level Hierarchy

| Level  | Name    | Timeout | Scope        | Fallback        |
|--------|---------|---------|--------------|-----------------|
| **T1** | Cache   | 100ms   | Cache lookup | Skip cache      |
| **T2** | File    | 500ms   | Single file  | Use fallback    |
| **T3** | Layer   | 2s      | Full layer   | Partial load    |
| **T4** | Full    | 5s      | Complete KB  | Core only       |
| **T5** | Complex | 10s     | Analysis     | Abort + summary |

---

## 2. Timeout Flow

```
Request
    │
    ▼
┌─────────────┐
│ T1: Cache   │──timeout──▶ Skip, proceed
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ T2: File    │──timeout──▶ Use fallback
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ T3: Layer   │──timeout──▶ Return partial
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ T4: Full    │──timeout──▶ Core only
└──────┬──────┘
       │
       ▼
    Result
```

---

## 3. Fallback Strategies

| Situation        | Action                 |
|------------------|------------------------|
| Cache miss       | Proceed to file        |
| File timeout     | Use embedded fallback  |
| Layer timeout    | Return loaded portion  |
| Full timeout     | Return core principles |
| Analysis timeout | Return summary         |

---

## 4. Configuration

```yaml
timeout:
  operations:
    cache_lookup: 100ms    # T1
    file_read: 500ms       # T2
    layer_load: 2s         # T3
    full_load: 5s          # T4
    analysis: 10s          # T5

  fallback:
    strategy: graceful     # graceful | strict | none
    cache_stale_ms: 60000  # Use stale cache up to 60s
```

---

## 5. Implementation Guidelines

| Guideline            | Application           |
|----------------------|-----------------------|
| Always set timeouts  | Every external call   |
| Use appropriate tier | Match operation scope |
| Implement fallbacks  | Every timeout path    |
| Log timeouts         | For monitoring        |
| Test timeouts        | Include in test suite |

---

## 6. Related Patterns

For detailed implementation patterns, see `timeout_patterns.md`:

| Pattern             | Description               | Reference                                      |
|---------------------|---------------------------|------------------------------------------------|
| **Circuit Breaker** | Prevent cascade failures  | `timeout_patterns.md#4-circuit-breaker-pattern` |
| **Retry**           | Handle transient failures | `timeout_patterns.md#3-retry-pattern`           |
| **Bulkhead**        | Isolate failures          | `timeout_patterns.md#6-bulkhead-pattern`        |
| **Fallback**        | Provide alternatives      | `timeout_patterns.md#5-fallback-pattern`        |

---

**Golden Rule**: Always return something, never hang.

*Part of SAGE Knowledge Base*
