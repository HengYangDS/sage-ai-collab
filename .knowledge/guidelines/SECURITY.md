---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~3750
---

# Security Guidelines

> Security best practices for SAGE Knowledge Base development

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Secret Management](#2-secret-management)
- [3. Input Validation](#3-input-validation)
- [4. Output Sanitization](#4-output-sanitization)
- [5. Dependency Security](#5-dependency-security)
- [6. Logging Security](#6-logging-security)
- [7. API Security](#7-api-security)
- [8. File System Security](#8-file-system-security)
- [9. Security Checklist](#9-security-checklist)

---

## 1. Overview

### 1.1 Security Principles

| Principle            | Description                          |
|----------------------|--------------------------------------|
| **Defense in Depth** | Multiple layers of security controls |
| **Least Privilege**  | Minimum necessary permissions        |
| **Fail Secure**      | Default to secure state on failure   |
| **Zero Trust**       | Verify everything, trust nothing     |

### 1.2 Risk Categories

| Category     | Examples                               | Priority |
|--------------|----------------------------------------|----------|
| **Critical** | Secret exposure, remote code execution | P0       |
| **High**     | SQL injection, path traversal          | P1       |
| **Medium**   | Information disclosure, DoS            | P2       |
| **Low**      | Minor information leaks                | P3       |

---

## 2. Secret Management

### 2.1 Never Hardcode Secrets

```python
# ❌ Bad - Hardcoded secret
API_KEY = "sk-1234567890abcdef"

# ✅ Good - Environment variable
import os

API_KEY = os.environ.get("API_KEY")

# ✅ Better - With validation
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### 2.2 Secret Sources (Priority Order)

| Source                    | Use Case           | Security Level |
|---------------------------|--------------------|----------------|
| Secret Manager            | Production         | ⭐⭐⭐⭐⭐          |
| Environment Variables     | Development/CI     | ⭐⭐⭐⭐           |
| `.env` files (gitignored) | Local development  | ⭐⭐⭐            |
| Config files              | Non-sensitive only | ⭐⭐             |

### 2.3 .gitignore Requirements

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

### 2.4 Secret Rotation

| Secret Type        | Rotation Frequency |
|--------------------|--------------------|
| API Keys           | 90 days            |
| Database Passwords | 60 days            |
| Service Tokens     | 30 days            |
| Session Keys       | 24 hours           |

---

## 3. Input Validation

### 3.1 Validation Principles

| Principle               | Description                       |
|-------------------------|-----------------------------------|
| **Whitelist**           | Accept only known-good input      |
| **Validate Early**      | Check input at entry point        |
| **Validate Completely** | Check type, length, format, range |
| **Reject Invalid**      | Don't try to fix bad input        |

### 3.2 Path Validation

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
    # Resolve to absolute path
    requested = (base_dir / user_input).resolve()

    # Ensure path is within base directory
    if not str(requested).startswith(str(base_dir.resolve())):
        raise ValueError(f"Path traversal detected: {user_input}")

    return requested
```

### 3.3 String Validation

```python
import re
from typing import Optional


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

    # Allow only alphanumeric, underscore, hyphen
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError("Identifier contains invalid characters")

    return value
```

### 3.4 Numeric Validation

```python
def validate_timeout(value: int) -> int:
    """Validate timeout value.
    
    Args:
        value: Timeout in milliseconds.
        
    Returns:
        Validated timeout.
        
    Raises:
        ValueError: If value is out of range.
    """
    MIN_TIMEOUT = 100  # T1 minimum
    MAX_TIMEOUT = 10000  # T5 maximum

    if not isinstance(value, int):
        raise TypeError(f"Timeout must be int, got {type(value)}")

    if value < MIN_TIMEOUT or value > MAX_TIMEOUT:
        raise ValueError(f"Timeout must be {MIN_TIMEOUT}-{MAX_TIMEOUT}ms")

    return value
```

---

## 4. Output Sanitization

### 4.1 Log Sanitization

```python
import re

SENSITIVE_PATTERNS = [
    (r'password["\']?\s*[:=]\s*["\']?[^"\'\s]+', 'password=***'),
    (r'api[_-]?key["\']?\s*[:=]\s*["\']?[^"\'\s]+', 'api_key=***'),
    (r'token["\']?\s*[:=]\s*["\']?[^"\'\s]+', 'token=***'),
    (r'secret["\']?\s*[:=]\s*["\']?[^"\'\s]+', 'secret=***'),
]


def sanitize_log_message(message: str) -> str:
    """Remove sensitive data from log messages.
    
    Args:
        message: Raw log message.
        
    Returns:
        Sanitized message.
    """
    result = message
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result
```

### 4.2 Error Message Sanitization

```python
def safe_error_message(error: Exception, include_details: bool = False) -> str:
    """Create safe error message for users.
    
    Args:
        error: Exception instance.
        include_details: Whether to include technical details.
        
    Returns:
        Safe error message.
    """
    # Map internal errors to user-safe messages
    ERROR_MESSAGES = {
        FileNotFoundError: "The requested resource was not found",
        PermissionError  : "Access denied",
        TimeoutError     : "The operation timed out",
        ValueError       : "Invalid input provided",
    }

    # Get safe message or generic fallback
    safe_message = ERROR_MESSAGES.get(type(error), "An error occurred")

    if include_details and not _contains_sensitive_info(str(error)):
        safe_message += f": {error}"

    return safe_message
```

---

## 5. Dependency Security

### 5.1 Dependency Management

| Practice                   | Description                      |
|----------------------------|----------------------------------|
| **Pin Versions**           | Use exact versions in production |
| **Regular Updates**        | Update dependencies monthly      |
| **Vulnerability Scanning** | Scan on every commit             |
| **Minimal Dependencies**   | Only add necessary packages      |

### 5.2 Security Scanning

```bash
# Install safety scanner
pip install safety

# Scan dependencies
safety check

# Scan with requirements file
safety check -r requirements.txt

# Generate report
safety check --json > security-report.json
```

### 5.3 Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
```

### 5.4 Pre-commit Security Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [ "-r", "src/" ]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

---

## 6. Logging Security

### 6.1 What to Log

| Log                       | Don't Log           |
|---------------------------|---------------------|
| User actions (anonymized) | Passwords           |
| Error codes               | API keys            |
| Request IDs               | Session tokens      |
| Timestamps                | Personal data       |
| IP addresses (if needed)  | Credit card numbers |

### 6.2 Secure Logging Configuration

```python
import structlog


def configure_secure_logging():
    """Configure logging with security processors."""

    processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        # Add sanitization processor
        sanitize_processor,
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


def sanitize_processor(logger, method_name, event_dict):
    """Processor to sanitize sensitive data."""
    for key, value in list(event_dict.items()):
        if isinstance(value, str):
            event_dict[key] = sanitize_log_message(value)
    return event_dict
```

### 6.3 Audit Logging

```python
from datetime import datetime
from typing import Any


def audit_log(
    action: str,
    user_id: str,
    resource: str,
    details: dict[str, Any] | None = None,
) -> None:
    """Log security-relevant actions.
    
    Args:
        action: Action performed (e.g., "access", "modify", "delete").
        user_id: Anonymized user identifier.
        resource: Resource affected.
        details: Additional context (sanitized).
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action"   : action,
        "user_id"  : user_id,
        "resource" : resource,
        "details"  : details or {},
    }
    # Write to secure audit log
    audit_logger.info("audit_event", **log_entry)
```

---

## 7. API Security

### 7.1 Authentication

```python
from functools import wraps
from typing import Callable


def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request") or args[0]

        # Check for authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")

        token = auth_header.split(" ")[1]
        if not validate_token(token):
            raise HTTPException(status_code=401, detail="Invalid token")

        return await func(*args, **kwargs)

    return wrapper
```

### 7.2 Rate Limiting

```python
from collections import defaultdict
from time import time


class RateLimiter:
    """Simple rate limiter."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        now = time()
        window_start = now - self.window_seconds

        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if t > window_start
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True
```

### 7.3 CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://trusted-domain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Minimum required
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 8. File System Security

### 8.1 Safe File Operations

```python
from pathlib import Path
import tempfile

ALLOWED_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def safe_read_file(path: Path, base_dir: Path) -> str:
    """Safely read file with validation.
    
    Args:
        path: File path to read.
        base_dir: Allowed base directory.
        
    Returns:
        File content.
        
    Raises:
        ValueError: If validation fails.
    """
    # Validate path is within base directory
    resolved = safe_path(str(path), base_dir)

    # Check extension
    if resolved.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type not allowed: {resolved.suffix}")

    # Check file size
    if resolved.stat().st_size > MAX_FILE_SIZE:
        raise ValueError(f"File exceeds maximum size: {MAX_FILE_SIZE}")

    return resolved.read_text(encoding="utf-8")
```

### 8.2 Temporary File Handling

```python
import tempfile
from contextlib import contextmanager


@contextmanager
def secure_temp_file(suffix: str = ".tmp"):
    """Create secure temporary file that's cleaned up."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        yield path
    finally:
        os.close(fd)
        os.unlink(path)
```

---

## 9. Security Checklist

### 9.1 Code Review Checklist

| Check                  | Description                         |
|------------------------|-------------------------------------|
| ☐ No hardcoded secrets | All secrets from environment/config |
| ☐ Input validated      | All user input validated            |
| ☐ Output sanitized     | No sensitive data in logs/responses |
| ☐ Paths validated      | No path traversal possible          |
| ☐ Errors handled       | No sensitive info in error messages |
| ☐ Dependencies safe    | No known vulnerabilities            |

### 9.2 Pre-Deployment Checklist

| Check                  | Description                   |
|------------------------|-------------------------------|
| ☐ Security scan passed | Bandit, safety checks pass    |
| ☐ Secrets configured   | All secrets in secure storage |
| ☐ Logging configured   | Sensitive data not logged     |
| ☐ HTTPS enabled        | All traffic encrypted         |
| ☐ Rate limiting active | DoS protection in place       |
| ☐ Backups configured   | Recovery possible             |

### 9.3 Incident Response

| Step | Action                            |
|------|-----------------------------------|
| 1    | Identify and contain the incident |
| 2    | Assess impact and scope           |
| 3    | Rotate compromised credentials    |
| 4    | Fix vulnerability                 |
| 5    | Document and review               |

---

## Related

- `.knowledge/guidelines/ENGINEERING.md` — Engineering practices
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Error handling patterns
- `.knowledge/practices/engineering/LOGGING.md` — Logging practices
- `config/core/security.yaml` — Security configuration

---

*Part of SAGE Knowledge Base*
