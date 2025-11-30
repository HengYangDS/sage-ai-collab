# Python Backend Scenario Context

> Pre-configured context for Python backend development

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure-fastapi)
- [4. Common Patterns](#4-common-patterns)
- [5. Testing Patterns](#5-testing-patterns)
- [6. Configuration](#6-configuration)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)
- [9. Quick Commands](#9-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: python_backend
languages: [ python ]
frameworks: [ fastapi, flask, django ]
focus: [ api, database, testing, deployment ]
autonomy_default: L2
```
---

## 2. Relevant Knowledge

| Priority      | Files                                                                                          |
|---------------|------------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/PRINCIPLES.md`<br/>`.knowledge/guidelines/PYTHON.md`<br/>`.knowledge/practices/engineering/design/PATTERNS.md`            |
| **On-Demand** | `.knowledge/guidelines/ENGINEERING.md`<br/>`.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md`<br/>`.knowledge/templates/PROJECT_SETUP.md` |

---

## 3. Project Structure (FastAPI)

| Directory               | Purpose                  |
|-------------------------|--------------------------|
| `src/app/main.py`       | FastAPI app entry        |
| `src/app/config.py`     | Settings                 |
| `src/app/models/`       | Pydantic models          |
| `src/app/schemas/`      | Request/Response schemas |
| `src/app/services/`     | Business logic           |
| `src/app/repositories/` | Data access              |
| `src/app/api/routes/`   | Endpoints                |
| `src/app/core/`         | Security, exceptions     |
| `tests/`                | Test suite               |
| `alembic/`              | Migrations               |

---

## 4. Common Patterns

### 4.1 Endpoint Pattern

```python
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str, service: UserService = Depends(get_service)) -> UserResponse:
    user = await service.get(id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user
```
### 4.2 Service Layer

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self._repo = repository
    async def create(self, data: UserCreate) -> User:
        if await self._repo.exists_by_email(data.email):
            raise EmailExistsError(data.email)
        return await self._repo.save(User(email=data.email, password_hash=hash(data.password)))
```
### 4.3 Repository

```python
class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
    async def get(self, id: str) -> Optional[User]:
        result = await self._session.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()
```
---

## 5. Testing Patterns

### 5.1 Fixtures

```python
@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
@pytest.fixture
def user_factory():
    return lambda **kw: User(**{"email": "test@example.com", "name": "Test", **kw})
```
### 5.2 API Test

```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/users/", json={"email": "new@test.com", "password": "Pass123!"})
    assert response.status_code == 201
    assert "id" in response.json()
```
---

## 6. Configuration

```python
class Settings(BaseSettings):
    app_name: str = "My API"
    database_url: str
    secret_key: str
    class Config:
        env_file = ".env"
@lru_cache
def get_settings() -> Settings:
    return Settings()
```
---

## 7. Common Tasks

| Task                | Steps                                                                         |
|---------------------|-------------------------------------------------------------------------------|
| **Add Endpoint**    | Schema → Service method → Repository (if needed) → Route → Tests              |
| **DB Migration**    | `alembic revision --autogenerate -m "desc"` → Review → `alembic upgrade head` |
| **Background Task** | `background_tasks.add_task(func, *args)` in endpoint                          |

---

## 8. Autonomy Calibration

| Task Type               | Level | Notes                |
|-------------------------|-------|----------------------|
| New endpoint (standard) | L3    | Checkpoint at design |
| Database migration      | L1-L2 | Review before apply  |
| Bug fix (clear scope)   | L4    | Execute and report   |
| Refactoring             | L3    | Checkpoint at plan   |
| Test writing            | L4    | Execute and report   |
| Security changes        | L1-L2 | Full review required |

---

## 9. Quick Commands

| Category | Commands                                                |
|----------|---------------------------------------------------------|
| **Dev**  | `uvicorn app.main:app --reload`                         |
| **Test** | `pytest`<br/>`pytest tests/unit/ -v`<br/>`pytest --cov=app` |
| **Lint** | `ruff check .`<br/>`mypy src/`                            |
| **DB**   | `alembic upgrade head`<br/>`alembic downgrade -1`         |

---

## Related

- `.knowledge/guidelines/PYTHON.md` — Python guidelines
- `.knowledge/practices/engineering/design/PATTERNS.md` — Design patterns
- `.knowledge/frameworks/autonomy/LEVELS.md` — Autonomy framework

---

*AI Collaboration Knowledge Base*

