# Monitoring & Observability

> Best practices for system monitoring and observability

---

## Table of Contents

- [1. Three Pillars](#1-three-pillars)
- [2. Metrics](#2-metrics)
- [3. Logging](#3-logging)
- [4. Tracing](#4-tracing)
- [5. Alerting](#5-alerting)

---

## 1. Three Pillars

### Observability Overview

| Pillar      | Purpose                   | Tools               |
|-------------|---------------------------|---------------------|
| **Metrics** | Quantitative measurements | Prometheus, Grafana |
| **Logs**    | Event records             | ELK, Loki           |
| **Traces**  | Request flow              | Jaeger, Zipkin      |

```mermaid
flowchart LR
    subgraph Observability
        M["Metrics<br/>'What' happened"] <--> L["Logs<br/>'Why' happened"]
        L <--> T["Traces<br/>'Where' happened"]
    end
```
---

## 2. Metrics

### Key Metrics (RED/USE)

**RED Method (Services):**

- **R**ate: Requests per second
- **E**rrors: Failed requests per second
- **D**uration: Request latency

**USE Method (Resources):**

- **U**tilization: % time busy
- **S**aturation: Queue depth
- **E**rrors: Error count

### Implementation

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Counters
requests_total = Counter(
    'requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

# Histograms
request_duration = Histogram(
    'request_duration_seconds',
    'Request duration',
    ['endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

# Gauges
active_connections = Gauge(
    'active_connections',
    'Current active connections'
)

# Usage
def handle_request(endpoint):
    active_connections.inc()
    start = time.time()
    try:
        result = process_request()
        requests_total.labels(
            method='GET',
            endpoint=endpoint,
            status='200'
        ).inc()
        return result
    finally:
        duration = time.time() - start
        request_duration.labels(endpoint=endpoint).observe(duration)
        active_connections.dec()
```
---

## 3. Logging

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# ✅ Good: Structured with context
logger.info(
    "order_created",
    order_id=order.id,
    user_id=user.id,
    amount=order.total,
    items=len(order.items)
)

# ❌ Bad: Unstructured string
logger.info(f"Order {order.id} created for user {user.id}")
```
### Log Levels

| Level     | Use Case                       |
|-----------|--------------------------------|
| **ERROR** | Failures requiring attention   |
| **WARN**  | Unexpected but handled         |
| **INFO**  | Business events, state changes |
| **DEBUG** | Development troubleshooting    |

### Best Practices

- ✅ Use structured logging (JSON)
- ✅ Include correlation IDs
- ✅ Log at appropriate levels
- ✅ Include relevant context
- ❌ Don't log sensitive data
- ❌ Don't log in hot paths excessively

---

## 4. Tracing

### Distributed Tracing

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind

tracer = trace.get_tracer(__name__)

async def handle_request(request):
    with tracer.start_as_current_span(
        "handle_request",
        kind=SpanKind.SERVER
    ) as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        
        # Child span for database
        with tracer.start_as_current_span("db_query"):
            result = await db.query(...)
        
        return result
```
### Context Propagation

```python
# Extract trace context from incoming request
context = extract(request.headers)

# Propagate to outgoing requests
headers = {}
inject(headers)
await client.get(url, headers=headers)
```
---

## 5. Alerting

### Alert Design

| Severity     | Response          | Example         |
|--------------|-------------------|-----------------|
| **Critical** | Immediate         | Service down    |
| **Warning**  | Hours             | High error rate |
| **Info**     | Next business day | Disk 70%        |

### Good Alerts

- ✅ Actionable: Clear remediation
- ✅ Relevant: Affects users/SLOs
- ✅ Unique: Not duplicate
- ✅ Timely: Appropriate urgency

### Alert Examples

```yaml
# Prometheus alerting rules
groups:
  - name: service-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(requests_total{status=~"5.."}[5m]) / rate(requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate ({{ $value | humanizePercentage }})"
      
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
```
---

## Quick Reference

### Monitoring Checklist

- [ ] RED metrics for services
- [ ] USE metrics for resources
- [ ] Structured logging
- [ ] Distributed tracing
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] Runbooks written

### Key Dashboards

| Dashboard     | Metrics                        |
|---------------|--------------------------------|
| **Overview**  | Request rate, errors, latency  |
| **Resources** | CPU, memory, disk, network     |
| **Database**  | Query time, connections, locks |
| **Business**  | Users, transactions, revenue   |

---

## Related

- `.knowledge/practices/engineering/LOGGING.md` — Logging practices
- `.knowledge/frameworks/performance/PROFILING_FRAMEWORK.md` — Performance profiling

---

*AI Collaboration Knowledge Base*
