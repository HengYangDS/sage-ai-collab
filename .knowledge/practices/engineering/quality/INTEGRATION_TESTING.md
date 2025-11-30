# Integration Testing

> Best practices for testing component interactions and system integration

---

## Table of Contents

- [1. Overview](#1-overview)

- [2. Test Categories](#2-test-categories)

- [3. Database Testing](#3-database-testing)

- [4. API Testing](#4-api-testing)

- [5. Service Integration](#5-service-integration)

- [6. Test Isolation](#6-test-isolation)

- [7. CI/CD Integration](#7-cicd-integration)

---

## 1. Overview

### 1.1 Integration vs Unit Tests

| Aspect | Unit Tests | Integration Tests |
|------------------|-------------------|-----------------------|
| **Scope**        | Single unit | Multiple components |
| **Dependencies** | Mocked | Real or test doubles |
| **Speed**        | Fast (< 100ms)    | Slower (100ms - 5s)   |
| **Isolation**    | Complete | Partial |
| **Purpose**      | Logic correctness | Component interaction |

### 1.2 Integration Test Goals

| Goal | Description |

|------------------------|----------------------------------|
| **Verify interfaces**  | Components communicate correctly |
| **Test data flow**     | Data passes through layers |
| **Validate config**    | Configuration works together |
| **Check side effects** | External effects occur correctly |

---

## 2. Test Categories

### 2.1 Test Types

```mermaid
flowchart TB
    subgraph Pyramid["Test Pyramid"]
        E2E["E2E Tests<br/>(Full system, browser, real services)"]
        INT["Integration Tests<br/>(Multiple components, test database)"]
        UNIT["Unit Tests<br/>(Single unit, mocked deps)"]
    end
    
    E2E --> INT --> UNIT
```
### 2.2 Integration Test Scope

| Scope | Components | Example |
|------------|-----------------|----------------------|
| **Narrow** | 2-3 components | Service + Repository |
| **Medium** | Layer | API → Service → DB |
| **Broad**  | Multiple layers | Full request flow |

---

## 3. Database Testing

### 3.1 Test Database Setup

```python
import pytest

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def test_engine():

    """Create test database engine."""

    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    return engine

@pytest.fixture(scope="function")
def db_session(test_engine):

    """Create a new database session for each test."""

    Session = sessionmaker(bind=test_engine)

    session = Session()

    yield session

    session.rollback()

    session.close()

```
### 3.2 Database Fixtures

```python
@pytest.fixture
def sample_users(db_session):

    """Create sample users in test database."""

    users = [

        User(id="1", name="Alice", email="alice@test.com"),

        User(id="2", name="Bob", email="bob@test.com"),

    ]

    for user in users:

        db_session.add(user)

    db_session.commit()

    return users

def test_get_all_users(db_session, sample_users):

    repo = UserRepository(db_session)

    result = repo.get_all()

    assert len(result) == 2

    assert result[0].name == "Alice"

```
### 3.3 Transaction Rollback

```python
@pytest.fixture
def db_session(test_engine):

    """Session with automatic rollback after each test."""

    connection = test_engine.connect()

    transaction = connection.begin()

    Session = sessionmaker(bind=connection)

    session = Session()

    yield session

    session.close()

    transaction.rollback()

    connection.close()

```
### 3.4 Test Data Management

```python
class TestDataBuilder:

    """Builder for creating test data."""

    def __init__(self, session):
        self.session = session

    def create_user(self, **kwargs) -> User:
        defaults = {

            "id"   : str(uuid.uuid4()),

            "name" : "Test User",

            "email": f"test-{uuid.uuid4()}@example.com",

        }

        user = User(**{**defaults, **kwargs})

        self.session.add(user)

        self.session.commit()

        return user

    def create_order(self, user: User, **kwargs) -> Order:
        defaults = {

            "id"     : str(uuid.uuid4()),

            "user_id": user.id,

            "status" : "pending",

        }

        order = Order(**{**defaults, **kwargs})

        self.session.add(order)

        self.session.commit()

        return order

```
---

## 4. API Testing

### 4.1 FastAPI Testing

```python
import pytest

from fastapi.testclient import TestClient

from httpx import AsyncClient

from app.main import app

@pytest.fixture
def client():

    """Sync test client."""

    return TestClient(app)

@pytest.fixture
async def async_client():

    """Async test client."""

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

def test_get_users(client):

    response = client.get("/api/users")

    assert response.status_code == 200

    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user(async_client):

    response = await async_client.post(

        "/api/users",

        json={"name": "Alice", "email": "alice@test.com"}

    )

    assert response.status_code == 201

    assert response.json()["name"] == "Alice"

```
### 4.2 Request/Response Testing

```python
class TestUserAPI:

    """Integration tests for User API."""

    def test_create_user_success(self, client, db_session):
        # Arrange

        payload = {"name": "Alice", "email": "alice@test.com"}

        # Act

        response = client.post("/api/users", json=payload)

        # Assert response

        assert response.status_code == 201

        data = response.json()

        assert data["name"] == "Alice"

        assert "id" in data

        # Assert database

        user = db_session.query(User).filter_by(id=data["id"]).first()

        assert user is not None

        assert user.email == "alice@test.com"

    def test_create_user_duplicate_email(self, client, sample_users):
        payload = {"name": "Duplicate", "email": sample_users[0].email}

        response = client.post("/api/users", json=payload)

        assert response.status_code == 409

        assert "already exists" in response.json()["detail"]

```
### 4.3 Authentication Testing

```python
@pytest.fixture
def auth_headers(client):

    """Get authentication headers."""

    response = client.post(

        "/auth/login",

        json={"email": "admin@test.com", "password": "password"}

    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(client, auth_headers):

    response = client.get("/api/admin/users", headers=auth_headers)

    assert response.status_code == 200

def test_protected_endpoint_without_auth(client):

    response = client.get("/api/admin/users")

    assert response.status_code == 401

```
---

## 5. Service Integration

### 5.1 Service Layer Testing

```python
class TestOrderService:

    """Integration tests for OrderService."""

    @pytest.fixture
    def order_service(self, db_session):
        """Create OrderService with real dependencies."""

        user_repo = UserRepository(db_session)

        order_repo = OrderRepository(db_session)

        return OrderService(user_repo, order_repo)

    def test_create_order(self, order_service, sample_users):
        user = sample_users[0]

        items = [{"product_id": "p1", "quantity": 2}]

        order = order_service.create_order(user.id, items)

        assert order.id is not None

        assert order.user_id == user.id

        assert order.status == "pending"

    def test_create_order_invalid_user(self, order_service):
        with pytest.raises(UserNotFoundError):
            order_service.create_order("invalid-id", [])

```
### 5.2 External Service Mocking

```python
import responses

import httpx

@pytest.fixture
def mock_payment_service():

    """Mock external payment service."""

    with responses.RequestsMock() as rsps:
        rsps.add(

            responses.POST,

            "https://api.payment.com/charge",

            json={"status": "success", "transaction_id": "tx123"},

            status=200,

        )

        yield rsps

def test_process_payment(order_service, mock_payment_service):

    result = order_service.process_payment("order123", 100.00)

    assert result.success is True

    assert result.transaction_id == "tx123"

```
### 5.3 Event/Message Testing

```python
@pytest.fixture
def event_bus():

    """Create test event bus."""

    bus = EventBus()

    yield bus

    bus.clear()

def test_order_created_event(order_service, event_bus, sample_users):

    events = []

    event_bus.subscribe("order.created", lambda e: events.append(e))

    order = order_service.create_order(sample_users[0].id, [])

    assert len(events) == 1

    assert events[0].data["order_id"] == order.id

```
---

## 6. Test Isolation

### 6.1 Database Isolation

```python
@pytest.fixture(autouse=True)
def reset_database(db_session):

    """Reset database state before each test."""

    yield

    # Clean up after test

    db_session.query(Order).delete()

    db_session.query(User).delete()

    db_session.commit()

```
### 6.2 Test Containers

```python
import pytest

from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres():

    """Start PostgreSQL container for tests."""

    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture
def db_url(postgres):

    """Get database URL from container."""

    return postgres.get_connection_url()

```
### 6.3 Environment Isolation

```python
@pytest.fixture
def test_env(monkeypatch):

    """Set up test environment variables."""

    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("API_KEY", "test-key")
    monkeypatch.setenv("DEBUG", "true")
```
---

## 7. CI/CD Integration

### 7.1 GitHub Actions Example

```yaml
name: Integration Tests
on: [ push, pull_request ]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -e ".[dev]"
      - name: Run integration tests
        run: pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
```
### 7.2 Test Markers

```python
# conftest.py

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(

        "markers", "slow: mark test as slow running"
    )

# Run only integration tests
# pytest -m integration
# Skip slow tests
# pytest -m "not slow"
```
### 7.3 Test Organization

```
tests/

├── unit/                    # Fast, isolated tests
│   ├── test_models.py
│   └── test_services.py
├── integration/             # Component integration
│   ├── test_api.py
│   ├── test_database.py
│   └── test_services.py
├── e2e/                     # Full system tests
│   └── test_workflows.py
└── conftest.py              # Shared fixtures
```
---

## Quick Reference

### Integration Test Checklist

| Check | Description |

|----------------------------|--------------------------|
| ☐ Test database configured | Isolated from production |
| ☐ Data cleanup | Reset between tests |
| ☐ Real dependencies | Where appropriate |
| ☐ External services mocked | When needed |
| ☐ CI/CD compatible | Works in pipeline |

### Common Fixtures

| Fixture | Purpose |
|-----------------|-----------------------|
| `db_session`    | Database session |
| `client`        | HTTP test client |
| `sample_data`   | Pre-populated data |
| `auth_headers`  | Authentication |
| `mock_external` | External service mock |

---

## Related

- `.knowledge/practices/engineering/UNIT_TESTING_PATTERNS.md` — Unit testing
- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing strategy

---

*AI Collaboration Knowledge Base*

