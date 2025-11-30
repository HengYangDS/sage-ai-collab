# Secrets Management

> Secure handling of sensitive data, credentials, and encryption keys

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Types of Secrets](#2-types-of-secrets)
- [3. Storage Solutions](#3-storage-solutions)
- [4. Best Practices](#4-best-practices)
- [5. Implementation Patterns](#5-implementation-patterns)
- [6. Rotation Strategies](#6-rotation-strategies)

---

## 1. Overview

### What Are Secrets?

Secrets are sensitive data that must be protected from unauthorized access:

| Category               | Examples                                    |
|------------------------|---------------------------------------------|
| **Credentials**        | Passwords, API keys, tokens                 |
| **Keys**               | Encryption keys, SSH keys, TLS certificates |
| **Connection Strings** | Database URLs, service endpoints            |
| **Configuration**      | Sensitive settings, feature flags           |

### Threat Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Secret Exposure Risks                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Source Code ──────▶ Git history, public repos             │
│  Logs ─────────────▶ Log files, monitoring systems         │
│  Environment ──────▶ Process dumps, container inspection   │
│  Memory ───────────▶ Core dumps, debugging                 │
│  Network ──────────▶ Man-in-the-middle, sniffing           │
│  Storage ──────────▶ Unencrypted disks, backups            │
│  Humans ───────────▶ Social engineering, shoulder surfing  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Types of Secrets

### Classification

| Type                     | Sensitivity | Rotation Frequency | Example                  |
|--------------------------|-------------|--------------------|--------------------------|
| **API Keys**             | Medium      | Monthly-Quarterly  | Third-party service keys |
| **Database Credentials** | High        | Quarterly          | PostgreSQL password      |
| **Encryption Keys**      | Critical    | Annually           | AES master key           |
| **OAuth Secrets**        | High        | Quarterly          | Client secret            |
| **TLS Certificates**     | High        | Annually           | Server certificates      |
| **SSH Keys**             | High        | Annually           | Deployment keys          |
| **Tokens**               | Medium      | Short-lived        | JWT, session tokens      |

### Secret Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Generate │───▶│  Store   │───▶│   Use    │───▶│  Rotate  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     ▼               ▼               ▼               ▼
  Secure          Encrypted      Minimal         Automated
  Random          At Rest        Exposure        Schedule
```

---

## 3. Storage Solutions

### Comparison

| Solution                | Security | Ease of Use | Cost | Best For        |
|-------------------------|----------|-------------|------|-----------------|
| **Env Variables**       | Low      | High        | Free | Development     |
| **Config Files**        | Low      | High        | Free | Development     |
| **HashiCorp Vault**     | High     | Medium      | $$   | Enterprise      |
| **AWS Secrets Manager** | High     | High        | $    | AWS workloads   |
| **Azure Key Vault**     | High     | High        | $    | Azure workloads |
| **GCP Secret Manager**  | High     | High        | $    | GCP workloads   |
| **1Password/Bitwarden** | Medium   | High        | $    | Team secrets    |

### Environment Variables (Development Only)

```bash
# .env file (NEVER commit to git)
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk-secret-key-here
JWT_SECRET=your-jwt-secret

# .gitignore
.env
.env.*
!.env.example
```

```python
# Load in application
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv("DATABASE_URL")
```

### HashiCorp Vault

```python
import hvac

class VaultSecretManager:
    """HashiCorp Vault integration."""
    
    def __init__(self, url: str, token: str):
        self.client = hvac.Client(url=url, token=token)
    
    def get_secret(self, path: str, key: str) -> str:
        """Retrieve secret from Vault."""
        response = self.client.secrets.kv.v2.read_secret_version(
            path=path
        )
        return response["data"]["data"][key]
    
    def set_secret(self, path: str, data: dict) -> None:
        """Store secret in Vault."""
        self.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=data
        )
    
    def rotate_secret(self, path: str, key: str, new_value: str) -> None:
        """Rotate a secret."""
        current = self.client.secrets.kv.v2.read_secret_version(path=path)
        data = current["data"]["data"]
        data[key] = new_value
        self.set_secret(path, data)
```

### AWS Secrets Manager

```python
import boto3
import json

class AWSSecretManager:
    """AWS Secrets Manager integration."""
    
    def __init__(self, region: str = "us-east-1"):
        self.client = boto3.client(
            "secretsmanager",
            region_name=region
        )
    
    def get_secret(self, secret_name: str) -> dict:
        """Retrieve secret from AWS."""
        response = self.client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(response["SecretString"])
    
    def create_secret(self, name: str, value: dict) -> str:
        """Create new secret."""
        response = self.client.create_secret(
            Name=name,
            SecretString=json.dumps(value)
        )
        return response["ARN"]
    
    def rotate_secret(self, secret_name: str) -> None:
        """Trigger secret rotation."""
        self.client.rotate_secret(
            SecretId=secret_name,
            RotationLambdaARN="arn:aws:lambda:...:rotation-function"
        )
```

---

## 4. Best Practices

### DO's and DON'Ts

| ✅ DO                   | ❌ DON'T                    |
|------------------------|----------------------------|
| Use secrets manager    | Hardcode secrets           |
| Encrypt at rest        | Store in plain text        |
| Rotate regularly       | Use same secret forever    |
| Audit access           | Ignore access logs         |
| Use least privilege    | Share admin credentials    |
| Encrypt in transit     | Send over HTTP             |
| Use short-lived tokens | Use long-lived credentials |

### Secret Generation

```python
import secrets
import string

def generate_api_key(length: int = 32) -> str:
    """Generate cryptographically secure API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_password(
    length: int = 16,
    include_special: bool = True
) -> str:
    """Generate secure password."""
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += "!@#$%^&*"
    
    # Ensure at least one of each required type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]
    if include_special:
        password.append(secrets.choice("!@#$%^&*"))
    
    # Fill rest randomly
    password.extend(
        secrets.choice(alphabet)
        for _ in range(length - len(password))
    )
    
    # Shuffle
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def generate_encryption_key(bits: int = 256) -> bytes:
    """Generate encryption key."""
    return secrets.token_bytes(bits // 8)
```

### Secure Transmission

```python
from cryptography.fernet import Fernet
import base64

class SecretTransmitter:
    """Secure secret transmission."""
    
    def __init__(self, key: bytes):
        self.cipher = Fernet(base64.urlsafe_b64encode(key))
    
    def encrypt(self, secret: str) -> str:
        """Encrypt secret for transmission."""
        return self.cipher.encrypt(secret.encode()).decode()
    
    def decrypt(self, encrypted: str) -> str:
        """Decrypt received secret."""
        return self.cipher.decrypt(encrypted.encode()).decode()
```

---

## 5. Implementation Patterns

### Secret Provider Interface

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict

class SecretProvider(ABC):
    """Abstract secret provider interface."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Get secret value."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """Set secret value."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete secret."""
        pass
    
    @abstractmethod
    async def list(self, prefix: str = "") -> list[str]:
        """List secret keys."""
        pass

class CompositeSecretProvider(SecretProvider):
    """Fallback chain of providers."""
    
    def __init__(self, providers: list[SecretProvider]):
        self.providers = providers
    
    async def get(self, key: str) -> Optional[str]:
        for provider in self.providers:
            value = await provider.get(key)
            if value is not None:
                return value
        return None
```

### Caching with TTL

```python
from datetime import datetime, timedelta
from typing import Optional, Tuple

class CachedSecretProvider:
    """Cache secrets with TTL."""
    
    def __init__(
        self,
        provider: SecretProvider,
        ttl_seconds: int = 300
    ):
        self.provider = provider
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cache: Dict[str, Tuple[str, datetime]] = {}
    
    async def get(self, key: str) -> Optional[str]:
        # Check cache
        if key in self.cache:
            value, cached_at = self.cache[key]
            if datetime.now() - cached_at < self.ttl:
                return value
            del self.cache[key]
        
        # Fetch from provider
        value = await self.provider.get(key)
        if value:
            self.cache[key] = (value, datetime.now())
        return value
    
    def invalidate(self, key: str) -> None:
        """Invalidate cached secret."""
        self.cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cached secrets."""
        self.cache.clear()
```

### Configuration Integration

```python
from pydantic import BaseSettings, SecretStr
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with secrets."""
    
    # Regular settings
    app_name: str = "SAGE"
    debug: bool = False
    
    # Secrets (masked in logs/repr)
    database_url: SecretStr
    api_key: SecretStr
    jwt_secret: SecretStr
    
    class Config:
        env_file = ".env"
        secrets_dir = "/run/secrets"  # Docker secrets

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Usage
settings = get_settings()
db_url = settings.database_url.get_secret_value()
```

### Kubernetes Secrets

```yaml
# kubernetes/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  database-url: cG9zdGdyZXNxbDovLy4uLg==  # base64 encoded
  api-key: c2stc2VjcmV0LWtleQ==
---
# Mount in pod
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: app:latest
      envFrom:
        - secretRef:
            name: app-secrets
      volumeMounts:
        - name: secrets
          mountPath: /run/secrets
          readOnly: true
  volumes:
    - name: secrets
      secret:
        secretName: app-secrets
```

---

## 6. Rotation Strategies

### Rotation Types

| Strategy      | Downtime | Complexity | Use Case           |
|---------------|----------|------------|--------------------|
| **Manual**    | Possible | Low        | Small scale        |
| **Scheduled** | Minimal  | Medium     | Regular rotation   |
| **Automatic** | Zero     | High       | Critical systems   |
| **On-demand** | Variable | Medium     | Security incidents |

### Zero-Downtime Rotation

```python
class SecretRotator:
    """Zero-downtime secret rotation."""
    
    def __init__(
        self,
        secret_manager: SecretProvider,
        notifier: callable
    ):
        self.secrets = secret_manager
        self.notify = notifier
    
    async def rotate(self, key: str, new_value: str) -> None:
        """
        Rotate secret with zero downtime.
        
        Strategy:
        1. Store new secret alongside old
        2. Notify services to use new secret
        3. Wait for propagation
        4. Remove old secret
        """
        # 1. Store both versions
        old_value = await self.secrets.get(key)
        await self.secrets.set(f"{key}_new", new_value)
        await self.secrets.set(f"{key}_old", old_value)
        
        # 2. Update primary to new value
        await self.secrets.set(key, new_value)
        
        # 3. Notify services
        await self.notify(key, "rotated")
        
        # 4. Wait for propagation (services should reload)
        await asyncio.sleep(60)
        
        # 5. Clean up old version
        await self.secrets.delete(f"{key}_old")
        await self.secrets.delete(f"{key}_new")
        
        # 6. Audit log
        await self.audit_log(key, "rotation_complete")
```

### Rotation Schedule

| Secret Type        | Frequency | Trigger       |
|--------------------|-----------|---------------|
| API Keys           | 90 days   | Scheduled     |
| Database Passwords | 90 days   | Scheduled     |
| JWT Secrets        | 30 days   | Scheduled     |
| TLS Certificates   | 365 days  | Before expiry |
| Encryption Keys    | 365 days  | Scheduled     |
| OAuth Secrets      | 90 days   | Scheduled     |
| SSH Keys           | 365 days  | Scheduled     |

---

## Quick Reference

### Security Checklist

- [ ] No secrets in source code
- [ ] No secrets in logs
- [ ] Secrets encrypted at rest
- [ ] Secrets encrypted in transit
- [ ] Access to secrets audited
- [ ] Rotation schedule defined
- [ ] Emergency rotation procedure documented
- [ ] Least privilege access to secrets
- [ ] Secrets scoped to environment

### Emergency Response

```
1. Identify compromised secret
2. Generate new secret immediately
3. Update in secrets manager
4. Deploy/restart affected services
5. Revoke old secret
6. Audit access logs
7. Document incident
8. Review and improve
```

---

## Related

- `.knowledge/frameworks/security/authentication.md` — Credential usage patterns
- `.knowledge/frameworks/security/authorization.md` — Access control
- `.knowledge/frameworks/security/security_checklist.md` — Complete security review

---

*Part of SAGE Knowledge Base - Security Framework*
