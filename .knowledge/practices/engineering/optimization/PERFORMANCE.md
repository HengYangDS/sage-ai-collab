# Performance Optimization

> Performance best practices and optimization strategies for Python applications

---

## Table of Contents

- [1. Overview](#1-overview)

- [2. Profiling](#2-profiling)

- [3. Python Optimization](#3-python-optimization)

- [4. I/O Optimization](#4-io-optimization)

- [5. Memory Management](#5-memory-management)

- [6. Caching Strategies](#6-caching-strategies)

---

## 1. Overview

### 1.1 Performance Principles

| Principle                | Description                        |

|--------------------------|------------------------------------|

| **Measure First**        | Profile before optimizing          |

| **Optimize Bottlenecks** | Focus on the slowest parts         |

| **Trade-offs**           | Balance speed, memory, readability |

| **Incremental**          | Small improvements, verify each    |

### 1.2 Performance Targets

| Operation        | Target  | Timeout Level |

|------------------|---------|---------------|

| Cache lookup     | < 100ms | T1            |

| Single file read | < 500ms | T2            |

| Layer load       | < 2s    | T3            |

| Full KB load     | < 5s    | T4            |

| Complex analysis | < 10s   | T5            |

---

## 2. Profiling

### 2.1 Profiling Tools

| Tool              | Use Case             | Output              |

|-------------------|----------------------|---------------------|

| `cProfile`        | CPU profiling        | Function call stats |

| `line_profiler`   | Line-by-line         | Time per line       |

| `memory_profiler` | Memory usage         | Memory per line     |

| `py-spy`          | Production profiling | Flame graphs        |

### 2.2 cProfile Usage

```python
import cProfile

import pstats

from io import StringIO

def profile_function(func, *args, **kwargs):

    """Profile a function and return stats."""

    profiler = cProfile.Profile()

    profiler.enable()

    result = func(*args, **kwargs)

    profiler.disable()

    # Get stats

    stream = StringIO()

    stats = pstats.Stats(profiler, stream=stream)

    stats.sort_stats('cumulative')

    stats.print_stats(20)

    print(stream.getvalue())

    return result

# Command line

# python -m cProfile -s cumulative script.py

```
### 2.3 Line Profiler

```python
# Install: pip install line_profiler

# Add decorator to functions to profile

@profile  # Comment out when not profiling

def slow_function():

    # ... code ...

    pass

# Run with: kernprof -l -v script.py

```
### 2.4 Benchmarking

```python
import timeit

from functools import wraps

import time

def benchmark(func):

    """Decorator to benchmark function execution."""

    @wraps(func)

    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        print(f"{func.__name__}: {elapsed:.4f}s")

        return result

    return wrapper

# Using timeit for micro-benchmarks

def benchmark_snippet():

    setup = "data = list(range(1000))"

    stmt = "sum(data)"

    result = timeit.timeit(stmt, setup, number=10000)

    print(f"Average: {result / 10000:.6f}s")

```
---

## 3. Python Optimization

### 3.1 Data Structures

| Operation | list  | set  | dict |

|-----------|-------|------|------|

| Lookup    | O(n)  | O(1) | O(1) |

| Insert    | O(1)* | O(1) | O(1) |

| Delete    | O(n)  | O(1) | O(1) |

```python
# Slow: O(n) lookup

if item in large_list:

    pass

# Fast: O(1) lookup

item_set = set(large_list)

if item in item_set:

    pass

```
### 3.2 Comprehensions vs Loops

```python
# Slower

result = []

for i in range(1000):

    result.append(i * 2)

# Faster - list comprehension

result = [i * 2 for i in range(1000)]

# Even faster for large data - generator

result = (i * 2 for i in range(1000))

```
### 3.3 String Operations

```python
# Slow: String concatenation in loop

result = ""

for s in strings:

    result += s  # Creates new string each time

# Fast: Join

result = "".join(strings)

# Fast: f-strings for formatting

name = "MyApp"

message = f"Welcome to {name}"

```
### 3.4 Built-in Functions

```python
# Use built-ins - they're implemented in C

# Slow

total = 0

for x in numbers:

    total += x

# Fast

total = sum(numbers)

# Other fast built-ins

max(numbers)

min(numbers)

any(conditions)

all(conditions)

```
### 3.5 Local Variables

```python
# Slower: Global lookup

import math

def slow_function(values):

    return [math.sqrt(x) for x in values]

# Faster: Local reference

def fast_function(values):

    sqrt = math.sqrt  # Local reference

    return [sqrt(x) for x in values]

```
---

## 4. I/O Optimization

### 4.1 File Reading

```python
from pathlib import Path

# Slow: Read entire file into memory

content = Path("large_file.txt").read_text()

# Fast: Process line by line

def process_large_file(path: Path):

    with open(path) as f:

        for line in f:  # Iterator, low memory

            yield process_line(line)

# Fastest: Use mmap for random access

import mmap

def mmap_read(path: Path):

    with open(path, "rb") as f:

        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:

            return mm.read()

```
### 4.2 Async I/O

```python
import asyncio

import aiofiles

from pathlib import Path

async def read_file_async(path: Path) -> str:

    """Read file asynchronously."""

    async with aiofiles.open(path) as f:

        return await f.read()

async def read_multiple_files(paths: list[Path]) -> list[str]:

    """Read multiple files concurrently."""

    tasks = [read_file_async(p) for p in paths]

    return await asyncio.gather(*tasks)

# Usage

contents = asyncio.run(read_multiple_files(file_paths))

```
### 4.3 Batch Operations

```python
# Slow: Multiple small writes

for item in items:

    file.write(f"{item}\n")

# Fast: Batch write

file.write("\n".join(str(item) for item in items))

# Fast: Use writelines

file.writelines(f"{item}\n" for item in items)

```
---

## 5. Memory Management

### 5.1 Memory Profiling

```python
# Install: pip install memory_profiler

from memory_profiler import profile

@profile

def memory_intensive_function():

    # ... code ...

    pass

# Run: python -m memory_profiler script.py

```
### 5.2 Generators for Large Data

```python
# Memory heavy: List stores all items

def get_all_items() -> list:

    return [process(i) for i in range(1_000_000)]

# Memory efficient: Generator yields one at a time

def get_all_items() -> Iterator:

    for i in range(1_000_000):

        yield process(i)

```
### 5.3 __slots__ for Classes

```python
# Regular class: Uses dict for attributes

class RegularPoint:

    def __init__(self, x, y):

        self.x = x

        self.y = y

# Memory efficient: Fixed attributes

class SlotPoint:

    __slots__ = ['x', 'y']

    def __init__(self, x, y):

        self.x = x

        self.y = y

# ~40% memory savings for many instances

```
### 5.4 Weak References

```python
import weakref

class Cache:

    """Cache that doesn't prevent garbage collection."""

    def __init__(self):

        self._cache = weakref.WeakValueDictionary()

    def get(self, key):

        return self._cache.get(key)

    def set(self, key, value):

        self._cache[key] = value

```
---

## 6. Caching Strategies

### 6.1 Function Caching

```python
from functools import lru_cache, cache

# LRU cache with size limit

@lru_cache(maxsize=128)

def expensive_computation(n: int) -> int:

    # ... expensive operation ...

    return result

# Unlimited cache (Python 3.9+)

@cache

def another_expensive_function(x: str) -> str:

    return process(x)

# Clear cache when needed

expensive_computation.cache_clear()

```
### 6.2 Time-Based Caching

```python
import time

from functools import wraps

from typing import Any, Callable

def timed_cache(seconds: int):

    """Cache with expiration time."""

    def decorator(func: Callable) -> Callable:

        cache = {}

        @wraps(func)

        def wrapper(*args) -> Any:

            now = time.time()

            if args in cache:

                result, timestamp = cache[args]

                if now - timestamp < seconds:

                    return result

            result = func(*args)

            cache[args] = (result, now)

            return result

        return wrapper

    return decorator

@timed_cache(seconds=60)

def fetch_data(key: str) -> dict:

    # ... fetch from slow source ...

    pass

```
### 6.3 Multi-Level Cache

```python
from typing import Optional, Any

class MultiLevelCache:

    """L1 (memory) + L2 (disk) cache."""

    def __init__(self, l1_size: int = 100):

        self._l1 = {}  # Memory cache

        self._l1_size = l1_size

        self._disk_path = Path(".cache")

    def get(self, key: str) -> Optional[Any]:

        # Try L1 first

        if key in self._l1:

            return self._l1[key]

        # Try L2

        cache_file = self._disk_path / f"{key}.json"

        if cache_file.exists():

            data = json.loads(cache_file.read_text())

            self._l1[key] = data  # Promote to L1

            return data

        return None

    def set(self, key: str, value: Any) -> None:

        # Store in L1

        if len(self._l1) >= self._l1_size:

            self._evict_l1()

        self._l1[key] = value

        # Persist to L2

        cache_file = self._disk_path / f"{key}.json"

        cache_file.write_text(json.dumps(value))

```
---

## Quick Reference

### Profiling Commands

```bash
# CPU profiling

python -m cProfile -s cumulative script.py

# Line profiling

kernprof -l -v script.py

# Memory profiling

python -m memory_profiler script.py

# Flame graph (production)

py-spy record -o profile.svg -- python script.py

```
### Performance Checklist

| Area                | Check                                 |

|---------------------|---------------------------------------|

| **Data Structures** | Using appropriate types (set vs list) |

| **Algorithms**      | Optimal time complexity               |

| **I/O**             | Batched, async where possible         |

| **Memory**          | Generators for large data             |

| **Caching**         | Hot paths cached appropriately        |

| **Profiling**       | Measured before optimizing            |

### Common Optimizations

| Slow             | Fast               |

|------------------|--------------------|

| `for` + append   | List comprehension |

| String `+=`      | `"".join()`        |

| `item in list`   | `item in set`      |

| Nested loops     | Dict lookups       |

| Read all at once | Stream/iterate     |

---

## Related

- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Performance testing

- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Timeout handling

- `.context/intelligence/optimization/OPTIMIZATIONS.md` — Project optimizations

- `.context/policies/TIMEOUT_HIERARCHY.md` — Timeout config

---

*AI Collaboration Knowledge Base*

