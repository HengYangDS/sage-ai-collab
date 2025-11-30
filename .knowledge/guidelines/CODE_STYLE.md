# Code Style Guidelines

> Consistent, readable, maintainable code

---

## Table of Contents

- [1. General Principles](#1-general-principles)
- [2. Naming Conventions](#2-naming-conventions)
- [3. Code Structure](#3-code-structure)
- [4. Documentation](#4-documentation)
- [5. Error Handling](#5-error-handling)
- [6. Quality Checklist](#6-quality-checklist)

---

## 1. General Principles

| Principle               | Description              |
|-------------------------|--------------------------|
| Clarity over cleverness | Readable > compact       |
| Consistency             | Follow existing patterns |
| Explicit over implicit  | Make intent obvious      |
| Self-documenting        | Code explains itself     |

---

## 2. Naming Conventions

| Element   | Style       | Example           |
|-----------|-------------|-------------------|
| Variables | snake_case  | `user_count`      |
| Constants | UPPER_SNAKE | `MAX_RETRIES`     |
| Functions | snake_case  | `get_user()`      |
| Classes   | PascalCase  | `UserService`     |
| Private   | _prefix     | `_internal_state` |

### 2.1 Naming Rules

| Rule               | ❌ Bad      | ✓ Good                      |
|--------------------|------------|-----------------------------|
| Descriptive        | `d`, `tmp` | `days_elapsed`, `temp_file` |
| No abbreviations   | `usr_cnt`  | `user_count`                |
| Verb for functions | `user()`   | `get_user()`                |
| Noun for variables | `running`  | `is_running`                |

---

## 3. Code Structure

### 3.1 File Organization

```python
# 1. Imports (stdlib → third-party → local)
# 2. Constants
# 3. Classes/Functions
# 4. Main block (if applicable)
```
### 3.2 Function Guidelines

| Metric                | Target |
|-----------------------|--------|
| Lines per function    | < 50   |
| Parameters            | ≤ 5    |
| Nesting depth         | ≤ 3    |
| Cyclomatic complexity | ≤ 10   |

---

## 4. Documentation

### 4.1 When to Comment

| Comment            | Don't Comment           |
|--------------------|-------------------------|
| Why (rationale)    | What (obvious code)     |
| Complex algorithms | Simple operations       |
| Workarounds        | Self-explanatory names  |
| Public API         | Internal implementation |

### 4.2 Docstring Format

```python
def function(param: str) -> bool:
    """Brief description.

    Args:
        param: Parameter description.

    Returns:
        Return value description.

    Raises:
        ValueError: When param is invalid.
    """
```
---

## 5. Error Handling

| Pattern             | Use For                |
|---------------------|------------------------|
| Specific exceptions | Known error conditions |
| Early return        | Guard clauses          |
| Context managers    | Resource cleanup       |
| Logging             | Debugging, monitoring  |

```python
# ✓ Good: specific, early return
def process(data: str) -> Result:
    if not data:
        raise ValueError("Data required")
    return Result(data.strip())
```
---

## 6. Quality Checklist

- [ ] Names are descriptive
- [ ] Functions are focused (< 50 lines)
- [ ] No magic numbers
- [ ] Errors handled appropriately
- [ ] Public API documented
- [ ] Tests written

---

## Related

- `.knowledge/guidelines/PYTHON.md` — Python-specific guidelines
- `.knowledge/guidelines/TYPESCRIPT.md` — TypeScript guidelines
- `.knowledge/practices/engineering/CODE_REVIEW.md` — Code review practices
- `.knowledge/guidelines/QUALITY.md` — Quality assurance guidelines

---

*AI Collaboration Knowledge Base*
