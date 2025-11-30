# Authentication Patterns

> Identity verification mechanisms and best practices

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Authentication Methods](#2-authentication-methods)
- [3. Token-Based Auth](#3-token-based-auth)
- [4. Session Management](#4-session-management)
- [5. Multi-Factor Auth](#5-multi-factor-auth)
- [6. Implementation Patterns](#6-implementation-patterns)

---

## 1. Overview

### Authentication vs Authorization

| Aspect   | Authentication   | Authorization        |
|----------|------------------|----------------------|
| Question | "Who are you?"   | "What can you do?"   |
| Purpose  | Verify identity  | Grant permissions    |
| When     | Before access    | After authentication |
| Failure  | 401 Unauthorized | 403 Forbidden        |

### Authentication Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant Auth as Authn Server
    participant Authz as Authz Server
    participant R as Resource Server
    C->>Auth: Credentials
    Auth-->>C: Token
    C->>Authz: Token + Request
    Authz->>Auth: Validate
    Auth-->>Authz: Valid
    Authz->>R: Authorized Request
    R-->>C: Response
```
---

## 2. Authentication Methods

### Comparison

| Method            | Security   | UX        | Use Case           |
|-------------------|------------|-----------|--------------------|
| Password          | Medium     | Good      | Web apps           |
| API Key           | Low-Medium | Excellent | APIs               |
| JWT               | High       | Good      | Microservices      |
| OAuth 2.0         | High       | Medium    | Third-party        |
| SAML              | High       | Medium    | Enterprise SSO     |
| mTLS              | Very High  | Poor      | Service-to-service |
| Passkeys/WebAuthn | Very High  | Good      | Modern apps        |

### Password Authentication

```python
# Best practices for password handling
import hashlib
import secrets
from typing import Tuple
def hash_password(password: str) -> Tuple[str, str]:
    """Hash password with salt using secure algorithm."""
    salt = secrets.token_hex(32)
    # Use Argon2, bcrypt, or scrypt in production
    hash_value = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt.encode(),
        iterations=100000
    )
    return hash_value.hex(), salt
def verify_password(password: str, hash_value: str, salt: str) -> bool:
    """Verify password against stored hash."""
    new_hash, _ = hash_password_with_salt(password, salt)
    return secrets.compare_digest(new_hash, hash_value)
```
### API Key Authentication

```python
# API key validation pattern
from functools import wraps
from typing import Callable
def require_api_key(func: Callable) -> Callable:
    """Decorator to require valid API key."""
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise AuthenticationError("API key required")
        if not await validate_api_key(api_key):
            raise AuthenticationError("Invalid API key")
        return await func(request, *args, **kwargs)
    return wrapper
```
---

## 3. Token-Based Auth

### JWT Structure

```mermaid
flowchart LR
    subgraph JWT["JWT Token"]
        H["Header<br/>(Base64)<br/>alg, typ"]
        P["Payload<br/>(Base64)<br/>sub, iat, exp"]
        S["Signature<br/>(Base64)<br/>HMACSHA256()"]
    end
    H --> P --> S
```
### JWT Best Practices

| Practice   | Recommendation                                          |
|------------|---------------------------------------------------------|
| Algorithm  | Use RS256 or ES256, avoid HS256 for distributed systems |
| Expiration | Short-lived tokens (15-60 minutes)                      |
| Refresh    | Use secure refresh token rotation                       |
| Storage    | HttpOnly cookies or secure storage                      |
| Validation | Verify signature, expiration, issuer, audience          |
| Revocation | Implement token blacklist for critical actions          |

### JWT Implementation

```python
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any
class JWTManager:
    """JWT token management."""
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret = secret
        self.algorithm = algorithm
    def create_token(
        self,
        user_id: str,
        expires_in: timedelta = timedelta(hours=1),
        claims: Dict[str, Any] = None
    ) -> str:
        """Create JWT token."""
        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + expires_in,
            **(claims or {})
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token."""
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
```
---

## 4. Session Management

### Session Security

| Aspect        | Recommendation                    |
|---------------|-----------------------------------|
| ID Generation | Cryptographically secure random   |
| Storage       | Server-side (Redis, DB)           |
| Cookie Flags  | HttpOnly, Secure, SameSite=Strict |
| Expiration    | Absolute (24h) + idle (30min)     |
| Rotation      | After privilege change            |
| Invalidation  | On logout, password change        |

### Secure Session Pattern

```python
import secrets
from datetime import datetime, timedelta
from typing import Optional
class SessionManager:
    """Secure session management."""
    def __init__(self, store, idle_timeout: int = 1800):
        self.store = store
        self.idle_timeout = idle_timeout  # 30 minutes
    def create_session(self, user_id: str) -> str:
        """Create new session."""
        session_id = secrets.token_urlsafe(32)
        self.store.set(
            f"session:{session_id}",
            {
                "user_id"      : user_id,
                "created_at"   : datetime.utcnow().isoformat(),
                "last_activity": datetime.utcnow().isoformat()
            },
            expire=self.idle_timeout
        )
        return session_id
    def validate_session(self, session_id: str) -> Optional[str]:
        """Validate session and return user_id."""
        session = self.store.get(f"session:{session_id}")
        if not session:
            return None
        # Update last activity (sliding expiration)
        session["last_activity"] = datetime.utcnow().isoformat()
        self.store.set(
            f"session:{session_id}",
            session,
            expire=self.idle_timeout
        )
        return session["user_id"]
    def destroy_session(self, session_id: str) -> None:
        """Destroy session."""
        self.store.delete(f"session:{session_id}")
```
---

## 5. Multi-Factor Auth

### MFA Methods

| Method            | Security | Convenience | Cost   |
|-------------------|----------|-------------|--------|
| SMS OTP           | Low      | High        | Low    |
| Email OTP         | Low      | High        | Low    |
| TOTP (App)        | Medium   | Medium      | Free   |
| Push Notification | Medium   | High        | Medium |
| Hardware Key      | High     | Low         | High   |
| Biometric         | High     | High        | Medium |

### TOTP Implementation

```python
import pyotp
import qrcode
from io import BytesIO
class TOTPManager:
    """Time-based OTP management."""
    def generate_secret(self) -> str:
        """Generate new TOTP secret."""
        return pyotp.random_base32()
    def get_provisioning_uri(
        self,
        secret: str,
        user_email: str,
        issuer: str = "the system"
    ) -> str:
        """Get URI for QR code."""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
    def generate_qr_code(self, uri: str) -> bytes:
        """Generate QR code image."""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    def verify_code(self, secret: str, code: str) -> bool:
        """Verify TOTP code."""
        totp = pyotp.TOTP(secret)
        return totp.verify(code, valid_window=1)
```
---

## 6. Implementation Patterns

### Login Flow

```python
async def login(request: LoginRequest) -> LoginResponse:
    """Secure login implementation."""
    # 1. Rate limiting
    if await is_rate_limited(request.ip):
        raise TooManyRequestsError("Too many login attempts")
    # 2. Find user
    user = await find_user_by_email(request.email)
    if not user:
        # Constant time response to prevent enumeration
        await simulate_password_check()
        raise AuthenticationError("Invalid credentials")
    # 3. Verify password
    if not verify_password(request.password, user.password_hash):
        await record_failed_attempt(request.email, request.ip)
        raise AuthenticationError("Invalid credentials")
    # 4. Check MFA
    if user.mfa_enabled:
        if not request.mfa_code:
            return LoginResponse(requires_mfa=True)
        if not verify_mfa(user.mfa_secret, request.mfa_code):
            raise AuthenticationError("Invalid MFA code")
    # 5. Create session/token
    token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    # 6. Audit log
    await audit_log("login_success", user.id, request.ip)
    return LoginResponse(
        access_token=token,
        refresh_token=refresh_token,
        expires_in=3600
    )
```
### Middleware Pattern

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
security = HTTPBearer()
async def auth_middleware(request: Request, call_next):
    """Authentication middleware."""
    # Skip auth for public endpoints
    if request.url.path in PUBLIC_ENDPOINTS:
        return await call_next(request)
    # Extract token
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = auth_header.split(" ")[1]
    # Verify token
    try:
        payload = verify_token(token)
        request.state.user_id = payload["sub"]
        request.state.roles = payload.get("roles", [])
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return await call_next(request)
```
---

## Quick Reference

### Security Headers

```python
# Required security headers for auth endpoints
SECURITY_HEADERS = {
    "X-Content-Type-Options"   : "nosniff",
    "X-Frame-Options"          : "DENY",
    "X-XSS-Protection"         : "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Cache-Control"            : "no-store",
    "Pragma"                   : "no-cache"
}
```
### Password Requirements

| Requirement | Minimum                       |
|-------------|-------------------------------|
| Length      | 12 characters                 |
| Complexity  | Upper, lower, number, special |
| History     | Last 5 passwords              |
| Expiration  | 90 days (if required)         |
| Lockout     | 5 failures, 15 min lockout    |

---

## Related

- `.knowledge/frameworks/security/AUTHORIZATION.md` — Access control patterns
- `.knowledge/frameworks/security/SECRETS_MANAGEMENT.md` — Secure credential handling
- `.knowledge/frameworks/security/SECURITY_CHECKLIST.md` — Implementation checklist

---

*AI Collaboration Knowledge Base*
