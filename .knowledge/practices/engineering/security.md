# Security Practices

> Security best practices for Python applications and knowledge systems

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Code Security](#2-code-security)
- [3. Dependency Security](#3-dependency-security)
- [4. Secrets Management](#4-secrets-management)
- [5. Input Validation](#5-input-validation)
- [6. Authentication & Authorization](#6-authentication--authorization)

---

## 1. Overview

### 1.1 Security Principles

| Principle            | Description                       |
|----------------------|-----------------------------------|
| **Defense in Depth** | Multiple layers of security       |
| **Least Privilege**  | Minimum necessary access          |
| **Fail Secure**      | Default to secure state on errors |
| **Zero Trust**       | Verify everything, trust nothing  |

### 1.2 Security Checklist

- [ ] No hardcoded secrets in code
- [ ] Dependencies scanned for vulnerabilities
- [ ] Input validation on all user data
- [ ] Proper authentication/authorization
- [ ] Secure logging (no sensitive data)
- [ ] HTTPS for all network communication

---

## 2. Code Security

### 2.1 Common Vulnerabilities

| Vulnerability         | Risk | Mitigation                              |
|-----------------------|------|-----------------------------------------|
| **Injection**         | High | Parameterized queries, input validation |
| **Path Traversal**    | High | Validate and sanitize file paths        |
| **Deserialization**   | High | Avoid pickle, use safe formats          |
| **Command Injection** | High | Avoid shell=True, use subprocess safely |

### 2.2 Secure Coding Patterns

#### Safe File Operations

```python
from pathlib import Path


def safe_read_file(base_dir: Path, filename: str) -> str:
    """Read file safely, preventing path traversal."""
    # Resolve to absolute path
    base = base_dir.resolve()
    target = (base / filename).resolve()

    # Ensure target is within base directory
    if not str(target).startswith(str(base)):
        raise ValueError("Path traversal detected")

    return target.read_text()
```

#### Safe Subprocess Execution

```python
import subprocess
from shlex import quote


def safe_command(args: list[str]) -> str:
    """Execute command safely without shell injection."""
    # Never use shell=True with user input
    result = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return result.stdout
```

#### Safe Deserialization

```python
import json
from typing import Any


# UNSAFE - Never use with untrusted data
# import pickle
# data = pickle.loads(untrusted_bytes)

# SAFE - Use JSON for data exchange
def safe_deserialize(data: str) -> Any:
    """Safely deserialize JSON data."""
    return json.loads(data)


# For configuration, use YAML with safe loader
import yaml


def safe_yaml_load(content: str) -> dict:
    """Load YAML safely."""
    return yaml.safe_load(content)
```

### 2.3 Security Linting

```toml
# pyproject.toml - Ruff security rules
[tool.ruff.lint]
select = [
    "S", # flake8-bandit (security)
]

# Specific security checks
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
```

---

## 3. Dependency Security

### 3.1 Vulnerability Scanning

```bash
# Install pip-audit
pip install pip-audit

# Scan for vulnerabilities
pip-audit

# Scan specific requirements
pip-audit -r requirements.txt

# Generate report
pip-audit --format json -o audit-report.json
```

### 3.2 Automated Scanning in CI

```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install pip-audit

      - name: Run security audit
        run: pip-audit --strict
```

### 3.3 Dependency Best Practices

| Practice            | Description                 |
|---------------------|-----------------------------|
| **Pin versions**    | Use lock files with hashes  |
| **Regular updates** | Weekly dependency updates   |
| **Minimal deps**    | Only add what's necessary   |
| **Review sources**  | Verify package authenticity |

---

## 4. Secrets Management

### 4.1 Secret Types

| Type                | Examples              | Storage                  |
|---------------------|-----------------------|--------------------------|
| **API Keys**        | OpenAI, GitHub tokens | Environment variables    |
| **Credentials**     | Database passwords    | Secret manager           |
| **Certificates**    | TLS/SSL certs         | Secure file storage      |
| **Encryption Keys** | AES keys              | Hardware security module |

### 4.2 Environment Variables

```python
import os
from typing import Optional


def get_secret(name: str, default: Optional[str] = None) -> str:
    """Get secret from environment with validation."""
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Required secret {name} not found")
    return value


# Usage
api_key = get_secret("OPENAI_API_KEY")
```

### 4.3 Configuration with Pydantic

```python
from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    """Application settings with secret handling."""

    database_url: SecretStr
    api_key: SecretStr
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Usage
settings = Settings()
# SecretStr prevents accidental logging
print(settings.api_key)  # Outputs: SecretStr('**********')
# Get actual value when needed
actual_key = settings.api_key.get_secret_value()
```

### 4.4 Git Security

```gitignore
# .gitignore - Never commit secrets
.env
.env.*
*.pem
*.key
secrets/
config/local.yaml
```

Pre-commit hook to detect secrets:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: [ '--baseline', '.secrets.baseline' ]
```

---

## 5. Input Validation

### 5.1 Validation Patterns

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
import re


class UserInput(BaseModel):
    """Validated user input model."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=150)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v


# Usage
try:
    user = UserInput(username="john_doe", email="john@example.com")
except ValidationError as e:
    # Handle validation errors
    print(e.json())
```

### 5.2 File Upload Validation

```python
from pathlib import Path
from typing import BinaryIO

ALLOWED_EXTENSIONS = {'.txt', '.md', '.yaml', '.json'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_upload(filename: str, file: BinaryIO) -> bool:
    """Validate uploaded file."""
    # Check extension
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension {ext} not allowed")

    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset position

    if size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {size} bytes")

    return True
```

### 5.3 SQL Injection Prevention

```python
# UNSAFE - Never do this
# query = f"SELECT * FROM users WHERE name = '{user_input}'"

# SAFE - Use parameterized queries
import sqlite3


def safe_query(conn: sqlite3.Connection, username: str) -> list:
    """Query with parameterized input."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )
    return cursor.fetchall()
```

---

## 6. Authentication & Authorization

### 6.1 Authentication Best Practices

| Practice               | Description                               |
|------------------------|-------------------------------------------|
| **Strong passwords**   | Minimum length, complexity requirements   |
| **Password hashing**   | Use bcrypt, argon2, or scrypt             |
| **MFA**                | Multi-factor authentication when possible |
| **Session management** | Secure tokens, proper expiration          |

### 6.2 Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password securely."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)
```

### 6.3 Token-Based Auth

```python
from datetime import datetime, timedelta
from typing import Optional
import jwt

SECRET_KEY = get_secret("JWT_SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify and decode JWT token."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

## Quick Reference

### Security Commands

```bash
# Scan for vulnerabilities
pip-audit

# Check for secrets in code
detect-secrets scan

# Run security linter
ruff check --select S .

# Generate secure random key
python -c "import secrets; print(secrets.token_hex(32))"
```

### Security Checklist

| Area             | Check                               |
|------------------|-------------------------------------|
| **Code**         | No injection vulnerabilities        |
| **Dependencies** | No known vulnerabilities            |
| **Secrets**      | Not in version control              |
| **Input**        | All user input validated            |
| **Auth**         | Proper authentication/authorization |
| **Logging**      | No sensitive data logged            |

---

## Related

- `practices/engineering/error_handling.md` — Secure error handling
- `practices/engineering/logging.md` — Secure logging practices
- `guidelines/python.md` — Python coding standards
- `scenarios/devops/context.md` — DevOps security

---

*Part of SAGE Knowledge Base*
