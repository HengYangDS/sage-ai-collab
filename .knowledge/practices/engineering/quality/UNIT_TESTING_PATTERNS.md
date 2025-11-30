# Unit Testing Patterns

> Best practices and patterns for writing effective unit tests

---

## Table of Contents

- [1. Overview](#1-overview)

- [2. Test Structure](#2-test-structure)

- [3. Naming Conventions](#3-naming-conventions)

- [4. Fixtures](#4-fixtures)

- [5. Mocking](#5-mocking)

- [6. Assertions](#6-assertions)

- [7. Async Testing](#7-async-testing)

- [8. Parameterized Tests](#8-parameterized-tests)

---

## 1. Overview

### 1.1 Unit Test Principles

| Principle           | Description                             |

|---------------------|-----------------------------------------|

| **Fast**            | Tests should run quickly (< 100ms each) |

| **Isolated**        | No dependencies between tests           |

| **Repeatable**      | Same result every time                  |

| **Self-validating** | Pass or fail, no manual inspection      |

| **Thorough**        | Cover edge cases and error paths        |

### 1.2 Test Pyramid

```text
        /\

       /  \    E2E (few)

      /----\

     /      \  Integration

    /--------\

   /          \ Unit Tests (many)

  --------------

```
---

## 2. Test Structure

### 2.1 Arrange-Act-Assert (AAA)

```python
def test_user_can_be_created():

    # Arrange - Set up test data and conditions

    user_data = {"name": "Alice", "email": "alice@example.com"}

    service = UserService()

    # Act - Execute the code under test

    user = service.create(user_data)

    # Assert - Verify the results

    assert user.name == "Alice"

    assert user.email == "alice@example.com"

    assert user.id is not None

```
### 2.2 Given-When-Then (BDD Style)

```python
def test_user_registration():

    # Given a new user with valid data

    user_data = {"name": "Bob", "email": "bob@example.com"}

    service = UserService()

    # When the user registers

    result = service.register(user_data)

    # Then the registration succeeds

    assert result.success is True

    assert result.user.email == "bob@example.com"

```
### 2.3 Test Class Organization

```python
class TestUserService:

    """Tests for UserService."""

    class TestCreate:

        """Tests for create method."""

        def test_creates_user_with_valid_data(self): ...

        def test_raises_error_for_invalid_email(self): ...

        def test_raises_error_for_duplicate_email(self): ...

    class TestGet:

        """Tests for get method."""

        def test_returns_user_by_id(self): ...

        def test_returns_none_for_missing_user(self): ...

```
---

## 3. Naming Conventions

### 3.1 Test Function Names

| Pattern                   | Example                             |

|---------------------------|-------------------------------------|

| `test_<what>_<condition>` | `test_login_with_valid_credentials` |

| `test_<action>_<result>`  | `test_create_returns_new_user`      |

| `test_<scenario>`         | `test_user_can_reset_password`      |

### 3.2 Good vs Bad Names

```python
# ❌ Bad - Unclear what's being tested

def test_user():

    ...

def test_1():

    ...

def test_it_works():

    ...

# ✅ Good - Clear and descriptive

def test_create_user_with_valid_email_succeeds():

    ...

def test_create_user_with_invalid_email_raises_validation_error():

    ...

def test_get_user_returns_none_when_not_found():

    ...

```
---

## 4. Fixtures

### 4.1 Basic Fixtures

```python
import pytest

@pytest.fixture

def user():

    """Create a test user."""

    return User(id="1", name="Test User", email="test@example.com")

@pytest.fixture

def user_service(mock_repository):

    """Create UserService with mocked repository."""

    return UserService(repository=mock_repository)

def test_get_user(user_service, user):

    result = user_service.get(user.id)

    assert result == user

```
### 4.2 Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - new for each test

def user():

    ...

@pytest.fixture(scope="class")  # Shared within test class

def database():

    ...

@pytest.fixture(scope="module")  # Shared within module

def config():

    ...

@pytest.fixture(scope="session")  # Shared across all tests

def app():

    ...

```
### 4.3 Factory Fixtures

```python
@pytest.fixture

def user_factory():

    """Factory for creating users with custom attributes."""

    def _create_user(**kwargs):

        defaults = {

            "id"   : "1",

            "name" : "Test User",

            "email": "test@example.com",

        }

        return User(**{**defaults, **kwargs})

    return _create_user

def test_user_with_custom_name(user_factory):

    user = user_factory(name="Alice")

    assert user.name == "Alice"

```
### 4.4 Temporary Resources

```python
@pytest.fixture

def temp_config_file(tmp_path):

    """Create temporary config file."""

    config_file = tmp_path / "config.yaml"

    config_file.write_text("debug: true\n")

    return config_file

def test_load_config(temp_config_file):

    config = load_config(temp_config_file)

    assert config["debug"] is True

```
---

## 5. Mocking

### 5.1 Basic Mocking

```python
from unittest.mock import Mock, MagicMock

def test_service_calls_repository():

    # Create mock

    mock_repo = Mock()

    mock_repo.get.return_value = User(id="1", name="Test")

    # Inject mock

    service = UserService(repository=mock_repo)

    # Call method

    result = service.get("1")

    # Verify interactions

    mock_repo.get.assert_called_once_with("1")

    assert result.name == "Test"

```
### 5.2 Patching

```python
from unittest.mock import patch

def test_send_email():

    with patch("myapp.email.send_email") as mock_send:

        mock_send.return_value = True

        result = notify_user("user@example.com", "Hello")

        mock_send.assert_called_once()

        assert result is True

# Using decorator

@patch("myapp.email.send_email")

def test_send_email(mock_send):

    mock_send.return_value = True

    result = notify_user("user@example.com", "Hello")

    assert result is True

```
### 5.3 Mock Side Effects

```python
def test_retry_on_failure():

    mock_service = Mock()

    # First call fails, second succeeds

    mock_service.call.side_effect = [

        ConnectionError("Failed"),

        {"status": "ok"}

    ]

    result = retry_call(mock_service, max_retries=3)

    assert result == {"status": "ok"}

    assert mock_service.call.call_count == 2

```
### 5.4 Pytest-Mock

```python
def test_with_mocker(mocker):

    # mocker is a pytest-mock fixture

    mock_func = mocker.patch("myapp.utils.expensive_operation")

    mock_func.return_value = 42

    result = process_data()

    assert result == 42

    mock_func.assert_called_once()

```
---

## 6. Assertions

### 6.1 Basic Assertions

```python
# Equality

assert result == expected

assert result != other

# Identity

assert result is None

assert result is not None

# Truthiness

assert result

assert not result

# Containment

assert item in collection

assert key in dictionary

```
### 6.2 Exception Testing

```python
import pytest

def test_raises_value_error():

    with pytest.raises(ValueError) as exc_info:

        validate_email("invalid")

    assert "Invalid email" in str(exc_info.value)

def test_raises_with_match():

    with pytest.raises(ValueError, match=r"Invalid.*email"):

        validate_email("invalid")

```
### 6.3 Approximate Comparisons

```python
import pytest

from math import isclose

# Float comparison

assert result == pytest.approx(3.14159, rel=1e-5)

# Using math.isclose

assert isclose(result, 3.14159, rel_tol=1e-5)

```
### 6.4 Collection Assertions

```python
# List equality

assert result == [1, 2, 3]

# Unordered comparison

assert set(result) == {1, 2, 3}

assert sorted(result) == sorted(expected)

# Subset

assert expected_items <= set(result)

# Length

assert len(result) == 3

```
---

## 7. Async Testing

### 7.1 Pytest-Asyncio

```python
import pytest

@pytest.mark.asyncio

async def test_async_operation():

    result = await async_fetch_data()

    assert result is not None

@pytest.mark.asyncio

async def test_async_with_fixture(async_client):

    response = await async_client.get("/api/users")

    assert response.status_code == 200

```
### 7.2 Async Fixtures

```python
import pytest

@pytest.fixture

async def async_client():

    """Async HTTP client fixture."""

    async with AsyncClient() as client:

        yield client

@pytest.fixture

async def database():

    """Async database connection."""

    db = await Database.connect()

    yield db

    await db.disconnect()

```
### 7.3 Mocking Async Functions

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio

async def test_async_service():

    mock_repo = AsyncMock()

    mock_repo.get.return_value = User(id="1")

    service = UserService(repository=mock_repo)

    result = await service.get("1")

    mock_repo.get.assert_awaited_once_with("1")

```
---

## 8. Parameterized Tests

### 8.1 Basic Parameterization

```python
import pytest

@pytest.mark.parametrize(

    "input,expected", [

        ("hello", "HELLO"),

        ("world", "WORLD"),

        ("", ""),

    ]

)

def test_uppercase(input, expected):

    assert input.upper() == expected

```
### 8.2 Multiple Parameters

```python
@pytest.mark.parametrize(

    "a,b,expected", [

        (1, 2, 3),

        (0, 0, 0),

        (-1, 1, 0),

        (100, 200, 300),

    ]

)

def test_add(a, b, expected):

    assert add(a, b) == expected

```
### 8.3 Named Test Cases

```python
@pytest.mark.parametrize(

    "email,valid", [

        pytest.param("user@example.com", True, id="valid_email"),

        pytest.param("invalid", False, id="no_at_sign"),

        pytest.param("@example.com", False, id="no_local_part"),

        pytest.param("user@", False, id="no_domain"),

    ]

)

def test_validate_email(email, valid):

    assert validate_email(email) == valid

```
### 8.4 Combining Parameterization

```python
@pytest.mark.parametrize("method", ["GET", "POST"])

@pytest.mark.parametrize("path", ["/users", "/items"])

def test_endpoints(method, path):

    # Tests all combinations: GET /users, GET /items, POST /users, POST /items

    response = client.request(method, path)

    assert response.status_code in [200, 201, 405]

```
---

## Quick Reference

### Test Structure Checklist

| Check                      | Description              |

|----------------------------|--------------------------|

| ☐ Single assertion focus   | Test one thing           |

| ☐ Clear arrange/act/assert | Organized structure      |

| ☐ Descriptive name         | What and when            |

| ☐ Independent              | No test order dependency |

| ☐ Fast                     | < 100ms per test         |

### Common Patterns

| Pattern         | Use Case              |

|-----------------|-----------------------|

| Factory fixture | Create test objects   |

| Mock            | Isolate dependencies  |

| Parametrize     | Multiple test cases   |

| tmp_path        | Temporary files       |

| monkeypatch     | Environment variables |

---

## Related

- `.knowledge/practices/engineering/INTEGRATION_TESTING.md` — Integration testing

- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing strategy

- `.knowledge/guidelines/PYTHON.md` — Python guidelines

---

*AI Collaboration Knowledge Base*

