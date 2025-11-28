# Engineering Practices Guidelines

> **Load Time**: On-demand (~250 tokens)  
> **Purpose**: Configuration, testing, performance, change control, maintainability

---

## 3.1 Configuration Management

### Configuration Hierarchy

```
Priority (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Local config file (.env, config.local.yaml)
4. Project config file (config.yaml)
5. Default values in code
```

### Best Practices

```python
# GOOD: Typed configuration with defaults
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///default.db"
    debug: bool = False
    max_connections: int = 10
    
    class Config:
        env_prefix = "APP_"

# BAD: Scattered magic strings
DB_URL = os.getenv("DB_URL", "sqlite:///db.sqlite")
```

### Secrets Management

- ❌ Never commit secrets to version control
- ✅ Use environment variables or secret managers
- ✅ Document required environment variables
- ✅ Provide `.env.example` template

---

## 3.2 Testing Practices

### Test Pyramid

```
        /‾‾‾‾‾‾‾\
       / E2E     \      ← Few, slow, expensive
      /‾‾‾‾‾‾‾‾‾‾‾\
     / Integration \    ← Moderate amount
    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
   /     Unit        \  ← Many, fast, cheap
  /___________________\
```

### Test Organization

```
tests/
├── unit/           # Isolated component tests
├── integration/    # Component interaction tests
├── e2e/           # End-to-end scenarios
├── fixtures/      # Shared test data
└── conftest.py    # Pytest configuration
```

### Test Quality Criteria

| Criterion           | Description                |
|---------------------|----------------------------|
| **Fast**            | Unit tests < 100ms each    |
| **Isolated**        | No external dependencies   |
| **Repeatable**      | Same result every run      |
| **Self-validating** | Pass/fail, no manual check |
| **Timely**          | Written with/before code   |

### Testing Patterns

```python
# Arrange-Act-Assert (AAA)
def test_user_creation():
    # Arrange
    service = UserService(mock_repository)
    user_data = {"name": "Alice", "email": "alice@example.com"}
    
    # Act
    result = service.create_user(user_data)
    
    # Assert
    assert result.name == "Alice"
    assert mock_repository.save.called_once()
```

---

## 3.3 Performance Guidelines

### Performance Principles

1. **Measure first**: Profile before optimizing
2. **Optimize hot paths**: Focus on 20% causing 80% issues
3. **Cache wisely**: Trade memory for speed
4. **Async for I/O**: Don't block on network/disk

### Common Optimizations

```python
# GOOD: Batch database operations
users = repository.get_many(user_ids)  # Single query

# BAD: N+1 queries
users = [repository.get(id) for id in user_ids]  # N queries
```

### Performance Checklist

- [ ] Database queries are optimized (indexes, joins)
- [ ] Large data is paginated
- [ ] External calls have timeouts
- [ ] Caching strategy is defined
- [ ] Memory usage is bounded

---

## 3.4 Change Control

### Git Commit Standards

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Examples

```
feat(auth): add JWT token refresh endpoint

- Implement refresh token rotation
- Add token blacklist for revoked tokens
- Update API documentation

Closes #123
```

### Branch Strategy

```
main (production)
  └── develop (integration)
        ├── feature/user-auth
        ├── feature/payment-api
        └── bugfix/login-redirect
```

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Breaking changes documented

---

## 3.5 Maintainability

### Technical Debt Management

| Priority     | Action             | Timeline       |
|--------------|--------------------|----------------|
| **Critical** | Blocking issues    | Immediate      |
| **High**     | Significant impact | Next sprint    |
| **Medium**   | Moderate impact    | Roadmap        |
| **Low**      | Minor improvements | As time allows |

### Code Health Indicators

```python
# GOOD: Low complexity, clear flow
def process_order(order: Order) -> Result:
    if not order.is_valid():
        return Result.invalid("Order validation failed")
    
    inventory = check_inventory(order.items)
    if not inventory.available:
        return Result.unavailable(inventory.missing)
    
    return complete_order(order)

# BAD: High cyclomatic complexity
def process_order(order):
    if order:
        if order.items:
            for item in order.items:
                if item.quantity > 0:
                    if check_stock(item):
                        # ... deeply nested logic
```

### Refactoring Triggers

- Duplicate code (DRY violation)
- Long methods (> 50 lines)
- Large classes (> 300 lines)
- Complex conditionals
- Feature envy (class using another class's data excessively)

---

## 3.6 Engineering Checklist

### Before Starting

- [ ] Requirements documented
- [ ] Design reviewed
- [ ] Dependencies identified

### During Development

- [ ] Tests written alongside code
- [ ] Code follows style guide
- [ ] Changes are incremental and reviewable

### Before Merging

- [ ] All tests pass
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Performance validated

---

*Part of AI Collaboration Knowledge Base v2.0.0*
