# Profiling Guide

> Performance measurement and bottleneck identification

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Python Profiling](#2-python-profiling)
- [3. Database Profiling](#3-database-profiling)
- [4. System Profiling](#4-system-profiling)
- [5. Application Monitoring](#5-application-monitoring)
- [6. Load Testing](#6-load-testing)

---

## 1. Overview

### Profiling Process

```
┌─────────────────────────────────────────────────────────────┐
│                   Profiling Workflow                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Define Metrics                                          │
│     └─▶ What to measure (latency, throughput, memory)      │
│                                                             │
│  2. Establish Baseline                                      │
│     └─▶ Current performance numbers                         │
│                                                             │
│  3. Profile Under Load                                      │
│     └─▶ Realistic usage patterns                           │
│                                                             │
│  4. Identify Bottlenecks                                    │
│     └─▶ Where time/resources are spent                     │
│                                                             │
│  5. Optimize & Verify                                       │
│     └─▶ Fix issues, measure improvement                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

| Category     | Metric                  | Tool                         |
|--------------|-------------------------|------------------------------|
| **Time**     | Response time, CPU time | cProfile, line_profiler      |
| **Memory**   | Heap size, allocations  | memory_profiler, tracemalloc |
| **I/O**      | Disk reads/writes       | iostat, strace               |
| **Network**  | Latency, throughput     | tcpdump, Wireshark           |
| **Database** | Query time, connections | EXPLAIN, pg_stat             |

---

## 2. Python Profiling

### cProfile (Function-Level)

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function and print results."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    
    # Format output
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    print(stream.getvalue())
    return result

# Usage
profile_function(my_expensive_function, arg1, arg2)

# Command line usage
# python -m cProfile -s cumulative my_script.py
```

### line_profiler (Line-Level)

```python
# Install: pip install line_profiler

# Add decorator to functions to profile
@profile  # This decorator is added by kernprof
def slow_function(items):
    result = []
    for item in items:  # Line-by-line timing
        processed = process(item)
        result.append(processed)
    return result

# Run with: kernprof -l -v my_script.py
```

**Output example:**

```
Line #    Hits    Time  Per Hit   % Time  Line Contents
=======================================================
     3                                    def slow_function(items):
     4       1      1.0      1.0    0.0      result = []
     5    1001   5023.0      5.0   10.0      for item in items:
     6    1000  40000.0     40.0   80.0          processed = process(item)
     7    1000   5000.0      5.0   10.0          result.append(processed)
     8       1      1.0      1.0    0.0      return result
```

### memory_profiler (Memory Usage)

```python
# Install: pip install memory_profiler

from memory_profiler import profile

@profile
def memory_intensive():
    large_list = [i ** 2 for i in range(1000000)]
    filtered = [x for x in large_list if x % 2 == 0]
    return sum(filtered)

# Run with: python -m memory_profiler my_script.py
```

**Output example:**

```
Line #    Mem usage    Increment   Line Contents
================================================
     4     50.0 MiB     50.0 MiB   @profile
     5                             def memory_intensive():
     6     88.5 MiB     38.5 MiB       large_list = [i ** 2 for i in range(1000000)]
     7    107.2 MiB     18.7 MiB       filtered = [x for x in large_list if x % 2 == 0]
     8    107.2 MiB      0.0 MiB       return sum(filtered)
```

### tracemalloc (Memory Tracing)

```python
import tracemalloc

def trace_memory():
    tracemalloc.start()
    
    # Code to analyze
    data = process_large_data()
    
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("Top 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)
    
    tracemalloc.stop()

# Compare snapshots
tracemalloc.start()
snapshot1 = tracemalloc.take_snapshot()

# ... code that may leak ...

snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

for stat in top_stats[:10]:
    print(stat)
```

### Async Profiling

```python
import asyncio
import time
from contextlib import asynccontextmanager

class AsyncProfiler:
    """Profile async operations."""
    
    def __init__(self):
        self.timings = {}
    
    @asynccontextmanager
    async def measure(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            if name not in self.timings:
                self.timings[name] = []
            self.timings[name].append(elapsed)
    
    def report(self):
        for name, times in self.timings.items():
            avg = sum(times) / len(times)
            print(f"{name}: avg={avg*1000:.2f}ms, count={len(times)}")

# Usage
profiler = AsyncProfiler()

async def my_async_function():
    async with profiler.measure("database_query"):
        await db.query(...)
    
    async with profiler.measure("api_call"):
        await api.fetch(...)

await my_async_function()
profiler.report()
```

---

## 3. Database Profiling

### PostgreSQL EXPLAIN

```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- With execution statistics
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Full details
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM users WHERE email = 'test@example.com';
```

**Understanding EXPLAIN output:**

```
Seq Scan on users  (cost=0.00..1234.00 rows=1 width=100) (actual time=0.015..12.345 rows=1 loops=1)
  Filter: (email = 'test@example.com'::text)
  Rows Removed by Filter: 99999
Planning Time: 0.100 ms
Execution Time: 12.400 ms
```

| Term             | Meaning                       |
|------------------|-------------------------------|
| **Seq Scan**     | Full table scan (usually bad) |
| **Index Scan**   | Using index (good)            |
| **cost**         | Estimated cost units          |
| **actual time**  | Real execution time (ms)      |
| **rows**         | Rows returned                 |
| **Rows Removed** | Filtered out rows             |

### Query Performance Monitoring

```sql
-- PostgreSQL: Slow query log
ALTER SYSTEM SET log_min_duration_statement = '100ms';
SELECT pg_reload_conf();

-- View recent slow queries
SELECT
    query,
    calls,
    total_time / 1000 as total_seconds,
    mean_time as avg_ms,
    rows
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Find missing indexes
SELECT
    schemaname || '.' || relname as table,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_tup_read DESC;
```

### SQLAlchemy Profiling

```python
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

# Enable SQL logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Query timing
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    if total > 0.1:  # Log slow queries (>100ms)
        logger.warning(f"Slow query ({total*1000:.0f}ms): {statement[:100]}")
```

---

## 4. System Profiling

### CPU Profiling

```bash
# Linux: CPU usage by process
top -p $(pgrep -f python)

# Detailed CPU profiling with perf
perf record -g python my_script.py
perf report

# Python with py-spy (sampling profiler)
pip install py-spy
py-spy record -o profile.svg -- python my_script.py
py-spy top --pid <PID>  # Real-time view
```

### Memory Profiling

```bash
# Linux: Memory usage
ps aux --sort=-%mem | head -10

# Detailed memory with valgrind
valgrind --tool=massif python my_script.py
ms_print massif.out.*

# Python memory with pympler
pip install pympler
```

```python
from pympler import asizeof, tracker

# Object size
obj = {"key": [1, 2, 3] * 1000}
print(f"Size: {asizeof.asizeof(obj)} bytes")

# Track memory changes
tr = tracker.SummaryTracker()
# ... code ...
tr.print_diff()
```

### I/O Profiling

```bash
# Linux: I/O statistics
iostat -x 1

# Trace system calls
strace -c python my_script.py

# File operations only
strace -e trace=file python my_script.py
```

---

## 5. Application Monitoring

### Custom Metrics

```python
import time
from dataclasses import dataclass, field
from typing import Dict, List
from contextlib import contextmanager

@dataclass
class Metrics:
    """Application metrics collector."""
    counters: Dict[str, int] = field(default_factory=dict)
    gauges: Dict[str, float] = field(default_factory=dict)
    timings: Dict[str, List[float]] = field(default_factory=dict)
    
    def increment(self, name: str, value: int = 1):
        self.counters[name] = self.counters.get(name, 0) + value
    
    def set_gauge(self, name: str, value: float):
        self.gauges[name] = value
    
    def record_timing(self, name: str, duration: float):
        if name not in self.timings:
            self.timings[name] = []
        self.timings[name].append(duration)
    
    @contextmanager
    def timer(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.record_timing(name, time.perf_counter() - start)
    
    def summary(self) -> dict:
        timing_stats = {}
        for name, times in self.timings.items():
            if times:
                timing_stats[name] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times) * 1000,
                    "min_ms": min(times) * 1000,
                    "max_ms": max(times) * 1000,
                }
        return {
            "counters": self.counters,
            "gauges": self.gauges,
            "timings": timing_stats,
        }

# Global metrics instance
metrics = Metrics()

# Usage
metrics.increment("requests_total")
with metrics.timer("request_duration"):
    handle_request()
```

### Structured Logging for Performance

```python
import structlog
import time

logger = structlog.get_logger()

def log_performance(func):
    """Decorator to log function performance."""
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start
            logger.info(
                "function_completed",
                function=func.__name__,
                duration_ms=duration * 1000,
                status="success"
            )
            return result
        except Exception as e:
            duration = time.perf_counter() - start
            logger.error(
                "function_failed",
                function=func.__name__,
                duration_ms=duration * 1000,
                error=str(e)
            )
            raise
    return wrapper
```

### Health Endpoints

```python
from fastapi import FastAPI
import psutil
import time

app = FastAPI()
start_time = time.time()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    process = psutil.Process()
    return {
        "uptime_seconds": time.time() - start_time,
        "cpu_percent": process.cpu_percent(),
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "threads": process.num_threads(),
        "open_files": len(process.open_files()),
        "connections": len(process.connections()),
    }
```

---

## 6. Load Testing

### Locust (Python)

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def view_items(self):
        self.client.get("/items")
    
    @task(1)
    def view_item(self):
        item_id = random.randint(1, 1000)
        self.client.get(f"/items/{item_id}")
    
    @task(1)
    def create_item(self):
        self.client.post("/items", json={
            "name": "Test Item",
            "price": 99.99
        })

# Run: locust -f locustfile.py --host=http://localhost:8000
```

### pytest-benchmark

```python
# pip install pytest-benchmark

def test_performance(benchmark):
    """Benchmark a function."""
    result = benchmark(my_function, arg1, arg2)
    assert result is not None

def test_with_setup(benchmark):
    """Benchmark with setup/teardown."""
    def setup():
        return get_test_data()
    
    result = benchmark.pedantic(
        my_function,
        setup=setup,
        iterations=100,
        rounds=10
    )
```

### Simple Load Test Script

```python
import asyncio
import httpx
import time
from dataclasses import dataclass
from typing import List

@dataclass
class LoadTestResult:
    total_requests: int
    successful: int
    failed: int
    total_time: float
    avg_latency: float
    p95_latency: float
    p99_latency: float
    rps: float

async def load_test(
    url: str,
    num_requests: int = 1000,
    concurrency: int = 10
) -> LoadTestResult:
    """Simple async load test."""
    
    latencies: List[float] = []
    failed = 0
    
    async def make_request(client: httpx.AsyncClient):
        nonlocal failed
        start = time.perf_counter()
        try:
            response = await client.get(url)
            latency = time.perf_counter() - start
            if response.status_code == 200:
                latencies.append(latency)
            else:
                failed += 1
        except Exception:
            failed += 1
    
    start_time = time.perf_counter()
    
    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(concurrency)
        
        async def bounded_request():
            async with semaphore:
                await make_request(client)
        
        await asyncio.gather(*[
            bounded_request() for _ in range(num_requests)
        ])
    
    total_time = time.perf_counter() - start_time
    
    sorted_latencies = sorted(latencies)
    p95_idx = int(len(sorted_latencies) * 0.95)
    p99_idx = int(len(sorted_latencies) * 0.99)
    
    return LoadTestResult(
        total_requests=num_requests,
        successful=len(latencies),
        failed=failed,
        total_time=total_time,
        avg_latency=sum(latencies) / len(latencies) if latencies else 0,
        p95_latency=sorted_latencies[p95_idx] if latencies else 0,
        p99_latency=sorted_latencies[p99_idx] if latencies else 0,
        rps=len(latencies) / total_time
    )

# Usage
result = asyncio.run(load_test("http://localhost:8000/api/items"))
print(f"RPS: {result.rps:.2f}")
print(f"Avg Latency: {result.avg_latency*1000:.2f}ms")
print(f"P95 Latency: {result.p95_latency*1000:.2f}ms")
```

---

## Quick Reference

### Profiling Decision Tree

```
What to profile?
├── Function slow? → cProfile, line_profiler
├── Memory issues? → memory_profiler, tracemalloc
├── Database slow? → EXPLAIN ANALYZE, slow query log
├── System issues? → top, iostat, strace
└── Under load? → Locust, load test script
```

### Performance Targets

| Metric      | Good   | Acceptable | Poor   |
|-------------|--------|------------|--------|
| P50 Latency | <50ms  | <200ms     | >500ms |
| P99 Latency | <200ms | <1s        | >2s    |
| Error Rate  | <0.1%  | <1%        | >5%    |
| CPU Usage   | <50%   | <80%       | >90%   |
| Memory      | <70%   | <85%       | >95%   |

### Profiling Tools Summary

| Tool            | Type     | Use Case              |
|-----------------|----------|-----------------------|
| cProfile        | CPU      | Function-level timing |
| line_profiler   | CPU      | Line-by-line timing   |
| py-spy          | CPU      | Production profiling  |
| memory_profiler | Memory   | Line-by-line memory   |
| tracemalloc     | Memory   | Allocation tracking   |
| EXPLAIN         | Database | Query analysis        |
| Locust          | Load     | HTTP load testing     |

---

## Related

- `.knowledge/frameworks/performance/optimization_strategies.md` — Optimization techniques
- `.knowledge/frameworks/performance/caching_patterns.md` — Caching strategies
- `tools/timeout_manager.py` — the application timeout testing

---

*Part of AI Collaboration Knowledge Base - Performance Framework*
