# Timeout Hierarchy Framework

> Guarantee response times, prevent hangs, graceful degradation

---

## 1. Five-Level Hierarchy

| Level | Name | Timeout | Scope | Fallback |
|-------|------|---------|-------|----------|
| **T1** | Cache | 100ms | Cache lookup | Skip cache |
| **T2** | File | 500ms | Single file | Use fallback |
| **T3** | Layer | 2s | Full layer | Partial load |
| **T4** | Full | 5s | Complete KB | Core only |
| **T5** | Complex | 10s | Analysis | Abort + summary |

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

| Situation | Action |
|-----------|--------|
| Cache miss | Proceed to file |
| File timeout | Use embedded fallback |
| Layer timeout | Return loaded portion |
| Full timeout | Return core principles |
| Analysis timeout | Return summary |

---

## 4. Circuit Breaker

| Parameter | Value | Purpose |
|-----------|-------|---------|
| Failure threshold | 3 | Open after N failures |
| Reset timeout | 30s | Try again after |
| Half-open requests | 1 | Test recovery |

### 4.1 States

| State | Behavior |
|-------|----------|
| **Closed** | Normal operation |
| **Open** | Fail fast, use fallback |
| **Half-Open** | Test with single request |

---

## 5. Configuration

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

## 6. Implementation Guidelines

| Guideline | Application |
|-----------|-------------|
| Always set timeouts | Every external call |
| Use appropriate tier | Match operation scope |
| Implement fallbacks | Every timeout path |
| Log timeouts | For monitoring |
| Test timeouts | Include in test suite |

---

**Golden Rule**: Always return something, never hang.

*Part of SAGE Knowledge Base*
