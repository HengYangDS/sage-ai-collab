# Troubleshooting Guide Template

> **Purpose**: Template for creating troubleshooting documentation
> **Use When**: Documenting solutions to common problems or error scenarios

---

## Table of Contents

- [Overview](#overview)
- [Quick Diagnostics](#quick-diagnostics)
- [Issue: [Issue Title 1]](#issue-issue-title-1)
- [Issue: [Issue Title 2]](#issue-issue-title-2)
- [Error Reference](#error-reference)
- [Escalation](#escalation)
- [Instructions](#instructions)
- [Quick Diagnostics](#quick-diagnostics)
- [Issue: Server Not Starting](#issue-server-not-starting)
- [Best Practices](#best-practices)

## Overview

This template helps create structured troubleshooting guides for components, features, or error scenarios.

---

## Template

```markdown
# Troubleshooting: [Component/Feature Name]

> Quick solutions for common [component] issues

---

## Quick Diagnostics

### Health Check

[Commands or steps to verify component health]

```bash
# Example diagnostic commands
[command 1]
[command 2]
```
### Common Symptoms

| Symptom     | Likely Cause | Solution Section  |
|-------------|--------------|-------------------|
| [Symptom 1] | [Cause]      | [Link to section] |
| [Symptom 2] | [Cause]      | [Link to section] |
| [Symptom 3] | [Cause]      | [Link to section] |

---

## Issue: [Issue Title 1]

### Symptom

[Clear description of what the user observes]

### Possible Causes

1. [Cause 1]
2. [Cause 2]
3. [Cause 3]

### Diagnosis

```bash
# Commands to diagnose the issue
[diagnostic command]
```text
[How to interpret the output]

### Solution

**Option 1: [Solution Name]**

```bash
# Steps to fix
[fix command]
```
**Option 2: [Alternative Solution]**

[Alternative steps if Option 1 doesn't work]

### Prevention

[How to prevent this issue in the future]

---

## Issue: [Issue Title 2]

### Symptom

[Description]

### Possible Causes

1. [Cause 1]
2. [Cause 2]

### Diagnosis

[Diagnostic steps]

### Solution

[Solution steps]

---

## Error Reference

| Error Code/Message | Meaning         | Solution    |
|--------------------|-----------------|-------------|
| `[ERROR_001]`      | [What it means] | [Quick fix] |
| `[ERROR_002]`      | [What it means] | [Quick fix] |
| `[ERROR_003]`      | [What it means] | [Quick fix] |

---

## Escalation

### When to Escalate

- [Condition 1]
- [Condition 2]
- [Condition 3]

### Information to Collect

Before escalating, gather:

1. [ ] Error messages and logs
2. [ ] Steps to reproduce
3. [ ] Environment details
4. [ ] Configuration files

### Contact

- **Team**: [Team name]
- **Channel**: [Slack/Email/etc.]
- **Response Time**: [Expected SLA]

---

## Related

- [Link to related doc 1]
- [Link to related doc 2]
- [Link to configuration doc]

---

*Last Updated: [DATE]*

```
---

## Instructions

### 1. Header Section

- Use clear, descriptive title
- Include component or feature name
- Add brief description of scope

### 2. Quick Diagnostics

- Provide immediate health check commands
- Create symptom-to-solution mapping table
- Help users quickly identify their issue

### 3. Issue Sections

For each issue, include:

- **Symptom**: What the user sees (error messages, behaviors)
- **Possible Causes**: List from most to least common
- **Diagnosis**: How to confirm the cause
- **Solution**: Step-by-step fix instructions
- **Prevention**: How to avoid in future

### 4. Error Reference

- Create table of common errors
- Include error codes if applicable
- Provide quick solutions

### 5. Escalation Path

- Define when to escalate
- List required information
- Provide contact details

---

## Example

```markdown
# Troubleshooting: MCP Server

> Quick solutions for common MCP server issues

---

## Quick Diagnostics

### Health Check

```bash
app serve --status
curl http://localhost:8080/health
```
### Common Symptoms

| Symptom            | Likely Cause        | Solution Section       |
|--------------------|---------------------|------------------------|
| Connection refused | Server not running  | #server-not-starting   |
| Timeout errors     | Performance issue   | #slow-responses        |
| Auth failures      | Invalid credentials | #authentication-issues |

---

## Issue: Server Not Starting

### Symptom

Running `app serve` fails with "Address already in use" error.

### Possible Causes

1. Another process using the port
2. Previous server instance not stopped
3. Firewall blocking the port

### Diagnosis

```bash
# Check what's using the port
netstat -an | grep 8080
lsof -i :8080
```
### Solution

**Option 1: Kill existing process**

```bash
kill $(lsof -t -i:8080)
app serve
```
**Option 2: Use different port**

```bash
app serve --port 8081
```
### Prevention

- Always stop server properly with Ctrl+C
- Use unique ports per environment

```
---

## Best Practices

1. **Be specific**: Use exact error messages
2. **Test solutions**: Verify fixes work before documenting
3. **Keep updated**: Review and update regularly
4. **Link related docs**: Connect to relevant documentation
5. **Use consistent format**: Follow template structure

---

## Related

- `docs/guides/TROUBLESHOOTING.md` — Main troubleshooting guide
- `.knowledge/templates/RUNBOOK.md` — Operational runbook template
- `.knowledge/templates/POSTMORTEM.md` — Incident postmortem template

---

*Template from AI Collaboration Knowledge Base*
---

*AI Collaboration Knowledge Base*
