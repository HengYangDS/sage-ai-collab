# Error Handling Patterns

> Consistent error handling for robust applications

---

## Table of Contents

- [1. Core Principles](#1-core-principles)
- [2. Exception Hierarchy](#2-exception-hierarchy)
- [3. Error Handling Patterns](#3-error-handling-patterns)
- [4. Error Context](#4-error-context)
- [5. Logging Strategy](#5-logging-strategy)
- [6. Recovery Patterns](#6-recovery-patterns)
- [7. Anti-Patterns](#7-anti-patterns)

---

## 1. Core Principles

| Principle          | Description                       |
|--------------------|-----------------------------------|
| Fail fast          | Detect and report errors early    |
| Be specific        | Use specific exception types      |
| Provide context    | Include helpful information       |
| Recover gracefully | Handle or propagate appropriately |

---

## 2. Exception Hierarchy

```python
class AppError(Exception):
    """Base application error."""
    pass

class ValidationError(AppError):
    """Input validation failed."""
    pass

class NotFoundError(AppError):
    """Resource not found."""
    pass

class AuthorizationError(AppError):
    """Access denied."""
    pass
```
---

## 3. Error Handling Patterns

### 3.1 Guard Clauses

```python
def process(data: str) -> Result:
    if not data:
        raise ValidationError("Data required")
    if len(data) > MAX_LENGTH:
        raise ValidationError(f"Data exceeds {MAX_LENGTH}")
    return do_process(data)
```
### 3.2 Try-Except

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.warning(f"Expected error: {e}")
    return fallback_value
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```
---

## 4. Error Context

### 4.1 Rich Exceptions

```python
class ValidationError(AppError):
    def __init__(self, message: str, field: str = None):
        super().__init__(message)
        self.field = field
        self.message = message

raise ValidationError("Invalid email", field="email")
```
### 4.2 Error Chaining

```python
try:
    parse_config(path)
except ParseError as e:
    raise ConfigError(f"Invalid config: {path}") from e
```
---

## 5. Logging Strategy

| Level    | Use For            |
|----------|--------------------|
| DEBUG    | Diagnostic details |
| INFO     | Normal operations  |
| WARNING  | Handled errors     |
| ERROR    | Unhandled errors   |
| CRITICAL | System failures    |

```python
try:
    result = operation()
except ExpectedError as e:
    logger.warning("Operation failed", exc_info=True)
except Exception as e:
    logger.error("Unexpected failure", exc_info=True)
    raise
```
---

## 6. Recovery Patterns

| Pattern   | Use When              |
|-----------|-----------------------|
| Retry     | Transient failures    |
| Fallback  | Alternative available |
| Default   | Safe default exists   |
| Propagate | Caller should handle  |

---

## 7. Anti-Patterns

| Anti-Pattern       | Problem            | Solution            |
|--------------------|--------------------|---------------------|
| Bare except        | Catches everything | Specific exceptions |
| Silent catch       | Hides errors       | Log or re-raise     |
| String exceptions  | No type info       | Exception classes   |
| Exception for flow | Performance        | Use conditionals    |

---

## Related

- `.knowledge/frameworks/resilience/TIMEOUT_PATTERNS.md` — Resilience patterns
- `.knowledge/practices/engineering/API_DESIGN.md` — API error responses

---

*AI Collaboration Knowledge Base*
