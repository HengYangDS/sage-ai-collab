# ADR-0003: Timeout Hierarchy Design

> Architecture Decision Record for SAGE Knowledge Base

---

## Table of Contents

- [Status](#status)
- [Context](#context)
- [Decision](#decision)
- [Alternatives Considered](#alternatives-considered)
- [Consequences](#consequences)
- [Implementation](#implementation)
- [Related](#related)

---

## Status

**Accepted** | Date: 2025-11-28

---

## Context

SAGE Knowledge Base must handle operations with varying time requirements:

1. Fast cache lookups (milliseconds)
2. File reads (sub-second)
3. Layer loading (seconds)
4. Full KB loading (multiple seconds)
5. Complex analysis (extended time)

### Requirements

- Never hang on any operation
- Graceful degradation on timeout
- Clear timeout expectations per operation type
- Configurable timeout values
- Consistent fallback behavior

### Problem Statement

Without structured timeout handling:

- Operations may block indefinitely
- Users experience unresponsive behavior
- No clear expectation of operation duration
- Inconsistent fallback strategies

---

## Decision

Implement a **Five-Level Timeout Hierarchy (T1-T5)** with graduated timeouts and fallback strategies.

### Timeout Levels

| Level  | Name    | Timeout | Scope               | Fallback Strategy    |
|:-------|:--------|:--------|:--------------------|:---------------------|
| **T1** | Cache   | 100ms   | Cache lookup        | Skip cache, proceed  |
| **T2** | File    | 500ms   | Single file read    | Use fallback content |
| **T3** | Layer   | 2s      | Full layer load     | Return partial       |
| **T4** | Full    | 5s      | Complete KB load    | Core only            |
| **T5** | Complex | 10s     | Analysis operations | Abort + summary      |

### Golden Rule

> **Always return something, never hang.**

Every timeout path must have a defined fallback that returns useful (if degraded) content.

### Timeout Flow

```
Request → T1 Cache → T2 File → T3 Layer → T4 Full → Result
              ↓          ↓          ↓          ↓
           Skip      Fallback   Partial    Core Only
```

---

## Alternatives Considered

### Alternative 1: Single Global Timeout

One timeout value for all operations.

- **Pros**: Simple configuration
- **Cons**: Too long for fast ops, too short for slow ops
- **Rejected**: Operations have vastly different time requirements

### Alternative 2: Per-Operation Configuration

Individual timeout for every operation.

- **Pros**: Maximum flexibility
- **Cons**: Configuration explosion, inconsistent mental model
- **Rejected**: Too complex to manage

### Alternative 3: Three-Level Hierarchy

Only Fast/Medium/Slow levels.

- **Pros**: Simpler than five levels
- **Cons**: Insufficient granularity for SAGE use cases
- **Rejected**: Need distinction between cache/file and layer/full

---

## Consequences

### Positive

1. **Predictability**: Clear expectations per operation type
2. **Resilience**: System never hangs
3. **Graceful degradation**: Partial results better than nothing
4. **Observability**: Easy to monitor timeout rates per level
5. **Tunability**: Five knobs instead of hundreds

### Negative

1. **Complexity**: Developers must choose correct level
2. **Edge cases**: Some operations may not fit neatly
3. **Overhead**: Timeout tracking has small performance cost

### Mitigations

1. **Guidelines**: Document when to use each level
2. **Defaults**: Sensible defaults in configuration
3. **Monitoring**: Alert on high timeout rates

---

## Implementation

### TimeoutLevel Enum

```python
from enum import Enum


class TimeoutLevel(Enum):
    T1_CACHE = 100  # 100ms
    T2_FILE = 500  # 500ms
    T3_LAYER = 2000  # 2s
    T4_FULL = 5000  # 5s
    T5_COMPLEX = 10000  # 10s
```

### Usage Pattern

```python
from sage.core.timeout import TimeoutManager, TimeoutLevel

manager = TimeoutManager()

# Select appropriate level for operation scope
result = await manager.execute_with_timeout(
    coro=load_layer("core"),
    level=TimeoutLevel.T3_LAYER,
    fallback=cached_core_content
)
```

### Configuration

```yaml
# sage.yaml
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

### Level Selection Guide

| Operation Type         | Recommended Level |
|:-----------------------|:------------------|
| Cache check            | T1                |
| Single file read       | T2                |
| Directory scan         | T2-T3             |
| Knowledge layer load   | T3                |
| Full KB initialization | T4                |
| Code analysis          | T5                |
| Content search         | T3-T4             |

---

## Related

- `.context/policies/timeout_hierarchy.md` — Detailed configuration
- `.context/decisions/ADR_0001_ARCHITECTURE.md` — Architecture context
- `.knowledge/frameworks/resilience/timeout_patterns.md` — Universal patterns
- `docs/design/04-timeout-loading.md` — Full design documentation

---

*AI Collaboration Knowledge Base*
