# Operations Guide

> Configuration updates, hot reload, and error recovery (~10 min read)

---

## Table of Contents

- [1. Configuration Update Methods](#1-configuration-update-methods)
- [2. Hot Reload Capabilities](#2-hot-reload-capabilities)
- [3. MCP Error Recovery](#3-mcp-error-recovery)
- [4. Common Operations](#4-common-operations)

---

## 1. Configuration Update Methods

### Update Types

| Update Type           | Method                          | Downtime            |
|:----------------------|:--------------------------------|:--------------------|
| **Terminal Rules**    | IDE Settings → Apply            | None (immediate)    |
| **MCP Server Config** | Edit mcp.json → Restart servers | Brief (~5s)         |
| **YAML Config**       | Edit file → Restart IDE         | Full restart        |
| **Guidelines**        | Edit .md files                  | None (next session) |

### Configuration File Locations

```
.junie/
├── mcp/mcp.json          # MCP servers (requires server restart)
├── generic/config.yaml   # Generic settings (requires IDE restart)
├── project/config.yaml   # Project settings (requires IDE restart)
└── guidelines.md         # AI guidelines (next session)
```

---

## 2. Hot Reload Capabilities

### What Can Be Hot-Reloaded

| Component              | Hot Reload | Method                    |
|:-----------------------|:-----------|:--------------------------|
| **Terminal Allowlist** | ✅ Yes      | Settings → Apply          |
| **MCP Servers**        | ⚠️ Partial | Restart individual server |
| **YAML Configs**       | ❌ No       | Requires IDE restart      |
| **Guidelines**         | ✅ Yes      | Automatic on next session |
| **Schema Files**       | ✅ Yes      | Immediate validation      |

### Hot Reload Procedures

#### Terminal Rules (Immediate)

```
1. Settings | Tools | Junie | Action Allowlist
2. Add/modify rules
3. Click "Apply" → Changes effective immediately
```

#### MCP Servers (Partial Restart)

```
Option A: Restart Single Server
1. Settings | Tools | Junie | MCP Servers
2. Select server → Click "Restart"
3. Server reloads with new config

Option B: Restart All Servers
1. Settings | Tools | Junie | MCP Servers
2. Click "Restart All"
3. All servers reload (~5-10 seconds)
```

#### Full Configuration (IDE Restart Required)

```
For changes to:
- generic/config.yaml
- project/config.yaml
- Structural changes to mcp.json

Procedure:
1. Save all configuration changes
2. File | Invalidate Caches / Restart
3. Select "Just Restart"
4. Verify configuration after restart
```

### Reload Status Indicators

```
Configuration Status After Update:

✅ Applied     - Change is active
⏳ Pending    - Requires restart/reload
❌ Error      - Configuration invalid
⚠️ Partial    - Some changes applied
```

---

## 3. MCP Error Recovery

### Error Recovery Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP ERROR DETECTED                           │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │     Identify Error Type       │
              └───────────────┬───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Connection   │   │    Server     │   │ Configuration │
│    Error      │   │    Crash      │   │    Error      │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Check network │   │ Check logs    │   │ Validate JSON │
│ Verify deps   │   │ Restart server│   │ Check schema  │
│ Restart server│   │ Check memory  │   │ Fix syntax    │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                   │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      Verify Recovery          │
              │   - Test server connection    │
              │   - Execute sample command    │
              │   - Check functionality       │
              └───────────────┬───────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌───────────┐               ┌───────────┐
        │  Success  │               │  Failed   │
        │  Resume   │               │  Escalate │
        │  work     │               │  Use      │
        └───────────┘               │  fallback │
                                    └───────────┘
```

### Error Types and Solutions

#### Connection Errors

| Symptom                 | Cause              | Solution                    |
|:------------------------|:-------------------|:----------------------------|
| "Server not responding" | Server not started | Restart MCP server          |
| "Connection refused"    | Wrong port/address | Check mcp.json config       |
| "Timeout"               | Server overloaded  | Restart or increase timeout |

**Recovery Steps**:

```powershell
# 1. Check if server process exists
Get-Process -Name "node" -ErrorAction SilentlyContinue

# 2. Restart server via IDE
# Settings | Tools | Junie | MCP Servers → Restart

# 3. If still failing, restart all MCP servers
# Settings | Tools | Junie | MCP Servers → Restart All
```

#### Server Crash

| Symptom                      | Cause                 | Solution                   |
|:-----------------------------|:----------------------|:---------------------------|
| "Server exited unexpectedly" | Bug or resource issue | Check logs, restart        |
| "Out of memory"              | Memory leak           | Restart server, report bug |
| "Unhandled exception"        | Server bug            | Update server, restart     |

**Recovery Steps**:

```powershell
# 1. Check MCP server logs
# View | Tool Windows | Junie | MCP Logs

# 2. Clear server state
Remove-Item "$env:TEMP\mcp-*" -Recurse -ErrorAction SilentlyContinue

# 3. Restart affected server
# Settings | Tools | Junie | MCP Servers → Select server → Restart
```

#### Configuration Errors

| Symptom                  | Cause               | Solution             |
|:-------------------------|:--------------------|:---------------------|
| "Invalid JSON"           | Syntax error        | Validate with schema |
| "Unknown server"         | Typo in server name | Check mcp.json       |
| "Missing required field" | Incomplete config   | Add required fields  |

**Recovery Steps**:

```powershell
# 1. Validate mcp.json syntax
python -c "import json; json.load(open('.junie/mcp/mcp.json'))"

# 2. Validate against schema
# Use IDE JSON validation or online validator

# 3. Fix errors and restart
# Settings | Tools | Junie | MCP Servers → Restart All
```

### Fallback Strategies

When MCP servers are unavailable, use these alternatives:

| MCP Server              | Fallback Method               |
|:------------------------|:------------------------------|
| **Filesystem**          | IDE built-in file operations  |
| **Memory**              | Document in `.history/` files |
| **GitHub**              | Use `git` CLI commands        |
| **Fetch**               | Ask user to provide content   |
| **Sequential Thinking** | Use Expert Committee pattern  |

### Escalation Path

```
Level 1: Self-Recovery
    │   - Restart server
    │   - Clear cache
    │   - Validate config
    │
    ▼ (If failed after 3 attempts)
Level 2: IDE Restart
    │   - File | Invalidate Caches / Restart
    │   - Verify all MCP servers
    │
    ▼ (If still failing)
Level 3: Full Reset
    │   - Backup current config
    │   - Reset to default config
    │   - Re-apply customizations
    │
    ▼ (If persistent issues)
Level 4: External Support
        - Check JetBrains Junie docs
        - Check MCP server GitHub issues
        - Contact support
```

---

## 4. Common Operations

### Daily Operations

| Task                      | Command/Action                            |
|:--------------------------|:------------------------------------------|
| **Start MCP servers**     | Automatic on IDE start                    |
| **Check server status**   | Settings → MCP Servers                    |
| **View server logs**      | View → Tool Windows → Junie → MCP Logs    |
| **Restart single server** | Settings → MCP Servers → Select → Restart |

### Weekly Maintenance

```markdown
## Weekly Checklist

☐ Review MCP server logs for errors
☐ Check auto-approval rate metrics
☐ Update Terminal rules if needed
☐ Prune unused Memory entities
☐ Verify backup configurations exist
```

### Configuration Backup

```powershell
# Create configuration backup
$timestamp = Get-Date -Format "yyyyMMdd"
$backupDir = ".junie.backup-$timestamp"

Copy-Item -Recurse .junie $backupDir
Write-Host "Backup created: $backupDir"

# List backups
Get-ChildItem ".junie.backup-*" | Sort-Object LastWriteTime -Descending
```

---

## Related

- `06-migration-guide.md` — Version migration and rollback
- `03-mcp-integration.md` — MCP server setup
- `08-efficiency-metrics.md` — Performance tracking
- `../mcp/mcp.json` — MCP server configuration

---

*Part of the Junie Configuration Guide*
