# Performance Quick Reference

> Essential performance checks and commands for DevOps workflows

---

## Table of Contents

- [1. Timeout Targets](#1-timeout-targets)
- [2. Profiling Commands](#2-profiling-commands)
- [3. Performance Checklist](#3-performance-checklist)
- [4. Common Optimizations](#4-common-optimizations)
- [5. Key Patterns](#5-key-patterns)

---

## 1. Timeout Targets

| Operation        | Target  | Level |
|------------------|---------|-------|
| Cache lookup     | < 100ms | T1    |
| Single file      | < 500ms | T2    |
| Layer load       | < 2s    | T3    |
| Full KB load     | < 5s    | T4    |
| Complex analysis | < 10s   | T5    |

---

## 2. Profiling Commands

```bash
# CPU profiling
python -m cProfile -s cumulative script.py

# Line profiling
kernprof -l -v script.py

# Memory profiling
python -m memory_profiler script.py

# Production flame graph
py-spy record -o profile.svg -- python script.py
```
---

## 3. Performance Checklist

| Area                | Check                         |
|---------------------|-------------------------------|
| **Data Structures** | Using set vs list for lookups |
| **Algorithms**      | Optimal time complexity       |
| **I/O**             | Batched, async where possible |
| **Memory**          | Generators for large data     |
| **Caching**         | Hot paths cached              |
| **Profiling**       | Measured before optimizing    |

---

## 4. Common Optimizations

| Slow             | Fast               |
|------------------|--------------------|
| `for` + append   | List comprehension |
| String `+=`      | `"".join()`        |
| `item in list`   | `item in set`      |
| Nested loops     | Dict lookups       |
| Read all at once | Stream/iterate     |

---

## 5. Key Patterns

```python
# LRU Cache
from functools import lru_cache
@lru_cache(maxsize=128)
def expensive_fn(n): ...

# Generator for large data
def process_large(items):
    for item in items:
        yield transform(item)
# Async I/O
async def read_files(paths):
    return await asyncio.gather(*[read(p) for p in paths])
```
---

## Related

- `.knowledge/practices/engineering/PERFORMANCE.md` — Full performance guide
- `.knowledge/frameworks/performance/INDEX.md` — Performance framework
- `.knowledge/frameworks/performance/CACHING_PATTERNS.md` — Caching strategies
- `.knowledge/frameworks/performance/PROFILING_FRAMEWORK.md` — Profiling guide

---

*AI Collaboration Knowledge Base*
