# Configuration Maintenance

> Daily operations and hot reload procedures (~10 min read)

---

## Configuration Update Methods

### Update Types Overview

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

## Hot Reload Capabilities

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

**Option A: Restart Single Server**

```
1. Settings | Tools | Junie | MCP Servers
2. Select server → Click "Restart"
3. Server reloads with new config
```

**Option B: Restart All Servers**

```
1. Settings | Tools | Junie | MCP Servers
2. Click "Restart All"
3. All servers reload (~5-10 seconds)
```

#### Full Configuration (IDE Restart Required)

For changes to:

- `generic/config.yaml`
- `project/config.yaml`
- Structural changes to `mcp.json`

**Procedure**:

```
1. Save all changes
2. File | Exit (or IDE exit shortcut)
3. Restart IDE
4. Verify configuration loaded correctly
```

---

## Daily Maintenance Tasks

### Weekly Checklist

```markdown
## Week of [DATE]

### Configuration Health

- [ ] Verify MCP servers connected
- [ ] Check Terminal rule count (target: 87)
- [ ] Review any blocked commands
- [ ] Update rules for new patterns if needed

### Documentation

- [ ] Update session history if significant work done
- [ ] Review and clean up .outputs/ directory
- [ ] Archive old session files if needed

### Performance

- [ ] Check auto-approval rate (target: 90%+)
- [ ] Review token efficiency metrics
- [ ] Identify optimization opportunities
```

### Monthly Checklist

```markdown
## Month of [DATE]

### Configuration Review

- [ ] Review all Terminal rules for relevance
- [ ] Check for deprecated patterns
- [ ] Update MCP server versions if available
- [ ] Validate schema compliance

### Knowledge Cleanup

- [ ] Review Memory server entities
- [ ] Remove obsolete entities
- [ ] Consolidate duplicate information
- [ ] Update relationships

### Documentation

- [ ] Review and update project/quickref.md
- [ ] Check cross-references are valid
- [ ] Update version numbers if needed
```

---

## Configuration Backup

### Before Changes

Always backup before significant changes:

```bash
# Full backup
cp -r .junie .junie.backup-$(date +%Y%m%d)

# Specific file backup
cp .junie/mcp/mcp.json .junie/mcp/mcp.json.backup
```

**Windows PowerShell**:

```powershell
# Full backup
Copy-Item -Recurse .junie ".junie.backup-$( Get-Date -Format 'yyyyMMdd' )"

# Specific file backup
Copy-Item .junie\mcp\mcp.json .junie\mcp\mcp.json.backup
```

### Restore from Backup

```bash
# Restore full backup
rm -rf .junie
cp -r .junie.backup-20251130 .junie

# Restore specific file
cp .junie/mcp/mcp.json.backup .junie/mcp/mcp.json
```

### List Backups

```bash
# Unix
ls -la .junie.backup-*

# Windows PowerShell
Get-ChildItem ".junie.backup-*" | Sort-Object LastWriteTime -Descending
```

---

## Cross-Platform Configuration

### Windows to Unix Conversion

```bash
# Convert npx.cmd to npx
sed -i 's/npx\.cmd/npx/g' .junie/mcp/mcp.json
```

### Unix to Windows Conversion

```powershell
# Convert npx to npx.cmd
(Get-Content .junie/mcp/mcp.json) -replace '"npx"', '"npx.cmd"' | Set-Content .junie/mcp/mcp.json
```

### Platform-Specific Templates

Maintain separate templates for different platforms:

```
.junie/mcp/
├── mcp.json              # Active config
├── mcp.windows.json      # Windows template
└── mcp.unix.json         # macOS/Linux template
```

---

## Validation

### Configuration Validation

#### JSON Syntax Check

```bash
# Using Python
python -m json.tool .junie/mcp/mcp.json > /dev/null && echo "Valid JSON"

# Using Node.js
node -e "require('./.junie/mcp/mcp.json')" && echo "Valid JSON"
```

#### YAML Syntax Check

```bash
# Using Python
python -c "import yaml; yaml.safe_load(open('.junie/generic/config.yaml'))" && echo "Valid YAML"
```

### Schema Validation

Run the test suite to validate configuration:

```bash
pytest tests/tools/test_junie_config.py -v
```

---

## Monitoring

### Auto-Approval Rate

Track weekly:

```
Auto-Approval Rate = (Auto-Approved Commands / Total Commands) × 100%
Target: ≥90%
```

### MCP Server Health

Check daily:

- All P0 servers (filesystem, memory) connected
- No recurring errors in logs
- Response times acceptable

### Configuration Drift

Monthly review:

- Compare current config with baseline
- Document intentional changes
- Revert unintended changes

---

## Related

- [Migration Guide](migration.md) — Version migration
- [Metrics](metrics.md) — Efficiency tracking
- [Recovery](recovery.md) — Error recovery procedures

---

*Part of the Junie Configuration Template System*
