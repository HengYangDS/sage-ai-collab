# Security Checklist

> Comprehensive security review guide for development, deployment, and audit

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Development](#2-development)
- [3. Code Review](#3-code-review)
- [4. Deployment](#4-deployment)
- [5. Operations](#5-operations)
- [6. Incident Response](#6-incident-response)

---

## 1. Overview

### Checklist Categories

| Category        | When to Use    | Frequency          |
|-----------------|----------------|--------------------|
| **Development** | During coding  | Continuous         |
| **Code Review** | Before merge   | Every PR           |
| **Deployment**  | Before release | Every deploy       |
| **Operations**  | In production  | Weekly/Monthly     |
| **Audit**       | Compliance     | Quarterly/Annually |

### Risk Levels

| Level    | Icon | Response Time |
|----------|------|---------------|
| Critical | 🔴   | Immediate     |
| High     | 🟠   | 24 hours      |
| Medium   | 🟡   | 1 week        |
| Low      | 🟢   | Next sprint   |

---

## 2. Development

### Input Validation

- [ ] 🔴 All user inputs validated server-side
- [ ] 🔴 Input length limits enforced
- [ ] 🔴 Input type validation (numbers, emails, dates)
- [ ] 🟠 Whitelist validation where possible
- [ ] 🟠 Reject unexpected fields in API requests
- [ ] 🟡 Custom error messages don't leak information

```python
# Good: Explicit validation
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

### SQL Injection Prevention

- [ ] 🔴 Parameterized queries used exclusively
- [ ] 🔴 No string concatenation in SQL
- [ ] 🟠 ORM used correctly
- [ ] 🟠 Stored procedures parameterized

```python
# Bad: SQL injection vulnerability
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# Good: Parameterized query
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))

# Good: ORM with proper filtering
User.objects.filter(name=user_input)
```

### XSS Prevention

- [ ] 🔴 Output encoding for HTML context
- [ ] 🔴 Content-Security-Policy header set
- [ ] 🟠 Input sanitization for rich text
- [ ] 🟠 Template auto-escaping enabled
- [ ] 🟡 DOM manipulation uses safe APIs

```python
# HTML encoding
from markupsafe import escape
safe_output = escape(user_input)

# Content-Security-Policy
response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'"
)
```

### Authentication

- [ ] 🔴 Passwords hashed with bcrypt/Argon2
- [ ] 🔴 Password strength requirements enforced
- [ ] 🔴 Account lockout after failed attempts
- [ ] 🔴 Session tokens cryptographically random
- [ ] 🟠 Multi-factor authentication available
- [ ] 🟠 Password reset tokens expire
- [ ] 🟡 Login attempts logged

### Authorization

- [ ] 🔴 Server-side authorization checks
- [ ] 🔴 Resource ownership verified
- [ ] 🔴 Admin functions protected
- [ ] 🟠 Least privilege principle applied
- [ ] 🟠 Role-based access control implemented
- [ ] 🟡 Authorization decisions logged

### Secrets Management

- [ ] 🔴 No secrets in source code
- [ ] 🔴 No secrets in logs
- [ ] 🔴 Secrets loaded from environment/vault
- [ ] 🟠 Different secrets per environment
- [ ] 🟠 Secrets rotation documented
- [ ] 🟡 Secrets have expiration dates

---

## 3. Code Review

### Security-Focused Review

```
┌─────────────────────────────────────────────────────────────┐
│                  Code Review Security Focus                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Authentication Changes                                  │
│     □ Password handling correct?                            │
│     □ Session management secure?                            │
│     □ Token validation proper?                              │
│                                                             │
│  2. Authorization Changes                                   │
│     □ Access control enforced?                              │
│     □ Resource ownership checked?                           │
│     □ No privilege escalation?                              │
│                                                             │
│  3. Data Handling                                           │
│     □ Input validated?                                      │
│     □ Output encoded?                                       │
│     □ Sensitive data protected?                             │
│                                                             │
│  4. Dependencies                                            │
│     □ New dependencies reviewed?                            │
│     □ Known vulnerabilities checked?                        │
│     □ Minimal permissions granted?                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Review Checklist

- [ ] 🔴 No hardcoded credentials
- [ ] 🔴 No sensitive data in logs
- [ ] 🔴 SQL queries parameterized
- [ ] 🔴 User input validated
- [ ] 🔴 Output properly encoded
- [ ] 🟠 Error handling doesn't leak info
- [ ] 🟠 New dependencies security-reviewed
- [ ] 🟠 Cryptographic functions used correctly
- [ ] 🟡 Comments don't contain sensitive info
- [ ] 🟡 Debug code removed

### Automated Checks

```yaml
# .github/workflows/security.yml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    # Static analysis
    - name: Run Bandit
      run: bandit -r src/ -ll
    
    # Dependency scanning
    - name: Check dependencies
      run: pip-audit
    
    # Secret scanning
    - name: Scan for secrets
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
    
    # SAST
    - name: CodeQL Analysis
      uses: github/codeql-action/analyze@v2
```

---

## 4. Deployment

### Pre-Deployment

- [ ] 🔴 All security tests passing
- [ ] 🔴 Dependencies vulnerability-free
- [ ] 🔴 Secrets configured in target environment
- [ ] 🔴 TLS certificates valid
- [ ] 🟠 Security headers configured
- [ ] 🟠 Logging and monitoring ready
- [ ] 🟡 Rollback procedure documented

### Infrastructure

- [ ] 🔴 HTTPS only (TLS 1.2+)
- [ ] 🔴 Firewall rules configured
- [ ] 🔴 Database not publicly accessible
- [ ] 🔴 Admin interfaces IP-restricted
- [ ] 🟠 Rate limiting enabled
- [ ] 🟠 DDoS protection configured
- [ ] 🟠 WAF rules applied

### Security Headers

```python
# Required security headers
SECURITY_HEADERS = {
    # Prevent XSS
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    
    # HTTPS enforcement
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
    
    # Content Security Policy
    "Content-Security-Policy": "default-src 'self'; script-src 'self'",
    
    # Referrer policy
    "Referrer-Policy": "strict-origin-when-cross-origin",
    
    # Permissions policy
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}
```

### Container Security

- [ ] 🔴 Base image from trusted source
- [ ] 🔴 No root user in container
- [ ] 🔴 Read-only file system where possible
- [ ] 🔴 No sensitive data in image
- [ ] 🟠 Image vulnerability scanned
- [ ] 🟠 Resource limits set
- [ ] 🟡 Security context defined

```dockerfile
# Secure Dockerfile example
FROM python:3.12-slim AS base

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app
WORKDIR /home/app

# Copy only necessary files
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app src/ ./src/

# Run as non-root
USER app
CMD ["python", "-m", "sage"]
```

---

## 5. Operations

### Monitoring

- [ ] 🔴 Authentication failures monitored
- [ ] 🔴 Authorization failures monitored
- [ ] 🔴 Error rate anomalies alerted
- [ ] 🟠 Request rate anomalies detected
- [ ] 🟠 Data access patterns monitored
- [ ] 🟡 Security events aggregated

### Logging

- [ ] 🔴 Authentication events logged
- [ ] 🔴 Authorization decisions logged
- [ ] 🔴 Data access logged (who, what, when)
- [ ] 🔴 No sensitive data in logs
- [ ] 🟠 Logs shipped to secure location
- [ ] 🟠 Log retention policy defined
- [ ] 🟡 Log integrity protected

```python
# Secure logging pattern
import structlog

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

### Regular Tasks

| Task               | Frequency | Owner    |
|--------------------|-----------|----------|
| Dependency updates | Weekly    | Dev Team |
| Vulnerability scan | Weekly    | Security |
| Access review      | Monthly   | Security |
| Secret rotation    | Quarterly | Ops      |
| Penetration test   | Annually  | External |
| Security training  | Annually  | All      |

### Weekly Security Tasks

- [ ] Review security alerts
- [ ] Check dependency vulnerabilities
- [ ] Review failed login attempts
- [ ] Check certificate expiration
- [ ] Review access logs for anomalies

### Monthly Security Tasks

- [ ] Review user access rights
- [ ] Check for unused accounts
- [ ] Review API key usage
- [ ] Update security documentation
- [ ] Review firewall rules

---

## 6. Incident Response

### Incident Classification

| Severity | Definition    | Response Time | Examples                                 |
|----------|---------------|---------------|------------------------------------------|
| P1       | Active breach | Immediate     | Data exfiltration, system compromise     |
| P2       | High risk     | 1 hour        | Credential leak, vulnerability exploit   |
| P3       | Medium risk   | 4 hours       | Failed attacks, suspicious activity      |
| P4       | Low risk      | 24 hours      | Policy violation, minor misconfiguration |

### Response Procedure

```
┌─────────────────────────────────────────────────────────────┐
│                   Incident Response Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DETECT                                                  │
│     ├── Alert triggered                                     │
│     ├── Report received                                     │
│     └── Anomaly identified                                  │
│              │                                              │
│              ▼                                              │
│  2. ASSESS                                                  │
│     ├── Classify severity                                   │
│     ├── Identify scope                                      │
│     └── Notify stakeholders                                 │
│              │                                              │
│              ▼                                              │
│  3. CONTAIN                                                 │
│     ├── Isolate affected systems                           │
│     ├── Block attack vectors                               │
│     └── Preserve evidence                                   │
│              │                                              │
│              ▼                                              │
│  4. ERADICATE                                               │
│     ├── Remove threat                                       │
│     ├── Patch vulnerabilities                              │
│     └── Reset compromised credentials                       │
│              │                                              │
│              ▼                                              │
│  5. RECOVER                                                 │
│     ├── Restore from clean backup                          │
│     ├── Verify system integrity                            │
│     └── Monitor for recurrence                             │
│              │                                              │
│              ▼                                              │
│  6. LEARN                                                   │
│     ├── Document incident                                   │
│     ├── Conduct post-mortem                                │
│     └── Implement improvements                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Emergency Contacts

| Role          | Responsibility         | Contact   |
|---------------|------------------------|-----------|
| Security Lead | Incident coordination  | [On-call] |
| Platform Lead | System access          | [On-call] |
| Legal         | Compliance/disclosure  | [Contact] |
| PR            | External communication | [Contact] |

### Immediate Actions

```
□ Credential Compromise
  1. Revoke affected credentials immediately
  2. Force password reset for affected users
  3. Review access logs for unauthorized activity
  4. Notify affected users

□ Data Breach
  1. Identify scope of exposed data
  2. Preserve logs and evidence
  3. Notify legal team
  4. Prepare disclosure if required

□ System Compromise
  1. Isolate affected systems
  2. Capture memory/disk images
  3. Block attacker access
  4. Restore from known-good backup
```

---

## Quick Reference Card

### Critical Controls (Must Have)

| Control               | Status |
|-----------------------|--------|
| Input validation      | ☐      |
| Output encoding       | ☐      |
| Parameterized queries | ☐      |
| Password hashing      | ☐      |
| HTTPS everywhere      | ☐      |
| No hardcoded secrets  | ☐      |
| Access control        | ☐      |
| Security logging      | ☐      |

### OWASP Top 10 Mapping

| Risk                          | Checklist Section     |
|-------------------------------|-----------------------|
| A01 Broken Access Control     | Authorization         |
| A02 Cryptographic Failures    | Secrets Management    |
| A03 Injection                 | Input Validation, SQL |
| A04 Insecure Design           | Code Review           |
| A05 Security Misconfiguration | Deployment            |
| A06 Vulnerable Components     | Dependencies          |
| A07 Auth Failures             | Authentication        |
| A08 Data Integrity Failures   | Deployment            |
| A09 Logging Failures          | Operations            |
| A10 SSRF                      | Input Validation      |

---

## Related

- [Authentication](authentication.md) — Identity verification
- [Authorization](authorization.md) — Access control
- [Secrets Management](secrets_management.md) — Credential handling
- `.knowledge/practices/engineering/code_review.md` — Review practices

---

*Part of SAGE Knowledge Base - Security Framework*
