# Testing Strategy

> Universal testing layers, organization, and best practices

---

## Table of Contents

- [1. Test Pyramid](#1-test-pyramid)
- [2. Test Types](#2-test-types)
- [3. Test Naming](#3-test-naming)
- [4. Test Structure](#4-test-structure)
- [5. Fixtures](#5-fixtures)
- [6. Mocking](#6-mocking)
- [7. Coverage](#7-coverage)

---

## 1. Test Pyramid

```text
        /\          E2E (Few) - User flows
       /──\         Integration (Some) - Components
      /────\        Unit (Many) - Functions
     /──────\
```
| Type        | Ratio | Speed  | Focus     |
|-------------|-------|--------|-----------|
| Unit        | 70%   | < 10ms | Logic     |
| Integration | 20%   | < 1s   | Contracts |
| E2E         | 10%   | < 30s  | Flows     |

---

## 2. Test Types

### 2.1 Unit Tests

| Aspect       | Description           |
|--------------|-----------------------|
| Scope        | Single function/class |
| Dependencies | All mocked            |
| Speed        | Very fast             |
| Goal         | Logic correctness     |

### 2.2 Integration Tests

| Aspect       | Description         |
|--------------|---------------------|
| Scope        | Multi-component     |
| Dependencies | Partially real      |
| Speed        | Medium              |
| Goal         | Interface contracts |

### 2.3 E2E Tests

| Aspect       | Description    |
|--------------|----------------|
| Scope        | Complete flows |
| Dependencies | All real       |
| Speed        | Slow           |
| Goal         | Business flows |

---

## 3. Test Naming

### 3.1 Convention

```python
def test_[function]_[scenario]

_[expected]():
pass

# Examples
def test_calculate_total_empty_cart_returns_zero():
    ...

def test_login_invalid_password_raises_error():
    ...
```
### 3.2 Class Organization

```python
class TestUserService:
    class TestCreate:
        def test_valid_data_creates_user(self): ...

        def test_duplicate_email_raises_error(self): ...
```
---

## 4. Test Structure

### 4.1 Arrange-Act-Assert (AAA)

```python
def test_add_item_to_cart():
    # Arrange
    cart = Cart()
    item = Item(id=1, price=100)

    # Act
    cart.add(item)

    # Assert
    assert cart.total == 100
    assert len(cart.items) == 1
```
### 4.2 Given-When-Then (BDD)

```python
def test_user_registration():
    # Given a new user
    user_data = {"email": "test@example.com"}

    # When registering
    result = service.register(user_data)

    # Then user is created
    assert result.id is not None
```
---

## 5. Fixtures

### 5.1 Pytest Fixtures

```python
@pytest.fixture
def user():
    return User(name="Test", email="test@example.com")

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
```
### 5.2 Fixture Scopes

| Scope    | Lifetime   | Use For          |
|----------|------------|------------------|
| function | Each test  | Default          |
| class    | Per class  | Related tests    |
| module   | Per file   | Expensive setup  |
| session  | Entire run | Global resources |

---

## 6. Mocking

### 6.1 Basic Mocking

```python
def test_with_mock(mocker):
    mock_api = mocker.patch("module.api_call")
    mock_api.return_value = {"status": "ok"}

    result = service.process()

    mock_api.assert_called_once()
```
### 6.2 When to Mock

| Mock          | Don't Mock          |
|---------------|---------------------|
| External APIs | Core logic          |
| Databases     | Pure functions      |
| Time/random   | Value objects       |
| File system   | Simple calculations |

---

## 7. Coverage

### 7.1 Targets

| Metric          | Target |
|-----------------|--------|
| Line coverage   | > 80%  |
| Branch coverage | > 70%  |
| Critical paths  | 100%   |

### 7.2 Quality over Quantity

| Good Coverage         | Bad Coverage          |
|-----------------------|-----------------------|
| Tests edge cases      | Tests only happy path |
| Meaningful assertions | Trivial assertions    |
| Tests behavior        | Tests implementation  |

---

## Related

- `.knowledge/guidelines/QUALITY.md` — Quality standards
- `.knowledge/practices/engineering/CODE_REVIEW.md` — Review practices

---

*AI Collaboration Knowledge Base*
