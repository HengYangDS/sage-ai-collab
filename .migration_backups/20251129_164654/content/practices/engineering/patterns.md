# Engineering Patterns Practice Guide

> **Load Time**: On-demand (~200 tokens)  
> **Purpose**: Common engineering patterns and their practical application

---

## Repository Pattern

### Purpose

Abstract data access logic from business logic.

### Implementation

```python
from abc import ABC, abstractmethod
from typing import Optional, List, Generic, TypeVar

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    """Abstract repository interface."""
    
    @abstractmethod
    def get(self, id: str) -> Optional[T]:
        """Retrieve entity by ID."""
        pass
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Persist entity."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Remove entity."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Retrieve all entities."""
        pass

class UserRepository(Repository[User]):
    """Concrete user repository."""
    
    def __init__(self, session: Session):
        self._session = session
    
    def get(self, id: str) -> Optional[User]:
        return self._session.query(User).get(id)
    
    def save(self, user: User) -> User:
        self._session.add(user)
        self._session.commit()
        return user
```

### When to Use

- Multiple data sources possible
- Need to swap storage backends
- Testing requires mock data access
- Complex query logic to encapsulate

---

## Service Layer Pattern

### Purpose

Encapsulate business logic separate from presentation and data access.

### Implementation

```python
class UserService:
    """Business logic for user operations."""
    
    def __init__(
        self,
        repository: UserRepository,
        email_service: EmailService,
        event_bus: EventBus
    ):
        self._repository = repository
        self._email_service = email_service
        self._event_bus = event_bus
    
    def register(self, data: UserCreate) -> User:
        """Register new user with validation and notifications."""
        # Validate
        if self._repository.find_by_email(data.email):
            raise EmailAlreadyExistsError(data.email)
        
        # Create
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            name=data.name
        )
        user = self._repository.save(user)
        
        # Side effects
        self._email_service.send_welcome(user)
        self._event_bus.publish(UserRegistered(user.id))
        
        return user
```

### When to Use

- Business logic spans multiple entities
- Operations have side effects (email, events)
- Same logic needed from multiple entry points
- Transaction management required

---

## Factory Pattern

### Purpose

Encapsulate object creation logic.

### Implementation

```python
from typing import Dict, Type

class HandlerFactory:
    """Factory for creating message handlers."""
    
    _handlers: Dict[str, Type[Handler]] = {}
    
    @classmethod
    def register(cls, message_type: str):
        """Decorator to register handler."""
        def decorator(handler_class: Type[Handler]):
            cls._handlers[message_type] = handler_class
            return handler_class
        return decorator
    
    @classmethod
    def create(cls, message_type: str, **kwargs) -> Handler:
        """Create handler for message type."""
        handler_class = cls._handlers.get(message_type)
        if not handler_class:
            raise UnknownMessageTypeError(message_type)
        return handler_class(**kwargs)

@HandlerFactory.register("order.created")
class OrderCreatedHandler(Handler):
    def handle(self, message: Message) -> None:
        # Handle order created
        pass
```

### When to Use

- Object creation is complex
- Multiple types share interface
- Need to decouple creation from usage
- Dynamic type selection at runtime

---

## Strategy Pattern

### Purpose

Define family of algorithms, encapsulate each, make them interchangeable.

### Implementation

```python
from abc import ABC, abstractmethod
from typing import Protocol

class PricingStrategy(Protocol):
    """Protocol for pricing strategies."""
    
    def calculate(self, base_price: float, quantity: int) -> float:
        """Calculate final price."""
        ...

class RegularPricing:
    def calculate(self, base_price: float, quantity: int) -> float:
        return base_price * quantity

class BulkPricing:
    def __init__(self, threshold: int, discount: float):
        self.threshold = threshold
        self.discount = discount
    
    def calculate(self, base_price: float, quantity: int) -> float:
        if quantity >= self.threshold:
            return base_price * quantity * (1 - self.discount)
        return base_price * quantity

class Order:
    def __init__(self, pricing: PricingStrategy):
        self._pricing = pricing
    
    def total(self, items: List[Item]) -> float:
        return sum(
            self._pricing.calculate(item.price, item.quantity)
            for item in items
        )
```

### When to Use

- Multiple algorithms for same task
- Algorithm selection at runtime
- Avoid complex conditionals
- Need to add new algorithms easily

---

## Observer Pattern

### Purpose

Define one-to-many dependency; when one object changes, dependents are notified.

### Implementation

```python
from typing import List, Callable, Any

class EventBus:
    """Simple event bus implementation."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def publish(self, event_type: str, data: Any) -> None:
        """Publish event to all subscribers."""
        for handler in self._subscribers.get(event_type, []):
            handler(data)

# Usage
event_bus = EventBus()
event_bus.subscribe("user.created", send_welcome_email)
event_bus.subscribe("user.created", update_analytics)
event_bus.publish("user.created", {"user_id": "123"})
```

### When to Use

- Decoupled communication needed
- Multiple reactions to single event
- Plugin/extension architecture
- Async event processing

---

## Circuit Breaker Pattern

### Purpose

Prevent cascading failures by failing fast when service is unavailable.

### Implementation

```python
from enum import Enum
from datetime import datetime, timedelta


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreaker:
    """Circuit breaker for external calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = datetime.now()
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
```

### When to Use

- Calling external services
- Preventing cascade failures
- Graceful degradation needed
- Self-healing systems

---

## Pattern Selection Guide

| Scenario                     | Recommended Pattern |
|------------------------------|---------------------|
| Data access abstraction      | Repository          |
| Business logic encapsulation | Service Layer       |
| Complex object creation      | Factory             |
| Interchangeable algorithms   | Strategy            |
| Decoupled event handling     | Observer            |
| External service resilience  | Circuit Breaker     |

---

## Anti-Patterns to Avoid

| Anti-Pattern      | Problem                | Solution               |
|-------------------|------------------------|------------------------|
| God Object        | Does everything        | Split responsibilities |
| Anemic Domain     | Logic outside entities | Rich domain models     |
| Service Locator   | Hidden dependencies    | Dependency injection   |
| Singleton Overuse | Global state           | Scoped instances       |

---

*Part of AI Collaboration Knowledge Base v2.0.0*
