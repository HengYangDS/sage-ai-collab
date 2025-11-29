# Configuration Migration Guide

> Version migration strategies and breaking change handling (~10 min read)

---

## Table of Contents

- [1. Version Management](#1-version-management)
- [2. Migration Strategies](#2-migration-strategies)
- [3. Breaking Changes Log](#3-breaking-changes-log)
- [4. Migration Procedures](#4-migration-procedures)
- [5. Rollback Procedures](#5-rollback-procedures)

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
| **Schema**     | 1.0     | 2025-01-15   |
| **MCP Config** | 1.0     | 2025-01-15   |
| **Guidelines** | 1.0     | 2025-01-15   |

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

**Initial stable release** - No breaking changes from previous versions.

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

### 4.1 Pre-Migration Checklist

```markdown
☐ Backup `.junie/` directory
☐ Document current schema_version
☐ Review target version breaking changes
☐ Verify IDE and plugin compatibility
☐ Test migration in development environment
```

### 4.2 Backup Procedure

```bash
# Create timestamped backup
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item -Recurse .junie ".junie.backup-$timestamp"

# Verify backup
Get-ChildItem ".junie.backup-$timestamp" -Recurse | Measure-Object
```

### 4.3 Configuration Update

**Step 1: Update schema_version**

```yaml
# In generic/config.yaml and project/config.yaml
schema_version: "2.0"  # Update to target version
```

**Step 2: Apply Required Changes**

Refer to the Breaking Changes Log for specific changes needed.

**Step 3: Validate Configuration**

```bash
# Validate MCP configuration
python -c "import json; json.load(open('.junie/mcp/mcp.json'))"

# Validate YAML configuration
python -c "import yaml; yaml.safe_load(open('.junie/generic/config.yaml'))"
python -c "import yaml; yaml.safe_load(open('.junie/project/config.yaml'))"
```

### 4.4 Post-Migration Verification

```markdown
☐ IDE restarts without errors
☐ MCP servers connect successfully
☐ Session history functions correctly
☐ All configured tools are accessible
☐ No deprecation warnings in logs
```

---

## 5. Rollback Procedures

### Quick Rollback

```bash
# Restore from backup
$latestBackup = Get-ChildItem ".junie.backup-*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Remove-Item -Recurse .junie
Move-Item $latestBackup.FullName .junie

# Restart IDE
```

### Selective Rollback

If only specific files need rollback:

```bash
# Rollback specific file
Copy-Item ".junie.backup-TIMESTAMP/mcp/mcp.json" ".junie/mcp/mcp.json"
```

### Rollback Verification

```markdown
☐ Verify schema_version matches backup
☐ Test MCP server connections
☐ Confirm all features work as expected
```

---

## Related

- `README.md` — Configuration guide index
- `generic/config.yaml` — Generic settings with schema_version
- `project/config.yaml` — Project settings with schema_version
- `generic/config.schema.json` — Configuration validation schema
- `mcp/mcp.schema.json` — MCP configuration validation schema

---

*Part of the Junie Configuration Guide*
