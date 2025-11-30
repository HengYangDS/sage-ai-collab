
# Version Migration Guide

> Version migration strategies and breaking change handling (~10 min read)

---

## Table of Contents

1. [Version Management](#1-version-management)
2. [Migration Strategies](#2-migration-strategies)
3. [Breaking Changes Log](#3-breaking-changes-log)
4. [Migration Procedures](#4-migration-procedures)
5. [Rollback Procedures](#5-rollback-procedures)
6. [Version Checking](#6-version-checking)
7. [Migration Checklist](#7-migration-checklist)
8. [Related](#8-related)

---

## 1. Version Management

### Schema Version Format

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, documentation updates
  │     └──────── New features, backward compatible
  └────────────── Breaking changes, migration required
```

### Current Version

| Component      | Version | Last Updated |
|:---------------|:--------|:-------------|
| **Schema**     | 1.0     | 2025-11-30   |
| **MCP Config** | 1.0     | 2025-11-30   |
| **Guidelines** | 1.0     | 2025-11-30   |

### Version Compatibility Matrix

| Schema Version | Junie Plugin | IDE Version | Status        |
|:---------------|:-------------|:------------|:--------------|
| 1.0            | 2025.1+      | 2024.3+     | ✅ Current     |
| 0.9 (Legacy)   | 2024.3+      | 2024.2+     | ⚠️ Deprecated |

---

## 2. Migration Strategies

### Strategy Selection

| Change Type       | Strategy         | Downtime | Risk   |
|:------------------|:-----------------|:---------|:-------|
| **Patch** (x.x.1) | In-place update  | None     | Low    |
| **Minor** (x.1.x) | Rolling update   | None     | Low    |
| **Major** (2.x.x) | Staged migration | Minimal  | Medium |

### Staged Migration Process

```
Phase 1: Preparation
    │
    ├── Backup current configuration
    ├── Review breaking changes
    └── Test in isolated environment
    │
    v
Phase 2: Migration
    │
    ├── Update schema version
    ├── Apply configuration changes
    └── Validate with schema
    │
    v
Phase 3: Verification
    │
    ├── Run configuration tests
    ├── Verify MCP server connections
    └── Test critical workflows
    │
    v
Phase 4: Completion
    │
    ├── Update documentation
    ├── Remove deprecated configs
    └── Archive old version
```

---

## 3. Breaking Changes Log

### Version 1.0 (Current)

**Initial stable release** — No breaking changes from previous versions.

**Key Features**:

- Thin Layer architecture (generic/project separation)
- MCP server configuration with metadata
- Session history management
- Timeout hierarchy (T1-T5)

### Future Version 2.0 (Planned)

**Anticipated Breaking Changes**:

| Change                   | Impact                 | Migration Action           |
|:-------------------------|:-----------------------|:---------------------------|
| MCP profile restructure  | MCP config             | Update profile definitions |
| Session history format   | History files          | Run migration script       |
| Autonomy level expansion | Collaboration settings | Map L1-L6 to new scale     |

---

## 4. Migration Procedures

### Patch Update (x.x.1)

**When**: Bug fixes, documentation updates

**Procedure**:

```bash
# 1. Pull latest configuration
git pull origin main

# 2. Verify no breaking changes
cat .junie/docs/operations/migration.md

# 3. Test configuration
pytest tests/tools/test_junie_config.py -v

# 4. Done - no restart needed for most patch updates
```

### Minor Update (x.1.x)

**When**: New features, backward compatible

**Procedure**:

```bash
# 1. Backup current config
cp -r .junie .junie.backup-$(date +%Y%m%d)

# 2. Pull latest configuration
git pull origin main

# 3. Review new features
# Check release notes or changelog

# 4. Update schema_version in config files
# Edit generic/config.yaml and project/config.yaml

# 5. Test configuration
pytest tests/tools/test_junie_config.py -v

# 6. Restart IDE to apply changes
```

### Major Update (x.0.0)

**When**: Breaking changes, new architecture

**Procedure**:

```bash
# 1. Full backup
cp -r .junie .junie.backup-major-$(date +%Y%m%d)

# 2. Review breaking changes
# Read migration guide for specific version

# 3. Create migration branch
git checkout -b migrate-to-v2

# 4. Apply configuration changes
# Follow version-specific migration steps

# 5. Update schema_version
# Edit all config files

# 6. Run migration scripts (if provided)
python tools/migrate_config.py --from 1.0 --to 2.0

# 7. Test thoroughly
pytest tests/tools/test_junie_config.py -v

# 8. Verify MCP servers
# Settings | Tools | Junie | MCP Servers

# 9. Test critical workflows manually

# 10. Merge migration branch
git checkout main
git merge migrate-to-v2
```

---

## 5. Rollback Procedures

### Quick Rollback

If issues detected immediately:

```bash
# 1. Stop MCP servers
# Settings | Tools | Junie | MCP Servers | Stop All

# 2. Restore from backup
rm -rf .junie
cp -r .junie.backup-YYYYMMDD .junie

# 3. Restart IDE

# 4. Verify configuration restored
```

### Partial Rollback

If only specific component affected:

```bash
# Rollback MCP config only
cp .junie/mcp/mcp.json.backup .junie/mcp/mcp.json

# Rollback YAML config only
cp .junie/generic/config.yaml.backup .junie/generic/config.yaml

# Restart IDE
```

### Emergency Rollback

If system is unstable:

```bash
# 1. Exit IDE completely

# 2. Restore entire configuration
rm -rf .junie
cp -r .junie.backup-YYYYMMDD .junie

# 3. Clear IDE caches (optional)
# Location varies by IDE and OS

# 4. Restart IDE

# 5. Verify all services working
```

---

## 6. Version Checking

### Check Current Version

```bash
# View schema version in config
grep "schema_version" .junie/generic/config.yaml
grep "schema_version" .junie/project/config.yaml
```

### Validate Version Consistency

```bash
# Run validation tests
pytest tests/tools/test_junie_config.py::TestYamlConfiguration::test_schema_versions_synchronized -v
```

### Compare with Latest

```bash
# Fetch latest without merging
git fetch origin main

# Compare versions
git diff origin/main -- .junie/generic/config.yaml | grep schema_version
```

---

## 7. Migration Checklist

### Pre-Migration

```markdown
- [ ] Backup current configuration
- [ ] Review breaking changes for target version
- [ ] Test migration in isolated environment
- [ ] Notify team of planned migration
- [ ] Schedule maintenance window (if needed)
```

### During Migration

```markdown
- [ ] Apply configuration changes
- [ ] Update schema_version
- [ ] Run migration scripts (if any)
- [ ] Validate JSON/YAML syntax
- [ ] Run configuration tests
```

### Post-Migration

```markdown
- [ ] Verify MCP servers connected
- [ ] Test Terminal rules working
- [ ] Verify critical workflows
- [ ] Update documentation
- [ ] Confirm all features work as expected
```

---

## 8. Related

- [Maintenance](maintenance.md) — Daily operations
- [Recovery](recovery.md) — Error recovery
- [Metrics](metrics.md) — Track migration impact

---

*AI Collaboration Knowledge Base*
