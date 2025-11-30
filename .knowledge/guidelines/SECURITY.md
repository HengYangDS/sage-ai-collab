# Security Guidelines

> Security principles and standards for knowledge base development

---

## Table of Contents

- [1. Security Principles](#1-security-principles)
- [2. Risk Categories](#2-risk-categories)
- [3. Secret Management](#3-secret-management)
- [4. Input Validation](#4-input-validation)
- [5. Output Sanitization](#5-output-sanitization)
- [6. Dependency Security](#6-dependency-security)
- [7. Logging Security](#7-logging-security)
- [8. API Security](#8-api-security)
- [9. File System Security](#9-file-system-security)
- [10. Security Checklist](#10-security-checklist)

---

## 1. Security Principles

| Principle            | Description                          |
|----------------------|--------------------------------------|
| **Defense in Depth** | Multiple layers of security controls |
| **Least Privilege**  | Minimum necessary permissions        |
| **Fail Secure**      | Default to secure state on failure   |
| **Zero Trust**       | Verify everything, trust nothing     |

---

## 2. Risk Categories

| Category     | Examples                               | Priority |
|--------------|----------------------------------------|----------|
| **Critical** | Secret exposure, remote code execution | P0       |
| **High**     | SQL injection, path traversal          | P1       |
| **Medium**   | Information disclosure, DoS            | P2       |
| **Low**      | Minor information leaks                | P3       |

---

## 3. Secret Management

| Rule                    | Description                     |
|-------------------------|---------------------------------|
| Never hardcode          | No secrets in source code       |
| Use secret managers     | Production: Vault, AWS SM, etc. |
| Environment variables   | Development/CI environments     |
| Rotate regularly        | API keys: 90d, DB: 60d, Tokens: 30d |
| gitignore secrets       | .env, *.pem, *.key, credentials |

### Secret Sources (Priority Order)

| Source              | Use Case          | Security Level |
|---------------------|-------------------|----------------|
| Secret Manager      | Production        | ⭐⭐⭐⭐⭐          |
| Environment Vars    | Development/CI    | ⭐⭐⭐⭐           |
| .env (gitignored)   | Local development | ⭐⭐⭐            |
| Config files        | Non-sensitive     | ⭐⭐             |

---

## 4. Input Validation

| Principle               | Description                       |
|-------------------------|-----------------------------------|
| **Whitelist**           | Accept only known-good input      |
| **Validate Early**      | Check input at entry point        |
| **Validate Completely** | Check type, length, format, range |
| **Reject Invalid**      | Don't try to fix bad input        |

### Validation Types

| Type     | Check                            |
|----------|----------------------------------|
| Path     | No traversal, within base dir    |
| String   | Length, format, allowed chars    |
| Numeric  | Type, range, bounds              |
| Email    | Format, domain validation        |

---

## 5. Output Sanitization

| Context  | Action                    |
|----------|---------------------------|
| HTML     | Escape special characters |
| SQL      | Use parameterized queries |
| Shell    | Escape or avoid entirely  |
| JSON     | Proper encoding           |
| Logs     | Redact sensitive data     |

---

## 6. Dependency Security

| Practice              | Frequency     |
|-----------------------|---------------|
| Vulnerability scan    | Every build   |
| Dependency updates    | Weekly        |
| License review        | On addition   |
| Minimal dependencies  | Always        |

### Tools

| Tool        | Purpose              |
|-------------|----------------------|
| pip-audit   | Python vulnerabilities |
| npm audit   | Node.js vulnerabilities |
| Dependabot  | Automated updates    |
| Snyk        | Comprehensive scan   |

---

## 7. Logging Security

| Rule                  | Description                    |
|-----------------------|--------------------------------|
| No secrets in logs    | Redact passwords, tokens, keys |
| No PII in logs        | Mask user data                 |
| Structured logging    | Easy to parse and audit        |
| Secure log storage    | Access control, encryption     |

---

## 8. API Security

| Control             | Implementation              |
|---------------------|----------------------------|
| Authentication      | OAuth2, JWT, API keys      |
| Authorization       | RBAC, resource ownership   |
| Rate limiting       | Per-user, per-endpoint     |
| Input validation    | Schema validation          |
| HTTPS only          | TLS 1.2+                   |

---

## 9. File System Security

| Rule                 | Description                    |
|----------------------|--------------------------------|
| Path validation      | Prevent traversal attacks      |
| Minimal permissions  | Read-only where possible       |
| Temp file cleanup    | Remove after use               |
| Secure defaults      | Restrictive file permissions   |

---

## 10. Security Checklist

### Critical (P0)

- [ ] No hardcoded secrets
- [ ] Input validation on all entry points
- [ ] Parameterized queries (no SQL injection)
- [ ] HTTPS everywhere

### High (P1)

- [ ] Authentication on all protected endpoints
- [ ] Authorization checks (resource ownership)
- [ ] Path traversal prevention
- [ ] Dependency vulnerability scan

### Medium (P2)

- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Logging without sensitive data
- [ ] Error messages without stack traces

---

## Related

- `.knowledge/practices/engineering/security/SECURITY_PATTERNS.md` — Implementation patterns and code examples
- `.knowledge/frameworks/security/SECRETS_MANAGEMENT.md` — Secrets management framework
- `.knowledge/frameworks/security/SECURITY_CHECKLIST.md` — Comprehensive security checklist
- `.knowledge/frameworks/security/AUTHENTICATION.md` — Authentication patterns
- `.knowledge/frameworks/security/AUTHORIZATION.md` — Authorization patterns

---

*AI Collaboration Knowledge Base*
