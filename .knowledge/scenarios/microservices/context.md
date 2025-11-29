# Microservices Scenario Context

> Pre-configured context for microservices architecture development

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Architecture Patterns](#3-architecture-patterns)
- [4. Service Design](#4-service-design)
- [5. Communication Patterns](#5-communication-patterns)
- [6. Data Management](#6-data-management)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)

---

## 1. Scenario Profile

```yaml
scenario: microservices
languages: [ python, typescript, go, java ]
frameworks: [ fastapi, express, gin, spring ]
focus: [ service_design, api, messaging, deployment ]
autonomy_default: L3
```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                      |
|---------------|--------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/principles.md` · `guidelines/engineering.md` · `practices/engineering/api_design.md` |
| **On-Demand** | `guidelines/security.md` · `practices/engineering/error_handling.md`                       |

---

## 3. Architecture Patterns

### 3.1 Service Decomposition

| Pattern           | Description                            | When to Use            |
|-------------------|----------------------------------------|------------------------|
| **Domain-Driven** | Services aligned with business domains | Complex business logic |
| **Functional**    | Services by technical function         | Cross-cutting concerns |
| **Strangler Fig** | Gradual migration from monolith        | Legacy modernization   |

### 3.2 Service Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                         API Gateway                          │
├─────────┬─────────┬─────────┬─────────┬─────────────────────┤
│  User   │  Order  │ Product │ Payment │    Notification     │
│ Service │ Service │ Service │ Service │      Service        │
├─────────┴─────────┴─────────┴─────────┴─────────────────────┤
│                    Message Bus / Events                      │
├─────────────────────────────────────────────────────────────┤
│             Databases (per-service ownership)                │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Key Principles

| Principle                 | Description                                |
|---------------------------|--------------------------------------------|
| **Single Responsibility** | One service, one business capability       |
| **Loose Coupling**        | Services independent, communicate via APIs |
| **High Cohesion**         | Related functionality grouped together     |
| **Data Ownership**        | Each service owns its data                 |
| **Resilience**            | Design for failure                         |

---

## 4. Service Design

### 4.1 Service Template Structure

```
service-name/
├── src/
│   ├── api/           # API endpoints
│   ├── domain/        # Business logic
│   ├── infrastructure/  # External integrations
│   └── config/        # Configuration
├── tests/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### 4.2 API Design

```python
# FastAPI service example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Order Service",
    version="1.0.0",
    description="Handles order management"
)


class Order(BaseModel):
    id: str
    user_id: str
    items: list[dict]
    status: str


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await order_repository.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/orders", response_model=Order, status_code=201)
async def create_order(order: Order):
    created = await order_repository.create(order)
    await event_bus.publish("order.created", created)
    return created
```

### 4.3 Health Checks

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/health/ready")
async def readiness_check():
    db_ok = await check_database()
    cache_ok = await check_cache()

    if not (db_ok and cache_ok):
        raise HTTPException(status_code=503, detail="Not ready")

    return {"status": "ready", "checks": {"db": db_ok, "cache": cache_ok}}
```

---

## 5. Communication Patterns

### 5.1 Synchronous (HTTP/gRPC)

| Pattern      | Use Case         | Consideration             |
|--------------|------------------|---------------------------|
| **REST API** | CRUD operations  | Simple, widely supported  |
| **gRPC**     | High performance | Binary protocol, code gen |
| **GraphQL**  | Flexible queries | Client-driven             |

### 5.2 Asynchronous (Events/Messages)

| Pattern                 | Use Case                 | Example                  |
|-------------------------|--------------------------|--------------------------|
| **Event Notification**  | State change broadcast   | OrderCreated event       |
| **Event-Carried State** | Data transfer via events | Full order data in event |
| **Command**             | Request action           | ProcessPaymentCommand    |
| **Saga**                | Distributed transactions | Order fulfillment flow   |

### 5.3 Event Example

```python
# Publishing events
class OrderCreatedEvent(BaseModel):
    event_type: str = "order.created"
    timestamp: datetime
    data: dict


async def create_order(order: Order):
    saved = await repository.save(order)

    event = OrderCreatedEvent(
        timestamp=datetime.utcnow(),
        data={"order_id": saved.id, "user_id": saved.user_id}
    )
    await message_bus.publish("orders", event)

    return saved


# Consuming events
async def handle_order_created(event: OrderCreatedEvent):
    # Send notification
    await notification_service.send(
        user_id=event.data["user_id"],
        message=f"Order {event.data['order_id']} confirmed"
    )
```

### 5.4 Circuit Breaker

```python
from circuitbreaker import circuit


@circuit(failure_threshold=5, recovery_timeout=30)
async def call_payment_service(order_id: str):
    response = await http_client.post(
        f"{PAYMENT_SERVICE_URL}/payments",
        json={"order_id": order_id}
    )
    return response.json()
```

---

## 6. Data Management

### 6.1 Database per Service

| Approach                              | Pros                 | Cons                       |
|---------------------------------------|----------------------|----------------------------|
| **Separate databases**                | Full isolation       | Cross-service queries hard |
| **Shared database, separate schemas** | Easier ops           | Coupling risk              |
| **Polyglot persistence**              | Best fit per service | Operational complexity     |

### 6.2 Data Consistency Patterns

| Pattern            | Use Case                 | Implementation                |
|--------------------|--------------------------|-------------------------------|
| **Saga**           | Distributed transactions | Choreography or orchestration |
| **Event Sourcing** | Audit, temporal queries  | Event store                   |
| **CQRS**           | Read/write optimization  | Separate models               |

### 6.3 Saga Example (Choreography)

```
Order Service          Payment Service       Inventory Service
      │                       │                      │
      │ OrderCreated          │                      │
      │──────────────────────>│                      │
      │                       │ PaymentProcessed     │
      │                       │─────────────────────>│
      │                       │                      │ InventoryReserved
      │<─────────────────────────────────────────────│
      │ OrderCompleted        │                      │
```

---

## 7. Common Tasks

| Task                      | Steps                                                            |
|---------------------------|------------------------------------------------------------------|
| **Create new service**    | Template → Domain model → API → Tests → Docker → Deploy          |
| **Add endpoint**          | Define contract → Implement handler → Add tests → Document       |
| **Service communication** | Define interface → Implement client → Add circuit breaker → Test |
| **Add event**             | Define schema → Publish → Subscribe → Test end-to-end            |
| **Database migration**    | Create migration → Test → Deploy → Verify                        |

### 7.1 Service Creation Checklist

| Item                             | Status |
|----------------------------------|--------|
| ☐ Service boundaries defined     |        |
| ☐ API contract documented        |        |
| ☐ Health endpoints implemented   |        |
| ☐ Logging and tracing configured |        |
| ☐ Error handling standardized    |        |
| ☐ Tests (unit, integration)      |        |
| ☐ Docker configuration           |        |
| ☐ CI/CD pipeline                 |        |
| ☐ Monitoring and alerts          |        |

---

## 8. Autonomy Calibration

| Task Type                        | Level | Notes                    |
|----------------------------------|-------|--------------------------|
| Add endpoint to existing service | L3-L4 | Follow existing patterns |
| Create new service               | L2-L3 | Checkpoint at design     |
| Cross-service communication      | L2-L3 | Review interface design  |
| Database schema change           | L2    | Data migration risk      |
| Event schema change              | L2    | Breaking change risk     |
| Infrastructure changes           | L1-L2 | Production impact        |
| Security configuration           | L1-L2 | Full review required     |

---

## Quick Commands

| Category     | Commands                                                  |
|--------------|-----------------------------------------------------------|
| **Docker**   | `docker-compose up -d` · `docker-compose logs -f service` |
| **API Test** | `curl localhost:8000/health` · `httpie POST :8000/orders` |
| **Logs**     | `docker-compose logs -f --tail=100`                       |
| **Debug**    | `docker-compose exec service bash`                        |

---

## Related

- `.knowledge/guidelines/engineering.md` — Engineering practices
- `.knowledge/practices/engineering/api_design.md` — API design patterns
- `.knowledge/guidelines/security.md` — Security guidelines
- `.knowledge/frameworks/patterns/collaboration.md` — Collaboration patterns

---

*Part of SAGE Knowledge Base*
