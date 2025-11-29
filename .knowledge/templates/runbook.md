# Operational Runbook Template

> **Purpose**: Document operational procedures for system maintenance and incident response
> **Use When**: Creating standard operating procedures, on-call guides, or maintenance documentation

---

## Template

```markdown
# [System/Service Name] Runbook

> **Owner**: [Team/Person]
> **Last Updated**: [YYYY-MM-DD]
> **On-Call**: [Rotation/Contact info]

---

## Overview

**Service**: [Service name and brief description]

**Dependencies**:
- [Dependency 1]
- [Dependency 2]

**SLA**: [Availability target, e.g., 99.9%]

---

## Quick Reference

| Item | Value |
|------|-------|
| Dashboard | [Link to monitoring dashboard] |
| Logs | [Link to log aggregation] |
| Alerts | [Link to alert configuration] |
| Repository | [Link to code repository] |
| Documentation | [Link to detailed docs] |

---

## Health Checks

### Service Status

```bash
# Check service health
curl -s https://service.example.com/health | jq

# Expected response
{"status": "healthy", "version": "x.y.z"}
```

### Key Metrics

| Metric              | Normal Range | Alert Threshold |
|---------------------|--------------|-----------------|
| Response time (p99) | < 200ms      | > 500ms         |
| Error rate          | < 0.1%       | > 1%            |
| CPU usage           | < 70%        | > 85%           |
| Memory usage        | < 80%        | > 90%           |

---

## Common Operations

### [Operation 1: e.g., Restart Service]

**When to use**: [Trigger condition]

**Impact**: [User impact during operation]

**Steps**:

1. [Step 1]
   ```bash
   [command]
   ```

2. [Step 2]
   ```bash
   [command]
   ```

3. **Verify**:
   ```bash
   [verification command]
   ```

**Rollback**: [How to undo if needed]

---

### [Operation 2: e.g., Scale Up]

**When to use**: [Trigger condition]

**Impact**: [User impact during operation]

**Steps**:

1. [Step 1]
2. [Step 2]
3. **Verify**: [Verification steps]

**Rollback**: [How to undo if needed]

---

## Incident Response

### Severity Levels

| Level | Description       | Response Time     | Examples         |
|-------|-------------------|-------------------|------------------|
| SEV1  | Critical outage   | Immediate         | Service down     |
| SEV2  | Major degradation | 15 min            | High error rate  |
| SEV3  | Minor issue       | 1 hour            | Slow performance |
| SEV4  | Low impact        | Next business day | Cosmetic issues  |

### Escalation Path

| Level | Contact             | Method        |
|-------|---------------------|---------------|
| L1    | On-call engineer    | PagerDuty     |
| L2    | Team lead           | Slack + Phone |
| L3    | Engineering manager | Phone         |
| L4    | VP Engineering      | Phone         |

---

## Troubleshooting

### [Issue 1: e.g., High Latency]

**Symptoms**:

- [Symptom 1]
- [Symptom 2]

**Diagnosis**:

```bash
# Check current latency
[diagnostic command]

# Check for bottlenecks
[diagnostic command]
```

**Resolution**:

1. [Step 1]
2. [Step 2]

**Root Causes**:

- [Common cause 1]
- [Common cause 2]

---

### [Issue 2: e.g., Out of Memory]

**Symptoms**:

- [Symptom 1]
- [Symptom 2]

**Diagnosis**:

```bash
[diagnostic command]
```

**Resolution**:

1. [Step 1]
2. [Step 2]

---

## Maintenance Procedures

### Scheduled Maintenance

| Task     | Frequency | Duration | Impact   |
|----------|-----------|----------|----------|
| [Task 1] | Weekly    | 5 min    | None     |
| [Task 2] | Monthly   | 30 min   | Degraded |
| [Task 3] | Quarterly | 2 hours  | Outage   |

### Pre-Maintenance Checklist

- [ ] Notify stakeholders
- [ ] Schedule maintenance window
- [ ] Prepare rollback plan
- [ ] Verify backup status
- [ ] Test in staging

### Post-Maintenance Checklist

- [ ] Verify service health
- [ ] Check all metrics
- [ ] Update documentation
- [ ] Send completion notice

---

## Contacts

| Role              | Name      | Contact   |
|-------------------|-----------|-----------|
| Primary On-Call   | [Name]    | [Contact] |
| Secondary On-Call | [Name]    | [Contact] |
| Team Lead         | [Name]    | [Contact] |
| External Vendor   | [Company] | [Contact] |

---

## Changelog

| Date       | Author | Changes         |
|------------|--------|-----------------|
| YYYY-MM-DD | [Name] | Initial version |

---

*Runbook from SAGE Knowledge Base*

```

---

## Instructions

### 1. Runbook Structure

| Section | Purpose |
|---------|---------|
| Overview | Service context and dependencies |
| Quick Reference | Fast access to key links |
| Health Checks | How to verify service status |
| Common Operations | Standard procedures |
| Incident Response | Emergency procedures |
| Troubleshooting | Problem diagnosis guides |
| Maintenance | Scheduled tasks |
| Contacts | Escalation information |

### 2. Best Practices

| Practice | Description |
|----------|-------------|
| Keep it current | Update after every incident |
| Test procedures | Verify commands work |
| Include verification | Always confirm success |
| Document rollbacks | Every change needs undo steps |
| Use copy-paste commands | Reduce typing errors |

### 3. Command Documentation

Always include:
- Exact command to run
- Expected output
- Error handling
- Verification step

### 4. Review Schedule

| Frequency | Action |
|-----------|--------|
| After incident | Update relevant sections |
| Monthly | Review accuracy |
| Quarterly | Full audit |

---

## Related

- `templates/postmortem.md` — Incident postmortem template
- `practices/engineering/error_handling.md` — Error handling patterns
- `practices/engineering/logging.md` — Logging practices

---

*Template from SAGE Knowledge Base*
