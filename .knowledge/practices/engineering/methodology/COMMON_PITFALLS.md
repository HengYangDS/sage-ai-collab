# Common Pitfalls

> Known pitfalls and how to avoid them in software development

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Architecture Pitfalls](#2-architecture-pitfalls)
- [3. Implementation Pitfalls](#3-implementation-pitfalls)
- [4. Configuration Pitfalls](#4-configuration-pitfalls)
- [5. Testing Pitfalls](#5-testing-pitfalls)
- [6. AI Collaboration Pitfalls](#6-ai-collaboration-pitfalls)

---

## 1. Overview

This document catalogs common pitfalls encountered during software development. Each pitfall includes symptoms, root
cause, and prevention strategies.

### 1.1 Pitfall Severity

| Severity     | Impact                     | Response              |
|--------------|----------------------------|-----------------------|
| **Critical** | System failure, data loss  | Immediate fix         |
| **High**     | Major functionality broken | Fix in current sprint |
| **Medium**   | Degraded performance/UX    | Plan for fix          |
| **Low**      | Minor inconvenience        | Fix when convenient   |

---

## 2. Architecture Pitfalls

### 2.1 Circular Dependencies

**Severity**: High

**Symptoms**:

- Import errors at runtime
- Unexpected `None` values
- Module initialization failures

**Root Cause**: Two modules importing each other directly.

**Prevention**:

```python
# ❌ Bad - Circular import
# module_a.py
from module_b import B

class A:
    def use_b(self): return B()

# module_b.py
from module_a import A  # Circular!

class B:
    def use_a(self): return A()

# ✅ Good - Use protocol/interface
# protocols.py
class AProtocol(Protocol):
    def method(self) -> None: ...

# module_b.py
from protocols import AProtocol

class B:
    def __init__(self, a: AProtocol):
        self.a = a
```
**Detection**: Run `pydeps` or check import graph.

---

### 2.2 Missing Timeout Protection

**Severity**: Critical

**Symptoms**:

- Application hangs
- Unresponsive CLI
- Memory growth

**Root Cause**: I/O operations without timeout.

**Prevention**:

```python
# ❌ Bad - No timeout
content = await file.read()

# ✅ Good - With timeout
async with asyncio.timeout(5.0):
    content = await file.read()
```
**Rule**: Every I/O operation must have a timeout.

---

### 2.3 Tight Coupling Between Layers

**Severity**: Medium

**Symptoms**:

- Changes cascade across files
- Hard to test in isolation
- Difficult to replace components

**Root Cause**: Direct dependencies instead of interfaces.

**Prevention**:

```python
# ❌ Bad - Direct dependency
class Service:
    def __init__(self):
        self.loader = FileLoader()  # Tight coupling

# ✅ Good - Dependency injection
class Service:
    def __init__(self, loader: LoaderProtocol):
        self.loader = loader  # Loose coupling
```
---

## 3. Implementation Pitfalls

### 3.1 Mutable Default Arguments

**Severity**: High

**Symptoms**:

- State shared between calls
- Unexpected data accumulation
- Hard-to-debug behavior

**Root Cause**: Python evaluates defaults once at definition.

**Prevention**:

```python
# ❌ Bad - Mutable default
def process(items: list = []):
    items.append("new")
    return items

# ✅ Good - None default
def process(items: list | None = None):
    if items is None:
        items = []
    items.append("new")
    return items
```
---

### 3.2 Catching Too Broad Exceptions

**Severity**: Medium

**Symptoms**:

- Silent failures
- Hidden bugs
- Incorrect error handling

**Root Cause**: Catching `Exception` or bare `except`.

**Prevention**:

```python
# ❌ Bad - Too broad
try:
    result = process()
except Exception:
    pass  # Swallows all errors

# ✅ Good - Specific exceptions
try:
    result = process()
except FileNotFoundError:
    result = default_value
except ValueError as e:
    log.error(f"Invalid value: {e}")
    raise
```
---

### 3.3 Forgetting Async Context

**Severity**: High

**Symptoms**:

- `RuntimeWarning: coroutine never awaited`
- Functions return coroutine objects
- Async operations not completing

**Root Cause**: Missing `await` keyword.

**Prevention**:

```python
# ❌ Bad - Missing await
def get_content():
    return loader.load("file.md")  # Returns coroutine!

# ✅ Good - Proper await
async def get_content():
    return await loader.load("file.md")

# ✅ Good - Or explicitly sync
def get_content():
    return asyncio.run(loader.load("file.md"))
```
---

### 3.4 Not Closing Resources

**Severity**: Medium

**Symptoms**:

- Resource exhaustion
- "Too many open files" errors
- Memory leaks

**Root Cause**: Not using context managers.

**Prevention**:

```python
# ❌ Bad - Resource leak
file = open("data.txt")
content = file.read()
# file never closed!

# ✅ Good - Context manager
with open("data.txt") as file:
    content = file.read()
# Automatically closed

# ✅ Good - Async context manager
async with aiofiles.open("data.txt") as file:
    content = await file.read()
```
---

## 4. Configuration Pitfalls

### 4.1 Hardcoded Values

**Severity**: Medium

**Symptoms**:

- Can't change behavior without code changes
- Different behavior in different environments
- Difficult to test

**Root Cause**: Magic numbers/strings in code.

**Prevention**:

```python
# ❌ Bad - Hardcoded
timeout = 5000
if len(content) > 10000:
    truncate(content)

# ✅ Good - Configurable
timeout = config.get("timeout_ms", 5000)
if len(content) > config.get("max_content_length", 10000):
    truncate(content)
```
---

### 4.2 Missing Environment-Specific Config

**Severity**: High

**Symptoms**:

- Dev settings in production
- Production data in dev
- Security issues

**Root Cause**: Single config for all environments.

**Prevention**:

```yaml
# config/app.yaml
defaults:
  timeout_ms: 5000

development:
  debug: true
  log_level: DEBUG

production:
  debug: false
  log_level: INFO
```
---

### 4.3 Secrets in Config Files

**Severity**: Critical

**Symptoms**:

- Secrets in git history
- Security vulnerabilities
- Compliance issues

**Root Cause**: Committing sensitive values.

**Prevention**:

```yaml
# ❌ Bad - Secret in config
api_key: "sk-1234567890"

# ✅ Good - Environment variable reference
api_key: "${API_KEY}"

# ✅ Good - Separate secrets file (gitignored)
# secrets.yaml (in .gitignore)
api_key: "sk-1234567890"
```
---

## 5. Testing Pitfalls

### 5.1 Testing Implementation, Not Behavior

**Severity**: Medium

**Symptoms**:

- Tests break on refactoring
- High test maintenance
- False confidence

**Root Cause**: Testing internal details.

**Prevention**:

```python
# ❌ Bad - Testing implementation
def test_user_service():
    service = UserService()
    service._cache["user1"] = user  # Testing internal
    assert service._cache["user1"] == user

# ✅ Good - Testing behavior
def test_user_service():
    service = UserService()
    service.save(user)
    result = service.get(user.id)
    assert result == user
```
---

### 5.2 Flaky Tests

**Severity**: High

**Symptoms**:

- Tests pass/fail randomly
- CI unreliable
- Test suite distrust

**Root Cause**: Timing dependencies, shared state, external services.

**Prevention**:

```python
# ❌ Bad - Time-dependent
def test_timeout():
    start = time.time()
    result = slow_operation()
    assert time.time() - start < 1.0  # Flaky!

# ✅ Good - Mock time
def test_timeout(mocker):
    mock_time = mocker.patch("time.time")
    mock_time.side_effect = [0, 0.5, 1.0]
    result = slow_operation()
    assert result.duration == 0.5
```
---

### 5.3 Missing Edge Case Tests

**Severity**: Medium

**Symptoms**:

- Bugs in production
- Unexpected behavior
- Crashes on unusual input

**Root Cause**: Only testing happy path.

**Prevention**:

```python
# Test edge cases
class TestLoadContent:
    def test_normal_file(self): ...

    def test_empty_file(self): ...

    def test_missing_file(self): ...

    def test_permission_denied(self): ...

    def test_very_large_file(self): ...

    def test_binary_file(self): ...

    def test_unicode_content(self): ...

    def test_special_characters_in_path(self): ...
```
---

## 6. AI Collaboration Pitfalls

### 6.1 Assuming AI Context

**Severity**: Medium

**Symptoms**:

- AI makes incorrect assumptions
- Inconsistent decisions
- Repeated mistakes

**Root Cause**: Not providing necessary context.

**Prevention**:

- Always load core principles
- Reference relevant design decisions
- Provide recent history

---

### 6.2 Overly Broad Instructions

**Severity**: Medium

**Symptoms**:

- AI does too much
- Unexpected changes
- Scope creep

**Root Cause**: Vague task descriptions.

**Prevention**:

```markdown
# ❌ Bad - Too broad

"Fix the loading issues"

# ✅ Good - Specific

"In src/core/loader.py, add timeout handling to the
load_file method. Use 500ms timeout. Return None on
timeout instead of raising exception."
```
---

### 6.3 Not Reviewing AI Changes

**Severity**: High

**Symptoms**:

- Bugs introduced
- Style inconsistencies
- Unintended side effects

**Root Cause**: Accepting AI output without review.

**Prevention**:

- Always review diffs
- Run tests after changes
- Check for side effects
- Verify against requirements

---

## Quick Reference

### Red Flags to Watch For

| Red Flag                 | Likely Pitfall          |
|--------------------------|-------------------------|
| `except Exception`       | Too broad exception     |
| No `await` on async call | Missing async context   |
| `def func(items=[])`     | Mutable default         |
| Direct file path strings | Missing path validation |
| `time.sleep` in tests    | Flaky test              |
| Hardcoded numbers        | Missing configuration   |

### Prevention Checklist

| Check                 | Description            |
|-----------------------|------------------------|
| ☐ Timeout on I/O      | Every I/O has timeout  |
| ☐ Specific exceptions | No bare `except`       |
| ☐ Resources closed    | Using context managers |
| ☐ Config externalized | No hardcoded values    |
| ☐ Tests cover edges   | Not just happy path    |
| ☐ AI output reviewed  | Diff checked           |

---

## Related

- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing best practices
- `.knowledge/practices/ai_collaboration/` — AI collaboration practices

---

*AI Collaboration Knowledge Base*
