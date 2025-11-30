---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~700
---

# Migration Guide

> Version upgrade procedures and compatibility notes

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Pre-Migration Checklist](#2-pre-migration-checklist)
- [3. Version Upgrade](#3-version-upgrade)
- [4. Configuration Migration](#4-configuration-migration)
- [5. Content Migration](#5-content-migration)
- [6. Breaking Changes](#6-breaking-changes)
- [7. Rollback Procedures](#7-rollback-procedures)

---

## 1. Overview

### 1.1 Migration Principles

| Principle | Description |
|-----------|-------------|
| Backward Compatibility | Support N-1 versions |
| Safe by Default | Dry-run before changes |
| Reversible | Always create backups |
| Incremental | Step-by-step migration |

### 1.2 Version Numbering

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking | MAJOR | 1.0.0 → 2.0.0 |
| Features | MINOR | 1.0.0 → 1.1.0 |
| Fixes | PATCH | 1.0.0 → 1.0.1 |

---

## 2. Pre-Migration Checklist

### 2.1 Before You Start

| Step | Command | Purpose |
|------|---------|---------|
| Check version | `sage --version` | Know starting point |
| Review changelog | See `CHANGELOG.md` | Understand changes |
| Create backup | `sage backup create` | Restore point |
| Test first | Clone and test | Verify in non-prod |

### 2.2 Backup Commands

```bash
sage backup create --name "pre-migration"  # Create backup
sage backup verify --latest                 # Verify backup
sage backup list                            # List backups
```

### 2.3 Compatibility Check

```bash
python --version      # Requires 3.12+
pip check             # Check dependencies
sage config validate  # Validate config
```

---

## 3. Version Upgrade

### 3.1 Standard Upgrade

```bash
pip install --upgrade sage-kb           # From PyPI
pip install -e ".[all]"                 # From source
sage --version                          # Verify
```

### 3.2 Major Version Upgrade

```bash
sage migrate --from 1.x --to 2.x --dry-run  # Preview
sage migrate --from 1.x --to 2.x            # Execute
sage migrate verify                          # Verify
```

### 3.3 Upgrade Path

| From | To | Notes |
|------|----|-------|
| 0.x | 1.0 | Config format change |
| 1.x | 2.0 | API breaking changes |

---

## 4. Configuration Migration

### 4.1 Auto-Migration

```bash
sage config migrate --dry-run  # Preview changes
sage config migrate            # Apply changes
```

### 4.2 Manual Migration

| Old Format | New Format |
|------------|------------|
| `timeout_ms: 5000` | `timeout.default_ms: 5000` |
| `cache: true` | `cache.enabled: true` |
| `content_path: ./` | `knowledge.content_root: ./` |

### 4.3 Configuration Mapping

```yaml
# Old (v0.x)
timeout_ms: 5000
cache: true

# New (v1.x)
timeout:
  default_ms: 5000
cache:
  enabled: true
```

---

## 5. Content Migration

### 5.1 Directory Changes

| Old Path | New Path |
|----------|----------|
| `content/` | `.knowledge/` |
| `content/core/` | `.knowledge/core/` |
| `GUIDELINES.md` | `.knowledge/guidelines/` |

### 5.2 Migration Commands

```bash
sage content migrate --dry-run  # Preview
sage content migrate            # Execute
sage content verify             # Verify
```

### 5.3 Frontmatter Update

```yaml
# Old format
---
title: Document
---

# New format
---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~500
---
```

---

## 6. Breaking Changes

### 6.1 v1.0 → v2.0

| Change | Migration |
|--------|-----------|
| Config format | Run `sage config migrate` |
| API changes | Update import paths |
| CLI syntax | See `sage --help` |

### 6.2 Deprecated Features

| Feature | Deprecated | Removed | Alternative |
|---------|------------|---------|-------------|
| `--legacy` flag | v1.5 | v2.0 | Use standard commands |
| Old config format | v1.0 | v2.0 | Use new YAML format |

### 6.3 API Changes

| Old | New |
|-----|-----|
| `from sage import load` | `from sage.core.loader import load` |
| `sage.get()` | `sage.core.loader.get()` |

---

## 7. Rollback Procedures

### 7.1 Quick Rollback

```bash
sage backup restore --latest    # Restore latest
pip install sage-kb==1.0.0      # Downgrade version
```

### 7.2 Manual Rollback

```bash
# Restore from backup
cp -r .backups/YYYYMMDD/config/ ./config/
cp -r .backups/YYYYMMDD/.knowledge/ ./.knowledge/

# Downgrade package
pip install sage-kb==<previous-version>
```

### 7.3 Rollback Checklist

| Step | Action |
|------|--------|
| 1 | Stop services: `sage serve --stop` |
| 2 | Restore backup |
| 3 | Downgrade package |
| 4 | Verify: `sage config validate` |
| 5 | Restart services |

---

## Migration Checklist

| Phase | Task | Status |
|-------|------|--------|
| **Prepare** | Backup created | ☐ |
| | Changelog reviewed | ☐ |
| | Test env ready | ☐ |
| **Execute** | Config migrated | ☐ |
| | Content migrated | ☐ |
| | Version upgraded | ☐ |
| **Verify** | Tests passing | ☐ |
| | Services running | ☐ |
| | Rollback tested | ☐ |

---

## Related

- `docs/guides/TROUBLESHOOTING.md` — Troubleshooting guide
- `docs/guides/CONFIGURATION.md` — Configuration reference
- `CHANGELOG.md` — Version history

---

*Part of SAGE Knowledge Base*
