# Performance Quick Reference

> Essential performance checks and commands for DevOps workflows

---

## Timeout Targets

| Operation        | Target  | Level |
|------------------|---------|-------|
| Cache lookup     | < 100ms | T1    |
| Single file      | < 500ms | T2    |
| Layer load       | < 2s    | T3    |
| Full KB load     | < 5s    | T4    |
| Complex analysis | < 10s   | T5    |

---

## Profiling Commands

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

## Performance Checklist

| Area                | Check                         |
|---------------------|-------------------------------|
| **Data Structures** | Using set vs list for lookups |
| **Algorithms**      | Optimal time complexity       |
| **I/O**             | Batched, async where possible |
| **Memory**          | Generators for large data     |
| **Caching**         | Hot paths cached              |
| **Profiling**       | Measured before optimizing    |

---

## Common Optimizations

| Slow             | Fast               |
|------------------|--------------------|
| `for` + append   | List comprehension |
| String `+=`      | `"".join()`        |
| `item in list`   | `item in set`      |
| Nested loops     | Dict lookups       |
| Read all at once | Stream/iterate     |

---

## Key Patterns

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

**Full Guide**: `practices/engineering/performance.md`
