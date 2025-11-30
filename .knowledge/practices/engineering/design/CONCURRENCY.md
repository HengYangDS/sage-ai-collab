# Concurrency Practices

> Best practices for concurrent and parallel programming

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Python Concurrency](#2-python-concurrency)
- [3. Common Patterns](#3-common-patterns)
- [4. Best Practices](#4-best-practices)

---

## 1. Overview

### Concurrency vs Parallelism

| Aspect         | Concurrency             | Parallelism              |
|----------------|-------------------------|--------------------------|
| **Definition** | Managing multiple tasks | Executing multiple tasks |
| **Focus**      | Structure               | Execution                |
| **Hardware**   | Single core possible    | Multiple cores required  |
| **Use Case**   | I/O-bound work          | CPU-bound work           |

### Python Options

| Model               | Module               | Best For                    | GIL Impact          |
|---------------------|----------------------|-----------------------------|---------------------|
| **Threading**       | `threading`          | I/O-bound                   | Limited by GIL      |
| **Multiprocessing** | `multiprocessing`    | CPU-bound                   | Bypasses GIL        |
| **Asyncio**         | `asyncio`            | I/O-bound, high concurrency | No GIL issue        |
| **Futures**         | `concurrent.futures` | Both                        | Depends on executor |

---

## 2. Python Concurrency

### Asyncio (Recommended for I/O)

```python
import asyncio
import httpx

async def fetch_url(client: httpx.AsyncClient, url: str) -> str:
    response = await client.get(url)
    return response.text

async def fetch_all(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_url(client, url) for url in urls]
        return await asyncio.gather(*tasks)

# With concurrency limit
async def fetch_with_limit(urls: list[str], limit: int = 10) -> list[str]:
    semaphore = asyncio.Semaphore(limit)
    
    async def bounded_fetch(client, url):
        async with semaphore:
            return await fetch_url(client, url)
    
    async with httpx.AsyncClient() as client:
        tasks = [bounded_fetch(client, url) for url in urls]
        return await asyncio.gather(*tasks)
```
### Multiprocessing (For CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

def cpu_intensive(data):
    # Heavy computation
    return sum(x ** 2 for x in data)

def process_parallel(items: list, workers: int = None):
    workers = workers or mp.cpu_count()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(cpu_intensive, items))
```
### Thread Pool (For Blocking I/O)

```python
from concurrent.futures import ThreadPoolExecutor

def blocking_io(item):
    # Blocking operation (e.g., file I/O, legacy API)
    return process(item)

def process_threaded(items: list, workers: int = 10):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(blocking_io, items))
```
---

## 3. Common Patterns

### Producer-Consumer

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, items: list):
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel

async def consumer(queue: Queue, process_func):
    while True:
        item = await queue.get()
        if item is None:
            break
        await process_func(item)

async def run_pipeline(items, process_func, num_consumers=3):
    queue = Queue(maxsize=100)
    
    consumers = [
        asyncio.create_task(consumer(queue, process_func))
        for _ in range(num_consumers)
    ]
    
    await producer(queue, items)
    
    # Send sentinel to each consumer
    for _ in range(num_consumers - 1):
        await queue.put(None)
    
    await asyncio.gather(*consumers)
```
### Worker Pool

```python
import asyncio
from typing import Callable, Any

class WorkerPool:
    def __init__(self, num_workers: int = 5):
        self.num_workers = num_workers
        self.queue = asyncio.Queue()
        self.workers = []
    
    async def worker(self):
        while True:
            func, args, future = await self.queue.get()
            try:
                result = await func(*args)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self.queue.task_done()
    
    async def start(self):
        self.workers = [
            asyncio.create_task(self.worker())
            for _ in range(self.num_workers)
        ]
    
    async def submit(self, func: Callable, *args) -> Any:
        future = asyncio.get_event_loop().create_future()
        await self.queue.put((func, args, future))
        return await future
    
    async def shutdown(self):
        await self.queue.join()
        for worker in self.workers:
            worker.cancel()
```
---

## 4. Best Practices

### Do's

- ✅ Use `asyncio` for I/O-bound concurrent work
- ✅ Use `multiprocessing` for CPU-bound parallel work
- ✅ Limit concurrency with semaphores
- ✅ Handle exceptions in all tasks
- ✅ Use context managers for resource cleanup
- ✅ Set timeouts on async operations

### Don'ts

- ❌ Don't share mutable state without locks
- ❌ Don't use threads for CPU-bound in Python
- ❌ Don't create unlimited concurrent tasks
- ❌ Don't ignore task exceptions
- ❌ Don't mix sync and async carelessly

### Error Handling

```python
async def safe_gather(tasks):
    """Gather with proper error handling."""
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    errors = [r for r in results if isinstance(r, Exception)]
    successes = [r for r in results if not isinstance(r, Exception)]
    
    if errors:
        logger.error(f"{len(errors)} tasks failed")
    
    return successes, errors
```
---

## Related

- `.knowledge/frameworks/performance/OPTIMIZATION_STRATEGIES.md` — Performance optimization
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns

---

*AI Collaboration Knowledge Base*
