# Security Implementation Patterns

> Code patterns and examples for implementing security controls

---

## Table of Contents

- [1. Secret Management](#1-secret-management)
- [2. Input Validation](#2-input-validation)
- [3. Output Sanitization](#3-output-sanitization)
- [4. Path Security](#4-path-security)
- [5. SQL Injection Prevention](#5-sql-injection-prevention)
- [6. Logging Security](#6-logging-security)

---

## 1. Secret Management

### Environment Variables

```python
import os

# ❌ Bad - Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# ✅ Good - Environment variable
API_KEY = os.environ.get("API_KEY")

# ✅ Better - With validation
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```
### .gitignore for Secrets

```gitignore
# Secrets and credentials
.env
.env.*
*.pem
*.key
*_secret*
credentials.json
secrets.yaml
```
---

## 2. Input Validation

### Path Validation

```python
from pathlib import Path

def safe_path(user_input: str, base_dir: Path) -> Path:
    """Validate and resolve path safely.
    
    Args:
        user_input: User-provided path string.
        base_dir: Allowed base directory.
        
    Returns:
        Resolved safe path.
        
    Raises:
        ValueError: If path escapes base directory.
    """
    requested = (base_dir / user_input).resolve()

    if not str(requested).startswith(str(base_dir.resolve())):
        raise ValueError(f"Path traversal detected: {user_input}")

    return requested
```
### String Validation

```python
import re

def validate_identifier(value: str, max_length: int = 64) -> str:
    """Validate identifier string.
    
    Args:
        value: Input string to validate.
        max_length: Maximum allowed length.
        
    Returns:
        Validated string.
        
    Raises:
        ValueError: If validation fails.
    """
    if not value:
        raise ValueError("Identifier cannot be empty")

    if len(value) > max_length:
        raise ValueError(f"Identifier exceeds {max_length} characters")

    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError("Identifier contains invalid characters")

    return value
```
### Numeric Validation

```python
def validate_timeout(value: int, min_val: int = 100, max_val: int = 10000) -> int:
    """Validate timeout value.
    
    Args:
        value: Timeout in milliseconds.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
        
    Returns:
        Validated timeout.
        
    Raises:
        ValueError: If value is out of range.
    """
    if not isinstance(value, int):
        raise TypeError(f"Timeout must be int, got {type(value)}")

    if value < min_val or value > max_val:
        raise ValueError(f"Timeout must be {min_val}-{max_val}ms")

    return value
```
### Pydantic Validation

```python
from pydantic import BaseModel, Field, validator

class UserInput(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$")
    email: str = Field(..., max_length=255)
    age: int = Field(..., ge=0, le=150)
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
```
---

## 3. Output Sanitization

### HTML Escaping

```python
from markupsafe import escape

def safe_html_output(user_input: str) -> str:
    """Escape HTML special characters."""
    return escape(user_input)
```
### JSON Output

```python
import json

def safe_json_response(data: dict) -> str:
    """Safely encode data as JSON."""
    return json.dumps(data, ensure_ascii=True)
```
---

## 4. Path Security

### Safe File Operations

```python
from pathlib import Path
import tempfile

def safe_temp_file(suffix: str = ".tmp") -> Path:
    """Create a secure temporary file."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return Path(path)

def safe_read_file(filepath: Path, base_dir: Path) -> str:
    """Read file safely within allowed directory."""
    safe = safe_path(str(filepath), base_dir)
    return safe.read_text()
```
---

## 5. SQL Injection Prevention

### Parameterized Queries

```python
# ❌ Bad - SQL injection vulnerability
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ Good - Parameterized query
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))

# ✅ Good - ORM with proper filtering
User.objects.filter(name=user_input)
```
---

## 6. Logging Security

### Secure Logging Pattern

```python
import structlog
from datetime import datetime

logger = structlog.get_logger()

def log_security_event(
    event_type: str,
    user_id: str,
    resource: str,
    action: str,
    result: str,
    **extra
):
    """Log security event without sensitive data."""
    logger.info(
        "security_event",
        event_type=event_type,
        user_id=user_id,  # Not the full user object
        resource=resource,
        action=action,
        result=result,
        timestamp=datetime.utcnow().isoformat(),
        **extra
    )
```
### Redacting Sensitive Data

```python
import re

def redact_secrets(text: str) -> str:
    """Redact potential secrets from text."""
    patterns = [
        (r'password["\']?\s*[:=]\s*["\']?[^"\'\\s]+', 'password=***'),
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\'\\s]+', 'api_key=***'),
        (r'token["\']?\s*[:=]\s*["\']?[^"\'\\s]+', 'token=***'),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text
```
---

## Related

- `.knowledge/guidelines/SECURITY.md` — Security principles and standards
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/frameworks/security/SECRETS_MANAGEMENT.md` — Secrets management

---

*AI Collaboration Knowledge Base*
