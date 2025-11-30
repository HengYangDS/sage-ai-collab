# Python Guidelines

> Python coding standards, type hints, and best practices

---

## Table of Contents

- [1. Type Hints](#1-type-hints)
- [2. Code Organization](#2-code-organization)
- [3. Naming Conventions](#3-naming-conventions)
- [4. Documentation](#4-documentation)
- [5. Best Practices](#5-best-practices)
- [6. Quality Checklist](#6-quality-checklist)

---

## 1. Type Hints

### Requirements

| Rule                     | Description                    |
|--------------------------|--------------------------------|
| All public functions     | Must have type hints           |
| Optional for nullable    | Use `Optional[T]` not `T \| None` |
| Use TypeVar for generics | `T = TypeVar("T")`             |
| Return type required     | Always specify return type     |

### Type Hint Examples

| Type               | Usage                          |
|--------------------|--------------------------------|
| `str`, `int`, etc. | Basic types                    |
| `Optional[T]`      | Nullable values                |
| `List[T]`          | List of items                  |
| `Dict[K, V]`       | Dictionary                     |
| `Callable[[A], R]` | Function type                  |
| `TypeVar("T")`     | Generic type parameter         |

---

## 2. Code Organization

### File Structure

| Order | Content                    |
|-------|----------------------------|
| 1     | Imports (stdlib → third-party → local) |
| 2     | Constants                  |
| 3     | Type definitions           |
| 4     | Classes/Functions          |
| 5     | Main block (if applicable) |

### Import Order

| Priority | Type          | Example                |
|----------|---------------|------------------------|
| 1        | Standard lib  | `import os`            |
| 2        | Third-party   | `import requests`      |
| 3        | Local         | `from .utils import x` |

---

## 3. Naming Conventions

| Element       | Convention  | Example              |
|---------------|-------------|----------------------|
| Variables     | snake_case  | `user_count`         |
| Constants     | UPPER_SNAKE | `MAX_RETRIES`        |
| Functions     | snake_case  | `get_user()`         |
| Classes       | PascalCase  | `UserService`        |
| Private       | _prefix     | `_internal_state`    |
| Type vars     | Single cap  | `T`, `K`, `V`        |
| Protocols     | Suffix-able | `Comparable`, `Iterable` |

---

## 4. Documentation

### Docstring Format (Google Style)

| Section   | Purpose                |
|-----------|------------------------|
| Summary   | Brief description      |
| Args      | Parameter descriptions |
| Returns   | Return value           |
| Raises    | Exceptions raised      |
| Examples  | Usage examples         |

### When to Document

| Document                  | Don't Document           |
|---------------------------|--------------------------|
| Public API                | Internal helpers         |
| Complex algorithms        | Obvious operations       |
| Non-obvious behavior      | Self-explanatory code    |
| Workarounds/hacks         | Simple getters/setters   |

---

## 5. Best Practices

### DO's and DON'Ts

| ✅ DO                      | ❌ DON'T                    |
|---------------------------|----------------------------|
| Use type hints            | Use dynamic typing blindly |
| Use dataclasses           | Manual `__init__` for data |
| Use context managers      | Manual resource cleanup    |
| Use pathlib               | String path manipulation   |
| Use f-strings             | % or .format()             |
| Use `is None`             | `== None`                  |

### Function Guidelines

| Metric                | Target      |
|-----------------------|-------------|
| Lines per function    | < 50        |
| Parameters            | ≤ 5         |
| Nesting depth         | ≤ 3         |
| Cyclomatic complexity | ≤ 10        |

### Common Patterns to Use

| Pattern          | Use Case                  |
|------------------|---------------------------|
| `@dataclass`     | Data containers           |
| `@property`      | Computed attributes       |
| `@classmethod`   | Alternative constructors  |
| `@staticmethod`  | Utility functions         |
| `contextmanager` | Resource management       |
| `async/await`    | I/O-bound operations      |

---

## 6. Quality Checklist

- [ ] Type hints on all public functions
- [ ] Docstrings on public API
- [ ] No mutable default arguments
- [ ] Context managers for resources
- [ ] Async for I/O-bound operations
- [ ] No bare `except:` clauses
- [ ] Specific exception types used
- [ ] No magic numbers (use constants)

---

## Related

- `.knowledge/practices/engineering/PYTHON_PATTERNS.md` — Implementation patterns and code examples
- `.knowledge/guidelines/CODE_STYLE.md` — General code style standards
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing strategies

---

*AI Collaboration Knowledge Base*
