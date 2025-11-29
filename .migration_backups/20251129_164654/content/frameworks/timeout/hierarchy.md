# Timeout Hierarchy Framework

> **Load Time**: On-demand (~150 tokens)  
> **Purpose**: Guarantee response times, prevent hangs, graceful degradation

---

## Overview

The Timeout Hierarchy ensures the system always responds within acceptable time limits by implementing cascading
fallbacks. The principle: **Always return something, never hang.**

---

## 5-Level Timeout Hierarchy

```
Level 0: Cache (100ms)
    ↓ timeout
Level 1: File (500ms)
    ↓ timeout
Level 2: Layer (2s)
    ↓ timeout
Level 3: Full (5s)
    ↓ timeout
Level 4: Emergency (10s)
    ↓ timeout
Hard Fallback: Embedded minimal response
```

---

## Level Definitions

### Level 0: Cache (100ms)

```
Source: In-memory cache
Timeout: 100ms
Fallback: Level 1

Use Case:
- Frequently accessed content
- Hot paths
- Repeated queries

Response:
- Full cached content if available
- Proceed to Level 1 if miss or timeout
```

### Level 1: File (500ms)

```
Source: Local file system
Timeout: 500ms
Fallback: Level 2

Use Case:
- Single file reads
- Index lookups
- Configuration files

Response:
- Complete file content
- Partial content if interrupted
- Proceed to Level 2 if timeout
```

### Level 2: Layer (2s)

```
Source: Knowledge layer loading
Timeout: 2s
Fallback: Level 3

Use Case:
- Load specific guideline chapter
- Load framework document
- Multi-file operations

Response:
- Requested layer content
- Core content only if timeout
```

### Level 3: Full (5s)

```
Source: Complete knowledge base
Timeout: 5s
Fallback: Level 4

Use Case:
- Full search operations
- Cross-reference lookups
- Complex queries

Response:
- Complete results
- Partial results with continuation token
```

### Level 4: Emergency (10s)

```
Source: Any available content
Timeout: 10s
Fallback: Embedded

Use Case:
- System under stress
- Network issues
- Degraded mode

Response:
- Whatever content is available
- Hard fallback if timeout
```

### Hard Fallback: Embedded

```
Source: Compiled-in minimal content
Timeout: None (immediate)
Fallback: None

Content:
- Core principles (~100 tokens)
- Essential defaults
- Error message

Always available, never fails.
```

---

## Implementation Pattern

### Python Implementation

```python
from typing import Optional, TypeVar, Callable
import asyncio

T = TypeVar('T')


async def with_timeout(
    operation: Callable[[], T],
    timeout_ms: int,
    fallback: Optional[Callable[[], T]] = None
) -> T:
    """Execute operation with timeout and fallback."""
    try:
        return await asyncio.wait_for(
            operation(),
            timeout=timeout_ms / 1000
        )
    except asyncio.TimeoutError:
        if fallback:
            return await fallback()
        raise


async def load_with_hierarchy(query: str) -> str:
    """Load content using timeout hierarchy."""

    # Level 0: Cache
    try:
        return await with_timeout(
            lambda: cache.get(query),
            timeout_ms=100,
            fallback=lambda: load_level_1(query)
        )
    except Exception:
        pass

    # Level 1: File
    try:
        return await with_timeout(
            lambda: file_loader.load(query),
            timeout_ms=500,
            fallback=lambda: load_level_2(query)
        )
    except Exception:
        pass

    # ... continue through levels ...

    # Hard fallback
    return EMBEDDED_FALLBACK
```

---

## Timeout Configuration

### Default Timeouts (sage.yaml)

```yaml
timeouts:
  cache_ms: 100
  file_ms: 500
  layer_ms: 2000
  full_ms: 5000
  emergency_ms: 10000

  # Adjustment factors
  network_multiplier: 1.5  # For remote sources
  stress_multiplier: 2.0   # Under high load
```

### Dynamic Adjustment

```python
def adjust_timeout(base_ms: int, context: Context) -> int:
    """Adjust timeout based on context."""
    timeout = base_ms

    if context.is_remote:
        timeout *= config.network_multiplier

    if context.system_load > 0.8:
        timeout *= config.stress_multiplier

    return min(timeout, config.max_timeout_ms)
```

---

## Fallback Content Strategy

### Graceful Degradation

| Level Failed      | Response Strategy    |
|-------------------|----------------------|
| Cache miss        | Load from file       |
| File timeout      | Return cached subset |
| Layer timeout     | Return core only     |
| Full timeout      | Return index + error |
| Emergency timeout | Embedded fallback    |

### Partial Response Format

```json
{
  "content": "... partial content ...",
  "complete": false,
  "loaded_from": "level_1",
  "timeout_at": "level_2",
  "continuation": "token_xyz",
  "message": "Partial response due to timeout. Use continuation token for more."
}
```

---

## Monitoring and Alerting

### Metrics to Track

```
- timeout_count_by_level
- fallback_trigger_count
- average_response_time_by_level
- cache_hit_rate
- emergency_fallback_rate
```

### Alert Thresholds

| Metric              | Warning | Critical |
|---------------------|---------|----------|
| Level 2+ timeouts   | >5%     | >15%     |
| Emergency fallbacks | >1%     | >5%      |
| Cache hit rate      | <80%    | <60%     |
| Avg response time   | >1s     | >3s      |

---

## Best Practices

### Do

- ✅ Always have a fallback at each level
- ✅ Log timeout events for analysis
- ✅ Cache aggressively for hot paths
- ✅ Return partial results over nothing
- ✅ Include metadata about response completeness

### Don't

- ❌ Let any operation run unbounded
- ❌ Fail silently on timeout
- ❌ Return empty response without explanation
- ❌ Retry infinitely
- ❌ Block on slow operations

---

## Quick Reference

```
Timeout Hierarchy:
L0: Cache     100ms  → Fast, memory
L1: File      500ms  → Local disk
L2: Layer     2s     → Multi-file
L3: Full      5s     → Complete KB
L4: Emergency 10s    → Degraded mode
L∞: Embedded  0ms    → Hard fallback

Rule: Always return something, never hang.
```

---

*Part of AI Collaboration Knowledge Base v2.0.0*
