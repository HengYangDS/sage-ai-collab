# Security Checklist

> Comprehensive security review checklist for development, deployment, and operations

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Development Checklist](#2-development-checklist)
- [3. Code Review Checklist](#3-code-review-checklist)
- [4. Deployment Checklist](#4-deployment-checklist)
- [5. Operations Checklist](#5-operations-checklist)
- [6. Incident Response](#6-incident-response)
- [7. Quick Reference](#7-quick-reference)

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

## 2. Development Checklist

### Input Validation

- [ ] 🔴 All user inputs validated server-side
- [ ] 🔴 Input length limits enforced
- [ ] 🔴 Input type validation (numbers, emails, dates)
- [ ] 🟠 Whitelist validation where possible
- [ ] 🟠 Reject unexpected fields in API requests
- [ ] 🟡 Custom error messages don't leak information

### SQL Injection Prevention

- [ ] 🔴 Parameterized queries used exclusively
- [ ] 🔴 No string concatenation in SQL
- [ ] 🟠 ORM used correctly
- [ ] 🟠 Stored procedures parameterized

### XSS Prevention

- [ ] 🔴 Output encoding for HTML context
- [ ] 🔴 Content-Security-Policy header set
- [ ] 🟠 Input sanitization for rich text
- [ ] 🟠 Template auto-escaping enabled
- [ ] 🟡 DOM manipulation uses safe APIs

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

## 3. Code Review Checklist

### Security Focus Areas

| Area                    | Check                              |
|-------------------------|------------------------------------|
| Authentication changes  | Password handling, session mgmt    |
| Authorization changes   | Access control, ownership check    |
| Data handling           | Input validation, output encoding  |
| Dependencies            | New deps reviewed, vulnerabilities |

### Review Items

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

---

## 4. Deployment Checklist

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

### Container Security

- [ ] 🔴 Base image from trusted source
- [ ] 🔴 No root user in container
- [ ] 🔴 Read-only file system where possible
- [ ] 🔴 No sensitive data in image
- [ ] 🟠 Image vulnerability scanned
- [ ] 🟠 Resource limits set
- [ ] 🟡 Security context defined

---

## 5. Operations Checklist

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

### Regular Tasks

| Task               | Frequency | Owner    |
|--------------------|-----------|----------|
| Dependency updates | Weekly    | Dev Team |
| Vulnerability scan | Weekly    | Security |
| Access review      | Monthly   | Security |
| Secret rotation    | Quarterly | Ops      |
| Penetration test   | Annually  | External |
| Security training  | Annually  | All      |

---

## 6. Incident Response

### Incident Classification

| Severity | Definition    | Response Time | Examples                             |
|----------|---------------|---------------|--------------------------------------|
| P1       | Active breach | Immediate     | Data exfiltration, system compromise |
| P2       | High risk     | 1 hour        | Credential leak, vulnerability       |
| P3       | Medium risk   | 4 hours       | Failed attacks, suspicious activity  |
| P4       | Low risk      | 24 hours      | Policy violation, misconfiguration   |

### Response Flow

```
Detect → Assess → Contain → Eradicate → Recover → Learn
```
### Immediate Actions by Type

| Incident Type        | Actions                                    |
|----------------------|--------------------------------------------|
| Credential Compromise | Revoke, reset, audit, notify              |
| Data Breach          | Scope, preserve, legal, disclose          |
| System Compromise    | Isolate, image, block, restore            |

---

## 7. Quick Reference

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

- `.knowledge/practices/engineering/SECURITY_PATTERNS.md` — Implementation patterns and code
- `.knowledge/frameworks/security/AUTHENTICATION.md` — Authentication patterns
- `.knowledge/frameworks/security/AUTHORIZATION.md` — Authorization patterns
- `.knowledge/frameworks/security/SECRETS_MANAGEMENT.md` — Secrets management

---

*AI Collaboration Knowledge Base*
