
# Error Recovery Guide

> Recovery procedures for common issues (~10 min read)

---

## Table of Contents

1. [Quick Reference](#1-quick-reference)
2. [MCP Recovery](#2-mcp-recovery)
3. [Configuration Recovery](#3-configuration-recovery)
4. [IDE Recovery](#4-ide-recovery)
5. [Full Reset Procedure](#5-full-reset-procedure)
6. [Prevention Strategies](#6-prevention-strategies)
7. [Recovery Checklist](#7-recovery-checklist)
8. [Related](#8-related)

---

## 1. Quick Reference

### Recovery Decision Tree

```
Issue Detected
    │
    ├── MCP Server Issue?
    │   └── See: MCP Recovery
    │
    ├── Configuration Issue?
    │   └── See: Configuration Recovery
    │
    ├── IDE/Plugin Issue?
    │   └── See: IDE Recovery
    │
    └── Unknown Issue?
        └── See: Full Reset Procedure
```

### Emergency Contacts

| Issue Type       | First Action               | Escalation                     |
|:-----------------|:---------------------------|:-------------------------------|
| MCP Server Down  | Restart server             | Check logs, reinstall          |
| Config Corrupted | Restore from backup        | Rebuild from template          |
| IDE Unresponsive | Force quit, restart        | Clear caches, reinstall plugin |
| Data Loss        | Check .history/ and Memory | Restore from backups           |

---

## 2. MCP Recovery

### Server Won't Start

**Symptoms**: Server status shows "Disconnected" or "Error"

**Quick Fix**:

```text
1. Settings | Tools | Junie | MCP Servers
2. Select affected server
3. Click "Restart"
4. Wait 10 seconds
5. If still failing, proceed to diagnosis
```

**Diagnosis**:

```bash
# Check Node.js
node --version

# Test server manually
npx -y @modelcontextprotocol/server-filesystem .

# Check for errors in output
```

**Full Recovery**:

```bash
# 1. Stop all servers in IDE

# 2. Clear npm cache
npm cache clean --force

# 3. Remove npx cache
rm -rf ~/.npm/_npx           # Unix
Remove-Item -Recurse "$env:LOCALAPPDATA\npm-cache\_npx"  # Windows

# 4. Restart IDE

# 5. Reload MCP configuration
# Settings | Tools | Junie | MCP Servers | Reload

# 6. Start servers one by one
```

### Server Crashes Repeatedly

**Symptoms**: Server starts then crashes within seconds

**Diagnosis**:

1. Check IDE logs: `Help | Show Log in Explorer`
2. Look for MCP-related errors
3. Note error messages

**Common Causes & Fixes**:

| Cause                | Fix                                    |
|:---------------------|:---------------------------------------|
| Invalid JSON config  | Validate and fix mcp.json              |
| Missing dependencies | Reinstall server package               |
| Permission denied    | Check file/directory permissions       |
| Port conflict        | Restart IDE or system                  |
| Memory exhaustion    | Close other applications, increase RAM |

### Memory Server Data Loss

**Symptoms**: Stored knowledge not retrievable

**Recovery Options**:

1. **Check server status** — May just need restart
2. **Search with different terms** — Data may exist under different names
3. **Restore from .history/** — Fallback documentation
4. **Rebuild from scratch** — Re-enter critical knowledge

**Prevention**:

- Regularly export important decisions to `.history/`
- Use meaningful entity names
- Create relationships for better retrieval

---

## 3. Configuration Recovery

### Corrupted JSON/YAML

**Symptoms**: Parse errors, IDE won't load config

**Quick Fix**:

```bash
# Restore from backup
cp .junie/mcp/mcp.json.backup .junie/mcp/mcp.json

# Or restore entire config
cp -r .junie.backup-YYYYMMDD .junie
```

**No Backup Available**:

```bash
# 1. Validate current file
python -m json.tool .junie/mcp/mcp.json

# 2. Fix syntax errors based on output

# 3. Or start fresh from template
# Copy from another project or documentation
```

### Missing Configuration Files

**Symptoms**: Files deleted or moved

**Recovery**:

```bash
# Check if files exist
ls -la .junie/

# Restore from git
git checkout -- .junie/

# Or restore from backup
cp -r .junie.backup-YYYYMMDD/* .junie/
```

### Schema Version Mismatch

**Symptoms**: Validation errors about schema version

**Fix**:

```bash
# Check current versions
grep "schema_version" .junie/generic/config.yaml
grep "schema_version" .junie/project/config.yaml

# Update to match (edit files manually)
# Both should have same version, e.g., "1.0"
```

---

## 4. IDE Recovery

### Junie Plugin Not Responding

**Symptoms**: Junie chat unresponsive, commands not executing

**Quick Fix**:

```text
1. View | Tool Windows | Junie
2. Click refresh/reload if available
3. If no response, restart IDE
```

**Full Recovery**:

```text
1. File | Invalidate Caches / Restart
2. Select "Invalidate and Restart"
3. Wait for IDE to rebuild caches
4. Verify Junie plugin is enabled
```

### Plugin Conflicts

**Symptoms**: IDE crashes or behaves unexpectedly

**Diagnosis**:

```text
1. Help | Diagnostic Tools | Activity Monitor
2. Look for exceptions or high CPU
3. Check recently installed plugins
```

**Fix**:

```text
1. Settings | Plugins
2. Disable recently added plugins
3. Restart IDE
4. Re-enable one by one to find conflict
```

### Settings Lost

**Symptoms**: Action Allowlist rules missing, MCP config gone

**Recovery**:

```text
1. Check if .junie/ directory exists
2. Reload from project configuration
3. Settings | Tools | Junie | Action Allowlist
4. Import or manually re-add rules
```

---

## 5. Full Reset Procedure

When all else fails, perform a complete reset:

### Step 1: Backup Current State

```bash
# Backup everything
cp -r .junie .junie.pre-reset-$(date +%Y%m%d-%H%M%S)

# Note current state
ls -la .junie/ > .junie-state.txt
```

### Step 2: Stop All Services

```text
1. Settings | Tools | Junie | MCP Servers | Stop All
2. Close all Junie-related panels
3. File | Exit (close IDE completely)
```

### Step 3: Clear Caches

```bash
# Clear npm/npx cache
npm cache clean --force
rm -rf ~/.npm/_npx

# Clear IDE caches (optional, more aggressive)
# Location varies by IDE and OS
# Windows: %LOCALAPPDATA%\JetBrains\<Product>
# macOS: ~/Library/Caches/JetBrains/<Product>
# Linux: ~/.cache/JetBrains/<Product>
```

### Step 4: Reset Configuration

**Option A: Restore from backup**

```bash
rm -rf .junie
cp -r .junie.backup-YYYYMMDD .junie
```

**Option B: Start fresh**

```bash
rm -rf .junie
# Copy template from documentation or another project
```

### Step 5: Restart and Verify

```text
1. Start IDE
2. Open project
3. Settings | Tools | Junie | MCP Servers
4. Reload configuration
5. Start servers one by one
6. Verify each component works
```

### Step 6: Verify Recovery

```bash
# Run validation tests
pytest tests/tools/test_junie_config.py -v

# Check MCP status
# All servers should show "Connected"

# Test basic operations
# git status (should auto-approve)
# Ask Junie to read a file (tests filesystem server)
```

---

## 6. Prevention Strategies

### Regular Backups

```bash
# Daily backup script (add to cron/scheduler)
cp -r .junie ".junie.backup-$(date +%Y%m%d)"

# Keep last 7 days
find . -maxdepth 1 -name ".junie.backup-*" -mtime +7 -exec rm -rf {} \;
```

### Configuration Validation

```bash
# Add to pre-commit hook
pytest tests/tools/test_junie_config.py -v --tb=short
```

### Monitoring

- Check MCP server status daily
- Review IDE logs weekly for warnings
- Track auto-approval rate for anomalies

---

## 7. Recovery Checklist

### Post-Recovery Verification

```markdown
- [ ] IDE starts without errors
- [ ] Junie plugin is active
- [ ] MCP servers connected (P0: filesystem, memory)
- [ ] Terminal rules loaded (target: 87)
- [ ] Test command auto-approves (e.g., git status)
- [ ] Memory server responds to queries
- [ ] Configuration tests pass
```

### Documentation

After recovery, document:

- What went wrong
- How it was fixed
- Prevention measures added

---

## 8. Related

- [Maintenance](maintenance.md) — Regular operations
- [Migration](migration.md) — Version updates
- [MCP Troubleshooting](../mcp/troubleshooting.md) — MCP-specific issues

---

*AI Collaboration Knowledge Base*
