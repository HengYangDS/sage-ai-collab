# Python-Specific Guidelines

> **Load Time**: On-demand (~180 tokens)  
> **Purpose**: Python best practices, type hints, decorators

---

## 5.1 Type Hints

### Basic Type Hints

```python
from typing import Optional, List, Dict, Callable, TypeVar

def greet(name: str) -> str:
    return f"Hello, {name}"

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: str) -> Optional[User]:
    """Returns User if found, None otherwise."""
    return db.get(user_id)
```

### Advanced Type Hints

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Repository(Generic[T]):
    def get(self, id: str) -> Optional[T]: ...
    def save(self, entity: T) -> T: ...

class Comparable(Protocol):
    def __lt__(self, other: Self) -> bool: ...

def sort_items(items: List[Comparable]) -> List[Comparable]:
    return sorted(items)
```

### Type Hint Best Practices

- ✅ Use type hints for all public APIs
- ✅ Use `Optional[X]` instead of `X | None` for Python 3.9 compatibility
- ✅ Use `TypeVar` for generic functions
- ❌ Avoid `Any` unless absolutely necessary

---

## 5.2 Docstrings (Google Style)

### Function Docstring

```python
def calculate_total(
    items: List[Item],
    discount: float = 0.0,
    tax_rate: float = 0.1
) -> float:
    """Calculate total price with discount and tax.
    
    Applies discount first, then adds tax to the discounted amount.
    
    Args:
        items: List of items to calculate total for.
        discount: Discount percentage (0.0 to 1.0).
        tax_rate: Tax rate to apply (default 10%).
        
    Returns:
        Final total amount after discount and tax.
        
    Raises:
        ValueError: If discount is negative or > 1.0.
        
    Example:
        >>> items = [Item(price=100), Item(price=50)]
        >>> calculate_total(items, discount=0.1)
        148.5
    """
```

### Class Docstring

```python
class UserService:
    """Service for user management operations.
    
    Provides CRUD operations for users with validation,
    caching, and event publishing.
    
    Attributes:
        repository: User data repository.
        cache: Optional cache backend.
        
    Example:
        >>> service = UserService(repository, cache)
        >>> user = service.create({"name": "Alice"})
    """
```

---

## 5.3 Import Organization

### Import Order

```python
# 1. Future imports (if needed)
from __future__ import annotations

# 2. Standard library
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# 3. Third-party packages
import httpx
from pydantic import BaseModel, Field
from rich.console import Console

# 4. Local imports (absolute)
from myproject.models import User
from myproject.services import UserService

# 5. Local imports (relative)
from .utils import helper_function
from ..shared import constants
```

### Import Anti-Patterns

```python
# BAD: Wildcard imports
from mymodule import *

# BAD: Unused imports
import os  # Never used

# BAD: Circular imports
# file_a.py imports file_b, file_b imports file_a

# GOOD: Import what you need
from mymodule import specific_function, SpecificClass
```

---

## 5.4 Decorator Patterns

### Basic Decorator with functools.wraps

```python
import functools
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs function calls."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Completed {func.__name__}")
        return result
    return wrapper

@log_calls
def process_data(data: str) -> str:
    return data.upper()
```

### Decorator with Arguments

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator that retries failed function calls."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2.0)
def fetch_data(url: str) -> dict:
    return httpx.get(url).json()
```

### Registry Pattern

```python
from typing import Dict, Type, TypeVar

T = TypeVar('T')

class HandlerRegistry:
    """Registry for dynamic handler lookup."""
    
    _handlers: Dict[str, Type] = {}
    
    @classmethod
    def register(cls, name: str):
        """Decorator to register a handler."""
        def decorator(handler_class: Type[T]) -> Type[T]:
            cls._handlers[name] = handler_class
            return handler_class
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Type:
        return cls._handlers[name]

@HandlerRegistry.register("json")
class JsonHandler:
    pass

@HandlerRegistry.register("xml")
class XmlHandler:
    pass
```

---

## 5.5 Context Managers

### Custom Context Manager

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def timed_operation(name: str) -> Generator[None, None, None]:
    """Context manager that times an operation."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name} took {elapsed:.3f}s")

# Usage
with timed_operation("data processing"):
    process_large_dataset()
```

### Class-Based Context Manager

```python
class DatabaseConnection:
    """Database connection with automatic cleanup."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._connection = None
    
    def __enter__(self) -> 'DatabaseConnection':
        self._connection = create_connection(self.connection_string)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._connection:
            self._connection.close()
        return False  # Don't suppress exceptions
```

---

## 5.6 Async Patterns

### Async Best Practices

```python
import asyncio
from typing import List

async def fetch_all(urls: List[str]) -> List[dict]:
    """Fetch multiple URLs concurrently."""
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# With timeout
async def fetch_with_timeout(url: str, timeout: float = 30.0) -> dict:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url)
        return response.json()
```

---

## 5.7 Python Checklist

- [ ] Type hints on all public functions
- [ ] Google-style docstrings
- [ ] Imports organized (stdlib → third-party → local)
- [ ] Decorators use `functools.wraps`
- [ ] Context managers for resource cleanup
- [ ] Async for I/O-bound operations
- [ ] No mutable default arguments

---

*Part of AI Collaboration Knowledge Base v2.0.0*
