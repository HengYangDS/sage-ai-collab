# Logging Standards

> Universal logging standards and best practices

---

## Table of Contents

- [1. Log Levels](#1-log-levels)
- [2. Structured Logging](#2-structured-logging)
- [3. Required Fields](#3-required-fields)
- [4. Message Content Standards](#4-message-content-standards)
- [5. Performance Logging](#5-performance-logging)
- [6. Error Logging](#6-error-logging)
- [7. Log Configuration](#7-log-configuration)
- [8. Quick Checklist](#8-quick-checklist)
- [9. Log Analysis Tips](#9-log-analysis-tips)

---

## 1. Log Levels

| Level        | Purpose                           | Examples                          |
|--------------|-----------------------------------|-----------------------------------|
| **DEBUG**    | Development debug info            | Variable values, execution paths  |
| **INFO**     | Normal business events            | Request processed, task completed |
| **WARNING**  | Potential issues, recoverable     | Retry succeeded, fallback used    |
| **ERROR**    | Errors affecting functionality    | Request failed, data anomaly      |
| **CRITICAL** | Severe errors, system unavailable | Service crash, data loss          |

### Level Selection Guide

```
Can continue normally? ─Yes─▶ INFO
        │
        No
        ▼
Can auto-recover? ─Yes─▶ WARNING
        │
        No
        ▼
Affects single request? ─Yes─▶ ERROR
        │
        No
        ▼
Affects entire service? ─Yes─▶ CRITICAL
```
---

## 2. Structured Logging

### Recommended Format

```python
logger.info(
    "Request processed",
    extra={
        "request_id" : "abc-123",
        "user_id"    : 42,
        "duration_ms": 150,
        "status"     : "success"
    }
)
```
### Output Example (JSON)

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "Request processed",
  "request_id": "abc-123",
  "user_id": 42,
  "duration_ms": 150,
  "status": "success"
}
```
---

## 3. Required Fields

### Common Fields

| Field       | Description       | Example                |
|-------------|-------------------|------------------------|
| `timestamp` | ISO 8601 format   | `2024-01-15T10:30:00Z` |
| `level`     | Log level         | `INFO`                 |
| `message`   | Brief description | `User login`           |
| `logger`    | Log source        | `app.auth`             |

### Request-Related

| Field         | Description                 |
|---------------|-----------------------------|
| `request_id`  | Request trace ID            |
| `user_id`     | User identifier (sanitized) |
| `duration_ms` | Processing time             |
| `status_code` | HTTP status code            |

### Error-Related

| Field           | Description          |
|-----------------|----------------------|
| `error_code`    | Error code           |
| `error_message` | Error description    |
| `stack_trace`   | Stack trace (ERROR+) |

---

## 4. Message Content Standards

### Message Format

| ✓ Good                        | ✗ Bad                |
|-------------------------------|----------------------|
| `User login failed`           | `Error!!!`           |
| `Order created: order_id=123` | `Something happened` |
| `Cache miss for key: user_42` | `cache`              |
| `Retry attempt 2/3`           | `retrying...`        |

### Sensitive Information Handling

| Data Type   | Handling                 |
|-------------|--------------------------|
| Passwords   | Never log                |
| API keys    | Never log                |
| Tokens      | Last 4 chars only        |
| Email       | Mask: `j***@example.com` |
| Phone       | Mask: `***-***-1234`     |
| Credit card | Last 4 digits only       |

### Masking Example

```python
def mask_email(email: str) -> str:
    local, domain = email.split("@")
    return f"{local[0]}***@{domain}"

def mask_token(token: str) -> str:
    return f"***{token[-4:]}"
```
---

## 5. Performance Logging

### Timing Pattern

```python
import time

start = time.perf_counter()
result = process_request()
duration_ms = (time.perf_counter() - start) * 1000

logger.info(
    "Request completed",
    extra={"duration_ms": round(duration_ms, 2)}
)
```
### Performance Thresholds

| Duration  | Level   | Action      |
|-----------|---------|-------------|
| < 100ms   | DEBUG   | Normal      |
| 100-500ms | INFO    | Monitor     |
| 500ms-2s  | WARNING | Investigate |
| > 2s      | ERROR   | Alert       |

---

## 6. Error Logging

### Error Log Content

```python
try:
    process_order(order_id)
except OrderError as e:
    logger.error(
        "Order processing failed",
        extra={
            "order_id"     : order_id,
            "error_code"   : e.code,
            "error_message": str(e),
            "retry_count"  : retry_count,
        },
        exc_info=True  # Include stack trace
    )
```
### Error Context Checklist

- [ ] What operation failed?
- [ ] What was the input?
- [ ] What was the error?
- [ ] What was the system state?
- [ ] Is it retryable?

---

## 7. Log Configuration

### Environment-Based Levels

| Environment | Default Level | Notes             |
|-------------|---------------|-------------------|
| Development | DEBUG         | Full details      |
| Testing     | INFO          | Test coverage     |
| Staging     | INFO          | Production-like   |
| Production  | WARNING       | Performance focus |

### Configuration Example

```yaml
logging:
  level: INFO
  format: structured
  output:
    console: true
    file: false

  # Per-module levels
  modules:
    app.core: INFO
    app.services: INFO
    app.external: WARNING
```
---

## 8. Quick Checklist

| ✓ Do                       | ✗ Don't                  |
|----------------------------|--------------------------|
| Use structured logging     | Use string concatenation |
| Include request_id         | Log without context      |
| Mask sensitive data        | Log passwords/tokens     |
| Set appropriate levels     | Log everything as INFO   |
| Include timing metrics     | Ignore performance       |
| Use consistent field names | Vary field naming        |

---

## 9. Log Analysis Tips

### Common Queries

| Purpose       | Query Pattern                  |
|---------------|--------------------------------|
| Error rate    | `level:ERROR \| count by time` |
| Slow requests | `duration_ms:>1000`            |
| User activity | `user_id:123`                  |
| Request trace | `request_id:abc-123`           |

### Alerting Thresholds

| Metric           | Warning     | Critical    |
|------------------|-------------|-------------|
| Error rate       | > 1%        | > 5%        |
| P99 latency      | > 1s        | > 5s        |
| Log volume spike | 2x baseline | 5x baseline |

---

## Related

- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `config/core/logging.yaml` — Logging configuration
- `.knowledge/guidelines/ENGINEERING.md` — Engineering guidelines

---

*AI Collaboration Knowledge Base*
