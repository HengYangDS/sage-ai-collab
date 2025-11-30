
# MCP Troubleshooting

> Problem solving guide for MCP server issues (~10 min read)

---

## Table of Contents

1. [Quick Diagnosis](#1-quick-diagnosis)
2. [Connection Issues](#2-connection-issues)
3. [Configuration Issues](#3-configuration-issues)
4. [Runtime Issues](#4-runtime-issues)
5. [Platform-Specific Issues](#5-platform-specific-issues)
6. [Recovery Procedures](#6-recovery-procedures)
7. [Getting Help](#7-getting-help)
8. [FAQ](#8-faq)
9. [Related](#9-related)

---

## 1. Quick Diagnosis

### Server Status Check

1. Open `Settings | Tools | Junie | MCP Servers`
2. Check server status:
    - 🟢 **Connected** — Working normally
    - 🟡 **Starting** — Initializing (wait ~10s)
    - 🔴 **Disconnected** — Not running or error

### Common Status Indicators

| Status       | Meaning                        | Action                   |
|:-------------|:-------------------------------|:-------------------------|
| Connected    | Server running normally        | None needed              |
| Disconnected | Server not running             | Start or restart server  |
| Error        | Configuration or runtime error | Check logs, fix config   |
| Timeout      | Server took too long           | Restart, check resources |

---

## 2. Connection Issues

### Server Won't Start

**Symptoms**: Server stays "Disconnected" after clicking Start

**Diagnosis**:

```bash
# Verify Node.js installation
node --version    # Should show v18.x or higher

# Verify npx works
npx --version

# Test server manually
npx -y @modelcontextprotocol/server-filesystem .
```

**Solutions**:

| Cause                 | Solution                                   |
|:----------------------|:-------------------------------------------|
| Node.js not installed | Install Node.js v18+                       |
| npx not in PATH       | Add Node.js to system PATH                 |
| Package not found     | Check package name spelling                |
| Network issues        | Check internet connection for npm registry |

### Server Disconnects Immediately

**Symptoms**: Server shows "Connected" briefly then "Disconnected"

**Possible Causes**:

1. **Invalid configuration** — Check JSON syntax
2. **Missing dependencies** — Server package needs installation
3. **Permission issues** — Server can't access required resources
4. **Port conflicts** — Another process using required port

**Solutions**:

```bash
# Clear npm cache
npm cache clean --force

# Reinstall server package
npx -y @modelcontextprotocol/server-filesystem .

# Check for errors
# Look in IDE logs: Help | Show Log in Explorer
```

### Timeout During Connection

**Symptoms**: Server connection times out

**Solutions**:

1. **Increase timeout** — Some servers need more startup time
2. **Check system resources** — CPU/memory availability
3. **Disable antivirus temporarily** — May block server processes
4. **Restart IDE** — Clear any stuck processes

---

## 3. Configuration Issues

### Invalid JSON Syntax

**Symptoms**: Error message about JSON parsing

**Diagnosis**:

```bash
# Validate JSON syntax
# Use online JSON validator or IDE JSON support
```

**Common Mistakes**:

| Mistake              | Fix                             |
|:---------------------|:--------------------------------|
| Trailing comma       | Remove comma after last item    |
| Missing quotes       | Add quotes around string values |
| Single quotes        | Use double quotes for JSON      |
| Unescaped characters | Escape backslashes: `\\`        |

**Example Fix**:

```json
// Wrong
{
  "command": "npx.cmd",
  "args": [
    "-y",
    "server"
  ]
  // <- trailing comma error
}

// Correct
{
  "command": "npx.cmd",
  "args": [
    "-y",
    "server"
  ]
}
```

### Path Not Found

**Symptoms**: Server can't find specified paths

**Diagnosis**:

```bash
# Verify path exists
ls .junie    # or dir .junie on Windows
```

**Solutions**:

| Issue                | Solution                           |
|:---------------------|:-----------------------------------|
| Path doesn't exist   | Create directory or fix path       |
| Wrong path separator | Use `/` not `\` in JSON            |
| Relative path wrong  | Paths are relative to project root |

### Environment Variable Not Set

**Symptoms**: Server requiring token fails to authenticate

**Diagnosis**:

```bash
# Check if variable is set
echo $GITHUB_PERSONAL_ACCESS_TOKEN    # Unix
echo $env:GITHUB_PERSONAL_ACCESS_TOKEN  # PowerShell
```

**Solutions**:

**Windows PowerShell**:

```powershell
# Set for current session
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "your-token"

# Set permanently (User level)
[Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "your-token", "User")
```

**macOS/Linux**:

```bash
# Set for current session
export GITHUB_PERSONAL_ACCESS_TOKEN="your-token"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="your-token"' >> ~/.bashrc
source ~/.bashrc
```

---

## 4. Runtime Issues

### Tool Invocation Fails

**Symptoms**: Server connected but tools return errors

**Diagnosis**:

1. Check server logs in IDE
2. Test tool with simple input
3. Verify permissions

**Common Causes**:

| Error             | Cause                 | Solution                    |
|:------------------|:----------------------|:----------------------------|
| Permission denied | File/directory access | Check file permissions      |
| File not found    | Wrong path            | Verify path exists          |
| Invalid argument  | Wrong parameter type  | Check tool documentation    |
| Rate limited      | Too many requests     | Add delays between requests |

### Memory Server Issues

**Symptoms**: Knowledge not persisting or search returns empty

**Solutions**:

1. **Verify entity creation** — Check for errors in response
2. **Use correct names** — Entity names are case-sensitive
3. **Search broadly** — Try different search terms
4. **Check server status** — Ensure memory server is running

### Filesystem Server Issues

**Symptoms**: Can't read or write files

**Solutions**:

1. **Check allowed paths** — Verify path is in server args
2. **Check permissions** — File system permissions
3. **Verify path format** — Use forward slashes in JSON

---

## 5. Platform-Specific Issues

### Windows

**Issue**: `npx` not recognized

**Solution**:

```powershell
# Use npx.cmd instead of npx
"command": "npx.cmd"

# Or add Node.js to PATH
$env:PATH += ";C:\Program Files\nodejs"
```

**Issue**: Long path errors

**Solution**:

```powershell
# Enable long paths in Windows
# Run as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### macOS/Linux

**Issue**: Permission denied for npx

**Solution**:

```bash
# Check npm permissions
npm config get prefix

# If needed, fix permissions
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
```

**Issue**: Server not found in PATH

**Solution**:

```bash
# Add to PATH in shell config
export PATH="$PATH:$(npm config get prefix)/bin"
```

---

## 6. Recovery Procedures

### Full Reset

When nothing else works:

```bash
# 1. Stop all MCP servers in IDE settings

# 2. Clear npm cache
npm cache clean --force

# 3. Remove node_modules cache
rm -rf ~/.npm/_npx    # Unix
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\npm-cache\_npx"  # Windows

# 4. Restart IDE

# 5. Reload MCP configuration
# Settings | Tools | Junie | MCP Servers | Reload

# 6. Start servers one by one
```

### Configuration Backup

Before making changes:

```bash
# Backup current config
cp .junie/mcp/mcp.json .junie/mcp/mcp.json.backup

# Restore if needed
cp .junie/mcp/mcp.json.backup .junie/mcp/mcp.json
```

### Minimal Configuration Test

Test with minimal config to isolate issues:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
      ]
    }
  }
}
```

---

## 7. Getting Help

### IDE Logs

1. `Help | Show Log in Explorer`
2. Look for MCP-related entries
3. Search for error messages

### Server Logs

1. `Settings | Tools | Junie | MCP Servers`
2. Select server → View logs
3. Look for error messages

### Resources

- **Junie MCP Docs**: https://www.jetbrains.com/help/junie/model-context-protocol-mcp.html
- **MCP Specification**: https://modelcontextprotocol.io/specification
- **MCP GitHub Issues**: https://github.com/modelcontextprotocol/servers/issues

---

## 8. FAQ

### Q: Why does my server keep disconnecting?

**A**: Common causes:

1. Server process crashes — check logs
2. Resource exhaustion — check memory/CPU
3. Configuration error — validate JSON
4. Network issues — check connectivity

### Q: Can I use multiple filesystem paths?

**A**: Yes, add paths as additional arguments:

```json
"args": ["-y", "@modelcontextprotocol/server-filesystem", ".", ".junie", "docs"]
```

### Q: Why doesn't `${PROJECT_ROOT}` work?

**A**: Junie doesn't expand environment variables in args. Use relative paths:

```json
// Wrong
"args": ["-y", "server", "${PROJECT_ROOT}"]

// Correct
"args": ["-y", "server", "."]
```

### Q: How do I switch between Windows and Unix configs?

**A**: Keep platform-specific templates and copy as needed:

```bash
# Unix
cp mcp.unix.json mcp.json

# Windows  
copy mcp.windows.json mcp.json
```

---

## 9. Related

- [Overview](overview.md) — MCP architecture
- [Configuration](configuration.md) — Setup guide
- [Servers Reference](servers.md) — Server documentation
- [Memory Best Practices](memory.md) — Knowledge persistence

---

*AI Collaboration Knowledge Base*
