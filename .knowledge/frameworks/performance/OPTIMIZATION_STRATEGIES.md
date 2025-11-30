# Optimization Strategies

> Systematic approaches to improving system performance

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Code Optimization](#2-code-optimization)
- [3. Database Optimization](#3-database-optimization)
- [4. Network Optimization](#4-network-optimization)
- [5. System Optimization](#5-system-optimization)
- [6. Scaling Strategies](#6-scaling-strategies)

---

## 1. Overview

### Optimization Process

```mermaid
flowchart LR
    M["Measure Baseline"] --> I["Identify Hotspots"]
    I --> O["Optimize Targeted"]
    M --> V["Validate Results"]
    O --> V
```
> **Rule**: Measure → Analyze → Optimize → Verify → Repeat

### Optimization Priorities

| Priority | Focus                | Expected Impact |
|----------|----------------------|-----------------|
| 1        | Algorithm complexity | 10x-1000x       |
| 2        | I/O and database     | 10x-100x        |
| 3        | Caching              | 5x-50x          |
| 4        | Concurrency          | 2x-10x          |
| 5        | Micro-optimizations  | 1.1x-2x         |

---

## 2. Code Optimization

### Algorithm Complexity

| Complexity | Name         | Example       | Scalability |
|------------|--------------|---------------|-------------|
| O(1)       | Constant     | Hash lookup   | Excellent   |
| O(log n)   | Logarithmic  | Binary search | Excellent   |
| O(n)       | Linear       | Array scan    | Good        |
| O(n log n) | Linearithmic | Merge sort    | Good        |
| O(n²)      | Quadratic    | Nested loops  | Poor        |
| O(2ⁿ)      | Exponential  | Brute force   | Terrible    |

```python
# Bad: O(n²) - nested iteration
def find_duplicates_slow(items: list) -> list:
    duplicates = []
    for i, item in enumerate(items):
        for j, other in enumerate(items):
            if i != j and item == other:
                duplicates.append(item)
    return duplicates

# Good: O(n) - hash-based
def find_duplicates_fast(items: list) -> list:
    seen = set()
    duplicates = []
    for item in items:
        if item in seen:
            duplicates.append(item)
        seen.add(item)
    return duplicates
```
### Data Structure Selection

| Need             | Best Choice       | Why                 |
|------------------|-------------------|---------------------|
| Fast lookup      | dict, set         | O(1) average        |
| Ordered data     | list, deque       | Sequence access     |
| Sorted iteration | sorted containers | Maintained order    |
| Queue operations | deque             | O(1) both ends      |
| Priority queue   | heapq             | O(log n) operations |

```python
from collections import deque
import heapq

# Queue: Use deque, not list
queue = deque()
queue.append(item)      # O(1)
item = queue.popleft()  # O(1)

# Priority queue: Use heapq
heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)

# Membership testing: Use set, not list
items_set = set(items)  # O(n) once
if item in items_set:   # O(1) per lookup
    ...
```
### Loop Optimization

```python
# Bad: Repeated computation in loop
for item in items:
    result = expensive_function()  # Called every iteration
    process(item, result)

# Good: Compute once outside loop
result = expensive_function()
for item in items:
    process(item, result)

# Bad: String concatenation in loop
result = ""
for item in items:
    result += str(item)  # O(n²) total

# Good: Join list
result = "".join(str(item) for item in items)  # O(n)

# Bad: Function call in loop condition
for i in range(len(items)):  # len() called each time
    ...

# Good: Cache length
n = len(items)
for i in range(n):
    ...
```
### Generator Patterns

```python
# Bad: Materialize entire list
def get_all_users():
    return [process(user) for user in db.get_all_users()]

# Good: Generator for memory efficiency
def get_all_users():
    for user in db.get_all_users():
        yield process(user)

# Good: Generator expression
processed = (process(user) for user in users)

# Batch processing with generators
def batch_iterator(items, batch_size=100):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
```
---

## 3. Database Optimization

### Query Optimization

```sql
-- Bad: SELECT *
SELECT * FROM users WHERE status = 'active';

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE status = 'active';

-- Bad: N+1 queries
for user in users:
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user.id)

-- Good: Single query with JOIN
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';
```
### Index Strategies

| Index Type    | Use Case               | Example                   |
|---------------|------------------------|---------------------------|
| **B-tree**    | Range queries, sorting | `created_at`, `price`     |
| **Hash**      | Equality lookups       | `user_id`, `email`        |
| **Composite** | Multi-column queries   | `(user_id, created_at)`   |
| **Partial**   | Filtered subset        | `WHERE status = 'active'` |
| **Covering**  | Avoid table lookup     | Include all query columns |

```sql
-- Create composite index for common query pattern
CREATE INDEX idx_user_status_created
ON orders (user_id, status, created_at);

-- Partial index for subset of data
CREATE INDEX idx_active_users
ON users (email)
WHERE status = 'active';

-- Covering index
CREATE INDEX idx_user_orders_covering
ON orders (user_id)
INCLUDE (total, status, created_at);
```
### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Configure connection pool
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,          # Maintained connections
    max_overflow=20,       # Extra connections when needed
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections after 30 min
    pool_pre_ping=True,    # Verify connections before use
)
```
### Batch Operations

```python
# Bad: Individual inserts
for item in items:
    db.execute("INSERT INTO items VALUES (?)", item)

# Good: Batch insert
db.executemany(
    "INSERT INTO items VALUES (?)",
    items
)

# Better: Bulk insert with COPY (PostgreSQL)
from io import StringIO
import csv

buffer = StringIO()
writer = csv.writer(buffer)
writer.writerows(items)
buffer.seek(0)
cursor.copy_from(buffer, 'items', sep=',')
```
---

## 4. Network Optimization

### Request Optimization

| Technique        | Benefit               | Implementation  |
|------------------|-----------------------|-----------------|
| **Compression**  | 60-80% size reduction | gzip, brotli    |
| **Minification** | 20-40% size reduction | JS/CSS minify   |
| **Bundling**     | Fewer requests        | Webpack, rollup |
| **CDN**          | Lower latency         | CloudFlare, AWS |
| **HTTP/2**       | Multiplexing          | Server config   |

```python
# Enable compression in FastAPI
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
```
### Connection Management

```python
import httpx

# Bad: New connection per request
async def fetch_many_bad(urls):
    results = []
    for url in urls:
        async with httpx.AsyncClient() as client:
            results.append(await client.get(url))
    return results

# Good: Reuse connections
async def fetch_many_good(urls):
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*[
            client.get(url) for url in urls
        ])

# Better: Connection pool with limits
limits = httpx.Limits(
    max_keepalive_connections=10,
    max_connections=20,
    keepalive_expiry=30.0
)
async with httpx.AsyncClient(limits=limits) as client:
    ...
```
### Response Optimization

```python
# Pagination
@app.get("/items")
async def list_items(
    page: int = 1,
    page_size: int = 20,
    max_page_size: int = 100
):
    page_size = min(page_size, max_page_size)
    offset = (page - 1) * page_size
    
    items = await db.get_items(offset=offset, limit=page_size)
    total = await db.count_items()
    
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": (total + page_size - 1) // page_size
    }

# Field selection
@app.get("/users/{user_id}")
async def get_user(user_id: str, fields: str = None):
    user = await db.get_user(user_id)
    
    if fields:
        allowed_fields = {"id", "name", "email", "created_at"}
        requested = set(fields.split(",")) & allowed_fields
        user = {k: v for k, v in user.items() if k in requested}
    
    return user
```
---

## 5. System Optimization

### Concurrency Patterns

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O-bound: Use asyncio
async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# CPU-bound: Use ProcessPoolExecutor
def process_all(items):
    with ProcessPoolExecutor(max_workers=4) as executor:
        return list(executor.map(cpu_intensive_task, items))

# Mixed workloads: Combine approaches
async def hybrid_processing(items):
    loop = asyncio.get_event_loop()
    
    # CPU work in process pool
    with ProcessPoolExecutor() as pool:
        cpu_results = await loop.run_in_executor(
            pool,
            cpu_intensive_batch,
            items
        )
    
    # I/O work with asyncio
    io_results = await asyncio.gather(*[
        async_io_task(item) for item in cpu_results
    ])
    
    return io_results
```
### Memory Optimization

```python
# Use __slots__ for memory-efficient classes
class UserSlots:
    __slots__ = ['id', 'name', 'email']
    
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

# Use generators instead of lists for large datasets
def process_large_file(filepath):
    with open(filepath) as f:
        for line in f:  # Reads one line at a time
            yield process_line(line)

# Use numpy for numerical data
import numpy as np
# Bad: Python list of floats
python_list = [0.0] * 1_000_000  # ~8MB

# Good: NumPy array
numpy_array = np.zeros(1_000_000)  # ~8MB but faster operations
```
### Resource Pooling

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio

class ResourcePool:
    """Generic async resource pool."""
    
    def __init__(self, factory, max_size: int = 10):
        self.factory = factory
        self.max_size = max_size
        self.pool = asyncio.Queue(maxsize=max_size)
        self.size = 0
    
    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator:
        if self.pool.empty() and self.size < self.max_size:
            resource = await self.factory()
            self.size += 1
        else:
            resource = await self.pool.get()
        
        try:
            yield resource
        finally:
            await self.pool.put(resource)
```
---

## 6. Scaling Strategies

### Vertical vs Horizontal

| Aspect         | Vertical       | Horizontal    |
|----------------|----------------|---------------|
| **Method**     | Bigger machine | More machines |
| **Limit**      | Hardware max   | Unlimited     |
| **Cost**       | Exponential    | Linear        |
| **Downtime**   | Required       | Zero          |
| **Complexity** | Low            | High          |

### Load Balancing

```mermaid
flowchart TB
    C["Client"] --> LB["Load Balancer"]
    LB --> S1["Server1"]
    LB --> S2["Server2"]
    LB --> S3["Server3"]
```
### Load Balancing Algorithms

| Algorithm             | Use Case         | Pros            | Cons                |
|-----------------------|------------------|-----------------|---------------------|
| **Round Robin**       | Equal servers    | Simple          | Ignores load        |
| **Least Connections** | Varying requests | Adaptive        | More overhead       |
| **IP Hash**           | Session affinity | Sticky sessions | Uneven distribution |
| **Weighted**          | Mixed capacity   | Flexible        | Manual config       |

### Read Replicas

```python
class DatabaseRouter:
    """Route reads to replicas, writes to primary."""
    
    def __init__(self, primary, replicas):
        self.primary = primary
        self.replicas = replicas
        self.replica_index = 0
    
    def get_read_connection(self):
        # Round-robin across replicas
        replica = self.replicas[self.replica_index]
        self.replica_index = (self.replica_index + 1) % len(self.replicas)
        return replica
    
    def get_write_connection(self):
        return self.primary
    
    async def execute_read(self, query):
        conn = self.get_read_connection()
        return await conn.execute(query)
    
    async def execute_write(self, query):
        conn = self.get_write_connection()
        return await conn.execute(query)
```
---

## Quick Reference

### Optimization Checklist

- [ ] Profile before optimizing
- [ ] Fix algorithmic complexity first
- [ ] Add database indexes
- [ ] Implement caching
- [ ] Enable compression
- [ ] Use connection pooling
- [ ] Implement pagination
- [ ] Consider async/concurrent processing
- [ ] Set up monitoring
- [ ] Load test regularly

### Performance Anti-Patterns

| Anti-Pattern           | Problem       | Solution               |
|------------------------|---------------|------------------------|
| N+1 queries            | Many DB calls | Batch/JOIN             |
| Premature optimization | Wasted effort | Profile first          |
| Missing indexes        | Slow queries  | Add indexes            |
| No caching             | Repeated work | Cache results          |
| Blocking I/O           | Wasted CPU    | Use async              |
| Large payloads         | Slow transfer | Pagination/compression |

---

## Related

- `.knowledge/frameworks/performance/CACHING_PATTERNS.md` — Caching strategies
- `.knowledge/frameworks/performance/PROFILING_FRAMEWORK.md` — Performance measurement
- `.knowledge/practices/engineering/BATCH_OPTIMIZATION.md` — Batch processing

---

*AI Collaboration Knowledge Base*
