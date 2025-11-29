# Python-Specific Guidelines

> Python best practices, type hints, decorators, patterns

---

## Table of Contents

[1. Type Hints](#1-type-hints) · [2. Decorators](#2-decorators) · [3. Context Managers](#3-context-managers) · [4. Async Patterns](#4-async-patterns) · [5. Data Classes](#5-data-classes) · [6. Common Patterns](#6-common-patterns)

---

## 1. Type Hints

### 1.1 Basic Types

```python
from typing import Optional, List, Dict, Callable

def process(name: str, count: int = 1) -> List[str]:
    return [name] * count

def find_user(user_id: int) -> Optional[User]:
    return db.get(user_id)
```

### 1.2 Complex Types

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar("T")

class Repository(Generic[T], Protocol):
    def get(self, id: str) -> Optional[T]: ...
    def save(self, entity: T) -> T: ...
```

### 1.3 Type Hint Rules

| Rule | Example |
|------|---------|
| All public functions | `def func(x: int) -> str:` |
| Optional for nullable | `Optional[str]` not `str | None` |
| Use TypeVar for generics | `T = TypeVar("T")` |

---

## 2. Decorators

### 2.1 Common Decorators

```python
from functools import wraps
import logging

def log_calls(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def process(data: str) -> str:
    return data.upper()
```

### 2.2 Class Decorators

| Decorator | Use For |
|-----------|---------|
| `@dataclass` | Data containers |
| `@property` | Computed attributes |
| `@classmethod` | Alternative constructors |
| `@staticmethod` | Utility functions |

---

## 3. Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start:.2f}s")

# Usage
with timer("process"):
    do_work()
```

---

## 4. Async Patterns

### 4.1 Basic Async

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_all(urls: List[str]) -> List[dict]:
    return await asyncio.gather(*[fetch_data(u) for u in urls])
```

### 4.2 Async Guidelines

| Pattern | Use For |
|---------|---------|
| `async/await` | I/O-bound operations |
| `asyncio.gather` | Concurrent execution |
| `asyncio.timeout` | Timeout protection |

---

## 5. Data Classes

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    name: str
    email: str
    roles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.email = self.email.lower()

@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080
```

---

## 6. Common Patterns

### 6.1 Factory Pattern

```python
class HandlerFactory:
    _handlers: Dict[str, Type[Handler]] = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(handler_cls):
            cls._handlers[name] = handler_cls
            return handler_cls
        return decorator
    
    @classmethod
    def create(cls, name: str) -> Handler:
        return cls._handlers[name]()
```

### 6.2 Repository Pattern

```python
class UserRepository:
    def __init__(self, session: Session):
        self._session = session
    
    def get(self, id: str) -> Optional[User]:
        return self._session.query(User).get(id)
    
    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        return user
```

---

## 7. Quality Checklist

- [ ] Type hints on public functions
- [ ] Docstrings on public API
- [ ] No mutable default arguments
- [ ] Context managers for resources
- [ ] Async for I/O-bound operations

---

*Part of SAGE Knowledge Base*
