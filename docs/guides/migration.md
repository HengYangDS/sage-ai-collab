# Migration Guide

> Version upgrade procedures, configuration migration, and compatibility notes

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Pre-Migration Checklist](#2-pre-migration-checklist)
- [3. Version Upgrade](#3-version-upgrade)
- [4. Configuration Migration](#4-configuration-migration)
- [5. Content Migration](#5-content-migration)
- [6. Breaking Changes](#6-breaking-changes)
- [7. Rollback Procedures](#7-rollback-procedures)
- [8. Troubleshooting](#8-troubleshooting)

---

## 1. Overview

### 1.1 Migration Philosophy

| Principle                  | Description                         |
|----------------------------|-------------------------------------|
| **Backward Compatibility** | Support N-1 versions where possible |
| **Safe by Default**        | Dry-run before actual changes       |
| **Reversible**             | Always create backups               |
| **Incremental**            | Step-by-step migration              |

### 1.2 Version Numbering

SAGE follows semantic versioning: `MAJOR.MINOR.PATCH`

| Change Type      | Version Bump | Example       |
|------------------|--------------|---------------|
| Breaking changes | MAJOR        | 1.0.0 → 2.0.0 |
| New features     | MINOR        | 1.0.0 → 1.1.0 |
| Bug fixes        | PATCH        | 1.0.0 → 1.0.1 |

---

## 2. Pre-Migration Checklist

### 2.1 Before You Start

| Step                     | Command              | Description              |
|--------------------------|----------------------|--------------------------|
| 1. Check current version | `sage --version`     | Know your starting point |
| 2. Review changelog      | See `CHANGELOG.md`   | Understand changes       |
| 3. Backup                | `sage backup create` | Create restore point     |
| 4. Test environment      | Clone and test       | Verify in non-production |

### 2.2 Backup Procedure

```bash
# Create full backup
sage backup create --name "pre-migration-$(date +%Y%m%d)"

# Verify backup
sage backup verify --latest

# List backups
sage backup list
```

**Manual backup** (alternative):

```bash
# Create timestamped backup directory
BACKUP_DIR=".backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup critical directories
cp -r config/ "$BACKUP_DIR/"
cp -r .knowledge/ "$BACKUP_DIR/"
cp -r .context/ "$BACKUP_DIR/"
cp pyproject.toml "$BACKUP_DIR/"
```

### 2.3 Compatibility Check

```bash
# Check Python version
python --version  # Requires 3.12+

# Check dependencies
pip check

# Validate current configuration
sage config validate
```

---

## 3. Version Upgrade

### 3.1 Standard Upgrade

```bash
# Update from PyPI
pip install --upgrade sage-kb

# Or update from source
git pull origin main
pip install -e .
```

### 3.2 Specific Version

```bash
# Install specific version
pip install sage-kb==1.2.0

# Install from specific commit
pip install git+https://github.com/HengYangDS/sage-kb@v1.2.0
```

### 3.3 Post-Upgrade Steps

```bash
# 1. Run migrations (if any)
sage migrate

# 2. Validate configuration
sage config validate

# 3. Check integrity
sage check --all

# 4. Verify functionality
sage info
```

---

## 4. Configuration Migration

### 4.1 Automatic Migration

```bash
# Run config migration
sage config migrate

# With dry-run
sage config migrate --dry-run

# Migrate specific version
sage config migrate --from 0.1.0 --to 0.2.0
```

### 4.2 Manual Configuration Changes

#### 4.2.1 Config Structure Changes

**v0.1.x → v0.2.x**: Modular config introduced

```yaml
# OLD: config/sage.yaml (monolithic)
timeout:
  default: 5000
  cache: 100
knowledge:
  layers: [ core, guidelines ]

# NEW: config/ (modular)
# config/core/timeout.yaml
default: 5000
cache: 100

# config/knowledge/loading.yaml
layers: [ core, guidelines ]
```

**Migration script**:

```python
import yaml
from pathlib import Path


def migrate_config_0_1_to_0_2():
    old_config = Path("config/sage.yaml")
    if not old_config.exists():
        return

    with open(old_config) as f:
        config = yaml.safe_load(f)

    # Split into modular configs
    if "timeout" in config:
        Path("config/core").mkdir(exist_ok=True)
        with open("config/core/timeout.yaml", "w") as f:
            yaml.dump(config["timeout"], f)

    if "knowledge" in config:
        Path("config/knowledge").mkdir(exist_ok=True)
        with open("config/knowledge/loading.yaml", "w") as f:
            yaml.dump(config["knowledge"], f)
```

#### 4.2.2 Environment Variable Changes

| Old Variable   | New Variable           | Notes                |
|----------------|------------------------|----------------------|
| `SAGE_TIMEOUT` | `SAGE_TIMEOUT_DEFAULT` | More specific naming |
| `SAGE_DEBUG`   | `SAGE_LOG_LEVEL=DEBUG` | Use log levels       |
| `SAGE_KB_PATH` | `SAGE_CONTENT_PATH`    | Clearer naming       |

### 4.3 Config Validation

```bash
# Validate after migration
sage config validate --verbose

# Check specific config file
sage config validate --file config/core/timeout.yaml
```

---

## 5. Content Migration

### 5.1 Content Structure Changes

#### Directory Structure Migration

```bash
# If directory structure changed
sage migrate content --dry-run

# Apply migration
sage migrate content
```

**Example: Moving guidelines**:

```bash
# v0.1.x location
.knowledge/guidelines/

# v0.2.x location (if changed)
.knowledge/guidelines/  # Usually unchanged

# Migration (if needed)
mv .knowledge/old_location/ .knowledge/new_location/
sage rebuild --indices
```

### 5.2 Frontmatter Changes

**v0.1.x format**:

```yaml
---
title: Document Title
tags: [ tag1, tag2 ]
---
```

**v0.2.x format** (if changed):

```yaml
---
title: Document Title
metadata:
  tags: [ tag1, tag2 ]
  layer: core
---
```

**Migration script**:

```python
import yaml
import re
from pathlib import Path


def migrate_frontmatter(file_path: Path):
    content = file_path.read_text()

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return

    fm = yaml.safe_load(match.group(1))
    body = match.group(2)

    # Transform frontmatter
    if "tags" in fm and "metadata" not in fm:
        fm["metadata"] = {"tags": fm.pop("tags")}

    # Write back
    new_content = f"---\n{yaml.dump(fm)}---\n{body}"
    file_path.write_text(new_content)
```

### 5.3 Link Updates

```bash
# Check for broken links after migration
sage check --links

# Auto-fix common patterns
sage fix --links --dry-run
sage fix --links
```

---

## 6. Breaking Changes

### 6.1 Version-Specific Changes

#### v0.2.0 Breaking Changes

| Change       | Migration Action          |
|--------------|---------------------------|
| Config split | Run `sage config migrate` |
| API changes  | Update tool calls         |
| CLI changes  | Update scripts            |

#### API Changes

```python
# OLD (v0.1.x)
from sage.core import load_knowledge

result = load_knowledge(layer=0)

# NEW (v0.2.x)
from sage.core.loader import KnowledgeLoader

loader = KnowledgeLoader()
result = loader.load_layer(0)
```

#### CLI Changes

```bash
# OLD (v0.1.x)
sage get --layer core

# NEW (v0.2.x)
sage get --layer 0  # or: sage get --layer core
```

### 6.2 Deprecation Warnings

```python
# Check for deprecation warnings
import warnings

warnings.filterwarnings("default", category=DeprecationWarning)

# Run with warnings visible
python - W
default - c
"import sage"
```

---

## 7. Rollback Procedures

### 7.1 Quick Rollback

```bash
# Restore from backup
sage backup restore --name "pre-migration-20250129"

# Or restore latest
sage backup restore --latest
```

### 7.2 Manual Rollback

```bash
# 1. Downgrade package
pip install sage-kb==0.1.0

# 2. Restore config
cp -r .backups/20250129_120000/config/ ./config/

# 3. Restore content (if needed)
cp -r .backups/20250129_120000/.knowledge/ ./.knowledge/

# 4. Validate
sage check --all
```

### 7.3 Partial Rollback

```bash
# Rollback only config
sage backup restore --latest --only config

# Rollback only content
sage backup restore --latest --only content
```

---

## 8. Troubleshooting

### 8.1 Common Migration Issues

| Issue                   | Cause            | Solution                  |
|-------------------------|------------------|---------------------------|
| Config validation fails | Schema changed   | Run `sage config migrate` |
| Import errors           | API changed      | Update import paths       |
| Missing files           | Path changed     | Check migration notes     |
| Tests failing           | Breaking changes | Update test code          |

### 8.2 Debug Migration

```bash
# Verbose migration output
sage migrate --verbose --dry-run

# Check migration logs
cat .logs/migration.log
```

### 8.3 Recovery Steps

**If migration fails mid-way**:

1. Don't panic - you have backups
2. Check migration logs for error point
3. Restore from backup: `sage backup restore --latest`
4. Fix the issue
5. Retry migration

**If no backup exists**:

```bash
# Try to recover from git
git stash  # Save current changes
git checkout HEAD~1 -- config/  # Restore previous config

# Or reset to last known good state
git log --oneline  # Find good commit
git checkout <commit> -- config/ .knowledge/
```

---

## Migration Checklist

### Pre-Migration

- [ ] Read changelog for target version
- [ ] Check Python version compatibility
- [ ] Create backup
- [ ] Test in staging environment

### During Migration

- [ ] Run version upgrade
- [ ] Run config migration
- [ ] Run content migration (if needed)
- [ ] Update environment variables

### Post-Migration

- [ ] Validate configuration
- [ ] Check all links
- [ ] Run test suite
- [ ] Verify key functionality
- [ ] Update documentation
- [ ] Remove deprecated code/config

---

## Version History

| Version | Release Date | Migration Notes                      |
|---------|--------------|--------------------------------------|
| 0.1.0   | 2025-11-15   | Initial release                      |
| 0.2.0   | TBD          | Modular config, see breaking changes |

---

## Related

- `CHANGELOG.md` — Detailed version changes
- `.knowledge/practices/engineering/troubleshooting.md` — Troubleshooting guide
- `docs/guides/configuration.md` — Configuration guide
- `.context/decisions/ADR-0007-configuration.md` — Config architecture

---

*Part of SAGE Knowledge Base — 信达雅 (Xin-Da-Ya)*
