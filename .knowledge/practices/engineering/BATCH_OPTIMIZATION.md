# Batch Optimization Patterns

> Efficient processing of large-scale operations

---

## Table of Contents

- [1. Core Principles](#1-core-principles)
- [2. Batch Size Guidelines](#2-batch-size-guidelines)
- [3. Implementation Patterns](#3-implementation-patterns)
- [4. Checkpoint Strategy](#4-checkpoint-strategy)
- [5. Error Handling](#5-error-handling)
- [6. Performance Optimization](#6-performance-optimization)
- [7. Monitoring](#7-monitoring)

---

## 1. Core Principles

| Principle  | Description                    |
|------------|--------------------------------|
| Chunk work | Process in manageable batches  |
| Checkpoint | Save progress regularly        |
| Recover    | Handle failures gracefully     |
| Monitor    | Track progress and performance |

---

## 2. Batch Size Guidelines

| Data Size  | Batch Size  | Rationale             |
|------------|-------------|-----------------------|
| < 1K       | All at once | Overhead not worth it |
| 1K - 10K   | 100-500     | Balance speed/memory  |
| 10K - 100K | 500-1000    | Reasonable chunks     |
| > 100K     | 1000-5000   | Prevent memory issues |

---

## 3. Implementation Patterns

### 3.1 Basic Batching

```python
def process_in_batches(items: List, batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)
```
### 3.2 With Progress

```python
def process_with_progress(items: List, batch_size: int = 100):
    total = len(items)
    for i in range(0, total, batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)
        progress = min(i + batch_size, total) / total * 100
        logger.info(f"Progress: {progress:.1f}%")
```
---

## 4. Checkpoint Strategy

### 4.1 Checkpoint Data

```python
@dataclass
class Checkpoint:
    processed: int
    last_id: str
    timestamp: datetime
    state: Dict[str, Any]
```
### 4.2 Resume Pattern

```python
def process_with_checkpoint(items: List, checkpoint_file: str):
    checkpoint = load_checkpoint(checkpoint_file)
    start = checkpoint.processed if checkpoint else 0

    for i, item in enumerate(items[start:], start):
        process_item(item)
        if i % 100 == 0:
            save_checkpoint(checkpoint_file, i)
```
---

## 5. Error Handling

| Strategy    | Use When               |
|-------------|------------------------|
| Skip + log  | Non-critical items     |
| Retry       | Transient errors       |
| Abort       | Critical failures      |
| Dead letter | Process failures later |

```python
def process_with_errors(items: List):
    failed = []
    for item in items:
        try:
            process_item(item)
        except TransientError:
            retry_with_backoff(item)
        except PermanentError as e:
            failed.append((item, e))
            logger.warning(f"Skipping {item}: {e}")
    return failed
```
---

## 6. Performance Optimization

| Technique           | Benefit                 |
|---------------------|-------------------------|
| Parallel processing | Utilize multiple cores  |
| Async I/O           | Efficient for I/O-bound |
| Bulk operations     | Reduce round trips      |
| Connection pooling  | Reuse connections       |

---

## 7. Monitoring

| Metric         | Purpose         |
|----------------|-----------------|
| Items/second   | Throughput      |
| Error rate     | Quality         |
| Memory usage   | Resource health |
| Time remaining | ETA             |

---

## Related

- `.knowledge/frameworks/patterns/PERSISTENCE.md` — Data patterns
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling

---

*AI Collaboration Knowledge Base*
