# Engineering Patterns Practice Guide

> Common engineering patterns and their practical application

---

## Table of Contents

- [1. Pattern Quick Reference](#1-pattern-quick-reference)
- [2. Repository Pattern](#2-repository-pattern)
- [3. Service Layer Pattern](#3-service-layer-pattern)
- [4. Factory Pattern](#4-factory-pattern)
- [5. Strategy Pattern](#5-strategy-pattern)
- [6. Observer Pattern](#6-observer-pattern)
- [7. Anti-Patterns](#7-anti-patterns)

---

## 1. Pattern Quick Reference

| Pattern         | Purpose                    | Use When               |
|-----------------|----------------------------|------------------------|
| Repository      | Abstract data access       | Multiple backends      |
| Service Layer   | Encapsulate business logic | Complex operations     |
| Factory         | Encapsulate creation       | Dynamic type selection |
| Strategy        | Interchangeable algorithms | Runtime selection      |
| Observer        | Decoupled notifications    | Event-driven systems   |
| Circuit Breaker | Prevent cascade failures   | External services      |

---

## 2. Repository Pattern

```python
class Repository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: str) -> Optional[T]: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, id: str) -> bool: ...

class UserRepository(Repository[User]):
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: str) -> Optional[User]:
        return self._session.query(User).get(id)
```
**Use for**: Data access abstraction, testing with mocks.

---

## 3. Service Layer Pattern

```python
class UserService:
    def __init__(self, repo: UserRepository, events: EventBus):
        self._repo = repo
        self._events = events

    def register(self, data: UserCreate) -> User:
        user = self._repo.save(User(**data.dict()))
        self._events.publish(UserRegistered(user.id))
        return user
```
**Use for**: Business logic encapsulation, transaction management.

---

## 4. Factory Pattern

```python
class HandlerFactory:
    _handlers: Dict[str, Type[Handler]] = {}

    @classmethod
    def register(cls, msg_type: str):
        def decorator(handler_cls):
            cls._handlers[msg_type] = handler_cls
            return handler_cls

        return decorator

    @classmethod
    def create(cls, msg_type: str) -> Handler:
        return cls._handlers[msg_type]()
```
**Use for**: Dynamic object creation, plugin systems.

---

## 5. Strategy Pattern

```python
class PricingStrategy(Protocol):
    def calculate(self, base: float, qty: int) -> float: ...

class RegularPricing:
    def calculate(self, base: float, qty: int) -> float:
        return base * qty

class BulkPricing:
    def __init__(self, threshold: int, discount: float):
        self.threshold, self.discount = threshold, discount

    def calculate(self, base: float, qty: int) -> float:
        mult = 1 - self.discount if qty >= self.threshold else 1
        return base * qty * mult
```
**Use for**: Algorithm selection at runtime.

---

## 6. Observer Pattern

```python
class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, handler: Callable):
        self._subs.setdefault(event, []).append(handler)

    def publish(self, event: str, data: Any):
        for handler in self._subs.get(event, []):
            handler(data)
```
**Use for**: Decoupled communication, plugin architecture.

---

## 7. Anti-Patterns

| Anti-Pattern      | Problem                | Solution               |
|-------------------|------------------------|------------------------|
| God Object        | Does everything        | Split responsibilities |
| Anemic Domain     | Logic outside entities | Rich domain models     |
| Service Locator   | Hidden dependencies    | Dependency injection   |
| Singleton Overuse | Global state           | Scoped instances       |

---

## Related

- `.knowledge/guidelines/CODE_STYLE.md` — Code style
- `.knowledge/frameworks/design/AXIOMS.md` — Design principles

---

*AI Collaboration Knowledge Base*
