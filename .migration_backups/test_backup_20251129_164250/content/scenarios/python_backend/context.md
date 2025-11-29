# Python Backend Scenario Context

> **Load Time**: Scenario-specific (~150 tokens)  
> **Purpose**: Pre-configured context for Python backend development

---

## Scenario Profile

```yaml
scenario: python_backend
languages: [ python ]
frameworks: [ fastapi, flask, django ]
focus: [ api, database, testing, deployment ]
autonomy_default: L2
```

---

## Relevant Knowledge

### Auto-Load (Always)

- 01_core/principles.md
- 02_guidelines/05_python.md
- 04_practices/engineering/patterns.md

### Load on Demand

- 02_guidelines/03_engineering.md (testing, config)
- 03_frameworks/timeout/hierarchy.md (external calls)
- 06_templates/project_setup.md (new projects)

---

## Common Patterns

### FastAPI Project Structure

```
project/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py           # FastAPI app
│       ├── config.py         # Settings
│       ├── models/           # Pydantic models
│       ├── schemas/          # Request/Response schemas
│       ├── services/         # Business logic
│       ├── repositories/     # Data access
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py       # Dependencies
│       │   └── routes/       # Endpoints
│       └── core/
│           ├── security.py
│           └── exceptions.py
├── tests/
├── alembic/                  # Migrations
└── pyproject.toml
```

### Standard Endpoint Pattern

```python
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """List all users with pagination."""
    return await service.list(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get user by ID."""
    user = await service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user
```

### Service Layer Pattern

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def create(self, data: UserCreate) -> User:
        # Validation
        if await self._repository.exists_by_email(data.email):
            raise EmailExistsError(data.email)

        # Create
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            name=data.name
        )
        return await self._repository.save(user)
```

### Repository Pattern

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, id: str) -> Optional[User]:
        result = await self._session.execute(
            select(User).where(User.id == id)
        )
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
```

---

## Testing Patterns

### Pytest Fixtures

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def user_factory():
    def _create_user(**kwargs):
        defaults = {
            "email": "test@example.com",
            "name" : "Test User"
        }
        return User(**{**defaults, **kwargs})

    return _create_user
```

### API Test Pattern

```python
@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient):
    # Arrange
    payload = {
        "email"   : "new@example.com",
        "password": "SecurePass123!",
        "name"    : "New User"
    }

    # Act
    response = await client.post("/api/users/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
```

---

## Configuration Pattern

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "My API"
    debug: bool = False

    # Database
    database_url: str
    database_pool_size: int = 5

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30

    # External Services
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

---

## Common Tasks

### Task: Add New Endpoint

```
1. Define schema (schemas/)
2. Add service method (services/)
3. Add repository method if needed (repositories/)
4. Create route (api/routes/)
5. Add tests
6. Update OpenAPI docs if needed
```

### Task: Add Database Migration

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Review generated migration
# Apply migration
alembic upgrade head
```

### Task: Add Background Task

```python
from fastapi import BackgroundTasks


@router.post("/users/")
async def create_user(
    data: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserService = Depends()
):
    user = await service.create(data)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
```

---

## Autonomy Calibration

> **Reference**: See `content/frameworks/autonomy/levels.md` for full 6-level framework

| Task Type               | Level | Notes                |
|-------------------------|-------|----------------------|
| New endpoint (standard) | L3    | Checkpoint at design |
| Database migration      | L1-L2 | Review before apply  |
| Bug fix (clear scope)   | L4    | Execute and report   |
| Refactoring             | L3    | Checkpoint at plan   |
| Test writing            | L4    | Execute and report   |
| Security changes        | L1-L2 | Full review required |

---

## Quick Commands

```bash
# Development
uvicorn app.main:app --reload

# Testing
pytest
pytest tests/unit/ -v
pytest --cov=app --cov-report=html

# Linting
ruff check .
mypy src/

# Database
alembic upgrade head
alembic downgrade -1
```

---

*Part of AI Collaboration Knowledge Base v2.0.0*
