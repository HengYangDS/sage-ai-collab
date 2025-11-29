# Code Style Guidelines

> **Load Time**: On-demand (~200 tokens)  
> **Purpose**: Consistent, readable, maintainable code

---

## 2.1 General Principles

### Readability First

```python
# GOOD: Self-documenting
def calculate_monthly_payment(principal: float, rate: float, months: int) -> float:
    monthly_rate = rate / 12
    return principal * monthly_rate / (1 - (1 + monthly_rate) ** -months)

# BAD: Cryptic
def calc(p, r, m):
    return p * r/12 / (1 - (1 + r/12) ** -m)
```

### Consistency Over Preference

- Follow project's existing style
- Use formatters (black, prettier, rustfmt)
- Configure linters for enforcement

---

## 2.2 Naming Conventions

| Element     | Style            | Example                           |
|-------------|------------------|-----------------------------------|
| Classes     | PascalCase       | `UserAccount`, `HttpClient`       |
| Functions   | snake_case       | `get_user()`, `calculate_total()` |
| Variables   | snake_case       | `user_count`, `max_retries`       |
| Constants   | SCREAMING_SNAKE  | `MAX_CONNECTIONS`, `API_URL`      |
| Private     | _prefix          | `_internal_state`, `_helper()`    |
| Type Params | Single uppercase | `T`, `K`, `V`                     |

### Naming Quality Checklist

- [ ] Reveals intent (`user_count` vs `n`)
- [ ] Avoids abbreviations (`configuration` vs `cfg`)
- [ ] Uses domain language (`Order` vs `Thing1`)
- [ ] Searchable in codebase

---

## 2.3 Code Formatting

### Line Length

- **Python**: 88 characters (black default)
- **JavaScript/TypeScript**: 100 characters
- **Markdown**: 120 characters (documentation)

### Indentation

- **Python**: 4 spaces
- **JavaScript/TypeScript**: 2 spaces
- **YAML/JSON**: 2 spaces

### Blank Lines

```python
# Two blank lines before top-level definitions
import os


class UserService:
    """User management service."""
    
    # One blank line between methods
    def create(self, data: dict) -> User:
        pass
    
    def delete(self, user_id: str) -> bool:
        pass
```

---

## 2.4 Import Organization

### Python Import Order

```python
# 1. Standard library
import os
import sys
from datetime import datetime
from typing import Optional, List

# 2. Third-party packages
import httpx
from pydantic import BaseModel

# 3. Local imports
from .models import User
from .services import UserService
```

### Import Best Practices

- Use absolute imports when possible
- Avoid wildcard imports (`from x import *`)
- Group related imports together
- Sort alphabetically within groups

---

## 2.5 Comments and Documentation

### When to Comment

```python
# GOOD: Explain WHY, not WHAT
# Using binary search for O(log n) lookup in sorted data
index = bisect.bisect_left(sorted_items, target)

# BAD: Stating the obvious
# Increment counter by 1
counter += 1
```

### Docstring Standards (Google Style)

```python
def fetch_user(user_id: str, include_deleted: bool = False) -> Optional[User]:
    """Fetch a user by their unique identifier.
    
    Args:
        user_id: The unique identifier of the user.
        include_deleted: Whether to include soft-deleted users.
        
    Returns:
        The User object if found, None otherwise.
        
    Raises:
        ValueError: If user_id is empty or invalid format.
        ConnectionError: If database is unavailable.
    """
    pass
```

---

## 2.6 Error Handling Style

### Explicit Error Handling

```python
# GOOD: Specific exceptions with context
try:
    user = repository.get(user_id)
except UserNotFoundError:
    logger.warning(f"User {user_id} not found")
    raise
except DatabaseError as e:
    logger.error(f"Database error fetching user {user_id}: {e}")
    raise ServiceUnavailableError("Unable to fetch user") from e

# BAD: Catching everything
try:
    user = repository.get(user_id)
except Exception:
    pass  # Silent failure
```

---

## 2.7 Code Organization

### File Structure Template

```python
"""Module docstring explaining purpose."""

# Imports (organized as per 2.4)
import ...

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Type definitions
UserDict = dict[str, Any]

# Classes
class MainClass:
    pass

# Functions
def helper_function():
    pass

# Entry point (if applicable)
if __name__ == "__main__":
    main()
```

---

## 2.8 Quick Style Checklist

- [ ] Names are descriptive and consistent
- [ ] Formatting follows project standards
- [ ] Imports are organized and minimal
- [ ] Comments explain "why" not "what"
- [ ] Error handling is explicit
- [ ] No magic numbers or strings
- [ ] Functions are focused (< 50 lines ideal)
- [ ] Classes follow single responsibility

---

*Part of AI Collaboration Knowledge Base v2.0.0*
