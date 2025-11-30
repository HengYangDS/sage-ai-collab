# SAGE Performance Tuning

> SAGE-specific performance goals, benchmarks, and monitoring

---

## Generic References

For comprehensive performance optimization guides, see:

| Topic                       | Reference                                                      |
|:----------------------------|:---------------------------------------------------------------|
| **Optimization Strategies** | `.knowledge/frameworks/performance/optimization_strategies.md` |
| **Caching Patterns**        | `.knowledge/frameworks/performance/caching_patterns.md`        |
| **Profiling Guide**         | `.knowledge/frameworks/performance/profiling_guide.md`         |

---

## Table of Contents

- [1. Performance Goals](#1-performance-goals)
- [2. Benchmarks](#2-benchmarks)
- [3. Monitoring](#3-monitoring)
- [4. Tuning Checklist](#4-tuning-checklist)

---

## 1. Performance Goals

### 1.1 Target Metrics

| Metric           | Target  | Measured | Status |
|:-----------------|:--------|:---------|:-------|
| Cold start       | < 2s    | ~1.5s    | ✓      |
| Warm start       | < 500ms | ~300ms   | ✓      |
| Single file load | < 100ms | ~50ms    | ✓      |
| Search (cached)  | < 50ms  | ~30ms    | ✓      |
| Memory baseline  | < 100MB | ~80MB    | ✓      |

### 1.2 Key Principles

| Principle        | Description                       |
|:-----------------|:----------------------------------|
| **Lazy Loading** | Load content only when needed     |
| **Caching**      | Cache frequently accessed content |
| **Timeouts**     | Never let operations hang         |
| **Incremental**  | Process in chunks when possible   |

### 1.3 Token Budget Allocation

| Layer      | Budget | Priority  |
|:-----------|:-------|:----------|
| Core       | 2000   | Always    |
| Guidelines | 2000   | High      |
| Frameworks | 2000   | Medium    |
| Practices  | 1500   | Low       |
| Scenarios  | 500    | On-demand |

---

## 2. Benchmarks

### 2.1 Current Benchmarks

| Operation          | P50   | P95   | P99   |
|:-------------------|:------|:------|:------|
| Load core layer    | 150ms | 200ms | 250ms |
| Load single file   | 30ms  | 50ms  | 80ms  |
| Search (indexed)   | 5ms   | 15ms  | 30ms  |
| Search (full scan) | 50ms  | 100ms | 200ms |
| Token counting     | 1ms   | 3ms   | 5ms   |

### 2.2 Running Benchmarks

```bash
# Run performance tests
pytest tests/performance/ -v

# Run specific benchmark
pytest tests/performance/test_load_performance.py -v

# Profile specific operation
python -m cProfile -s cumulative -m pytest tests/performance/
```

---

## 3. Monitoring

### 3.1 Key Metrics

| Metric            | Description            | Alert Threshold |
|:------------------|:-----------------------|:----------------|
| `load_time_ms`    | Time to load content   | > 2000ms        |
| `search_time_ms`  | Time to execute search | > 500ms         |
| `memory_mb`       | Memory usage           | > 200MB         |
| `cache_hit_ratio` | Cache effectiveness    | < 0.7           |
| `timeout_count`   | Timeout occurrences    | > 10/min        |

### 3.2 Instrumentation Pattern

```python
import time
from contextlib import contextmanager
import structlog

log = structlog.get_logger()


@contextmanager
def measure_time(operation: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        duration_ms = (time.perf_counter() - start) * 1000
        log.info("operation_complete", operation=operation, duration_ms=round(duration_ms, 2))
```

---

## 4. Tuning Checklist

| Area        | Check                            | Status |
|:------------|:---------------------------------|:-------|
| **Loading** | ☐ Lazy loading enabled           |        |
|             | ☐ Core preloading configured     |        |
|             | ☐ Parallel loading for batch ops |        |
| **Caching** | ☐ LRU cache configured           |        |
|             | ☐ Cache size appropriate         |        |
|             | ☐ Cache invalidation working     |        |
| **Search**  | ☐ Index built                    |        |
|             | ☐ Query caching enabled          |        |
|             | ☐ Result limits set              |        |
| **Memory**  | ☐ Token budget configured        |        |
|             | ☐ Eviction policy set            |        |
|             | ☐ Memory monitoring active       |        |

---

## Related

- `.knowledge/frameworks/performance/` — Generic performance guides
- `.context/policies/timeout_hierarchy.md` — Timeout settings
- `.context/intelligence/optimization/optimizations.md` — SAGE code optimizations
- `tests/performance/` — Performance test suite
- `config/core/memory.yaml` — Memory configuration

---

*Last updated: 2025-11-30*
*AI Collaboration Knowledge Base*
