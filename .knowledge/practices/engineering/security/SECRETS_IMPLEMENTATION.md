# Secrets Implementation Patterns

> Code patterns for implementing secrets management

---

## Table of Contents

- [1. Environment Variables](#1-environment-variables)
- [2. HashiCorp Vault](#2-hashicorp-vault)
- [3. AWS Secrets Manager](#3-aws-secrets-manager)
- [4. Secret Rotation](#4-secret-rotation)
- [5. Application Integration](#5-application-integration)

---

## 1. Environment Variables

### Basic Loading

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get with validation
def get_required_secret(name: str) -> str:
    """Get required secret from environment."""
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} environment variable required")
    return value

DATABASE_URL = get_required_secret("DATABASE_URL")
API_KEY = get_required_secret("API_KEY")
```
### Type-Safe Configuration

```python
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    database_url: SecretStr
    api_key: SecretStr
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
# Access: settings.api_key.get_secret_value()
```
---

## 2. HashiCorp Vault

### Basic Integration

```python
import hvac

class VaultSecretManager:
    """HashiCorp Vault integration."""
    
    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)
        if not self.client.is_authenticated():
            raise ValueError("Vault authentication failed")
    
    def get_secret(self, path: str, key: str) -> str:
        """Retrieve secret from Vault."""
        response = self.client.secrets.kv.v2.read_secret_version(path=path)
        return response["data"]["data"][key]
    
    def set_secret(self, path: str, data: dict) -> None:
        """Store secret in Vault."""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data
        )
```
### AppRole Authentication

```python
class VaultAppRole:
    """Vault AppRole authentication."""
    
    def __init__(self, url: str, role_id: str, secret_id: str):
        self.client = hvac.Client(url=url)
        self.client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id
        )
    
    def get_database_creds(self, role: str) -> dict:
        """Get dynamic database credentials."""
        response = self.client.secrets.database.generate_credentials(name=role)
        return {
            "username": response["data"]["username"],
            "password": response["data"]["password"],
            "ttl": response["lease_duration"]
        }
```
---

## 3. AWS Secrets Manager

### Basic Integration

```python
import boto3
import json

class AWSSecretManager:
    """AWS Secrets Manager integration."""
    
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client("secretsmanager", region_name=region)
    
    def get_secret(self, secret_name: str) -> dict:
        """Retrieve secret from AWS."""
        response = self.client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    
    def create_secret(self, name: str, value: dict) -> str:
        """Create new secret."""
        response = self.client.create_secret(
            Name=name,
            SecretString=json.dumps(value)
        )
        return response["ARN"]
    
    def update_secret(self, name: str, value: dict) -> None:
        """Update existing secret."""
        self.client.update_secret(
            SecretId=name,
            SecretString=json.dumps(value)
        )
```
### Caching for Performance

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedSecretManager:
    """Secret manager with caching."""
    
    def __init__(self, manager: AWSSecretManager, ttl_seconds: int = 300):
        self.manager = manager
        self.ttl = ttl_seconds
        self._cache = {}
        self._timestamps = {}
    
    def get_secret(self, name: str) -> dict:
        """Get secret with caching."""
        now = datetime.utcnow()
        
        if name in self._cache:
            if now - self._timestamps[name] < timedelta(seconds=self.ttl):
                return self._cache[name]
        
        secret = self.manager.get_secret(name)
        self._cache[name] = secret
        self._timestamps[name] = now
        return secret
```
---

## 4. Secret Rotation

### Automated Rotation Pattern

```python
from abc import ABC, abstractmethod

class SecretRotator(ABC):
    """Base class for secret rotation."""
    
    @abstractmethod
    def create_new_secret(self) -> str:
        """Generate new secret value."""
        pass
    
    @abstractmethod
    def test_secret(self, secret: str) -> bool:
        """Verify secret works."""
        pass
    
    @abstractmethod
    def apply_secret(self, secret: str) -> None:
        """Apply new secret to dependent services."""
        pass
    
    def rotate(self) -> None:
        """Perform rotation."""
        new_secret = self.create_new_secret()
        
        if not self.test_secret(new_secret):
            raise ValueError("New secret validation failed")
        
        self.apply_secret(new_secret)
```
### Database Password Rotation

```python
import secrets
import string

class DatabasePasswordRotator(SecretRotator):
    """Rotate database passwords."""
    
    def __init__(self, db_connection, secret_manager):
        self.db = db_connection
        self.secrets = secret_manager
    
    def create_new_secret(self) -> str:
        """Generate strong password."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(32))
    
    def test_secret(self, secret: str) -> bool:
        """Test database connection with new password."""
        try:
            # Test connection logic
            return True
        except Exception:
            return False
    
    def apply_secret(self, secret: str) -> None:
        """Update password in database and secret manager."""
        self.db.execute(f"ALTER USER app_user PASSWORD '{secret}'")
        self.secrets.update_secret("db-password", {"password": secret})
```
---

## 5. Application Integration

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

@lru_cache()
def get_secret_manager():
    settings = get_settings()
    return AWSSecretManager(region=settings.aws_region)

app = FastAPI()

@app.get("/api/data")
async def get_data(secrets: AWSSecretManager = Depends(get_secret_manager)):
    api_key = secrets.get_secret("external-api")["key"]
    # Use api_key...
```
### Context Manager Pattern

```python
from contextlib import contextmanager

@contextmanager
def secret_scope(secret_manager, secret_name: str):
    """Temporarily access a secret."""
    secret = secret_manager.get_secret(secret_name)
    try:
        yield secret
    finally:
        # Clear from memory
        del secret

# Usage
with secret_scope(manager, "api-credentials") as creds:
    response = call_api(creds["key"])
```
---

## Related

- `.knowledge/frameworks/security/SECRETS_MANAGEMENT.md` — Secrets management framework
- `.knowledge/practices/engineering/SECURITY_PATTERNS.md` — Security patterns
- `.knowledge/guidelines/SECURITY.md` — Security guidelines

---

*AI Collaboration Knowledge Base*
