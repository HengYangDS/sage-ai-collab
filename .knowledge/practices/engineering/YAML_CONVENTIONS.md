# YAML Configuration Conventions

> Universal standards for writing YAML configuration files

---

## Table of Contents

- [1. File Structure](#1-file-structure)
- [2. Naming Conventions](#2-naming-conventions)
- [3. Comment Standards](#3-comment-standards)
- [4. Hierarchy Structure](#4-hierarchy-structure)
- [5. List Formats](#5-list-formats)
- [6. Multi-line Strings](#6-multi-line-strings)
- [7. Environment Variables](#7-environment-variables)
- [8. File Organization](#8-file-organization)
- [9. Quick Checklist](#9-quick-checklist)

---

## 1. File Structure

### Standard Header

```yaml
# [Component/Module] Configuration
#
# [Description of what this file configures]
# Version: x.y.z

# =============================================================================
# [Section Name]
# =============================================================================
```
### Section Format

| Element        | Format                | Purpose                      |
|----------------|-----------------------|------------------------------|
| Main section   | `# ===...===` + title | Major config block separator |
| Subsection     | `# ---` or blank line | Logical grouping             |
| Inline comment | `# comment`           | Explain config item          |

---

## 2. Naming Conventions

### Key Names

| Type     | Format               | Example                          |
|----------|----------------------|----------------------------------|
| General  | `snake_case`         | `max_connections`, `retry_count` |
| Boolean  | `is_*` / `*_enabled` | `is_active`, `cache_enabled`     |
| Duration | `*_ms` / `*_seconds` | `timeout_ms: 5000`               |
| Size     | `*_bytes` / `*_mb`   | `max_size_mb: 50`                |
| Count    | `max_*` / `min_*`    | `max_retries: 3`                 |

### Value Types

| Type           | Format           | Example            |
|----------------|------------------|--------------------|
| Number         | No quotes        | `port: 8080`       |
| Boolean        | No quotes        | `enabled: true`    |
| String         | Simple no quotes | `name: myapp`      |
| Special string | With quotes      | `pattern: "*.log"` |

---

## 3. Comment Standards

### Comment Types

| Type            | Position      | Purpose               |
|-----------------|---------------|-----------------------|
| File header     | Top of file   | Describe file purpose |
| Section comment | Above section | Identify config group |
| Inline comment  | After value   | Explain single config |

### Comment Alignment

```yaml
# Align inline comments to the same column
database:
  host: localhost              # Database server address
  port: 5432                   # Default PostgreSQL port
  max_connections: 100         # Connection pool size
  timeout_ms: 5000             # Query timeout
```
---

## 4. Hierarchy Structure

### Recommended Depth

| Depth    | Purpose                              |
|----------|--------------------------------------|
| Level 1  | Main config domain                   |
| Level 2  | Config grouping                      |
| Level 3  | Specific config                      |
| Level 4+ | **Avoid** — consider splitting files |

### Indentation Rules

- Use **2 spaces** (YAML standard)
- Never use tabs
- Maintain consistency

---

## 5. List Formats

### Simple Lists

```yaml
allowed_hosts:
  - localhost
  - 127.0.0.1
  - "*.example.com"
```
### Object Lists

```yaml
servers:
  - name: primary
    host: db1.example.com
    port: 5432
  - name: replica
    host: db2.example.com
    port: 5432
```
---

## 6. Multi-line Strings

### Literal Block (Preserve Newlines)

```yaml
script: |
  #!/bin/bash
  echo "Line 1"
  echo "Line 2"
```
### Folded Block (Collapse Newlines)

```yaml
description: >
  This is a long description
  that will be folded into
  a single line with spaces.
```
---

## 7. Environment Variables

### Placeholder Convention

```yaml
database:
  password: ${DB_PASSWORD}
  host: ${DB_HOST:-localhost}    # With default value
```
---

## 8. File Organization

### Modular Principles

| Principle             | Description                     |
|-----------------------|---------------------------------|
| Single responsibility | Each file configures one domain |
| Reasonable size       | 50-150 lines recommended        |
| Consistent naming     | `[domain].yaml` format          |

---

## 9. Quick Checklist

| ✓ Do                   | ✗ Don't                  |
|------------------------|--------------------------|
| 2-space indent         | Tab or 4-space           |
| snake_case keys        | camelCase                |
| Numbers without quotes | `port: "8080"`           |
| Align inline comments  | Random comment placement |
| Include units          | No unit indication       |
| Keep nesting ≤3 levels | Deep nesting             |

---

## Related

- `.knowledge/practices/documentation/DOCUMENTATION_STANDARDS.md` — Documentation standards
- `.knowledge/guidelines/CODE_STYLE.md` — Code style guidelines

---

*AI Collaboration Knowledge Base*
