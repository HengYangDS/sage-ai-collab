# Planning and Design Guidelines

> **Load Time**: On-demand (~150 tokens)  
> **Purpose**: Architecture and design principles for sustainable systems

---

## 1.1 Execution Principles

### Think Before Acting

- **Understand** the full scope before implementation
- **Plan** the approach with clear milestones
- **Validate** assumptions early
- **Iterate** based on feedback

### Scope Management

```
GOOD: "Implement user authentication with JWT"
BAD:  "Make the app secure"
```

### Task Decomposition

1. Break large tasks into subtasks (max 2-4 hours each)
2. Define clear acceptance criteria per subtask
3. Identify dependencies between subtasks
4. Estimate and track progress

---

## 1.2 Architecture Patterns

### Layered Architecture

```
┌─────────────────────┐
│   Presentation      │  ← UI/API Layer
├─────────────────────┤
│   Business Logic    │  ← Core Domain
├─────────────────────┤
│   Data Access       │  ← Repository/ORM
├─────────────────────┤
│   Infrastructure    │  ← External Services
└─────────────────────┘
```

### Key Principles

| Principle | Description           | Example                    |
|-----------|-----------------------|----------------------------|
| **SRP**   | Single Responsibility | One class = one purpose    |
| **OCP**   | Open/Closed           | Extend, don't modify       |
| **LSP**   | Liskov Substitution   | Subtypes are substitutable |
| **ISP**   | Interface Segregation | Small, focused interfaces  |
| **DIP**   | Dependency Inversion  | Depend on abstractions     |

---

## 1.3 Modularity Guidelines

### Module Design

```python
# GOOD: Clear boundaries
class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create_user(self, data: UserCreate) -> User:
        # Business logic here
        return self._repository.save(data)

# BAD: Mixed concerns
class UserService:
    def create_user(self, data):
        # Direct DB access, email sending, logging all mixed
        conn = sqlite3.connect('db.sqlite')
        # ...
```

### Dependency Management

1. **Explicit dependencies**: Pass via constructor
2. **Interface-based**: Depend on protocols/ABCs
3. **Minimal coupling**: Only expose what's needed
4. **Testability**: Easy to mock/stub

---

## 1.4 Design Checklist

Before implementation, verify:

- [ ] Requirements are clear and complete
- [ ] Edge cases are identified
- [ ] Error handling strategy defined
- [ ] Performance requirements known
- [ ] Security considerations addressed
- [ ] Testing approach determined
- [ ] Documentation plan in place

---

## 1.5 Anti-Patterns to Avoid

| Anti-Pattern           | Problem                 | Solution                       |
|------------------------|-------------------------|--------------------------------|
| God Class              | Does everything         | Split by responsibility        |
| Spaghetti Code         | No structure            | Apply SOLID principles         |
| Premature Optimization | Complexity without need | Profile first, optimize second |
| Copy-Paste             | Duplication             | Extract to shared modules      |
| Magic Numbers          | Unclear intent          | Use named constants            |

---

*Part of AI Collaboration Knowledge Base v2.0.0*
