# Python Implementation Patterns

> Code patterns and examples for Python development

---

## Table of Contents

- [1. Type Hints](#1-type-hints)
- [2. Decorators](#2-decorators)
- [3. Context Managers](#3-context-managers)
- [4. Async Patterns](#4-async-patterns)
- [5. Data Classes](#5-data-classes)
- [6. Design Patterns](#6-design-patterns)

---

## 1. Type Hints

### Basic Types

```python
from typing import Optional, List, Dict, Callable

def process(name: str, count: int = 1) -> List[str]:
    return [name] * count

def find_user(user_id: int) -> Optional[User]:
    return db.get(user_id)
```
### Complex Types

```python
from typing import TypeVar, Generic, Protocol

T = TypeVar("T")

class Repository(Generic[T], Protocol):
    def get(self, id: str) -> Optional[T]: ...
    def save(self, entity: T) -> T: ...
```
### Callable Types

```python
from typing import Callable, Awaitable

# Sync function type
Handler = Callable[[Request], Response]

# Async function type
AsyncHandler = Callable[[Request], Awaitable[Response]]

def register(handler: Handler) -> None:
    pass
```
---

## 2. Decorators

### Function Decorator

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
### Decorator with Arguments

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    return requests.get(url).json()
```
### Class Decorator

```python
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Configuration:
    pass
```
---

## 3. Context Managers

### Using contextmanager

```python
from contextlib import contextmanager
import time

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
### Class-based Context Manager

```python
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        self.connection = create_connection(self.connection_string)
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection("postgresql://...") as conn:
    conn.execute("SELECT 1")
```
### Async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_timer(name: str):
    start = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start:.2f}s")

# Usage
async with async_timer("async_process"):
    await do_async_work()
```
---

## 4. Async Patterns

### Basic Async

```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_all(urls: List[str]) -> List[dict]:
    return await asyncio.gather(*[fetch_data(u) for u in urls])
```
### Async with Timeout

```python
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    async with asyncio.timeout(timeout):
        return await fetch_data(url)
```
### Async Semaphore (Rate Limiting)

```python
async def fetch_limited(urls: List[str], max_concurrent: int = 5) -> List[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_one(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)
    
    return await asyncio.gather(*[fetch_one(u) for u in urls])
```
---

## 5. Data Classes

### Basic Dataclass

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
```
### Immutable Dataclass

```python
@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080
    
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"
```
### Dataclass with Validation

```python
@dataclass
class Order:
    product_id: str
    quantity: int
    price: float
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
    
    @property
    def total(self) -> float:
        return self.quantity * self.price
```
---

## 6. Design Patterns

### Factory Pattern

```python
from typing import Dict, Type

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
        if name not in cls._handlers:
            raise ValueError(f"Unknown handler: {name}")
        return cls._handlers[name]()

@HandlerFactory.register("json")
class JsonHandler(Handler):
    pass
```
### Repository Pattern

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass

class SQLUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session
    
    def get(self, id: str) -> Optional[User]:
        return self._session.query(User).get(id)
    
    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        return user
```
### Strategy Pattern

```python
from abc import ABC, abstractmethod

class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

class GzipCompression(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        import gzip
        return gzip.compress(data)

class NoCompression(CompressionStrategy):
    def compress(self, data: bytes) -> bytes:
        return data

class DataProcessor:
    def __init__(self, compression: CompressionStrategy):
        self.compression = compression
    
    def process(self, data: bytes) -> bytes:
        return self.compression.compress(data)
```
---

## Related

- `.knowledge/guidelines/PYTHON.md` — Python coding standards
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/guidelines/CODE_STYLE.md` — General code style

---

*AI Collaboration Knowledge Base*
